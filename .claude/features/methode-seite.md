# Feature: Interaktive Methoden-Erklärseite (`methode.html`)

Status: **LIVE seit 2026-08-28** · geplant und gebaut in Session
„linguaflow-interactive-explanation" · Entscheidungen: `DECISIONS.md`
(Abschnitt 2026-08-28) · Plan: `plan-methode-seite.md` · Begriffe: `CONTEXT.md`

## Was es ist

`linguaflow.app/methode.html` erklärt interaktiv, wie Lernen mit LinguaFlow
funktioniert (inspiriert von der Birkenbihl-Methode): Sprachpaar wählen →
antippbarer Beispieltext im App-Stil (Wortkarten, 3/4-Zeilen-System) →
kapitelweise vorgelesene Erklärung mit Karaoke-Wort-Hervorhebung →
Download-Buttons. Verlinkt von der Startseite (Navbar „Methode" + Knopf
„✨ Erlebe die Methode interaktiv" in der `#methode`-Sektion).

## Akzeptanzkriterien (alle erfüllt, geprüft 2026-08-28)

- [x] 33 Sprachen als Mutter- UND Zielsprache → volle Matrix, 1.056 Dekodierungen
- [x] Wort antippen = Audio springt dorthin und spielt (kein Popup, wie die App)
- [x] A-B-Wiederholung, Langsam-Modus (0,5×, tonhöhen-erhaltend), Play/Pause
- [x] Karaoke-Hervorhebung (Wort- bzw. Zeichenbasis bei ZH/JA/TH)
- [x] 4-Zeilen-System mit Umschrift bei AR/HE/ZH/JA/KO/TH/EL/RU/UK/BG
- [x] RTL-Darstellung bei Arabisch/Hebräisch
- [x] Erklärung in der Muttersprache, komplett vorgelesen (App-Stimmen)
- [x] Kein API-Schlüssel im Browser (alles vorab generiert, statisch)
- [x] Muttersprache nach Sprachordner vorbelegt, Auswahl in localStorage
- [x] App-Modus `?app=1` (blendet Nav/Footer/Download aus, für WebView)
- [x] Mobil ohne horizontales Scrollen; Seite scrollt frei (keine Fixierung)
- [x] In Übersetzungs-Pipeline registriert; index.html per Cache-Trick verlinkt

## Datenhaltung

- `methode-daten/sprachen.json` — 33 Sprachen, App-Stimmen (voiceCatalog),
  TTS-Modelle, Nicht-Latein-/RTL-/Ohne-Leerzeichen-Kennzeichen, Ordner-Zuordnung
- `methode-daten/texte/` — Beispieltext (de + 32 Übersetzungen), Erklärtexte
  (33× 7 Kapitel), UI-Strings (`ui.json`)
- `methode-daten/dekodierungen/<ziel>_<mutter>.json` — 1.056 Dateien, Format
  wie App-Backend (`pairs` mit w/t/r, `translation` je Satz)
- `methode-daten/audio/` — Beispiel (33 MP3+Timing-JSON), Erklärung (231)
- Gesamt ~124 MB im Repo (bewusst: Seite bleibt ohne App-Backend lauffähig)

## Pflege / Neu generieren (Skripte in `scripts/methode/`, resume-fähig)

Schlüssel im macOS-Schlüsselbund: `DEEPL_API_KEY` + `ANTHROPIC_API_KEY`
(je `-a linguaflow`), `ELEVENLABS_API_KEY`.

1. Beispieltext ändern → `uebersetze-beispieltext.mjs` → betroffene
   `dekodierungen/` löschen → `dekodiere.mjs --all` → `audio/beispiel/` löschen
   → `vertone.mjs --beispiel`
2. Erklärtext ändern → `texte/erklaertext/de.json` UND statische Kapitel in
   `methode.html` anpassen → alte `erklaertext/<lang>.json` löschen →
   `uebersetze-erklaertext.mjs` → betroffene `audio/erklaerung/` löschen →
   `vertone.mjs --erklaerung`
3. Immer zum Schluss: `pruefe.mjs` (muss „Alles grün" melden)
4. `methode.html`-Änderungen kosten beim Push die Neu-Übersetzung der Seite
   (~2–4 €) — bündeln; die Datendateien (`methode-daten/`) kosten NICHTS
   (nicht in der DeepL-Pipeline)

## Bekannte Grenzen / Ideen

- Neue App-Sprache = Eintrag in `sprachen.json` + Skripte laufen lassen
  (Matrix wächst um 2×33 Paare) + `LANGUAGES` der Website prüfen
- Qualität exotischer Paare (z. B. TH→HU) nur stichprobenartig prüfbar —
  Restrisiko bewusst akzeptiert (Entscheidung Christian, 2026-08-28)
- Später möglich: Link aus der App auf `…/methode.html?app=1`
