#!/usr/bin/env python3
"""
Build the per-language app screenshots for the homepage gallery.
Baut die App-Bilder der Galerie pro Sprache.

Reads the raw screenshot runs (Aufnahmeläufe) from the shared screenshot folder,
takes the NEWEST recording per view and language, scales iPhone images to
1200 px width and writes WebP files to img/screens/<lang>/<view>.webp.
Liest die Aufnahmeläufe, nimmt je Ansicht und Sprache die NEUESTE Aufnahme,
skaliert iPhone-Bilder auf 1200 px Breite und schreibt WebP nach
img/screens/<sprache>/<ansicht>.webp.

Which language version shows which folder (fallbacks for en-gb, pt-br, th …)
is decided in translate-site.py (SCREENSHOT_LANG), not here.
Welche Sprachversion welchen Ordner zeigt, steht in translate-site.py.

Usage / Aufruf:  python3 scripts/build-screenshots.py
Needs / Braucht: cwebp (brew install webp)
"""

import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = pathlib.Path.home() / "Developer/LinguaFlow Apps beide/Screenshots LinguaFlow e.U.  Apps"
# Recording runs, NEWEST FIRST — a new run is added at the front.
# Aufnahmeläufe, NEUESTER ZUERST — ein neuer Lauf kommt vorne dazu.
RUNS = ["2026-09-27 Roh-Screenshots", "2026-09-22 Roh-Screenshots 6-7", "2026-09-15 Roh-Screenshots"]
OUT = REPO_ROOT / "img" / "screens"
# Raw images that must never be used (e.g. an error dialog in the picture);
# the next older recording is taken instead.
# Rohbilder, die nie verwendet werden dürfen (z. B. Fehlermeldung im Bild);
# stattdessen wird die nächstältere Aufnahme genommen.
SKIP = {
    "2026-09-27 Roh-Screenshots/iOS/lt Litauisch/02-decoded.png",  # read-aloud limit error / Vorlese-Limit-Fehler
}

# Output folder -> (platform, raw folder name). iOS where the iOS app has the
# language, Android only for languages iOS lacks.
# Ausgabeordner -> (Plattform, Rohordner). iOS, wo die iOS-App die Sprache hat,
# Android nur für Sprachen, die iOS fehlen.
IOS = {
    "ar": "ar Arabisch", "bg": "bg Bulgarisch", "cs": "cs Tschechisch", "da": "da Daenisch",
    "de": "de Deutsch", "el": "el Griechisch", "en": "en Englisch", "es": "es Spanisch",
    "fi": "fi Finnisch", "fr": "fr Franzoesisch", "hu": "hu Ungarisch", "id": "id Indonesisch",
    "it": "it Italienisch", "ja": "ja Japanisch", "ko": "ko Koreanisch", "lt": "lt Litauisch",
    "lv": "lv Lettisch", "nb": "nb Norwegisch", "pl": "pl Polnisch", "pt": "pt Portugiesisch",
    "ro": "ro Rumaenisch", "ru": "ru Russisch", "sk": "sk Slowakisch", "tr": "tr Tuerkisch",
    "uk": "uk Ukrainisch", "zh": "zh-Hans Chinesisch",
}
ANDROID = {"et": "et Estnisch", "nl": "nl Niederlaendisch", "sl": "sl Slowenisch", "sv": "sv Schwedisch"}

# View -> raw file names to try in order, per platform.
# Ansicht -> Rohdateinamen in Reihenfolge, je Plattform.
VIEWS = {
    "home":       {"iOS": ["01-home"], "Android": ["01-startseite"]},
    "decoding":   {"iOS": ["02-decoded"], "Android": ["02-dekodierung"]},
    "library":    {"iOS": ["07a-bibliothek"], "Android": ["07a-bibliothek"]},
    "reader":     {"iOS": ["07b-buch-offen"], "Android": ["07b-buch-offen"]},
    "lernweg":    {"iOS": ["03-lernweg"], "Android": ["03-lernweg"]},
    "lesson":     {"iOS": ["04-lernweg-lektion"], "Android": ["04-lernweg-lektion"]},
    "dialog":     {"iOS": ["08-dialog"], "Android": ["08-dialog"]},
    "textgen":    {"iOS": ["07-textgen"], "Android": ["07-text-generieren"]},
    "onboarding": {"iOS": ["12-onboarding-sprache"], "Android": []},
    "history":    {"iOS": ["06-verlauf", "09-verlauf"], "Android": ["06-verlauf", "09-verlauf"]},
}


def newest(platform: str, folder: str, names: list):
    """Newest recording of a view: first name wins, then newest run.
    Neueste Aufnahme einer Ansicht: erster Name zuerst, dann neuester Lauf."""
    for name in names:
        for run in RUNS:
            p = RAW / run / platform / folder / f"{name}.png"
            if p.exists() and str(p.relative_to(RAW)) not in SKIP:
                return p
    return None


def main() -> int:
    missing = []
    for lang, (platform, folder) in (
        [(k, ("iOS", v)) for k, v in IOS.items()] + [(k, ("Android", v)) for k, v in ANDROID.items()]
    ):
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        for view, names in VIEWS.items():
            src = newest(platform, folder, names[platform])
            # Android has no language-choice screen: use the English iPhone one.
            # Android hat keine Sprachwahl-Aufnahme: englisches iPhone-Bild.
            if src is None and view == "onboarding":
                src = newest("iOS", IOS["en"], names["iOS"])
            if src is None:
                missing.append(f"{lang}/{view}")
                continue
            # iPhone 1320 px -> 1200 px; Android stays 1080 px (no upscaling).
            # iPhone 1320 px -> 1200 px; Android bleibt 1080 px (nicht hochrechnen).
            resize = ["-resize", "1200", "0"] if "/iOS/" in str(src) else []
            dst = OUT / lang / f"{view}.webp"
            subprocess.run(["cwebp", "-quiet", "-q", "82", *resize, str(src), "-o", str(dst)], check=True)
            print(f"{lang}/{view}: {src.relative_to(RAW)}")
    if missing:
        print("FEHLT / MISSING:", ", ".join(missing), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
