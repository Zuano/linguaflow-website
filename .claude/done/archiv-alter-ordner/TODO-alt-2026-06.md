# TODO – LinguaFlow Website & Marketing

## In Arbeit
- [ ] **DMARC-Record erweitern** (WordPress DNS) – von `p=none` auf `p=quarantine` umstellen, damit Fake-Mails im Spam landen. Claude liefert den DNS-Eintrag, Christian trägt ihn in WordPress ein.

## Offen – mit Aufwand & Impact
### Marketing / Sichtbarkeit
- [ ] **App-Verzeichnisse eintragen** (Product Hunt, AlternativeTo, Capterra, G2, etc.) – 3–5 h, hoher Impact
- [ ] **Free Tool auf der Domain** (z.B. Wort-für-Wort-Demo ohne App-Download) – 5–15 h, sehr hoher Impact
- [ ] **Blog-Sektion starten** – laufend, hoher Impact

### Später / Optional
- [ ] (Platz für neue Ideen)

---

## Erledigt
- [x] **Bing Webmaster einrichten** – Inhaber hinzugefügt via Search Console (2026-04-22)
- [x] **Altes Token aus DNS entfernen** (Search Console → Inhaber und Berechtigungen) (2026-04-22)
- [x] **In-App-Rating-Prompt einbauen (iOS / Android)** – Hinweis: liegt im App-Code-Projekt, NICHT in diesem Website-Repo. Laut Christian gestern erledigt. ❓ Bitte kurz bestätigen, damit wir es endgültig abhaken können.
- [x] **Preissektion auf der Startseite** – 3 Abo-Varianten (wöchentlich / quartalsweise / jährlich) mit Hervorhebung "Bester Preis" auf Jährlich, inkl. Monatspreis-Vergleich und rechtlichem Disclaimer (2026-04-23)
- [x] **FAQ-Erweiterung via AnswerThePublic** – 15 neue Fragen + FAQ-Schema + Live-Suchfunktion in `hilfe.html` (2026-06-24). Gepusht (Commit `81ac229`).
- [x] **Cloudflare Web Analytics für linguaflow.app repariert** – der in allen 5 Seiten eingebaute Beacon-Token `fdb953…` war **verwaist** (im einzigen Cloudflare-Konto existierte keine zugehörige Web-Analytics-Site → linguaflow.app-Traffic wurde nie aufgezeichnet). Neue Site „linguaflow.app" (manuelles JS-Snippet) angelegt, neuer Token in allen 5 Seiten, gepusht (Commit `85843d4`), live verifiziert (2026-06-24).

---

## Änderungsprotokoll
- **2026-04-23** `.claude/`-Dokumentation angelegt (CLAUDE.md, TODO.md, DECISIONS.md, features/)
- **2026-04-23** Status-Check: DMARC-Erweiterung startet, In-App-Rating zur Bestätigung
- **2026-04-23** Preissektion `#preise` in `index.html` eingebaut (zwischen Sprachen und Download-CTA), CSS in `styles.css` ergänzt, Navigation um "Preise" erweitert, responsive für Desktop + Mobile. Feature-Datei `features/preise-auf-website.md` angelegt.
- **2026-05-01** Preissektion auf GitHub gepusht (Commit `1af58c2` auf `Zuano/linguaflow-website`). Auto-Übersetzung in 33 Sprachen via DeepL erfolgreich gelaufen. Lokaler Ordner mit GitHub-Stand synchronisiert (Master-Sync, ohne Sprachordner).
- **2026-05-01** i18n-Bug-Fix: Preis-Spans und Monatspreis-Spans mit `translate="no"` markiert. DeepL hatte im Englischen "109,99 €" beim Komma-zu-Punkt-Konvertieren über zwei Spans zerlegt. Commit `57baa2d` gepusht, Translate-Workflow erfolgreich durchgelaufen.
- **2026-05-01** "Jederzeit kündbar" als Reassurance-Bullet auch bei Quartals- und Jahresabo ergänzt (vorher nur bei Wöchentlich). Commit `2f3b1b8` gepusht.
- **2026-05-01** Kündigungs-Hinweis ausführlicher und in alle 3 Karten als Fineprint umgesetzt: "Kündigung jederzeit möglich – der Zugang bleibt bis zum Ende der bezahlten Laufzeit aktiv." Neuer CSS-Stil `.pricing-cancellation` mit Trennlinie und kleiner gedämpfter Schrift. Commit `c1c83c1`.
- **2026-05-01** SEO-Fix für Search Console "Duplikat-Problem": canonical, og:url und Sitemap-URLs auf `.html`-Variante umgestellt (konsistent zu internen Links). Bonus: hreflang-Bug in adjust_html() gefixt (DE/x-default zeigten in übersetzten Sub-Pages auf Root statt auf die korrespondierende DE-Sub-Page). Commit `4f6b1b6`. SCRIPT_VERSION 3→4 → ALLE 33 Sprachen × 5 Seiten werden neu übersetzt.
- **2026-06-24** Website gepusht (Commit `81ac229` auf `Zuano/linguaflow-website`, `f3724e5..81ac229`). Geänderte Dateien: `hilfe.html` (+253, FAQ-Erweiterung), `index.html` (+36), `datenschutz.html`/`eula.html`/`impressum.html` (je 1 Zeile). Auto-Übersetzung in 33 Sprachen via DeepL läuft auf GitHub Actions. Hinweis: Der lokale Stand von `index.html` und den Rechtsseiten wich noch vom Remote ab und wurde mit gepusht.
- **2026-06-24** FAQ in `hilfe.html` von 12 auf 27 Fragen erweitert (15 neue, Keyword-Recherche via AnswerThePublic: „Birkenbihl Methode" + „Sprachen lernen", DE/AT). Jede Frage zusätzlich im `FAQPage`-JSON-LD (Schema = sichtbarer Text, 1:1 verifiziert). Neue intelligente Live-Suchfunktion über der FAQ-Liste (umlaut-/case-insensitiv, Token-AND-Match, „keine Treffer"-Hinweis). Inhaltliche Schärfungen von Christian: App dekodiert für den User; 3 KIs (Dekodierung/ElevenLabs-Sprachausgabe/Inhalte); Bücher im Lesefluss; beliebige Texte & Berufsvokabular; seltene Sprachen (Schwedisch); Preis-Begründung. ElevenLabs bewusst nicht namentlich genannt. Via Claude Code gepusht am 2026-06-24 → Auto-Übersetzung in 33 Sprachen ausgelöst.
- **2026-06-24** Cloudflare Web Analytics repariert. Diagnose (via Chrome-MCP + Cloudflare-API): Der Beacon-Token `fdb953ef66d843b299b3c59298148b46` in allen 5 Seiten war **verwaist** – im (einzigen) Cloudflare-Konto „Christian@linguaflow.app's Account" gab es dazu keine Web-Analytics-Site, Cloudflare verwarf die Daten. linguaflow.app wurde also nie gezählt. Neue Web-Analytics-Site `linguaflow.app` angelegt (manuelles JS-Snippet, weil DNS nicht bei Cloudflare liegt) → neuer Token `7c42b58c8ea84d55a3af29e844db0df9`. Token in `index.html`, `hilfe.html`, `datenschutz.html`, `eula.html`, `impressum.html` ersetzt. Zusätzlich (auf Christians Wunsch) die lokal noch unveröffentlichten SEO-Strukturdaten in `index.html` mitgepusht (Schema.org `SoftwareApplication`: `screenshot[]`, `featureList[]`, `installUrl`, `publisher`, `applicationSubCategory`). Commit `85843d4` (`aa6b08e..85843d4`), DeepL-Translate + Pages-Deploy gelaufen, neuer Token live auf https://linguaflow.app verifiziert. **Nebenbefund:** Die einzige andere CF-Web-Analytics-Site `wasgelingtmir.com` steht auf „Enable, excluding visitor data in the EU" → EU-Besucher werden nicht gezählt (zeigt 0). Falls dort EU-Daten gewünscht sind, Einstellung ändern.
