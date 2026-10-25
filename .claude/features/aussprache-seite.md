# Feature: Ratgeber-Seite „Aussprache verbessern" (`aussprache.html`)

Status: **gebaut 2026-10-25 auf Branch `feature/search-console`, noch nicht live** ·
Plan: `plan-search-console.md` Schritt 6 · Entscheidungen: `DECISIONS.md`
(2026-10-25) · Begriffe: `CONTEXT.md`

## Warum

Search Console (16 Monate bis 22.10.2026): ~600 Impressionen auf Suchen wie
„deutsche aussprache app" (178), „aussprache verbessern software" (103),
„deutsch aussprache app" (90), „aussprache verbessern apps" (57) bei 0–2 % CTR
und Position 8–16 — es gab keine passende Seite. Der alte WordPress-Artikel
`/deutsch-aussprache-lernen-…/` leitete nur auf die Startseite um.

## Was es ist

Kompakter Ratgeber (DE-Quelle, 33 Sprachen per Übersetzungs-Workflow):
Hören vor Sprechen → so übst du mit der App (Dekodieren, langsames Tempo mit
Wort-Hervorhebung, Wort lange drücken, A-B-Wiederholung, passives Hören in
Dauerschleife, Chorsprechen) → Umschrift für fremde Schriften → Beispielblock
„Deutsche Aussprache: typische Schwierigkeiten" (Beispielwörter mit
`translate="no"`) → Dialog mit KI-Gesprächspartner → FAQ (4, auch als
FAQPage-JSON-LD). Text sprachneutral („deine Zielsprache"), Titel nennt
„Deutsch und mehr". Keine Aussprache-Bewertung versprochen (gibt es nicht).

## Verlinkung

- Karte auf `ratgeber.html` (DE + 33 Sprachen; nur die Karte per DeepL
  übersetzt, Cache-Hash nachgezogen, ~0,26 €)
- Alter Stub `deutsch-aussprache-lernen-…/` → `/aussprache.html`,
  `en/deutsch-aussprache-lernen-…/` → `/en/aussprache.html`
- Sitemap (automatisch, `SOURCE_FILES`)

## Akzeptanzkriterien

- [x] In `SOURCE_FILES` und im Workflow-Pfadfilter
- [x] Opus-Review Text (Fakten, Markenwording, Übersetzbarkeit) — Funde eingearbeitet
- [x] Kosten ≤ 10 €: geschätzt ~7,95 €, tatsächlich 3,94 € (197.010 Zeichen) dank Schutz der Sprachwahl-Blöcke
- [x] 33 Sprachversionen erzeugt (lokal, 2026-10-25), Link-Checker 0 fehlende Ziele
- [ ] Live: 5 Sprachversionen 200
- [ ] GSC: Seite indexiert; erscheint bei „deutsche aussprache app"; CTR > 2 % nach 6 Wochen

## Kosten

Schätzung pro Sprache ~12.000 Zeichen → 33 Sprachen ≈ 7,95 €; tatsächlich verbraucht 197.010 Zeichen ≈ 3,94 € (DeepL zählt HTML-Tags offenbar nicht voll). Ratgeber-Karte 6.270 Zeichen ≈ 0,13 €.
Ohne den Schutz der Sprachwahl-Blöcke wären es ~12,70 € gewesen.
