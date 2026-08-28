# Entscheidungen — linguaflow.app Website

## 2026-08-28 — Interaktive Methoden-Erklärseite (`methode.html`): Grundsatzentscheidungen

Geplant in der Session „linguaflow-interactive-explanation" (Grilling-Runden 1+2,
alle Punkte von Christian entschieden). Details und Schritte: `.claude/plan-methode-seite.md`.

- **Audio wird vorab generiert, nicht zur Laufzeit.** Die Vorlese-Audios (Beispieltext
  je Zielsprache, Erklärtext je Muttersprache) entstehen einmalig per Skript über die
  Sprachsynthese-API (Muster: `functions/scripts/generateLearningPathAudio.mjs` im
  App-Backend, Endpunkt `with-timestamps` liefert Wort-Zeitstempel für die
  Karaoke-Hervorhebung). Die Website liefert nur statische MP3+JSON aus.
  **Begründung:** Ein API-Schlüssel im Browser wäre sofort stehlbar; ein Proxy-Server
  hätte laufende Kosten und widerspricht der statischen GitHub-Pages-Architektur.
  Nachteil (akzeptiert): Textänderungen erfordern Neu-Generierung per Skript.
  Der Anbieter der Sprachsynthese wird auf der Website weiterhin nicht genannt
  (Bestandsregel, nur „Muttersprachler-Qualität").
- **Volle Sprachpaar-Matrix: 33 × 32 = 1.056 Dekodierungen.** Muttersprache und
  Zielsprache kommen beide aus der kanonischen App-Sprachliste (die 33 Kacheln auf
  der Startseite, Quelle `AVAILABLE_LANGUAGES.md` im App-Repo; inkl. Hebräisch und
  Russisch, die keine Website-Ordner haben — die Muttersprache wird auf der Seite
  gewählt, nicht über den Sprachordner). Die 10 „nur-Quellsprache"-Sprachen der App
  (Google-Übersetzung, ohne Sprachausgabe) sind ausdrücklich NICHT dabei.
- **Dekodierungen entstehen über die App-eigene Dekodier-Pipeline** (Cloud Function
  `decodeText`, Claude-gestützt, inkl. Umschrift bei nicht-lateinischen Schriften),
  nicht über eine Website-eigene Nachbildung. **Begründung:** Die Website soll
  exakt zeigen, was die App liefert; Qualität und Format (w/t/r-Paare) sind dort
  bereits produktionserprobt. Einmalige KI-Kosten grob 10–20 €.
- **Ein erfundener Beispieltext statt Lernweg-Inhalt der App** (Christians Wunsch):
  4 kurze Sätze zum Thema „zurück in deinen Beruf dank Sprachkenntnissen" —
  universell, nicht berufsspezifisch. Deutscher Meistertext, per DeepL in die 33
  Zielsprachen übersetzt, dann je Paar dekodiert.
- **Alle Daten liegen im Website-Repo** (Dekodierungs-JSON, Audio, Zeitstempel;
  geschätzt 50–90 MB), nicht im Google-Cloud-Speicher der App. **Begründung:**
  Die Seite bleibt eigenständig lauffähig, unabhängig von Umbauten am App-Backend.
- **`methode.html` wird in alle 33 Website-Sprachen übersetzt** (reguläre
  Pipeline, einmalig 2–4 €), weil die Seite selbst 33 Muttersprachen bedient —
  eine nur-deutsche Hülle wäre unstimmig. Die interaktiven Inhalte liegen in
  eigenen JSON-Dateien und laufen NICHT durch DeepLs Seitenübersetzung
  (Inline-JS/Daten sind dort ohnehin geschützt).
- **Verlinkung von `index.html` per Cache-Trick** + Hand-Nachtrag in EN/EN-GB
  (Präzedenz: Galerie-Erweiterung 2026-08-16); restliche Sprachen beim nächsten
  ohnehin bezahlten index-Lauf. Spart ~27 € Sofortkosten.
- **Kein Erklär-Popup beim Wort-Antippen:** Tippen springt im Audio zu diesem Wort
  und spielt ab dort — exakt das App-Verhalten. Keine Level-Abfrage vor dem Start;
  Anfänger- und Fortgeschrittenen-Weg werden beide gezeigt. Eigenständige Seite,
  keine technische Vorleistung für das Free-Tool aus dem Marketing-Backlog.
- **Geprüft und verworfen:** `npx create-ai-eng-app` (Kurs-Kit für
  Next.js/Supabase-Apps; passt weder zur statischen Website noch zur
  Tutorial-Seite, würde CLAUDE.md/Settings des Repos umschreiben, UNLICENSED
  ohne einsehbares Repository).

## Rechtstexte nur Deutsch + Englisch (2026-07-12)

**Entscheidung:** Datenschutzerklärung, EULA und Impressum gibt es nur noch auf
Deutsch (verbindlich) und Englisch (Service). Die übrigen 32 Sprachversionen
sind Redirect-Stubs auf die englische Fassung. AGB und Widerruf waren schon
immer nur Deutsch.

**Begründung:**
- DeepL-Kosten: Jede Änderung an einem Rechtstext kostete vorher eine
  Neu-Übersetzung in 33 Sprachen; jetzt nur noch Englisch (Cent-Bereich).
- Rechtlich sauberer: Maschinell übersetzte Rechtstexte in 33 Sprachen sind
  eher Risiko als Nutzen. In den Quelldateien steht jetzt der Hinweis
  „rechtlich verbindlich ist die deutsche Fassung".
- SEO irrelevant: Google indexierte diese Seiten in den exotischen Sprachen
  ohnehin nicht (Search-Console-Befund vom 12.07.2026).

**Umsetzung:** `LEGAL_FILES` + `languages_for()` in `scripts/translate-site.py`
steuern das automatisch (Übersetzung, hreflang, Sprach-Switcher, Sitemap).

**Das bleibt so.** Nicht rückgängig machen, ohne Christian zu fragen. Neue
Rechtstexte, die nur DE+EN sein sollen, einfach in `LEGAL_FILES` eintragen.
Die Redirect-Stubs in den Sprachordnern (z. B. `/fr/eula.html`) NICHT löschen
(sonst 404s in Google) und NICHT von Hand „zurückübersetzen".

## „Was ist neu"-Seite (Changelog) nur Deutsch + Englisch (2026-08-04)

**Entscheidung:** Die neue Changelog-Seite `/was-ist-neu.html` gibt es nur auf
Deutsch (Quelle) und Englisch (`/en/was-ist-neu.html`). Gesteuert über
`DE_EN_ONLY_FILES` in `scripts/translate-site.py` (gleicher Mechanismus wie
`LEGAL_FILES`, aber eigenes Set, weil es kein Rechtstext ist).

**Begründung:**
- Die Seite wird bei jedem App-Release aktualisiert — 33 Sprachen wären bei
  jeder Änderung teuer, DE+EN kostet nur Cent-Beträge (Wunsch von Christian,
  Session 2026-08-04).
- Die Versionshistorie wurde aus dem Git-Verlauf des iOS-Projekts und den
  App-Store-Release-Notes rekonstruiert (`.claude/appstore/release-notes-v2.3*.md`
  und `release-status.md` im iOS-Projekt).

**Umsetzung:** Einträge beziehen sich auf iOS-Versionen (2.4, 2.3.1, 2.3, 2.0,
1.0), neueste zuerst. Bei jedem neuen Release oben einen Eintrag ergänzen.
Android-Einträge können später ergänzt werden (Android aktuell 1.4.2).

## 2026-08-21 — JSON-LD wird uebersetzt, Nachruestung statt Neuuebersetzung

**Entscheidung:** Die Schema-Textfelder (`name`, `text`, `description`,
`headline`) werden mitübersetzt; Struktur, URLs, Datumsangaben und
`Organization`-Knoten bleiben unangetastet. Inline-JavaScript wird weiterhin
komplett vor DeepL geschützt.
**Begründung:** Bei Seiten, die auf Zitierbarkeit durch Antwortmaschinen gebaut
sind, ist genau das Schema der Teil, der ausgelesen wird. Ein deutsches
FAQPage-Schema auf einer englischen Seite ist ein widersprüchliches Signal.

**Bei jedem Problem gilt die Rückfallebene:** unlesbares JSON, API-Fehler,
abweichende Antwortlänge oder ungültiges JSON nach dem Zusammenbauen führen zum
unveränderten deutschen Originalblock. Ein deutsches Schema ist unschön, ein
kaputtes wäre ein kritischer Fehler in der Search Console.

**Nachrüstung statt Neuübersetzung:** Für Seiten, die schon übersetzt sind,
tauscht `scripts/retrofit-jsonld.py` nur den Schema-Block aus. Eine
Neuübersetzung allein wegen des Schemas kostet den vollen Seitentext mit — bei
`hilfe.html` 25,95 € statt 7,35 €. Der zugehörige Workflow läuft nur manuell.

## 2026-08-21 — AEO-Cluster „Zurück in deinen Beruf" (Deutschland)

**Entscheidung:** Die drei Seiten aus `linguaflow-briefing.md` entstehen im
GitHub-Pages-Repo, nicht in WordPress. Das Briefing (Stand 19.08.2026) nimmt an,
linguaflow.app laufe auf WordPress.com Atomic (Blog-ID 242747314). Das trifft
nicht mehr zu: Die Domain zeigt per DNS auf GitHub Pages (185.199.108–111.153),
`server: GitHub.com`, `/wp-json/` und `/wp-admin/` antworten mit 404, und jeder
WordPress-Schreibzugriff scheitert, weil die REST-API über die Domain nicht mehr
erreichbar ist. WordPress wurde am 12.07.2026 abgelöst (siehe unten).
**Begründung:** Seiten in WordPress wären unter linguaflow.app nie sichtbar.

**Folgeentscheidungen:**
- **Verzeichnisstruktur statt flacher Dateien** (`zurueck-in-deinen-beruf/index.html`
  usw.), weil das Briefing die URLs mit Verzeichnispfad vorgibt und die
  Pillar-Cluster-Struktur davon lebt. Nebeneffekt: Die Seiten werden von
  `SOURCE_FILES` nicht erfasst und lösen keine DeepL-Kosten aus — dafür müssen
  ihre URLs über `EXTRA_SITEMAP_URLS` in der Sitemap gehalten werden.
- **llms.txt statt Yoast-Funktion.** Das Briefing verlangt, llms.txt über Yoast zu
  aktivieren. Ohne WordPress gibt es kein Yoast; die Datei liegt jetzt statisch im
  Repo und erfüllt denselben Zweck.
- **Meta-Tags statt Yoast-Feldern** für Title und Description, wie bei allen
  bestehenden Seiten.
- **FAQ offen sichtbar statt im Akkordeon.** Die Bestandsseiten verstecken
  FAQ-Antworten hinter `.faq-answer` (display:none). Da das Ziel Zitierbarkeit
  durch Antwortmaschinen ist, stehen die Antworten hier offen als H3 + Absatz.
- **Autor im Schema ist `Organization` (LinguaFlow e.U.), nicht `Person`.** Das
  Briefing empfiehlt ein Person-Schema mit `knowsAbout`. Es gibt aber keine reale
  Person mit einschlägiger Qualifikation, die genannt werden könnte — eine zu
  erfinden wäre eine Falschangabe. Umstellbar, sobald eine echte Fachautorin oder
  ein Fachautor benannt werden kann.
- **Sperrliste schlägt Faktenteil.** Briefing 5.4 nennt „ca. 2,5–4 Monate"
  Vorbereitungsdauer für die Kenntnisprüfung, Briefing 5.14 verbietet genau diese
  Angabe. Bei solchen Widersprüchen gilt die Sperrliste.
- **Nav-Label „Anerkennung"** statt „Zurück in deinen Beruf": Das lange Label
  brach die Navbar schon bei 1298 px um. Mit dem kurzen Label ist sie bis 800 px
  sauber (Hamburger greift erst bei ≤768 px). Im Footer steht weiterhin die
  ausgeschriebene Form.
- **Übersetzung: vier Sprachen statt 33.** Die Cluster-Seiten gehen nach EN, TR,
  UK und AR (`CLUSTER_LANG_CODES` in `translate-site.py`). Grund: Das Thema ist
  „Anerkennung in Deutschland"; relevant sind Englisch als Verkehrssprache und die
  Herkunftssprachen der Zielgruppe. 33 Sprachen hätten rund 87 € gekostet, vier
  kosten rund 10 €. Erweitern ist ein Einzeiler.
- **Pipeline auf Pfade statt Dateinamen umgestellt** statt die Seiten flach ins
  Wurzelverzeichnis zu legen. Die flache Variante wäre einfacher gewesen, hätte
  aber die vom Briefing vorgegebenen URLs zerstört. `rel_key()` liefert für
  Wurzeldateien denselben Schlüssel wie zuvor — der Übersetzungs-Cache bleibt
  dadurch vollständig gültig.
- **Landesbezug:** Diese Seiten behandeln **Deutschland** (BAMF, TVöD, Landes-
  ärztekammern, Bundesland-Matrix), der bestehende Ratgeber behandelt Österreich.
  Das ist auf beiden Seiten ausdrücklich gekennzeichnet, auch in der llms.txt.
  Österreichische Verfahren sind im Briefing nicht recherchiert und bräuchten
  eigene Seiten (Briefing Abschnitt 9, offene Entscheidung 5).

## Frühere Entscheidungen (Kurzfassung, vor Einführung dieser Datei)

- Statische Website auf GitHub Pages, WordPress abgelöst; alte WordPress-URLs
  werden über Redirect-Stub-Ordner weitergeleitet (2026-07-12)
- Automatische Übersetzung in 33 Sprachen via DeepL API + GitHub Action mit
  Datei-Hash-Cache (`scripts/.translation-cache.json`); `SCRIPT_VERSION` nie
  ohne Grund erhöhen (~70 € Voll-Neuübersetzung)
- Markenwording: immer „inspiriert von der Birkenbihl-Methode"
