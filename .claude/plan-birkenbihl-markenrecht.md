# Plan: Birkenbihl-Markenrecht auf der Website entschärfen

Stand 2026-09-23, Grilling-Session „birkenbihl-trademark-review" (alle Punkte von
Christian entschieden; Vorher-Nachher-Tabelle am 2026-09-23 freigegeben). Entscheidungen: `.claude/DECISIONS.md` (2026-09-23),
Glossar: `CONTEXT.md` („LinguaFlow-Methode", „Birkenbihl-Methode").
Branch: `fix/birkenbihl-markenrecht` (Worktree `.claude/worktrees/birkenbihl-markenrecht`).

## Ziel

„Birkenbihl" darf auf der Website nur noch als sachlicher Hinweis im Fließtext
vorkommen („inspiriert von der Birkenbihl-Methode", höchstens 1–2× pro Seite) —
nie als Produktname, Seitentitel, Überschrift, Blickfang-Zeile, Bild-Alt-Text,
Meta-Keyword oder Schema-Name. Ausnahme: ein sauber getrennter **Info-Block auf der
Hilfeseite**, der die Methode selbst erklärt (Fragen dürfen die Methode benennen),
mit Klarstellungssatz. Suchtreffer für „Birkenbihl-Methode" bleiben so weitgehend
erhalten.

## Aktuelle Situation

- Registerstand (TMview, 2026-09-23): In Österreich gilt nur die Unionsmarke
  **„Birkenbihl"** Nr. 011480051 (Ashoka GmbH, bis 2033, u. a. Klasse 9
  Lernsoftware). „Birkenbihl-Methode", „Dekodieren", „gehirngerecht" in AT frei.
- Anwaltsberatung (WKO, 2026-09): aktuelle Nutzung „definitiv rechtswidrig" —
  konkret „Birkenbihl App" im Browser-Titel, H2 „Sprachen lernen mit der
  Birkenbihl-App", H3 „Die Lösung: Birkenbihl-inspiriertes Lernen". Erlaubt:
  „inspiriert von" im Fließtext. Nicht-Antwort der Erbin ist keine Erlaubnis.
- Rund 7.400 Treffer in 33 Sprachen — fast alles DeepL-Übersetzungen der deutschen
  Quellseiten. Geändert werden nur die deutschen Quellen (+ Skripte), die
  Übersetzungen entstehen neu über die Pipeline.

## Vorher → Nachher (deutsche Quellseiten)

### `index.html` (Startseite) — wird neu übersetzt (~27 €)

| Zeile | Vorher | Nachher |
|---|---|---|
| 6 `<title>` | Birkenbihl App: Sprachen lernen ohne Vokabeln \| LinguaFlow | **Sprachen lernen ohne Vokabeln – LinguaFlow App** |
| 8 `meta keywords` | „Birkenbihl-Methode App, …" | „Birkenbihl-Methode App" entfernen (Rest bleibt) |
| 91 Schema `alternateName` | „LinguaFlow – Birkenbihl Decoder" | Feld **entfernen** (auch in `scripts/update-ratings.py:75`) |
| 92 Schema `description` | „Von der Birkenbihl-Methode inspirierte Sprachlern-App. …" | „Sprachlern-App, inspiriert von der Birkenbihl-Methode. …" (bleibt 1 Nennung; auch in `update-ratings.py:76`) |
| 119 Schema HowTo `name` | „Sprachen lernen mit der Birkenbihl-Methode in 4 Schritten" | „**Die LinguaFlow-Methode in 4 Schritten**" |
| 120 Schema HowTo `description` | „Die Birkenbihl-Methode zum Sprachenlernen funktioniert in vier … Schritten" | „Die LinguaFlow-Methode funktioniert in vier aufeinanderfolgenden Schritten – inspiriert von der Birkenbihl-Methode …" (1 Nennung) |
| 278 Hero `section-label` | Inspiriert von der Birkenbihl-Methode | **Die LinguaFlow-Methode** |
| 281 Hero-Absatz | „… intuitiv, natürlich und ohne Auswendiglernen." | „… intuitiv, natürlich und ohne Auswendiglernen – inspiriert von der Birkenbihl-Methode." |
| 299 `alt` | „… inspiriert von der Birkenbihl-Methode" | Zusatz entfernen |
| 317 H2 | „Schluss mit dem alten Schulsystem – Sprachen lernen mit der Birkenbihl-App" | „**Schluss mit dem alten Schulsystem – Sprachen lernen mit LinguaFlow**" (Wortlaut des Anwalts) |
| 332 H3 | „Die Lösung: Birkenbihl-inspiriertes Lernen" | „**Die Lösung: die LinguaFlow-Methode**" |
| 392 Feature-Karte „Gehirngerecht lernen" | „Inspiriert von der bewährten Birkenbihl-Methode. Keine Tricks – echte Wissenschaft." | „So, wie dein Gehirn von Natur aus lernt. Keine Tricks – echte Wissenschaft." |
| 439 `alt` | „… inspiriert von der Birkenbihl-Methode" | Zusatz entfernen |
| 442 + 759 Galerie-Text „Dekodierung" | „… – inspiriert von der Birkenbihl-Methode." | Zusatz entfernen (beide Stellen, HTML + `slides`-Array) |
| 637 Footer | „Sprachen lernen, inspiriert von der Birkenbihl-Methode. Intuitiv, gehirngerecht und mit Freude." | bleibt (Fließtext, 1 Nennung) |
| Footer neu | — | Klarstellungssatz (klein): „Birkenbihl® ist eine eingetragene Marke der Ashoka GmbH. LinguaFlow ist ein unabhängiges Angebot und steht in keiner Verbindung zu den Markeninhabern." |

Ergebnis: sichtbarer Fließtext nennt Birkenbihl 2× (Hero-Absatz, Footer) + Klarstellung.

### `hilfe.html` (Hilfe/FAQ) — wird neu übersetzt (~15–20 €)

| Stelle | Vorher | Nachher |
|---|---|---|
| 6 `<title>` | Birkenbihl-Methode FAQ – LinguaFlow App \| Hilfe | **Hilfe & FAQ – LinguaFlow App: Sprachen lernen ohne Vokabeln** |
| 7/9 `description` + `og:description` | „Birkenbihl-Methode erklärt: Wort-für-Wort-Dekodierung, …" | „Alle Antworten zur LinguaFlow App: Wort-für-Wort-Dekodierung, Sprachen, Preise. Außerdem erklärt: die Birkenbihl-Methode und was LinguaFlow daraus macht." |
| FAQ-Struktur | ein gemischter Block | **Zwei Blöcke** (HTML **und** FAQ-Schema): |
| Block 1 „Hintergrund: Die Birkenbihl-Methode" | — | Über dem Block der Klarstellungssatz (wie Footer). Fragen bleiben: „Was ist die Birkenbihl-Methode?", „Wie funktioniert die Birkenbihl-Methode genau?", „Wer war Vera F. Birkenbihl?", „Ist die Birkenbihl-Methode heute noch aktuell?", „Funktioniert die Birkenbihl-Methode wirklich?". Antworten **nur über die Methode**, kein LinguaFlow-Verkaufssatz darin. |
| 118–121 Antwort „Funktioniert … wirklich?" | „… von Hunderttausenden Lernenden erfolgreich angewendet" | „… und wird seit den 1990er-Jahren von vielen Lernenden angewendet" (Q6) |
| 166–169 / 502 „Welche Erfahrungen gibt es mit der Birkenbihl-Methode?" | vorhanden | **streichen** (HTML + Schema) — verkauft LinguaFlow unter Birkenbihl-Überschrift |
| Block 2 „Fragen zu LinguaFlow" | Fragen mit Birkenbihl-Bezug im Produktkontext | Überschriften ohne Birkenbihl, z. B. „Welche Methode steckt hinter LinguaFlow?" (Antwort: „Die LinguaFlow-Methode … inspiriert von der Birkenbihl-Methode"). Bestehende Antworten mit „inspiriert von" bleiben, aber max. 1–2 Nennungen im Block. |
| 233 / 456 | „… die viele klassische Birkenbihl-Angebote gar nicht im Programm haben" | „… die viele andere Sprachkurse gar nicht im Programm haben" |
| 217 / 540 | „das Birkenbihl-inspirierte Lernen … gratis ausprobieren" | „die LinguaFlow-Methode … gratis ausprobieren" |
| Footer | — | Klarstellungssatz wie Startseite |

**Block 1 bleibt bis zur Anwalts-Rückmeldung (Q11) unverändert**; alles andere wird umgesetzt.

### `methode.html` — wird neu übersetzt (~2–4 €)

| Stelle | Vorher | Nachher |
|---|---|---|
| 6 `<title>` | „… \| LinguaFlow, inspiriert von der Birkenbihl-Methode" | „… \| LinguaFlow" |
| 33 Schema `name` | „Sprachen lernen mit LinguaFlow – inspiriert von der Birkenbihl-Methode" | „Sprachen lernen mit LinguaFlow – die LinguaFlow-Methode in 4 Schritten" |
| 259 Erklärtext | „Die Methode dahinter ist inspiriert von der Birkenbihl-Methode und hat vier Schritte …" | bleibt (Fließtext; identisch mit `methode-daten/texte/erklaertext/de.json` und Audio `k1.json` — **nicht** neu vertonen) |

### `youtube/index.html` — nur Deutsch, keine Übersetzung

| Zeile | Vorher | Nachher |
|---|---|---|
| 7/10 `description` | „… synchron zum Video, inspiriert von der Birkenbihl-Methode." | bleibt (Fließtext) |
| 84 `section-label` | Birkenbihl-inspiriertes Lernen für YouTube | **Die LinguaFlow-Methode für YouTube** |
| 136 H3 Vergleichskarte | „LinguaFlow (Birkenbihl-inspiriert)" | „LinguaFlow" |
| 185 H3 Feature | „Birkenbihl-inspirierte Dekodierung" | „Dekodierung im Kontext" |
| 265 Fließtext | „… (inspiriert von der Birkenbihl-Methode)." | bleibt |

### Kleine Dateien (von Hand, keine Übersetzung)

| Datei | Vorher | Nachher |
|---|---|---|
| `manifest.json:4` | „Sprachlern-App nach der Birkenbihl-Methode." | „Sprachlern-App, inspiriert von der Birkenbihl-Methode." |
| `llms.txt:4` | „inspiriert von der Birkenbihl-Methode" | bleibt (1 Nennung, Fließtext) |
| `privacy-extension.html:69` | „(the Birkenbihl method)" | „(inspired by the Birkenbihl method)" |
| `datenschutz-extension.html` | analog deutsch | „(inspiriert von der Birkenbihl-Methode)" |
| `was-ist-neu.html:379` | „… inspiriert von der Birkenbihl-Methode." | bleibt |
| `scripts/update-ratings.py:75-76` | `alternateName` „Birkenbihl Decoder" | Feld entfernen; `description` wie oben |
| `scripts/translate-site.py:403-413` | PL-Fix erzwingt H2 „… metodą Birkenbihla" | Eintrag **entfernen** (H2 enthält kein Birkenbihl mehr; Regex würde ins Leere greifen) |

### Ratgeber-Seiten (`ratgeber*.html`, 5 Seiten) — bleiben unverändert (entschieden 2026-09-23)

CTA-Kasten: „… Inspiriert von der Birkenbihl-Methode, kostenlos ausprobieren."
Ist regelkonform (Fließtext, max. 2 Nennungen pro Seite). Änderung würde 5 Seiten
neu übersetzen lassen (~15 €/Seite = ~75 €). **Christian: so lassen.**

## Geplante Schritte

1. **Skripte zuerst** (`update-ratings.py`, `translate-site.py`) → Check: `grep -n Birkenbihl scripts/*.py` zeigt nur noch die `description`-Zeile.
2. **Kleine Dateien** (manifest, privacy/datenschutz-extension) → Check: grep zeigt nur „inspiriert von"/„inspired by".
3. **`index.html`** laut Tabelle → Check: `grep -c Birkenbihl index.html` = 5 (Schema-description, HowTo-description, Hero-Absatz, Footer, Klarstellung); keine Treffer in `<title>`, `<h1>`–`<h3>`, `alt=`, `section-label`.
4. **`methode.html`, `youtube/index.html`** → Check: keine Treffer in `<title>`/Überschriften/`section-label`.
5. **`hilfe.html` Block 2 + Titel/Description + Q6 + Streichung „Erfahrungen"** (Block 1 nur umsortieren, Klarstellungssatz davor) → Check: FAQ-Schema und sichtbares HTML enthalten dieselben Fragen; JSON-LD validiert (`python3 -c 'import json…'`).
6. **Klarstellungssatz** in Footer von `index.html` + `hilfe.html` → Check: sichtbar, klein, unter dem Footer-Text.
7. **Lokal prüfen**: `python3 -m http.server` im Repo, Startseite/Hilfe/Methode/YouTube im Browser durchsehen (Titel in der Tab-Leiste!).
8. **Commit + Push auf `fix/birkenbihl-markenrecht`**, dann Merge nach Christians Freigabe → GitHub Action übersetzt `index.html`, `hilfe.html`, `methode.html` neu (Kosten ~45–55 €, bewusst akzeptiert). Vorher `translate-site.py --dry-run` (bzw. Workflow `dry_run=true`) prüfen, dass **nur** diese drei Seiten neu übersetzt werden.
9. **Nach dem Lauf**: `grep -rli "Birkenbihl" --include=index.html --include=hilfe.html` in 3 Stichproben-Sprachen (en, pl, fr): kein Birkenbihl in `<title>`/H2/H3; PL-H2 ohne „metodą Birkenbihla". Live-Check auf linguaflow.app.
10. **Block 1 der Hilfeseite** nach Anwalts-Antwort (Q11) ggf. anpassen — eigener kleiner Commit.

## Betroffene Dateien

`index.html`, `hilfe.html`, `methode.html`, `youtube/index.html`, `manifest.json`,
`privacy-extension.html`, `datenschutz-extension.html`, `scripts/update-ratings.py`,
`scripts/translate-site.py`, (indirekt: alle 33 Sprachfassungen von index/hilfe/methode).
Doku: `CONTEXT.md`, `.claude/DECISIONS.md`, `.claude/TODO.md`, diese Datei.

## Risiken / Seiteneffekte

- **DeepL-Kosten**: ~45–55 € für drei Seiten. Alles andere ohne Übersetzung.
  Nicht anfassen: `ratgeber*.html` (sonst +75 €), `was-ist-neu.html`, `llms.txt`.
- **`update-ratings.py`** überschreibt den Schema-Block der Startseite bei jedem
  Lauf — ohne Skriptänderung käme „Birkenbihl Decoder" zurück.
- **PL-H2**: `POST_TRANSLATION_FIXES` würde die neue H2 nicht mehr treffen; Eintrag
  entfernen, sonst toter Code.
- **SEO**: Rankings für „Birkenbihl App" sinken voraussichtlich etwas (Wortfolge aus
  Titel/H2 verschwindet). Bewusst akzeptiert (DECISIONS 2026-09-23).
- **Audio der Methode-Seite** bleibt gültig (Fließtext-Nennung erlaubt).
- **Hilfeseite Block 1** ist rechtlich die verbleibende Grauzone → Anwaltsfrage (Q11).

## Offene Fragen

- Antwort des Anwalts zu Block 1 (E-Mail-Entwurf unten).

## E-Mail-Entwurf an die Kanzlei (Q11)

Betreff: Kurze Nachfrage zur Markenberatung – „Birkenbihl" auf der LinguaFlow-Hilfeseite

Sehr geehrter Herr [Name des Rechtsanwalts aus der WKO-Beratung],

vielen Dank noch einmal für die Beratung. Ich setze Ihre Hinweise gerade um:
„Birkenbihl" verschwindet aus dem Seitentitel, aus allen Überschriften und aus
Produktbezeichnungen; es bleibt nur noch der Hinweis „inspiriert von der
Birkenbihl-Methode" im Fließtext. Zusätzlich ergänze ich einen Klarstellungssatz
(„Birkenbihl® ist eine eingetragene Marke der Ashoka GmbH. LinguaFlow ist ein
unabhängiges Angebot und steht in keiner Verbindung zu den Markeninhabern.").

Eine Stelle ist mir noch unklar: Auf meiner Hilfeseite (linguaflow.app/hilfe.html)
gibt es einen rein informativen Frage-Antwort-Block über die Methode selbst, z. B.
„Was ist die Birkenbihl-Methode?", „Wie funktioniert die Birkenbihl-Methode?",
„Wer war Vera F. Birkenbihl?". Die Antworten beschreiben nur die Methode und
Frau Birkenbihl, ohne Werbung für meine App; der Block wird optisch vom
Produktteil getrennt und trägt den Klarstellungssatz.

Darf ein solcher Info-Block – mit dem Namen in den Frage-Überschriften – auf
einer Unternehmensseite bleiben, oder sollte ich auch dort den Namen aus den
Überschriften nehmen?

Mit freundlichen Grüßen
Christian Nouza
LinguaFlow e.U.
