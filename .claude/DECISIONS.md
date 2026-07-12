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

## Frühere Entscheidungen (Kurzfassung, vor Einführung dieser Datei)

- Statische Website auf GitHub Pages, WordPress abgelöst; alte WordPress-URLs
  werden über Redirect-Stub-Ordner weitergeleitet (2026-07-12)
- Automatische Übersetzung in 33 Sprachen via DeepL API + GitHub Action mit
  Datei-Hash-Cache (`scripts/.translation-cache.json`); `SCRIPT_VERSION` nie
  ohne Grund erhöhen (~70 € Voll-Neuübersetzung)
- Markenwording: immer „inspiriert von der Birkenbihl-Methode"
