#!/usr/bin/env python3
"""Schreibt Weiterleitungs-Seiten (Stubs) fuer alte Adressen, die Google als 404 meldet.

Warum es das gibt: Google meldet 404-Fehler fuer Adressen wie /pl/newsletter.html,
die es nie gab. Jede dieser Adressen bekommt eine kleine Seite, die per
meta-refresh auf die richtige Zielseite weiterleitet.

Idempotent: Vorhandene Dateien werden nie ueberschrieben. Ein zweiter Lauf
erstellt deshalb nichts mehr.

Aufruf:  python3 scripts/make-stubs.py

/ Writes meta-refresh redirect stubs for old URLs that Google reports as 404.
Idempotent: existing files are never overwritten, so a second run creates nothing.
"""
import importlib.util
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

# translate-site.py hat einen Bindestrich im Namen und ist deshalb nicht
# direkt importierbar. / Loaded by path because of the dash in the filename.
_spec = importlib.util.spec_from_file_location(
    "translate_site", REPO_ROOT / "scripts" / "translate-site.py")
ts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ts)

# Sprachordner = dritter Eintrag jeder LANGUAGES-Zeile (33 Stueck).
# / Language folders = third element of each LANGUAGES entry (33 in total).
SLUGS = [lang[2] for lang in ts.LANGUAGES]

# Vorlage wie pl/datenschutz.html. / Template matching pl/datenschutz.html.
TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <title>LinguaFlow</title>
  <meta http-equiv="refresh" content="0; url=https://linguaflow.app/{target}">
  <link rel="canonical" href="https://linguaflow.app/{target}">
</head>
<body>
  <p>{moved} <a href="https://linguaflow.app/{target}">https://linguaflow.app/{target}</a></p>
</body>
</html>
"""

# Alte Adresse -> Ziel. Ziele unter "en/" sind englisch, alle anderen deutsch.
# / Old address -> target. Targets under "en/" are English, all others German.
STUBS = []
for slug in SLUGS:
    if slug != "en":
        for name in ("newsletter.html", "was-ist-neu.html", "funktionen.html"):
            STUBS.append((f"{slug}/{name}", f"en/{name}"))
    # AGB und Widerruf gibt es nur auf Deutsch. / AGB and Widerruf exist only in German.
    for name in ("agb.html", "widerruf.html"):
        STUBS.append((f"{slug}/{name}", name))
STUBS += [
    ("hilfe/index.html", "hilfe.html"),
    ("unterstutzte-sprachen/index.html", "#sprachen"),
    ("en/linguaflow-video-bibliothek/index.html", "youtube/"),
]


def main():
    created = skipped = 0
    for old, target in STUBS:
        out = REPO_ROOT / old
        if out.exists():
            # Echte Seiten nie ueberschreiben. / Never overwrite a real page.
            print(f"skip (exists): {old}")
            skipped += 1
            continue
        if target.startswith("en/"):
            lang, moved = "en", "This page has moved:"
        else:
            lang, moved = "de", "Diese Seite ist umgezogen:"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(TEMPLATE.format(lang=lang, target=target, moved=moved), encoding="utf-8")
        print(f"created: {old}")
        created += 1
    print(f"Fertig / Done: {created} created, {skipped} skipped.")


if __name__ == "__main__":
    main()
