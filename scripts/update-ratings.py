#!/usr/bin/env python3
"""
Holt die aktuellen App-Store-Bewertungen via iTunes Search API und
aktualisiert das MobileApplication JSON-LD in index.html.

- Fragt alle relevanten Länder ab (iTunes API liefert Ratings pro Land)
- Aggregiert die Gesamtzahl und den gewichteten Durchschnitt
- Schreibt aggregateRating nur ins HTML, wenn die Gesamtzahl >= THRESHOLD
- Wird von .github/workflows/update-ratings.yml täglich aufgerufen

Fetches current App Store ratings via iTunes Search API and
updates the MobileApplication JSON-LD in index.html.
"""

import json
import pathlib
import re
import sys
import urllib.request

APP_ID = "6744939323"
# Länder, in denen die App verfügbar ist (relevant für Ratings)
# Countries where the app is available (relevant for ratings)
COUNTRIES = [
    "at", "de", "ch", "li", "lu",          # DACH + kleine Nachbarn
    "us", "gb", "ca", "au", "ie", "nz",    # Englischsprachig
    "fr", "it", "es", "pt", "nl", "be",    # Westeuropa
    "se", "no", "dk", "fi",                # Nordeuropa
    "pl", "cz", "hu", "ro", "sk", "si",    # Mitteleuropa
    "gr", "tr"                              # Südost
]
THRESHOLD = 10  # Minimum Gesamt-Bewertungen bevor aggregateRating eingebaut wird

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX_FILE = REPO_ROOT / "index.html"


def fetch_ratings():
    """Holt die Ratings für alle Länder und aggregiert sie."""
    total_count = 0
    weighted_sum = 0.0
    per_country = {}

    for cc in COUNTRIES:
        url = f"https://itunes.apple.com/{cc}/lookup?id={APP_ID}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LinguaFlow-RatingBot/1.0"})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.load(response)
        except Exception as e:
            print(f"  [{cc}] Fehler: {e}", file=sys.stderr)
            continue

        results = data.get("results", [])
        if not results:
            continue
        app = results[0]
        count = int(app.get("userRatingCount") or 0)
        rating = float(app.get("averageUserRating") or 0)
        if count > 0:
            per_country[cc] = {"count": count, "rating": rating}
            total_count += count
            weighted_sum += rating * count

    avg = round(weighted_sum / total_count, 2) if total_count > 0 else 0.0
    return total_count, avg, per_country


def build_json_ld(count: int, avg: float) -> str:
    """Baut den MobileApplication JSON-LD Block als Text."""
    data = {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "LinguaFlow",
        "alternateName": "LinguaFlow – Birkenbihl Decoder",
        "description": "Sprachlern-App nach der Birkenbihl-Methode. Wort-für-Wort-Übersetzung mit Kontext, Bücher-Reader, 30+ Sprachen – ohne Vokabelpauken.",
        "applicationCategory": "EducationalApplication",
        "operatingSystem": "iOS, Android",
        "inLanguage": "de",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "EUR",
        },
        "downloadUrl": [
            "https://apps.apple.com/us/app/linguaflow-decoder/id6744939323",
            "https://play.google.com/store/apps/details?id=com.linguaflow&hl=de",
        ],
        "author": {
            "@type": "Organization",
            "name": "LinguaFlow e.U.",
            "url": "https://linguaflow.app",
        },
    }

    if count >= THRESHOLD:
        data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": avg,
            "ratingCount": count,
            "bestRating": 5,
            "worstRating": 1,
        }

    body = json.dumps(data, indent=2, ensure_ascii=False)
    # Einrückung an das umgebende HTML anpassen (2 Spaces)
    indented = "\n".join("  " + line for line in body.splitlines())
    return f'<script type="application/ld+json">\n{indented}\n  </script>'


def update_html(new_block: str) -> bool:
    """Ersetzt den Inhalt zwischen den Markern. Returns True, wenn etwas geändert wurde."""
    content = INDEX_FILE.read_text(encoding="utf-8")
    replacement = f"<!-- ratings:start -->\n  {new_block}\n  <!-- ratings:end -->"
    pattern = re.compile(r"<!-- ratings:start -->.*?<!-- ratings:end -->", re.DOTALL)
    if not pattern.search(content):
        print("FEHLER: Marker <!-- ratings:start --> / <!-- ratings:end --> nicht gefunden.", file=sys.stderr)
        sys.exit(1)
    updated = pattern.sub(replacement, content)
    if updated != content:
        INDEX_FILE.write_text(updated, encoding="utf-8")
        return True
    return False


def main():
    print(f"Hole Bewertungen für App-ID {APP_ID} aus {len(COUNTRIES)} Ländern …")
    total, avg, per_country = fetch_ratings()

    print(f"\nErgebnis:")
    for cc, info in sorted(per_country.items(), key=lambda x: -x[1]["count"]):
        print(f"  {cc.upper()}: {info['count']} Bewertungen, Ø {info['rating']}")
    print(f"\n  Gesamt: {total} Bewertungen, Ø {avg}")
    print(f"  Schwellwert: {THRESHOLD} Bewertungen")

    if total >= THRESHOLD:
        print(f"  → aggregateRating wird im HTML eingebaut")
    else:
        print(f"  → aggregateRating wird NICHT eingebaut (noch {THRESHOLD - total} fehlen)")

    block = build_json_ld(total, avg)
    changed = update_html(block)
    print(f"\nindex.html geändert: {changed}")


if __name__ == "__main__":
    main()
