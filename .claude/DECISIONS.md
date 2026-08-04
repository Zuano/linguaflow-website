# Entscheidungen — linguaflow.app Website

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

## Frühere Entscheidungen (Kurzfassung, vor Einführung dieser Datei)

- Statische Website auf GitHub Pages, WordPress abgelöst; alte WordPress-URLs
  werden über Redirect-Stub-Ordner weitergeleitet (2026-07-12)
- Automatische Übersetzung in 33 Sprachen via DeepL API + GitHub Action mit
  Datei-Hash-Cache (`scripts/.translation-cache.json`); `SCRIPT_VERSION` nie
  ohne Grund erhöhen (~70 € Voll-Neuübersetzung)
- Markenwording: immer „inspiriert von der Birkenbihl-Methode"
