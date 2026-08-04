# CLAUDE.md – Projekt: LinguaFlow Website

## Projektübersicht
- **Produkt:** LinguaFlow – Sprachlern-App nach der Birkenbihl-Methode (iOS, Android)
- **Domain:** linguaflow.app
- **Dieses Repo:** Statische Marketing-Website (HTML / CSS, kein Framework)
- **Hosting / DNS:** WordPress (DNS wird in WordPress verwaltet)
- **Versionskontrolle:** GitHub (lokal kein `.git` verbunden)
- **Entwicklermodus:** Vibe Coding – Christian beschreibt, Claude setzt um

## Dateistruktur
- `index.html` – Startseite (Hero, Methode, Features, Sprachen, Download-CTA)
- `hilfe.html` – Hilfe / FAQ
- `datenschutz.html` – Datenschutzerklärung
- `eula.html` – Nutzungsbedingungen
- `impressum.html` – Impressum
- `styles.css` – Zentrale Stylesheet-Datei
- `img/` – Bilder, Screenshots, Badges

## Wichtige Links
- App Store: https://apps.apple.com/us/app/linguaflow-decoder/id6744939323
- Google Play: https://play.google.com/store/apps/details?id=com.linguaflow&hl=de

## Regeln für dieses Projekt
- Website-Änderungen immer am Desktop-Layout und Mobile-Layout prüfen (CSS-Breakpoints)
- DNS-Änderungen (SPF, DKIM, DMARC) dokumentiert Christian manuell im WordPress-DNS
- Claude kann DNS-Records NICHT selbst eintragen, nur Werte vorschlagen
- App-Code (iOS/Android) liegt NICHT in diesem Repo – für App-Features eigene Session starten
- Nach jeder Änderung: `.claude/TODO.md` aktualisieren (erledigt / neu entdeckt)

## Dokumentationspflicht
Bei jeder Änderung / jedem abgeschlossenen Task aktualisieren:
- **TODO.md** → was offen, was erledigt, Datum im Änderungsprotokoll
- **DECISIONS.md** → wenn eine inhaltliche / technische Entscheidung getroffen wurde
- **features/** → wenn ein neues größeres Thema dazukommt (Blog, Free-Tool, etc.)
