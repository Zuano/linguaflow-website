#!/usr/bin/env python3
"""Ruestet uebersetzte Meta-Beschreibungen, Teilen-Vorschau und alt-Texte in
bereits vorhandene Sprachversionen nach.

Warum es das gibt: DeepL laesst im HTML-Modus Attributwerte unangetastet. Bis
zum 25.10.2026 standen deshalb in allen Sprachversionen die deutsche
Meta-Description, og:/twitter:-Texte und alt-Texte — unter jedem
fremdsprachigen Google-Treffer erschien deutscher Text. Seitdem uebersetzt die
Pipeline diese Attribute mit (translate_attributes() in translate-site.py),
aber nur, wenn eine Seite ohnehin neu uebersetzt wird.

Dieses Skript ersetzt NUR Attributwerte, die noch woertlich so in der deutschen
Quelle stehen, und laesst den uebersetzten Fliesstext unangetastet. Ein zweiter
Lauf findet nichts mehr (ausser Werten, die DeepL unveraendert zurueckgibt).

Aufruf:  python3 scripts/retrofit-meta.py              (alle Quelldateien)
         python3 scripts/retrofit-meta.py hilfe.html   (nur diese)
         DRY_RUN=1 davorsetzen, um nur zu berichten, ohne zu schreiben.

/ Retrofits translated meta descriptions, social previews and alt texts into
existing language versions, touching only values still identical to the
German source. A second run finds (almost) nothing.
"""
import importlib.util
import os
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

# translate-site.py hat einen Bindestrich im Namen und ist deshalb nicht
# direkt importierbar. / Loaded by path because of the dash in the filename.
_spec = importlib.util.spec_from_file_location(
    "translate_site", REPO_ROOT / "scripts" / "translate-site.py")
ts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ts)

# Wichtigste Maerkte zuerst (Search Console 2026-10-24), falls ein Lauf
# abbricht. / Strongest markets first, in case a run is interrupted.
PRIORITY = ["en", "pl", "hu", "sk", "it", "es", "tr"]

SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL)


def retrofit(filename: str, api_key: str, dry_run: bool) -> tuple:
    """Ruestet eine Quelldatei in allen ihren Sprachversionen nach.
    Gibt (geaendert, uebersprungen, zeichen) zurueck."""
    source = REPO_ROOT / filename
    if not source.exists():
        print(f"  ! {filename}: nicht gefunden")
        return 0, 0, 0
    only = ts.attribute_values(source.read_text(encoding="utf-8"))

    languages = sorted(ts.languages_for(filename),
                       key=lambda l: PRIORITY.index(l[2]) if l[2] in PRIORITY else len(PRIORITY))
    geaendert = uebersprungen = zeichen = 0
    print(f"  {filename}: {len(only)} deutsche Attributwerte, {len(languages)} Sprachen")

    for deepl_code, _lang_attr, slug, _name, _flag in languages:
        target = REPO_ROOT / slug / filename
        if not target.exists():
            print(f"     [{slug}] Datei fehlt, uebersprungen")
            uebersprungen += 1
            continue
        target_html = target.read_text(encoding="utf-8")
        offen = ts.attribute_values(target_html) & only
        if not offen:
            continue
        zeichen += sum(len(v) for v in offen)
        if dry_run:
            print(f"     [{slug}] {len(offen)} Werte (dry run)")
            continue

        print(f"     [{slug}] {len(offen)} Werte … ", end="", flush=True)
        out = ts.translate_attributes(target_html, deepl_code, api_key, only=only)
        if out == target_html:
            print("unveraendert (Fehler?), uebersprungen")
            uebersprungen += 1
            continue
        # Gegenprobe: Script-Bloecke (JSON-LD, JS) und hreflang muessen
        # unveraendert sein. / Sanity check: scripts and hreflang untouched.
        if (SCRIPT_RE.findall(out) != SCRIPT_RE.findall(target_html)
                or out.count("hreflang=") != target_html.count("hreflang=")):
            print("Gegenprobe gescheitert, Datei unveraendert")
            uebersprungen += 1
            continue
        target.write_text(out, encoding="utf-8")
        geaendert += 1
        print("OK")

    return geaendert, uebersprungen, zeichen


def main():
    dateien = sys.argv[1:] or ts.SOURCE_FILES
    dry_run = os.environ.get("DRY_RUN") == "1"
    api_key = os.environ.get("DEEPL_API_KEY", "")
    if not api_key and not dry_run:
        print("FEHLER: DEEPL_API_KEY nicht gesetzt.", file=sys.stderr)
        sys.exit(1)

    if not dry_run:
        ts.check_usage(api_key)
    print(f"\nRuestet Attribute nach{' (DRY RUN)' if dry_run else ''}: "
          f"{len(dateien)} Quelldateien\n")

    gesamt_g = gesamt_u = gesamt_z = 0
    for f in dateien:
        g, u, z = retrofit(f, api_key, dry_run)
        gesamt_g += g
        gesamt_u += u
        gesamt_z += z

    print(f"\nFertig. {gesamt_g} Dateien aktualisiert, {gesamt_u} uebersprungen.")
    print(f"An DeepL {'gingen' if not dry_run else 'gingen (geschaetzt)'} {gesamt_z:,} Zeichen "
          f"(~{gesamt_z / 1_000_000 * 20:.2f} EUR bei 20 EUR/Mio).")
    if not dry_run:
        ts.check_usage(api_key)


if __name__ == "__main__":
    main()
