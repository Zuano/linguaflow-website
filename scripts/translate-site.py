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
    "was-ist-neu.html",
    "newsletter.html",
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

# Ratgeber-Seiten werden per Dateimuster automatisch erkannt — neue Artikel
# brauchen keine Skript-Änderung. / Guide pages are auto-discovered by
# filename pattern — new articles need no script change.
SOURCE_FILES += sorted(p.name for p in REPO_ROOT.glob("ratgeber*.html"))

# Funktionsseiten (funktionen.html + funktion-*.html) ebenfalls per Muster —
# sie werden nur DE+EN übersetzt (siehe DE_EN_ONLY_FILES unten).
# / Feature pages are also auto-discovered; they are translated DE+EN only.
FEATURE_PAGES = sorted(p.name for p in REPO_ROOT.glob("funktion*.html"))
SOURCE_FILES += FEATURE_PAGES

BASE_URL = "https://linguaflow.app"

# Seiten in eigenen Verzeichnissen ("Cluster-Seiten"). Quelldateien werden hier
# nicht über den blossen Dateinamen angesprochen, sondern über den Pfad relativ
# zur Repo-Wurzel — deshalb url_path() weiter unten. / Pages living in their own
# directories: addressed by repo-relative path instead of bare filename.
CLUSTER_PAGES = [
    "zurueck-in-deinen-beruf/index.html",
    "zurueck-in-deinen-beruf/pflege/index.html",
    "zurueck-in-deinen-beruf/akademiker/index.html",
]
SOURCE_FILES += CLUSTER_PAGES

# Verzeichnis-Präfixe der Cluster-Seiten — gebraucht, um interne Links auf die
# passende Sprachversion umzubiegen. / Directory prefixes of the cluster pages.
CLUSTER_PREFIXES = sorted({rel.split("/")[0] + "/" for rel in CLUSTER_PAGES})


def rel_key(source_path: pathlib.Path) -> str:
    """Kennung einer Quelldatei: ihr Pfad relativ zur Repo-Wurzel, mit
    Schrägstrichen. Auch für relativ übergebene Pfade korrekt — deshalb
    resolve() vor relative_to(). / Repo-relative key of a source file;
    resolve() first so relative inputs work too."""
    return source_path.resolve().relative_to(REPO_ROOT).as_posix()


def url_path(rel: str) -> str:
    """URL-Pfad einer Quelldatei relativ zur Wurzel, ohne führenden Schrägstrich.
    Ersetzt die frühere Annahme, jede Quelldatei liege flach im Wurzelverzeichnis.
    / Repo-relative URL path of a source file, without the leading slash.

    "index.html"                          -> ""
    "hilfe.html"                          -> "hilfe.html"
    "zurueck-in-deinen-beruf/index.html"  -> "zurueck-in-deinen-beruf/"
    """
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[: -len("index.html")]
    return rel

# Rechtstexte nur Deutsch + Englisch — spart DeepL-Kosten. Die übrigen
# Sprachversionen sind Redirect-Stubs auf /en/ (nicht von diesem Skript
# verwaltet). / Legal pages German + English only — saves DeepL costs.
# The other language versions are redirect stubs to /en/ (not managed
# by this script).
LEGAL_FILES = {"datenschutz.html", "eula.html", "impressum.html"}

# Changelog-Seite ebenfalls nur DE + EN — wird bei jedem App-Release
# aktualisiert, 33 Sprachen wären zu teuer. / Changelog page also
# German + English only — it changes with every app release, so
# translating into 33 languages would be too expensive.
# Newsletter-Seite ebenfalls nur DE + EN — der Newsletter selbst erscheint
# nur auf Deutsch und Englisch. / Newsletter page also German + English
# only — the newsletter itself is only published in German and English.
# Funktionsseiten vorerst nur DE + EN — nach 4–8 Wochen Search-Console-
# Auswertung werden einzelne Seiten ggf. auf 33 Sprachen hochgezogen
# (Entscheidung 2026-08-05, siehe DECISIONS.md). / Feature pages DE+EN
# only for now — individual pages may get all 33 languages later based
# on Search Console data.
DE_EN_ONLY_FILES = LEGAL_FILES | {"was-ist-neu.html", "newsletter.html"} | set(FEATURE_PAGES)


# Cluster-Seiten vorerst nur in den vier Sprachen, die das Strategiebriefing
# nennt: Englisch als Verkehrssprache, dazu Türkisch, Ukrainisch und Arabisch —
# die Herkunftssprachen der Zielgruppe (Türkei, Ukraine und Syrien gehören zu
# den häufigsten Herkunftsländern bei Anerkennungsverfahren). Japanisch oder
# Finnisch wären für dieses Thema verschenktes Geld. Erweitern: einfach Codes
# ergänzen. / Cluster pages in four languages only, per the strategy briefing.
CLUSTER_LANG_CODES = {"EN-US", "TR", "UK", "AR"}


def languages_for(filename: str) -> list:
    """Zielsprachen für eine Quelldatei. / Target languages for a source file."""
    if filename in CLUSTER_PAGES:
        return [l for l in LANGUAGES if l[0] in CLUSTER_LANG_CODES]
    if filename in DE_EN_ONLY_FILES:
        return [l for l in LANGUAGES if l[0] == "EN-US"]
    return LANGUAGES


# Slugs, für die es Cluster-Übersetzungen gibt — Links dorthin werden nur für
# diese Sprachen umgebogen. / Slugs that actually have cluster translations.
CLUSTER_SLUGS = {l[2] for l in LANGUAGES if l[0] in CLUSTER_LANG_CODES}

# Erhöhen, wenn sich die Übersetzungs-Logik grundlegend ändert.
# Bei Mismatch wird der Cache invalidiert → alles neu übersetzt.
# v4: Fix für hreflang in Sub-Pages (DE/x-default zeigten auf Root) und
#     Sitemap-Konsistenz (deutsche Sub-Pages jetzt mit .html).
SCRIPT_VERSION = "4"


# ---------- Helper ----------

def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            if data.get("__version") != SCRIPT_VERSION:
                print(f"Cache-Version veraltet ({data.get('__version')} vs {SCRIPT_VERSION}) → invalidiere.")
                return {"__version": SCRIPT_VERSION}
            return data
        except json.JSONDecodeError:
            return {"__version": SCRIPT_VERSION}
    return {"__version": SCRIPT_VERSION}


def save_cache(cache: dict) -> None:
    cache["__version"] = SCRIPT_VERSION
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def file_hash(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deepl_translate_raw(text: str, target_lang: str, api_key: str) -> str:
    """Schickt Text an DeepL. tag_handling=html bewahrt HTML-Struktur."""
    data = urllib.parse.urlencode({
        "text": text,
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


def deepl_translate(html: str, target_lang: str, api_key: str) -> str:
    """Übersetzt HTML und schützt ALLE <script>-Blöcke vor DeepL's HTML-Escaping.

    DeepL escaped trotz ignore_tags=script die Inhalte von <script>-Tags:
    Anführungszeichen werden zu &quot;/&#x27;, ">" zu &gt;. Bei JSON-LD
    erzeugt das ungültiges JSON (GSC-Fehler), bei Inline-JavaScript einen
    SyntaxError — Mobile-Menü, Lightbox und Newsletter-Formular waren
    dadurch in allen Sprachversionen funktionsunfähig (entdeckt 2026-08-05).

    Lösung: Alle <script>-Blöcke (JSON-LD UND Inline-JS) vor der
    Übersetzung durch Platzhalter-Kommentare ersetzen, übersetzen, dann
    Platzhalter durch die unveränderten Original-Blöcke ersetzen.
    Nebeneffekt: weniger Zeichen pro API-Call → geringere Kosten.
    / Protect ALL <script> blocks (JSON-LD and inline JS) with placeholder
    comments — DeepL HTML-escapes script contents despite ignore_tags,
    which broke inline JS in every translated page."""
    script_pattern = re.compile(
        r'<script\b[^>]*>.*?</script>',
        re.DOTALL,
    )

    blocks = []

    def save_block(match):
        blocks.append(match.group(0))
        return f"<!--SCRIPT_{len(blocks) - 1}-->"

    html_safe = script_pattern.sub(save_block, html)
    translated = deepl_translate_raw(html_safe, target_lang, api_key)

    # Original-Blöcke zurückeinsetzen
    for idx, block in enumerate(blocks):
        translated = translated.replace(f"<!--SCRIPT_{idx}-->", block)

    return translated


# ---------- HTML-Post-Processing ----------

# Begriffe, die DeepL sprachlich richtig, aber fuer die Suche schaedlich
# uebersetzt. Sie werden nach der Uebersetzung pro Sprache zurueckgesetzt.
# Ohne das ging die polnische H2 bei jedem index.html-Lauf verloren: DeepL macht
# aus "Birkenbihl-App" ein "aplikacja Birkenbihla" — in Polen gesucht wird aber
# nach "metoda Birkenbihla". Der Regex greift die H2 ueber das Wort "Birkenbihl",
# ist also unabhaengig davon, wie DeepL den Rest des Satzes formuliert.
# / Terms DeepL renders correctly but in a way that hurts search visibility;
# restored per language after translation.
POST_TRANSLATION_FIXES = {
    "pl": [
        (
            r'(<h2 class="section-title">)[^<]*Birkenbihl[^<]*(</h2>)',
            "\\1Koniec ze starym systemem szkolnym – aplikacja do nauki języków "
            "metodą Birkenbihla\\2",
        ),
    ],
}


def adjust_html(html: str, lang_attr: str, slug: str, filename: str) -> str:
    """Nach der Übersetzung müssen einige HTML-Attribute angepasst werden,
    damit CSS/Bilder weiter geladen werden und SEO-Tags (canonical, hreflang,
    og:url) auf die richtige Sprachversion zeigen."""

    # 1. <html lang="de"> -> <html lang="xx">
    html = re.sub(r'(<html[^>]*\blang=")de("[^>]*>)', rf'\1{lang_attr}\2', html, count=1)

    # 2. Relative Asset-Pfade absolut machen (damit sie aus /<slug>/ auch funktionieren)
    # Wichtig: auch srcset muss erfasst werden (<picture><source srcset="..."></picture>)
    html = re.sub(r'(href|src|srcset)="(?!https?://|/|#|mailto:|tel:)(styles\.css|img/[^"]+|[^"]+\.ico|[^"]+\.png|[^"]+\.svg|[^"]+\.jpg|[^"]+\.jpeg|[^"]+\.webp)"', r'\1="/\2"', html)

    # 2b. Bildpfade in JS-String-Literalen absolut machen (z. B. das
    # Lightbox-slides-Array in index.html: { src: 'img/…' }). Der Regex
    # oben greift nur auf HTML-Attribute, nicht auf Strings im <script>.
    # / Absolutize image paths inside JS string literals (lightbox slides)
    # — the attribute regex above does not reach into <script> blocks.
    def _absolutize_js_img(match):
        return match.group(0).replace("'img/", "'/img/").replace('"img/', '"/img/')
    html = re.sub(r'<script\b[^>]*>.*?</script>', _absolutize_js_img, html, flags=re.DOTALL)

    # 2c. Links in den Cluster-Bereich auf die Sprachversion umbiegen, aber NUR
    # für Sprachen, die es dort auch gibt (CLUSTER_SLUGS). Sonst bliebe ein
    # türkischer Leser beim Klick auf der deutschen Seite hängen — und für
    # Sprachen ohne Übersetzung würde der Link ins Leere zeigen.
    # / Rewrite links into the cluster to the matching language version, but
    # only for languages that actually have one.
    if slug in CLUSTER_SLUGS:
        for prefix in CLUSTER_PREFIXES:
            html = html.replace(f'href="/{prefix}', f'href="/{slug}/{prefix}')

    # 3. Canonical-URL anpassen: https://linguaflow.app -> https://linguaflow.app/<slug>/
    page_path = url_path(filename)
    # Für index.html ist page_path leer -> /<slug>/ ; für Cluster-Seiten endet
    # page_path bereits auf "/" -> /<slug>/zurueck-in-deinen-beruf/
    canonical_url = f"{BASE_URL}/{slug}/{page_path}"
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
    # WICHTIG: hreflang="de" und x-default müssen auf die korrespondierende
    # deutsche Sub-Page zeigen (z.B. /hilfe.html), nicht aufs Root.
    de_url = f"{BASE_URL}/{url_path(filename)}"
    hreflang_links = [f'<link rel="alternate" hreflang="x-default" href="{de_url}">']
    hreflang_links.append(f'<link rel="alternate" hreflang="de" href="{de_url}">')
    for _, lattr, lslug, _, _ in languages_for(filename):
        # URL dieser Seite in dieser Sprache
        lang_url = f"{BASE_URL}/{lslug}/{url_path(filename)}"
        hreflang_links.append(f'<link rel="alternate" hreflang="{lattr}" href="{lang_url}">')

    hreflang_block = "\n  " + "\n  ".join(hreflang_links)
    # Vor </head> einfügen (nur falls noch nicht drin)
    if "hreflang" not in html:
        html = html.replace("</head>", f"{hreflang_block}\n</head>", 1)

    # 8. Alte Switcher entfernen (stammen aus der deutschen Quelle,
    #    wurden durch DeepL unverändert mitkopiert mit DE als "selected")
    html = re.sub(
        r'<!-- i18n-switcher:start -->.*?<!-- i18n-switcher:end -->\s*',
        '',
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<!-- i18n-navswitcher:start -->.*?<!-- i18n-navswitcher:end -->\s*',
        '',
        html,
        flags=re.DOTALL,
    )

    # 9. Neue Switcher mit der aktuellen Sprache als selected einfügen
    footer_switcher = build_footer_switcher(slug, filename)
    html = html.replace("</footer>", f"{footer_switcher}\n</footer>", 1)

    nav_switcher = build_navbar_switcher(slug, filename)
    html = re.sub(
        r'(<button class="hamburger")',
        nav_switcher + "\n    " + r"\1",
        html,
        count=1,
    )

    # 8. Sprachspezifische Keyword-Korrekturen (siehe POST_TRANSLATION_FIXES)
    for pattern, replacement in POST_TRANSLATION_FIXES.get(slug, []):
        html = re.sub(pattern, replacement, html, count=1)

    return html


def build_footer_switcher(current_slug: str, filename: str) -> str:
    """Full-Name Dropdown für den Footer (mit Markern für idempotentes Ersetzen)."""
    sub = url_path(filename)

    opts = []
    sel = " selected" if current_slug == "de" else ""
    opts.append(f'<option value="/{sub}"{sel}>🇩🇪 Deutsch</option>')
    for _, _, slug, name, flag in languages_for(filename):
        sel = " selected" if slug == current_slug else ""
        opts.append(f'<option value="/{slug}/{sub}"{sel}>{flag} {name}</option>')

    options_html = "\n    ".join(opts)
    return (
        "<!-- i18n-switcher:start -->\n"
        '<div class="language-switcher" style="text-align:center;padding:20px 0 8px;">\n'
        '  <select onchange="if(this.value)location.href=this.value" aria-label="Sprache / Language" style="padding:8px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.05);color:inherit;font-size:14px;cursor:pointer;font-family:inherit;">\n'
        f"    {options_html}\n"
        "  </select>\n"
        "</div>\n"
        "<!-- i18n-switcher:end -->"
    )


def build_navbar_switcher(current_slug: str, filename: str) -> str:
    """Kompakter Switcher für die Navbar oben rechts: nur Flagge + Kurzcode."""
    sub = url_path(filename)

    opts = []
    sel = " selected" if current_slug == "de" else ""
    opts.append(f'<option value="/{sub}"{sel}>🇩🇪 DE</option>')
    for _, _, slug, _, flag in languages_for(filename):
        sel = " selected" if slug == current_slug else ""
        opts.append(f'<option value="/{slug}/{sub}"{sel}>{flag} {slug.upper()}</option>')

    options_html = "\n      ".join(opts)
    return (
        "<!-- i18n-navswitcher:start -->\n"
        '    <select class="nav-lang-switcher" onchange="if(this.value)location.href=this.value" aria-label="Sprache / Language">\n'
        f"      {options_html}\n"
        "    </select>\n"
        "    <!-- i18n-navswitcher:end -->"
    )


def enrich_source_file(source_path: pathlib.Path) -> bool:
    """Fügt hreflang-Tags, Footer- und Navbar-Language-Switcher in die
    deutsche Quelldatei ein. Idempotent: Mehrfache Aufrufe erzeugen
    dasselbe Ergebnis. Returns True wenn die Datei geändert wurde."""
    filename = rel_key(source_path)
    original = source_path.read_text(encoding="utf-8")
    html = original

    # Alte Marker entfernen (falls vorhanden) für sauberes Wiedereinfügen.
    # WICHTIG: [ \t]* entfernt auch die Einrückung VOR dem Start-Marker —
    # sonst wächst sie bei jedem Lauf um 2 Leerzeichen, der Datei-Hash
    # ändert sich und ALLE Seiten werden kostenpflichtig neu übersetzt.
    # / [ \t]* also strips the indentation BEFORE the start marker —
    # otherwise it grows every run, changing the file hash and forcing a
    # paid full re-translation of every page.
    for marker in ("i18n-hreflang", "i18n-switcher", "i18n-navswitcher"):
        html = re.sub(
            rf'[ \t]*<!-- {marker}:start -->.*?<!-- {marker}:end -->\s*',
            '',
            html,
            flags=re.DOTALL,
        )

    # hreflang-Block bauen
    hreflang_links = [
        f'<link rel="alternate" hreflang="de" href="{BASE_URL}/{url_path(filename)}">',
        f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/{url_path(filename)}">',
    ]
    for _, lattr, lslug, _, _ in languages_for(filename):
        url = f"{BASE_URL}/{lslug}/{url_path(filename)}"
        hreflang_links.append(f'<link rel="alternate" hreflang="{lattr}" href="{url}">')

    hreflang_block = "<!-- i18n-hreflang:start -->\n  " + "\n  ".join(hreflang_links) + "\n  <!-- i18n-hreflang:end -->"

    footer_switcher = build_footer_switcher("de", filename)
    nav_switcher = build_navbar_switcher("de", filename)

    # hreflang vor </head> einfügen
    html = html.replace("</head>", f"  {hreflang_block}\n</head>", 1)
    # Footer-Switcher vor </footer> einfügen
    html = html.replace("</footer>", f"{footer_switcher}\n</footer>", 1)
    # Navbar-Switcher vor dem Hamburger-Button einfügen
    html = re.sub(
        r'(<button class="hamburger")',
        nav_switcher + "\n    " + r"\1",
        html,
        count=1,
    )

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
    filename = rel_key(source_path)
    new_hash = file_hash(source_path)
    cached_hash = cache.get(filename)

    if not force and cached_hash == new_hash:
        print(f"  ✓ {filename}: unverändert, skip (Cache-Hit)")
        return 0

    target_languages = languages_for(filename)
    print(f"  → {filename}: geändert oder erstmalig — übersetze in {len(target_languages)} Sprachen …")
    source_html = source_path.read_text(encoding="utf-8")

    translated_count = 0
    for idx, (deepl_code, lang_attr, slug, name, _flag) in enumerate(target_languages, 1):
        print(f"     [{idx:2}/{len(target_languages)}] {slug} ({name}) … ", end="", flush=True)
        try:
            translated = deepl_translate(source_html, deepl_code, api_key)
        except Exception as e:
            print(f"FEHLER: {e}")
            continue
        adjusted = adjust_html(translated, lang_attr, slug, filename)
        # filename kann ein Unterpfad sein (Cluster-Seiten) — Verzeichnisse
        # deshalb mit parents=True anlegen.
        out_file = REPO_ROOT / slug / filename
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(adjusted, encoding="utf-8")
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
    # WICHTIG: Sub-Pages MIT .html, damit Sitemap konsistent zu canonical-Tags
    # und internen Links ist (sonst sieht Google /hilfe und /hilfe.html als Duplikate)
    for filename in SOURCE_FILES:
        urls.append(f"{BASE_URL}/{url_path(filename)}")

    # Alle Sprachen (Rechtstexte nur dort, wo sie wirklich übersetzt werden)
    for lang in LANGUAGES:
        _, _, slug, _, _ = lang
        for filename in SOURCE_FILES:
            if lang not in languages_for(filename):
                continue
            urls.append(f"{BASE_URL}/{slug}/{url_path(filename)}")

    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        if url == BASE_URL + "/":
            priority = "1.0"
        elif "zurueck-in-deinen-beruf" in url:
            priority = "0.8"
        elif "hilfe" in url or url.endswith("/ratgeber.html"):
            priority = "0.8"
        elif "ratgeber-" in url:
            priority = "0.6"
        else:
            priority = "0.3"
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
