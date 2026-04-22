#!/usr/bin/env python3
"""
Übersetzt die Quell-HTML-Seiten (auf Deutsch) via DeepL API in alle
Zielsprachen und schreibt die Ergebnisse in Unterordner /<lang>/.

Caching: Pro Quelldatei wird ein SHA-256-Hash gespeichert. Ändert sich
der Hash nicht, wird die Datei übersprungen (keine API-Calls, keine
Kosten, alte Übersetzungen bleiben stehen).

Translates source HTML pages (German) via DeepL API into all target
languages and writes output to /<lang>/ subfolders. File-hash cache
skips unchanged files to save API calls.

Läuft von .github/workflows/translate-site.yml
Requires env var DEEPL_API_KEY (Pro subscription).
"""

import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

# ---------- Konfiguration / Configuration ----------

# DeepL Pro verwendet api.deepl.com; Free verwendet api-free.deepl.com
DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_USAGE_URL = "https://api.deepl.com/v2/usage"

SOURCE_LANG = "DE"
SOURCE_FILES = [
    "index.html",
    "hilfe.html",
    "datenschutz.html",
    "eula.html",
    "impressum.html",
]

# Alle 33 DeepL-Zielsprachen
# (DeepL-Code, HTML-lang-Attribut, Slug für URL, Anzeigename, Flagge)
LANGUAGES = [
    ("EN-US",  "en",    "en",    "English",       "🇺🇸"),
    ("EN-GB",  "en-GB", "en-gb", "English (UK)",  "🇬🇧"),
    ("FR",     "fr",    "fr",    "Français",      "🇫🇷"),
    ("IT",     "it",    "it",    "Italiano",      "🇮🇹"),
    ("ES",     "es",    "es",    "Español",       "🇪🇸"),
    ("PT-BR",  "pt-BR", "pt-br", "Português (BR)", "🇧🇷"),
    ("PT-PT",  "pt-PT", "pt-pt", "Português (PT)", "🇵🇹"),
    ("NL",     "nl",    "nl",    "Nederlands",    "🇳🇱"),
    ("SV",     "sv",    "sv",    "Svenska",       "🇸🇪"),
    ("DA",     "da",    "da",    "Dansk",         "🇩🇰"),
    ("NB",     "nb",    "nb",    "Norsk",         "🇳🇴"),
    ("FI",     "fi",    "fi",    "Suomi",         "🇫🇮"),
    ("PL",     "pl",    "pl",    "Polski",        "🇵🇱"),
    ("CS",     "cs",    "cs",    "Čeština",       "🇨🇿"),
    ("SK",     "sk",    "sk",    "Slovenčina",    "🇸🇰"),
    ("HU",     "hu",    "hu",    "Magyar",        "🇭🇺"),
    ("SL",     "sl",    "sl",    "Slovenščina",   "🇸🇮"),
    ("RO",     "ro",    "ro",    "Română",        "🇷🇴"),
    ("BG",     "bg",    "bg",    "Български",     "🇧🇬"),
    ("EL",     "el",    "el",    "Ελληνικά",      "🇬🇷"),
    ("ET",     "et",    "et",    "Eesti",         "🇪🇪"),
    ("LV",     "lv",    "lv",    "Latviešu",      "🇱🇻"),
    ("LT",     "lt",    "lt",    "Lietuvių",      "🇱🇹"),
    ("UK",     "uk",    "uk",    "Українська",    "🇺🇦"),
    ("JA",     "ja",    "ja",    "日本語",         "🇯🇵"),
    ("KO",     "ko",    "ko",    "한국어",         "🇰🇷"),
    ("ZH",     "zh",    "zh",    "简体中文",       "🇨🇳"),
    ("ZH-HANT","zh-Hant","zh-hant","繁體中文",     "🇹🇼"),
    ("VI",     "vi",    "vi",    "Tiếng Việt",    "🇻🇳"),
    ("ID",     "id",    "id",    "Bahasa",        "🇮🇩"),
    ("TH",     "th",    "th",    "ไทย",           "🇹🇭"),
    ("TR",     "tr",    "tr",    "Türkçe",        "🇹🇷"),
    ("AR",     "ar",    "ar",    "العربية",       "🇸🇦"),
]

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE_FILE = REPO_ROOT / "scripts" / ".translation-cache.json"

BASE_URL = "https://linguaflow.app"


# ---------- Helper ----------

def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def file_hash(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deepl_translate(html: str, target_lang: str, api_key: str) -> str:
    """Schickt HTML an DeepL. tag_handling=html bewahrt HTML-Struktur,
    ignore_tags schützt script/style vor Übersetzung."""
    data = urllib.parse.urlencode({
        "text": html,
        "source_lang": SOURCE_LANG,
        "target_lang": target_lang,
        "tag_handling": "html",
        "ignore_tags": "script,style,code,pre",
        "preserve_formatting": "1",
    }).encode("utf-8")

    req = urllib.request.Request(
        DEEPL_API_URL,
        data=data,
        headers={
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "LinguaFlow-TranslateBot/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        body = json.load(response)
    return body["translations"][0]["text"]


# ---------- HTML-Post-Processing ----------

def adjust_html(html: str, lang_attr: str, slug: str, filename: str) -> str:
    """Nach der Übersetzung müssen einige HTML-Attribute angepasst werden,
    damit CSS/Bilder weiter geladen werden und SEO-Tags (canonical, hreflang,
    og:url) auf die richtige Sprachversion zeigen."""

    # 1. <html lang="de"> -> <html lang="xx">
    html = re.sub(r'(<html[^>]*\blang=")de("[^>]*>)', rf'\1{lang_attr}\2', html, count=1)

    # 2. Relative Asset-Pfade absolut machen (damit sie aus /<slug>/ auch funktionieren)
    html = re.sub(r'(href|src)="(?!https?://|/|#|mailto:|tel:)(styles\.css|img/[^"]+|[^"]+\.ico|[^"]+\.png|[^"]+\.svg|[^"]+\.jpg|[^"]+\.jpeg|[^"]+\.webp)"', r'\1="/\2"', html)

    # 3. Canonical-URL anpassen: https://linguaflow.app -> https://linguaflow.app/<slug>/
    page_path = "" if filename == "index.html" else filename
    canonical_url = f"{BASE_URL}/{slug}/{page_path}"
    if page_path == "":
        # Startseite: endet mit /slug/ ohne Dateiname
        canonical_url = f"{BASE_URL}/{slug}/"
    # bestehende canonical-URLs umschreiben
    html = re.sub(
        r'<link rel="canonical" href="https://linguaflow\.app[^"]*"',
        f'<link rel="canonical" href="{canonical_url}"',
        html,
    )

    # 4. og:url anpassen
    html = re.sub(
        r'<meta property="og:url" content="https://linguaflow\.app[^"]*"',
        f'<meta property="og:url" content="{canonical_url}"',
        html,
    )

    # 5. og:locale anpassen
    html = re.sub(
        r'<meta property="og:locale" content="de_DE"',
        f'<meta property="og:locale" content="{lang_attr.replace("-", "_")}"',
        html,
    )

    # 6. Logo-Link anpassen: href="/" -> href="/<slug>/" (damit man in Sprache bleibt)
    html = html.replace('<a href="/" class="logo">', f'<a href="/{slug}/" class="logo">')

    # 7. hreflang-Tags einfügen
    hreflang_links = ['<link rel="alternate" hreflang="x-default" href="' + BASE_URL + '/">']
    hreflang_links.append(f'<link rel="alternate" hreflang="de" href="{BASE_URL}/">')
    for _, lattr, lslug, _, _ in LANGUAGES:
        # URL dieser Seite in dieser Sprache
        if filename == "index.html":
            lang_url = f"{BASE_URL}/{lslug}/"
        else:
            lang_url = f"{BASE_URL}/{lslug}/{filename}"
        hreflang_links.append(f'<link rel="alternate" hreflang="{lattr}" href="{lang_url}">')

    hreflang_block = "\n  " + "\n  ".join(hreflang_links)
    # Vor </head> einfügen (nur falls noch nicht drin)
    if "hreflang" not in html:
        html = html.replace("</head>", f"{hreflang_block}\n</head>", 1)

    # 8. Language-Switcher vor dem schließenden </footer> einfügen
    switcher = build_language_switcher(slug, filename)
    if switcher and 'class="language-switcher"' not in html:
        html = html.replace("</footer>", f"{switcher}\n</footer>", 1)

    return html


def build_language_switcher(current_slug: str, filename: str) -> str:
    """Baut das Dropdown für den Sprach-Wechsel (als HTML-String)."""
    def option(value: str, label: str, selected: bool) -> str:
        sel = " selected" if selected else ""
        return f'<option value="{value}"{sel}>{label}</option>'

    # Pfad innerhalb der Sprache
    sub = "" if filename == "index.html" else filename

    opts = [option(f"/{sub}", "🇩🇪 Deutsch", current_slug == "de")]
    for _, _, slug, name, flag in LANGUAGES:
        url = f"/{slug}/{sub}"
        opts.append(option(url, f"{flag} {name}", slug == current_slug))

    return f"""
<div class="language-switcher" style="text-align:center;padding:20px 0 8px;">
  <select onchange="if(this.value)location.href=this.value" style="padding:8px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.05);color:inherit;font-size:14px;cursor:pointer;">
    {chr(10).join('    ' + o for o in opts)}
  </select>
</div>"""


def enrich_source_file(source_path: pathlib.Path) -> bool:
    """Fügt hreflang-Tags und Language-Switcher in die deutsche Quelldatei ein.
    Idempotent: Mehrfache Aufrufe erzeugen dasselbe Ergebnis.
    Returns True wenn die Datei geändert wurde."""
    filename = source_path.name
    original = source_path.read_text(encoding="utf-8")
    html = original

    # Alte Marker entfernen (falls vorhanden) für sauberes Wiedereinfügen
    html = re.sub(
        r'<!-- i18n-hreflang:start -->.*?<!-- i18n-hreflang:end -->\s*',
        '',
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<!-- i18n-switcher:start -->.*?<!-- i18n-switcher:end -->\s*',
        '',
        html,
        flags=re.DOTALL,
    )

    # hreflang-Block bauen
    hreflang_links = [
        f'<link rel="alternate" hreflang="de" href="{BASE_URL}/' + ("" if filename == "index.html" else filename) + '">',
        f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/' + ("" if filename == "index.html" else filename) + '">',
    ]
    for _, lattr, lslug, _, _ in LANGUAGES:
        if filename == "index.html":
            url = f"{BASE_URL}/{lslug}/"
        else:
            url = f"{BASE_URL}/{lslug}/{filename}"
        hreflang_links.append(f'<link rel="alternate" hreflang="{lattr}" href="{url}">')

    hreflang_block = "<!-- i18n-hreflang:start -->\n  " + "\n  ".join(hreflang_links) + "\n  <!-- i18n-hreflang:end -->"

    # Switcher für die deutsche Seite (aktuell = "de")
    sub = "" if filename == "index.html" else filename
    opts = [f'<option value="/{sub}" selected>🇩🇪 Deutsch</option>']
    for _, _, slug, name, flag in LANGUAGES:
        opts.append(f'<option value="/{slug}/{sub}">{flag} {name}</option>')
    switcher = (
        '<!-- i18n-switcher:start -->\n'
        '<div class="language-switcher" style="text-align:center;padding:20px 0 8px;">\n'
        '  <select onchange="if(this.value)location.href=this.value" aria-label="Sprache wählen" style="padding:8px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.05);color:inherit;font-size:14px;cursor:pointer;font-family:inherit;">\n'
        + "\n".join("    " + o for o in opts) + "\n"
        '  </select>\n'
        '</div>\n'
        '<!-- i18n-switcher:end -->'
    )

    # hreflang vor </head> einfügen
    html = html.replace("</head>", f"  {hreflang_block}\n</head>", 1)
    # Switcher vor </footer> einfügen
    html = html.replace("</footer>", f"{switcher}\n</footer>", 1)

    if html != original:
        source_path.write_text(html, encoding="utf-8")
        return True
    return False


# ---------- Main ----------

def check_usage(api_key: str) -> None:
    """Zeigt die aktuelle DeepL-Nutzung an."""
    req = urllib.request.Request(
        DEEPL_USAGE_URL,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
        count = data.get("character_count", 0)
        limit = data.get("character_limit", 0)
        if limit:
            pct = count / limit * 100
            print(f"DeepL-Nutzung: {count:,} / {limit:,} Zeichen ({pct:.1f} %)")
        else:
            print(f"DeepL-Nutzung: {count:,} Zeichen (kein Limit / Pro)")
    except Exception as e:
        print(f"Konnte DeepL-Nutzung nicht abfragen: {e}", file=sys.stderr)


def process_source_file(
    source_path: pathlib.Path,
    api_key: str,
    cache: dict,
    force: bool = False,
) -> int:
    """Übersetzt eine Quelldatei in alle Zielsprachen. Gibt die Anzahl
    der tatsächlich per API übersetzten Sprachen zurück (0 wenn gecacht)."""
    filename = source_path.name
    new_hash = file_hash(source_path)
    cached_hash = cache.get(filename)

    if not force and cached_hash == new_hash:
        print(f"  ✓ {filename}: unverändert, skip (Cache-Hit)")
        return 0

    print(f"  → {filename}: geändert oder erstmalig — übersetze in {len(LANGUAGES)} Sprachen …")
    source_html = source_path.read_text(encoding="utf-8")

    translated_count = 0
    for idx, (deepl_code, lang_attr, slug, name, _flag) in enumerate(LANGUAGES, 1):
        print(f"     [{idx:2}/{len(LANGUAGES)}] {slug} ({name}) … ", end="", flush=True)
        try:
            translated = deepl_translate(source_html, deepl_code, api_key)
        except Exception as e:
            print(f"FEHLER: {e}")
            continue
        adjusted = adjust_html(translated, lang_attr, slug, filename)
        out_dir = REPO_ROOT / slug
        out_dir.mkdir(exist_ok=True)
        (out_dir / filename).write_text(adjusted, encoding="utf-8")
        translated_count += 1
        print("OK")
        # Rate-Limit-Schutz
        time.sleep(0.1)

    cache[filename] = new_hash
    return translated_count


def build_sitemap():
    """Erweitert die bestehende sitemap.xml um alle Sprachversionen."""
    import datetime
    today = datetime.date.today().isoformat()

    urls = []
    # Deutsche Versionen
    for filename in SOURCE_FILES:
        slug_path = "" if filename == "index.html" else filename.replace(".html", "")
        urls.append(f"{BASE_URL}/{slug_path}".rstrip("/") + ("/" if not slug_path else ""))

    # Alle Sprachen
    for _, _, slug, _, _ in LANGUAGES:
        for filename in SOURCE_FILES:
            if filename == "index.html":
                urls.append(f"{BASE_URL}/{slug}/")
            else:
                urls.append(f"{BASE_URL}/{slug}/{filename}")

    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        priority = "1.0" if url == BASE_URL + "/" else ("0.8" if "hilfe" in url else "0.3")
        body += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{priority}</priority>\n  </url>\n"
    body += "</urlset>\n"

    (REPO_ROOT / "sitemap.xml").write_text(body, encoding="utf-8")
    print(f"\nsitemap.xml aktualisiert ({len(urls)} URLs)")


def main():
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        print("FEHLER: Umgebungsvariable DEEPL_API_KEY nicht gesetzt.", file=sys.stderr)
        sys.exit(1)

    force = "--force" in sys.argv

    check_usage(api_key)
    print()

    cache = load_cache()
    total_translated = 0

    print(f"Verarbeite {len(SOURCE_FILES)} Quelldateien ({'FORCE-Modus' if force else 'mit Cache'}) …\n")
    for filename in SOURCE_FILES:
        source = REPO_ROOT / filename
        if not source.exists():
            print(f"  ! {filename}: nicht gefunden, skip")
            continue
        # Deutsche Quelldatei mit hreflang + Switcher anreichern (idempotent)
        if enrich_source_file(source):
            print(f"  ⚙ {filename}: hreflang + Switcher aktualisiert")
        total_translated += process_source_file(source, api_key, cache, force=force)

    save_cache(cache)
    build_sitemap()

    print(f"\nFertig. Insgesamt {total_translated} Sprach-Übersetzungen durchgeführt.")
    check_usage(api_key)


if __name__ == "__main__":
    main()
