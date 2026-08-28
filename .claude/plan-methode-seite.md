# Plan: Interaktive Methoden-Erklärseite (`methode.html`)

Stand: 2026-08-28 · Geplant in Session „linguaflow-interactive-explanation"
(Grilling-Runden 1+2 mit Christian, alle Entscheidungen siehe
`.claude/DECISIONS.md`, Abschnitt 2026-08-28). Begriffe: siehe `CONTEXT.md`.

## Ziel

Eine neue Website-Seite, die interaktiv erklärt, wie das Lernen mit LinguaFlow
funktioniert (inspiriert von der Birkenbihl-Methode) — kein Video, sondern zum
Anfassen: Der Besucher wählt Muttersprache und Zielsprache, sieht oben einen
antippbaren Beispieltext genau wie in der App (3- bzw. 4-Zeilen-Ansicht), darunter
die vorgelesene Erklärung mit Karaoke-Wort-Hervorhebung, ganz unten die
Download-Buttons. Später auch aus der App heraus verlinkbar (`?app=1` blendet
Navigation/Footer/Download aus).

## Aktuelle Situation

- Statische Website (GitHub Pages, kein Framework), DeepL-Pipeline
  `scripts/translate-site.py` mit Datei-Hash-Cache; jede Quellseiten-Änderung
  kostet Übersetzungsgeld → Änderungen bündeln.
- Es gibt noch keine Methoden-Erklärseite; auf `index.html` existiert nur die
  statische 4-Schritte-Sektion `#methode`.
- Die App bündelt Lernweg-Inhalte pro Sprachpaar
  (`LearningPath/LearningPathContent_*.json` im iOS-Repo) — Format-Vorbild,
  Inhalte werden aber NICHT übernommen (Entscheidung: eigener Beispieltext).
- Im App-Backend existiert das Muster für vorab generiertes Audio mit
  Wort-Zeitstempeln: `functions/scripts/generateLearningPathAudio.mjs`
  (ElevenLabs `/v1/text-to-speech/{voice}/with-timestamps`), Stimmen je Sprache
  in `functions/src/voiceCatalog.ts`, Dekodier-Funktion `decodeText` in
  `functions/src/decodeText.ts` (App-Repo:
  `~/Developer/LinguaFlow Apps beide/LinguaFlow iOS/LinguaFlowProject Claude
  Code debug with Emmas Liste. Wer ist schneller/functions/`).
- ElevenLabs-Konto: Pro-Tarif, 500.000 Zeichen/Monat; am 28.08. bereits
  ~709.000 verbraucht (Zusatzverbrauch aktiv, Aufpreis je 1.000 Zeichen);
  Kontingent-Reset ca. 9. September 2026.

## Feste Entscheidungen (nicht neu diskutieren)

1. **Sprachen:** die 33 kanonischen App-Sprachen (Kachelliste auf der Startseite;
   Quelle `AVAILABLE_LANGUAGES.md` im App-Repo). Volle Matrix: 33 Muttersprachen
   × 32 Zielsprachen = 1.056 Dekodierungen. Die 10 „nur-Quellsprache"-Sprachen
   (Google, ohne TTS) sind NICHT dabei.
2. **Beispieltext (freigegeben von Christian, deutscher Meistertext):**
   > „Ich habe viele Jahre in meinem Beruf gearbeitet. Dann bin ich in ein
   > neues Land gekommen. Jetzt lerne ich die Sprache. Bald arbeite ich wieder
   > in meinem Beruf."
3. **Erklärtext:** kompakt (~2.500 Zeichen gesamt), wird komplett kapitelweise
   vorgelesen (je Abschnitt ein Play-Knopf). Deutscher Meistertext wird in der
   Umsetzungssession geschrieben und von Christian freigegeben, DANN erst
   übersetzt/vertont. Markenwording: „inspiriert von der Birkenbihl-Methode".
   Inhalt: Intro/Überblick → die 4 Schritte (Dekodieren übernimmt die App /
   Aktives Hören / Passives Hören / Übungen je nach Lernziel: nur Verstehen →
   bei Schritt 3 aufhören; Sprechen → Chorsprechen mit A-B-Wiederholung und
   sehr langsamer Geschwindigkeit, geht überall, auch in der Straßenbahn;
   Schreiben → Text mitschreiben) → Anfänger-Weg und Fortgeschrittenen-Weg
   als zwei Karten nebeneinander (KEINE Level-Abfrage).
4. **Interaktion im Beispieltext-Player:** Wort antippen = Audio springt zu
   diesem Wort und spielt ab dort (KEIN Erklär-Popup, KEIN langes Drücken);
   Play/Pause; Geschwindigkeit 0,5×/1× (tonhöhen-erhaltend, `preservesPitch`);
   A-B-Wiederholung (Wort A antippen, Wort B antippen, Abschnitt läuft in
   Schleife); Karaoke-Hervorhebung des gesprochenen Worts. Darstellung wie App:
   Wortkarten (Original / Umschrift bei nicht-lateinischer Zielsprache / WfW)
   + sinngemäße Übersetzung als Satzzeile darunter.
5. **Aufbau:** eine scrollbare Seite (kein Wizard): Sprachauswahl → Inhalt wird
   eingeblendet, Beispieltext-Player oben sticky, darunter die Erklär-Kapitel
   mit Sprungmarken-Inhaltsverzeichnis, ganz unten Download-Badges
   (Bestands-Snippet `.store-badges` aus `index.html:285`).
6. **Setzungen (von Christian unbeanstandet):** Muttersprache wird nach
   Website-Sprachordner vorbelegt (Besucher von `/fr/` → Französisch), Auswahl
   in `localStorage` gemerkt; RTL-Darstellung bei Muttersprache Arabisch/
   Hebräisch; App-Modus-Parameter `?app=1`.
7. Nicht-lateinische Zielsprachen (4-Zeilen-System): AR, HE, ZH, JA, KO, TH,
   EL, RU, UK, BG (kanonisch: `languageScripts.ts` im App-Backend).

## Geplante Schritte

1. **Grundlagen extrahieren:** Sprachcodes (33) + je Sprache Voice-ID aus
   `functions/src/voiceCatalog.ts` (dieselben Stimmen wie die App; für den
   Erklärtext die Stimme der jeweiligen Muttersprache) + Nicht-Latein-Liste aus
   `languageScripts.ts` in eine kleine Konfigdatei im Website-Repo übernehmen.
   → Check: 33 Einträge, jede mit Voice-ID; Liste stimmt mit Startseiten-Kacheln
   überein.
2. **Deutschen Erklärtext schreiben** (~2.500 Zeichen, Kapitelstruktur wie oben).
   → Check: Christian gibt frei (harter Haltepunkt vor Übersetzung/Vertonung).
3. **Übersetzen per DeepL-API** (Schlüssel wie Website-Pipeline,
   `DEEPL_API_KEY`): Beispieltext → 33 Zielsprachen; Erklärtext → 33
   Muttersprachen; UI-Texte des Players (Knöpfe, Hinweise) → 33 Sprachen.
   Ablage als JSON unter `methode-daten/texte/`. Kosten ~2–3 €.
   → Check: 33+33 Dateien vorhanden, EN-Stichprobe gelesen, keine leeren Felder.
4. **1.056 Dekodierungen erzeugen** über die App-Pipeline: Skript ruft für jedes
   Paar (Zielsprachen-Text → Muttersprache) die Dekodier-Logik auf. Bevorzugt
   die Cloud Function `decodeText`; falls deren Auth/App-Check-Schutz den
   Skript-Aufruf verhindert, stattdessen die identischen Prompts aus
   `decodeText.ts` lokal mit dem Anthropic-SDK ausführen (gleiche Modelle,
   gleiches w/t/r-Format — vorher in `decodeText.ts` nachlesen). Kosten grob
   10–20 €. Ablage `methode-daten/dekodierungen/<ziel>_<mutter>.json`.
   Automatischer Validator: Schema, jeder Satz vorhanden, Wortzahl plausibel,
   Umschrift genau bei den 10 nicht-lateinischen Zielsprachen, keine leeren
   Übersetzungen.
   → Check: Validator meldet 1.056/1.056 grün; Christian macht Stichproben bei
   Muttersprache Deutsch (z. B. EN→DE, JA→DE, AR→DE).
5. **Audio generieren** (Muster `generateLearningPathAudio.mjs`,
   `with-timestamps`, ElevenLabs-Schlüssel aus dem macOS-Schlüsselbund, nie
   ausgeben): 33 Beispieltext-Audios (je Zielsprache, ~250 Zeichen) + 33×
   Kapitel-Audios des Erklärtexts (je Muttersprache, zusammen ~2.500 Zeichen).
   Gesamt grob 90–110k Zeichen. Wort-Zeitstempel als JSON neben jede MP3
   (`methode-daten/audio/…`). **Zeitpunkt (Entscheidung Christian 2026-08-28):
   sofort generieren, Aufpreis fürs überschrittene Monatskontingent akzeptiert.**
   Vor dem Lauf die exakte Zeichenzahl nennen.
   → Check: jede MP3 spielt ab; Zeitstempel streng aufsteigend; Stichprobe:
   Hervorhebung läuft synchron (DE + eine nicht-lateinische Sprache).
6. **Seite bauen:** `methode.html` (deutsche Quelle, Design wie Bestand:
   `styles.css`-Tokens, seitenspezifisches CSS inline, Navbar/Footer wie
   `funktionen.html`), ein Vanilla-JS-Player (Wortkarten, Tap-to-Play, A-B,
   Geschwindigkeit, Karaoke; lädt JSON/Audio je Paar erst bei Bedarf), Kapitel-
   Karaoke für den Erklärtext, Sprachauswahl mit Vorbelegung, `?app=1`,
   RTL-Umschaltung, JSON-LD (`HowTo`, Muster `index.html:114`).
   Karaoke-Detail: bei Muttersprachen/Zielsprachen ohne Leerzeichen (ZH, JA, TH)
   Hervorhebung über Zeichenbereiche statt Wort-Splitting.
   → Check: lokaler Preview (`static-preview`, Port 8137): Kernflüsse in DE,
   EN→JA (4 Zeilen), AR als Muttersprache (RTL); mobil 375 px ohne horizontales
   Scrollen; `?app=1` blendet Nav/Footer/Badges aus.
7. **Pipeline-Registrierung:** `methode.html` in `SOURCE_FILES` (alle 33
   Sprachen, NICHT in `DE_EN_ONLY_FILES`), **`.github/workflows/translate-site.yml`
   `paths:`-Filter ergänzen** (bekannte Falle vom 2026-08-04!), Sitemap prüft
   sich über `build_sitemap()` selbst. `SCRIPT_VERSION` NICHT anfassen.
   Vorher `enrich_source_file()`-Stabilität herstellen (zwei Läufe, byte-
   identisch — bekanntes Einrückungs-Thema), damit kein Hash-Flattern entsteht.
   → Check: lokale Trockenlauf-Simulation: nur `methode.html` wird übersetzt
   (33 Sprachen, ~2–4 €), alle Bestandsdateien Cache-Hits.
8. **Verlinkung `index.html` per Cache-Trick** (Präzedenz 2026-08-16): Link in
   die deutsche Quelle (z. B. Knopf „Interaktiv erleben" in der `#methode`-
   Sektion oder Navbar-Punkt „Methode"), Hash in
   `scripts/.translation-cache.json` aktualisieren, EN + EN-GB von Hand
   nachziehen (wird beim nächsten bezahlten index-Lauf sauber überschrieben).
   → Check: Simulation meldet Cache-Hit für `index.html`; Link funktioniert in
   DE + EN lokal.
9. **Commit/Push + Launch-QA:** Nach Push `git pull` (Bot-Commit). Live prüfen:
   `/methode.html` + Stichprobe Sprachordner (en, ja, ar) → 200; Audio lädt erst
   bei Interaktion (lazy); JSON-LD valide; Sitemap enthält die neuen URLs.
   → Check: Alle Punkte grün, Christian testet am Handy.
10. **Doku:** TODO.md (Erledigt + Protokoll), ggf. DECISIONS.md-Nachträge,
    neue Feature-Datei `.claude/features/methode-seite.md` (Akzeptanzkriterien),
    diesen Plan nach `.claude/done/` verschieben (mit Christians Bestätigung).

## Betroffene Dateien

- **Neu:** `methode.html`; `methode-daten/` (texte/, dekodierungen/ [1.056 JSON],
  audio/ [MP3+Zeitstempel-JSON]); Generier-Skripte unter `scripts/`
  (Übersetzen, Dekodieren, Audio, Validator); `.claude/features/methode-seite.md`
- **Geändert:** `scripts/translate-site.py` (SOURCE_FILES),
  `.github/workflows/translate-site.yml` (paths), `index.html` (+ `en/index.html`,
  `en-gb/index.html` von Hand), `scripts/.translation-cache.json` (Cache-Trick),
  `.claude/TODO.md`, ggf. `llms.txt` (Seite eintragen)
- **Nur lesen (App-Repo):** `functions/src/voiceCatalog.ts`,
  `functions/src/languageScripts.ts`, `functions/src/decodeText.ts`,
  `functions/scripts/generateLearningPathAudio.mjs`

## Risiken / Seiteneffekte

- **`decodeText`-Aufrufbarkeit:** Die Cloud Function kann Auth/App-Check
  verlangen → Fallback: identische Prompts lokal (Schritt 4). Nichts am
  Backend ändern, nur lesen/aufrufen.
- **Qualität exotischer Paare** (z. B. TH→HU) ist nur stichprobenartig prüfbar
  → Validator + Stichproben; Restrisiko von Christian akzeptiert (volle Matrix
  war seine Entscheidung in Kenntnis dessen).
- **ElevenLabs-Kontingent** aktuell überschritten → Zeitpunkt-Entscheidung
  (unten). Zeichen vor dem Lauf exakt zählen und Christian nennen.
- **Repo wächst um ~50–90 MB** (Audio) — für GitHub Pages ok, Klonzeit steigt.
- **Übersetzungs-Kostenfallen:** `SCRIPT_VERSION` nie erhöhen; `methode.html`
  erst registrieren, wenn der deutsche Text final ist (jeder spätere Edit
  kostet die Neu-Übersetzung der Seite); Enrichment-Stabilität vor dem ersten
  Lauf prüfen; NICHT `deepl_translate` mocken für Kostenschätzungen, sondern
  `deepl_translate_raw` (Lehre vom 2026-08-21).
- **Handbearbeitung von Sprachordnern** ist nur als dokumentierter Cache-Trick-
  Nachtrag in en/en-gb erlaubt (Präzedenz Galerie 2026-08-16) — sonst Regel
  „Sprachordner nie von Hand" beachten.
- **Parallele Session:** Eine separate Session repariert evtl. die toten
  `funktion-*.html`-Links (Task-Chip vom 28.08.). Berührungspunkt nur, falls
  dort `funktion-dekodieren.html` angelegt wird → dann von dort auf
  `/methode.html` verlinken, nicht doppelt bauen.

## Offene Fragen

1. Genauer Ort des index-Links (Navbar-Punkt „Methode" vs. Knopf in der
   `#methode`-Sektion) — Navbar-Platz ist knapp (Umbruch-Thema, siehe
   Entscheidung „Anerkennung" 2026-08-21). Vorschlag: Knopf in der Sektion.
   → Bei Schritt 8 kurz mit Christian klären.
