# TODO — linguaflow.app Website

## In Arbeit
- (nichts)

## Erledigt
- Rechtstexte (Datenschutz, EULA, Impressum) nur noch Deutsch + Englisch: `LEGAL_FILES` + `languages_for()` in translate-site.py, 96 Sprachversionen durch Redirect-Stubs auf /en/ ersetzt, Hinweissatz „deutsche Fassung verbindlich" ergänzt. Spart ~10 €/Datei bei künftigen Änderungen (nur noch EN wird übersetzt, ~30 Cent)
- GSC-Indexierungs-Fixes: 27 Redirect-Stubs für alte WordPress-URLs (z. B. /kontakt/ → /hilfe.html), alle `href="index.html"`-Links → `href="./"` (310 Dateien, Quelle + Übersetzungen per sed), eigene 404.html. Translation-Cache-Hashes manuell aktualisiert → KEINE DeepL-Neu-Übersetzung nötig/ausgelöst
- 30-Tage-Testzeitraum (nur Jahresabo, iOS + Android) auf der Website: Preiskarte „Jährlich" in index.html (Feature-Zeile + Transparenzhinweis: gilt für neue Abonnenten, automatischer Übergang ins bezahlte Abo) + neue FAQ „Gibt es einen kostenlosen Testzeitraum?" in hilfe.html (sichtbar + JSON-LD)
- Ratgeber-Bereich Phase 1: Hub (`ratgeber.html`) + 4 Artikel (Anerkennung, 24h-Pflege→Festanstellung, Deutsch B2 Pflege, Haushaltshilfe Wien), automatisch in 33 Sprachen übersetzt
- „Ratgeber"-Links in Navbar + Footer von index.html und hilfe.html
- 404-Fix: AGB/Widerruf-Footer-Links auf absolute Pfade (`/agb.html`, `/widerruf.html`) — vorher 404 in allen Sprachversionen
- Kosten-Bug im Übersetzungs-Skript gefixt: `enrich_source_file()` ließ die Einrückung vor den i18n-Markern bei jedem Lauf wachsen → Datei-Hash änderte sich → JEDER Workflow-Lauf übersetzte die komplette Website neu (~17 €/Lauf)

## Backlog (Ratgeber Phase 2 — je Artikel einmalig ~15 € DeepL)
- Geringfügige Jobs in Österreich (Grenzen, Regeln)
- Putzfrau-Verdienst-Vergleich (privat vs. Firma vs. Plattform)
- Pflegeassistenz-Ausbildung in Österreich (Weg, Kosten, Stipendium)
- Gesundheitsberuferegister: Registrierung Schritt für Schritt
- Bewerbung auf Deutsch (Lebenslauf, Vorstellungsgespräch)
- Agentur-Vergleich 24-Stunden-Betreuung
- SK/RO-Feinschliff: Wenn /sk/ und /ro/ Traffic zeigen, Titles/H1 dort manuell auf idiomatische Suchbegriffe anpassen („opatrovateľka", „îngrijitoare")

## Nach dem Launch (manuell zu erledigen)
- Google Search Console: Sitemap neu einreichen, Indexierung von /ratgeber.html + Artikeln anfordern
- Nach 4–8 Wochen: Rankings/Klicks prüfen (v. a. /sk/ und /ro/), dann Phase 2 entscheiden

## Änderungsprotokoll
- 2026-07-12: Rechtstexte nur noch DE+EN (LEGAL_FILES in translate-site.py, 96 Redirect-Stubs, Disclaimer-Satz in 3 Quelldateien) — einmalige Kosten ~1 € (3 Dateien × EN), Enrichment-Simulation vor Push bestätigte: keine ungewollte Neu-Übersetzung
- 2026-07-12: GSC-Fixes: index.html-Links → "./" (Quelle + alle Sprachordner, Cache-Hashes angepasst, keine Übersetzungskosten), 27 Redirect-Stubs für alte WordPress-404-URLs, 404.html neu
- 2026-07-11: 30-Tage-Testzeitraum (Jahresabo) auf Preiskarte + FAQ ergänzt (index.html, hilfe.html) → löst Neu-Übersetzung beider Dateien aus
- 2026-07-11: Ratgeber-Bereich Phase 1 komplett (Pipeline-Registrierung, Hub, 4 Artikel, Verlinkung, 404-Fix, Kosten-Bug-Fix)

## Wichtige Regeln für dieses Repo
- Deutsche Root-HTML-Dateien sind die Quelle; /<sprache>/-Ordner NIE von Hand bearbeiten (werden von scripts/translate-site.py überschrieben)
- Rechtstexte (datenschutz/eula/impressum, siehe LEGAL_FILES in translate-site.py) gibt es nur DE + EN; die übrigen /<sprache>/-Versionen sind Redirect-Stubs auf /en/ und werden vom Skript NICHT angefasst
- Jede `ratgeber*.html` im Root wird automatisch übersetzt und geht live — keine Entwürfe unter diesem Namen committen
- Jeder Edit an einer Quelldatei kostet die volle Neu-Übersetzung dieser Datei (~14–18 € bei Artikeln) → Änderungen bündeln, vor Commit Korrektur lesen
- `SCRIPT_VERSION` in translate-site.py NIE ohne Grund erhöhen (~70 € Voll-Neuübersetzung)
- Nach jedem Push: `git pull` vor dem Weiterarbeiten (Bot committet Übersetzungen)
- Markenwording: immer „inspiriert von der Birkenbihl-Methode"
