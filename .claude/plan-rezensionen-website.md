# Plan: Rezensionsblock „Das sagen Lernende" auf der Startseite (DE + EN)

Stand: 2026-09-08 · Geplant in der Session „Rezensionen: Play/App Store + Website"
(Workspace „LinguaFlow Apps beide"). Umsetzung in einer NEUEN Session in diesem Repo.

## Ziel

Die drei 5-Sterne-Rezensionen aus Google Play als **Textzitate** (keine Screenshots)
auf der Startseite zeigen — als sozialer Beweis zwischen „So sieht LinguaFlow aus"
und „Preise". Nur Deutsch und Englisch; die 31 anderen Sprachversionen bleiben
unverändert (kein DeepL-Lauf, kein Geld).

## Aktuelle Situation

- Startseite `index.html` (Quelle, deutsch) → DeepL-Pipeline `scripts/translate-site.py`
  übersetzt in 33 Sprachordner; **jede Änderung an index.html ohne Cache-Trick löst eine
  kostenpflichtige Neuübersetzung aus** (Startseite ≈ 5 €, siehe DECISIONS 2026-08-28).
- Es gibt noch keinen Rezensions-/Testimonial-Bereich. JSON-LD `aggregateRating` wird von
  `scripts/update-ratings.py` nur aus dem App Store (iTunes-API) befüllt, erst ab 10
  Bewertungen (`THRESHOLD`) — bleibt wie es ist, hat mit diesem Block nichts zu tun.
- Rezensionen (Play Console, Stand 2026-09-08, alle 5★, Standardbewertung 5,0 bei 3 Nutzern):
  1. **Ben S.** (8. Sept. 2026, Original Englisch, Anfang wörtlich: „A great language
     learning tool 🔥 My favourite part is that you can now find free ebooks to decode a…"
     — **Rest des Originals in der Play Console über „Ursprüngliche Rezension anzeigen"
     wörtlich abholen**, nichts ergänzen). Deutsche Fassung aus der Play Console (vollständig):
     „Ein großartiges Sprachlerntool 🔥 Besonders toll finde ich, dass man jetzt kostenlose
     E-Books zum Entschlüsseln und Lesen in der Zielsprache findet! Nach meiner ersten
     Rezension hat sich der Entwickler gemeldet und mein Feedback berücksichtigt. Die Fehler
     wurden behoben und weitere Funktionen hinzugefügt, die das gesamte Erlebnis deutlich
     angenehmer machen. Dank der neuen Wiedergabeoptionen kann ich einzelne Wörter oder
     Sätze auswählen und sie so oft und in meiner bevorzugten Geschwindigkeit abspielen,
     wie ich möchte. Vielen Dank fürs Zuhören!"
  2. **Stefan C.** (6. Juli 2026, Deutsch): „Endlich eine App für Fans der Sprachlernmethode
     nach Vera F. Birkenbihl. Die vier Schritte der Methode werden unverfälscht und elegant
     umgesetzt. Sehr engagierter und vor allem offener Entwickler. Über kleinere
     Kinderkrankheiten kann man locker hinwegsehen, vor allem weil die App kontinuierlich
     verbessert wird. Ich wünsche der App und dem Entwickler einen großen Erfolg."
  3. **Dawid J.** (5. Juli 2026, Original Polnisch): „Bardzo polecam te aplikację, pomaga
     zaoszczędzić dużo czasu i znacznie przyspiesza naukę języka💯💥, …" — deutsche
     Fassung (Play-Übersetzung): „Ich kann diese App wärmstens empfehlen, sie spart viel
     Zeit und beschleunigt das Sprachenlernen erheblich💯💥. Die Entwickler sorgen für eine
     einwandfreie Funktion und lösen alle Probleme sehr schnell."
- App Store: 0 schriftliche Rezensionen (per API geprüft) → vorerst nur Play-Zitate;
  Block so bauen, dass später App-Store-Zitate mit eigenem Quellen-Label dazukommen.

## Feste Entscheidungen (Christian 2026-09-08)

- **Textzitate, keine Screenshots** (Profilbilder/volle Namen = DSGVO-heikel, nicht
  lesbar am Handy, nicht übersetzbar, für Google unsichtbar).
- **Nur DE + EN.** Andere Sprachen bekommen den Block NICHT (auch nicht beim nächsten
  bezahlten index-Lauf — dafür Block als DE/EN-only markieren, siehe Schritt 2).
- **Namensform: Vorname + Initial** („Ben S."), Quelle „Google Play" + Monat/Jahr,
  Link zum Play-Eintrag, damit Besucher nachprüfen können.
- **Zitate wörtlich, Kürzungen nur mit „…"**; die Passage „kleinere Kinderkrankheiten"
  darf gekürzt, aber nicht sinnverfälscht werden. Übersetzte Zitate mit Hinweis
  „übersetzt aus dem Polnischen/Englischen".
- **Markenregel:** Stefans Zitat nennt „Birkenbihl" — als Nutzerzitat zulässig, aber
  Überschrift/Umtext bleibt „inspiriert von der Birkenbihl-Methode" (CONTEXT.md).
- **Ben vorher fragen** (Mail-Kontakt besteht, siehe Memory `ben-sharratt-antwort-gesendet`):
  kurze Bitte um Erlaubnis, ihn mit „Ben S." zu zitieren. Erst nach Ja live schalten;
  bis dahin zwei Zitate zeigen.

## Geplante Schritte

1. **Ben um Zitat-Erlaubnis bitten** (Christian schreibt, Entwurf kommt aus der Session)
   → Check: Antwort liegt vor; ohne Ja bleibt sein Zitat draußen.
2. **Übersetzungs-Pipeline vorbereiten:** in `scripts/translate-site.py` einen Weg schaffen,
   dass ein markierter Block (`<!-- i18n:de-en-only -->` … `<!-- /i18n:de-en-only -->`)
   bei allen Sprachen außer EN/EN-GB **entfernt** statt übersetzt wird; oder — einfacher,
   wenn es der Pipeline-Code hergibt — den Block ausschließlich per Hand in `index.html`,
   `en/index.html`, `en-gb/index.html` einfügen und den Cache-Hash von `index.html` per
   Cache-Trick nachziehen (Präzedenz DECISIONS 2026-08-28). **Zuerst prüfen, ob die
   Pipeline Blöcke überspringen kann**; Entscheidung dokumentieren.
   → Check: `translate-site.py --dry-run` meldet 0 zu übersetzende Dateien.
3. **Sektion bauen** in `index.html` zwischen `#app` (App-Showcase) und `#preise`:
   `section.reviews#rezensionen` mit `section-label` „Rezensionen", Titel „Das sagen
   Lernende", Untertitel mit Bewertung („5,0 ★ bei Google Play"), drei Karten im Stil der
   `pricing-card` (Sterne, Zitat, Name + Quelle + Datum + Hinweis „übersetzt"), darunter
   Link „Alle Rezensionen bei Google Play". Mobil untereinander, ab Tablet drei Spalten.
   Kein JS. Kein `Review`-JSON-LD mit Einzelrezensionen (Google erlaubt Self-Serving-
   Reviews nicht als Rich Result → kein Nutzen, Abmahnrisiko null, aber unnötig).
   → Check: Seite validiert (`pruefe.mjs` falls vorhanden / HTML-Validator), Lighthouse
   ohne neue Fehler, dunkles Schema sauber.
4. **Englische Fassung** per Hand in `en/index.html` + `en-gb/index.html` (Bens Original,
   Stefans und Dawids Zitat ins Englische übersetzt, Hinweis „translated from German/Polish").
   → Check: /en/ und /en-gb/ zeigen den Block, alle anderen Sprachen nicht.
5. **Navbar/Footer NICHT anfassen** (würde alle Sprachen betreffen). Sprungziel
   `#rezensionen` nur intern.
6. **Push + Live-Check** (Cloudflare/GitHub Pages), Sitemap unverändert.
   → Check: `curl` auf /, /en/, /fr/ — Block nur in den ersten beiden.
7. **Pflege-Regel** in `.claude/features/rezensionen.md` festhalten: Neue Rezension →
   Zitat prüfen (Erlaubnis bei Namensnennung), Karte ergänzen, EN nachziehen; App-Store-
   Zitate mit Label „App Store". Bewertungsdurchschnitt im Untertitel bei jeder Änderung
   gegen die Play Console prüfen.

## Betroffene Dateien

- `index.html` (neue Sektion), `styles.css` (`.reviews`, `.review-card`, Sterne)
- `en/index.html`, `en-gb/index.html` (Hand-Nachtrag)
- `scripts/translate-site.py` (nur falls Schritt 2 den Block-Skip einbaut) +
  `scripts/.translation-cache.json` (Cache-Trick)
- `.claude/features/rezensionen.md` (neu), `.claude/TODO.md`, `.claude/DECISIONS.md`

## Risiken / Seiteneffekte

- **Kosten:** Ohne Cache-Trick übersetzt der nächste Workflow-Lauf die Startseite in
  33 Sprachen (~5 €) und der Block landet überall. Schritt 2 ist Pflicht vor dem Push.
- **Persönlichkeitsrecht:** Volle Namen nur mit Erlaubnis; Initial-Form ist Standard.
  Zitate nie umformulieren.
- **Glaubwürdigkeit:** Nur drei Rezensionen — kein Problem, solange die Play-Zahl (3)
  ehrlich verlinkt ist. Keine erfundenen oder „aufgehübschten" Zitate.
- **Wettbewerbsrecht (AT):** Echte Nutzerbewertungen mit Quelle sind zulässig; die
  Bewertung „5,0" muss zum Store-Stand passen — bei Änderung nachziehen.

## Offene Fragen

- Soll der Block auch in `funktionen.html`/`hilfe.html`? (Vorschlag: nein, nur Startseite.)
- Darf die Session den Erlaubnis-Entwurf an Ben direkt über Christians Mail-Konto
  versenden oder nur den Text liefern? (Standard: nur Text liefern.)
