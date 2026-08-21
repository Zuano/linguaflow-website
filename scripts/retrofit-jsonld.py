#!/usr/bin/env python3
"""Ruestet uebersetztes JSON-LD in bereits vorhandene Sprachversionen nach.

Warum es das gibt: Bis zum 21.08.2026 hat translate-site.py alle <script>-Bloecke
pauschal vor DeepL geschuetzt, deshalb tragen alle vor diesem Datum uebersetzten
Seiten ein deutsches Schema. Seitdem uebersetzt die Pipeline die Schema-Texte mit
— aber nur, wenn eine Seite ohnehin neu uebersetzt wird. Eine Seite allein wegen
des Schemas neu zu uebersetzen kostet den vollen Seitentext mit: bei hilfe.html
rund 26 Euro statt der 7 Euro, die die Schema-Felder selbst ausmachen.

Dieses Skript ersetzt deshalb NUR den JSON-LD-Block in den vorhandenen
Sprachdateien und laesst den bereits uebersetzten Fliesstext unangetastet.

Aufruf:  python3 scripts/retrofit-jsonld.py hilfe.html [weitere.html ...]
         DRY_RUN=1 davorsetzen, um nur zu berichten, ohne zu schreiben.

/ Retrofits translated JSON-LD into existing language versions, leaving the
already-translated body text untouched.
"""
import importlib.util
import json
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

JSONLD_RE = re.compile(r'<script type="application/ld\+json">.*?</script>', re.DOTALL)


def retrofit(filename: str, api_key: str, dry_run: bool = False) -> tuple:
    """Ruestet eine Quelldatei in allen ihren Sprachversionen nach.
    Gibt (geaendert, uebersprungen, zeichen) zurueck."""
    source = REPO_ROOT / filename
    if not source.exists():
        print(f"  ! {filename}: nicht gefunden")
        return 0, 0, 0

    source_html = source.read_text(encoding="utf-8")
    source_blocks = JSONLD_RE.findall(source_html)
    if not source_blocks:
        print(f"  ! {filename}: kein JSON-LD enthalten")
        return 0, 0, 0

    geaendert = uebersprungen = zeichen = 0
    languages = ts.languages_for(filename)
    print(f"  {filename}: {len(source_blocks)} JSON-LD-Block/Bloecke, "
          f"{len(languages)} Sprachen")

    for deepl_code, lang_attr, slug, name, _flag in languages:
        target = REPO_ROOT / slug / filename
        if not target.exists():
            print(f"     [{slug}] Datei fehlt, uebersprungen")
            uebersprungen += 1
            continue

        target_html = target.read_text(encoding="utf-8")
        target_blocks = JSONLD_RE.findall(target_html)
        if len(target_blocks) != len(source_blocks):
            print(f"     [{slug}] Blockzahl weicht ab "
                  f"({len(target_blocks)} statt {len(source_blocks)}), uebersprungen")
            uebersprungen += 1
            continue

        print(f"     [{slug}] {name} … ", end="", flush=True)

        neue_blocks = []
        fehler = False
        for src_block in source_blocks:
            if dry_run:
                # Nur zaehlen, was an DeepL ginge
                m = re.match(r'<script type="application/ld\+json">(.*)</script>',
                             src_block, re.DOTALL)
                try:
                    slots = []
                    ts._collect_jsonld_texts(json.loads(m.group(1)), slots)
                    zeichen += sum(len(c[k]) for c, k in slots)
                except Exception:
                    pass
                neue_blocks.append(src_block)
                continue

            neu = ts.translate_jsonld_block(src_block, deepl_code, lang_attr, api_key)
            if neu == src_block:
                # translate_jsonld_block ist auf das Original zurueckgefallen
                fehler = True
            neue_blocks.append(neu)

        if fehler:
            print("Uebersetzung fehlgeschlagen, Datei unveraendert")
            uebersprungen += 1
            continue

        if dry_run:
            print("(dry run)")
            continue

        # Bloecke der Reihe nach ersetzen
        idx = {"i": 0}

        def _replace(_m):
            b = neue_blocks[idx["i"]]
            idx["i"] += 1
            return b

        out = JSONLD_RE.sub(_replace, target_html)

        # Gegenprobe: jeder Block muss lesbares JSON sein
        try:
            for b in JSONLD_RE.findall(out):
                inner = re.match(r'<script[^>]*>(.*)</script>', b, re.DOTALL).group(1)
                json.loads(inner)
        except Exception as e:
            print(f"ungueltiges JSON nach dem Ersetzen ({e}), Datei unveraendert")
            uebersprungen += 1
            continue

        target.write_text(out, encoding="utf-8")
        geaendert += 1
        print("OK")

    return geaendert, uebersprungen, zeichen


def main():
    dateien = sys.argv[1:]
    if not dateien:
        print("Aufruf: python3 scripts/retrofit-jsonld.py <datei.html> [...]",
              file=sys.stderr)
        sys.exit(1)

    dry_run = os.environ.get("DRY_RUN") == "1"
    api_key = os.environ.get("DEEPL_API_KEY", "")
    if not api_key and not dry_run:
        print("FEHLER: DEEPL_API_KEY nicht gesetzt.", file=sys.stderr)
        sys.exit(1)

    if not dry_run:
        ts.check_usage(api_key)
    print(f"\nRuestet JSON-LD nach{' (DRY RUN)' if dry_run else ''}: "
          f"{', '.join(dateien)}\n")

    gesamt_g = gesamt_u = gesamt_z = 0
    for f in dateien:
        g, u, z = retrofit(f, api_key, dry_run)
        gesamt_g += g
        gesamt_u += u
        gesamt_z += z

    print(f"\nFertig. {gesamt_g} Dateien aktualisiert, {gesamt_u} uebersprungen.")
    if dry_run:
        print(f"An DeepL gingen {gesamt_z:,} Zeichen "
              f"(~{gesamt_z / 1_000_000 * 20:.2f} EUR bei 20 EUR/Mio).")
    if not dry_run:
        ts.check_usage(api_key)


if __name__ == "__main__":
    main()
