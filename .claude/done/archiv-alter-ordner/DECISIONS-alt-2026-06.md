# DECISIONS – LinguaFlow Website

Technische und inhaltliche Entscheidungen, die später noch wichtig sein könnten.

---

## 2026-04-23 – DMARC-Policy auf `p=quarantine` erhöhen
**Entscheidung:** DMARC-Eintrag der Domain `linguaflow.app` wird von `p=none` (nur beobachten) auf `p=quarantine` (verdächtige Mails in Spam) erhöht.

**Begründung:** Schutz der Markenreputation. `p=none` warnt nur, blockt aber nichts. `p=reject` wäre der härteste Schritt, birgt aber das Risiko, legitime Mails zu verlieren, wenn SPF / DKIM irgendwo fehlt. `p=quarantine` ist ein sicherer Mittelweg: falsche Mails landen im Spam, aber nichts geht verloren. Später evtl. Upgrade auf `reject`.

**Risiken:** Falls noch ein Dienst im Namen von linguaflow.app Mails verschickt, der nicht über SPF/DKIM autorisiert ist, könnten dessen Mails in den Spam rutschen. → Vorher Report-Adresse (`rua`) einbauen, um solche Fälle zu erkennen.

---

## 2026-04-23 – Dokumentationsstruktur unter `.claude/`
**Entscheidung:** Neue Ordnerstruktur `.claude/` mit `CLAUDE.md`, `TODO.md`, `DECISIONS.md`, `features/`, `done/` eingeführt.

**Begründung:** Entspricht der globalen Vorgabe aus `~/.claude/CLAUDE.md`. Sorgt dafür, dass Context nach Session-Ende nicht verloren geht.

---

## 2026-04-23 – Preissektion auf der Startseite mit allen 3 Abo-Varianten
**Entscheidung:** Alle drei Abo-Varianten (Wöchentlich 9,99 €, Quartalsweise 54,99 €, Jährlich 109,99 €) werden transparent auf der Startseite angezeigt. Die jährliche Variante wird visuell als "Bester Preis" hervorgehoben. Zusätzlich wird für jede Variante der rechnerische Monatspreis angegeben, um den Preisvorteil der längeren Abos deutlich zu machen.

**Begründung:** Preistransparenz erhöht Vertrauen und Conversion. Das bewusste Nebeneinanderstellen der 3 Varianten zeigt dem Kunden den Preisvorteil des Jahresabos (~79 % günstiger als wöchentlich) – das soll bewusst in Richtung Jahresabo lenken.

**Rechtlicher Disclaimer:** Da Preise je Land/Währung vom Apple App Store und Google Play gesetzt werden, steht unter der Sektion ein Hinweis: "Preise können je nach Land und Währung abweichen – der aktuelle, gültige Preis wird im Store angezeigt. Preisänderungen vorbehalten." Damit keine rechtliche Angriffsfläche entsteht, wenn Apple/Google die Preise verändern.

**Risiken:** Wenn die Preise in der App (Store-seitig) deutlich abweichen, wirkt die Website unseriös. Deshalb gelten die angegebenen Preise explizit als EU-/DACH-Referenzpreise. Bei künftigen Preisanpassungen im Store muss die Website aktualisiert werden.

---

## 2026-05-01 – Preise vor DeepL-Übersetzung schützen mit `translate="no"`
**Entscheidung:** Alle Preis-Spans (`pricing-amount`) und Monatspreis-Spans erhalten das HTML-Attribut `translate="no"`. Dadurch übersetzt DeepL die Zahlen nicht und konvertiert auch nicht das deutsche Komma in einen englischen Punkt.

**Begründung:** Beim ersten Push hatte DeepL im Englischen "109,99 €" beim Komma-zu-Punkt-Konvertieren über zwei Spans zerlegt: `<span>€109.</span> <span>99/year</span>` → der Preis erschien als "€109." mit "99/year" daneben. Der Bug trat nur beim Englischen auf, nicht bei FR/IT/ES/NL/JA/AR.

**Lösung:** `translate="no"` auf allen Preis-Werten. Die Preise erscheinen jetzt in **allen 33 Sprachen einheitlich** als "9,99 €" / "54,99 € " / "109,99 €" (deutsche Komma-Notation).

**Trade-off:** Englischsprachige sehen Komma statt Punkt. Akzeptabel, weil:
- Euro-Notation ist eindeutig erkennbar
- Konsistenz über alle Sprachen
- Disclaimer sagt sowieso, dass im Store der lokale Preis steht
- Kein Bug-Risiko mehr bei zukünftigen DeepL-Updates

**Pattern für die Zukunft:** Alle Zahlen, die nicht übersetzt werden sollen (Preise, IDs, Versions-Nummern, Maße), bekommen `translate="no"`.

---

## 2026-05-01 – SEO-Fix: Canonical-/Sitemap-/hreflang-Konsistenz für Search Console
**Entscheidung:** Alle URLs (canonical, og:url, sitemap, hreflang) für die deutschen Master-Pages werden auf `.html`-Variante umgestellt, konsistent zu den internen Links und den übersetzten Sub-Pages.

**Hintergrund:** Google Search Console meldete "Duplikat – Google hat eine andere Seite als kanonisch bestimmt". Ursache: Inkonsistenz zwischen:
- Internen Links: `hilfe.html` (mit .html)
- Canonical-Tags: `linguaflow.app/hilfe` (ohne .html)
- Sitemap: `linguaflow.app/hilfe` (ohne .html)
- Übersetzte Versionen: `linguaflow.app/en/hilfe.html` (mit .html)

GitHub Pages liefert für `/hilfe` UND `/hilfe.html` denselben Content → Google sieht Duplikate.

**Lösung:** Alle URLs einheitlich mit `.html`-Variante (Sub-Pages) bzw. trailing slash (Index).

**Geänderte Dateien:**
- `index.html`: canonical + og:url → `https://linguaflow.app/` (mit Slash)
- `hilfe.html`, `datenschutz.html`, `eula.html`, `impressum.html`: canonical + og:url → `linguaflow.app/<filename>.html`
- `scripts/translate-site.py`:
  - `build_sitemap()`: deutsche Sub-Pages jetzt mit `.html`
  - `adjust_html()`: hreflang="de" + x-default zeigen jetzt auf die korrespondierende deutsche Sub-Page (vorher immer aufs Root – das war ein Bug)
  - SCRIPT_VERSION 3 → 4 (Cache invalidiert, alle Sprachen werden neu übersetzt)

**Pattern für die Zukunft:** Bei statischen Sites mit GitHub Pages: Entweder konsequent mit `.html` oder konsequent ohne – nie mischen. Sitemap, canonical, og:url und interne Links müssen identisch sein.

---

## 2026-06-24 – Traffic-Analyse: Cloudflare Web Analytics (statt Jetpack/GA4)
**Entscheidung:** Der Website-Traffic von linguaflow.app wird mit **Cloudflare Web Analytics** gemessen (kleines JS-Snippet in jeder Seite). Google Search Console bleibt zusätzlich für den Such-Traffic (SEO).

**Begründung:**
- **Jetpack** fällt weg – die Seite läuft nicht mehr auf WordPress, sondern als statische Site auf GitHub Pages.
- Cloudflare Web Analytics ist **kostenlos** und **DSGVO-freundlich**: keine Cookies, **kein Cookie-Banner nötig** (wichtig für österreichische/EU-Besucher). Das war der Hauptgrund gegen **Google Analytics 4** (GA4 bräuchte ein Einwilligungs-Banner und ist komplexer).

**Wichtige technische Lektion (Token ≠ Site-ID):**
- linguaflow.app liegt **nicht** als Zone bei Cloudflare (DNS in WordPress) → nur die **manuelle Snippet-Methode** möglich (keine „Automatic setup").
- Der Token im Snippet (`data-cf-beacon='{"token":"…"}'`) ist **NICHT** identisch mit der Site-ID in der Cloudflare-URL. Den korrekten Token immer aus dem Snippet selbst nehmen (API: `/accounts/{acc}/rum/site_info/list` → Feld `snippet`), nicht die Site-ID einbauen.
- Aktueller gültiger Token linguaflow.app: `7c42b58c8ea84d55a3af29e844db0df9` (Site-ID `596c065474a5415cb757da2b3ca17f1a`).

**Was schiefgelaufen war:** Ein früher eingebauter Token (`fdb953ef66d843b299b3c59298148b46`) war **verwaist** – die zugehörige Web-Analytics-Site existierte im Konto nicht (mehr), also wurden alle linguaflow.app-Daten von Cloudflare verworfen. **Pattern für die Zukunft:** Nach dem Einbau eines Analytics-Snippets immer prüfen, dass der Token einer **existierenden** Site im richtigen Konto entspricht – sonst zählt man monatelang ins Leere.

**Hosting-Korrektur (Doku-Hinweis):** In `CLAUDE.md` steht „Hosting/DNS: WordPress". Tatsächlich ist nur **DNS/Domain** bei WordPress; **gehostet wird die Seite auf GitHub Pages** (Repo `Zuano/linguaflow-website`, CNAME `linguaflow.app`).

**Zwei Cloudflare-Konten (Achtung Verwechslungsgefahr):** Christian hat **zwei getrennte Cloudflare-Konten unter verschiedenen Logins**.
- **Konto A** = „Christian@linguaflow.app's Account" (ID `f03558401b7feace010007576124761f`, Login = linguaflow.app-Adresse). **Hier liegt die Web-Analytics von linguaflow.app und wasgelingtmir.com.** → Zum Ansehen der Zahlen muss man in **diesem** Konto eingeloggt sein.
- **Konto B** = anderes Konto unter einem anderen Login (war in Safari offen). Enthält linguaflow.app **nicht**. Für den linguaflow-Login unsichtbar (Memberships-API gibt nur Konto A zurück).
- **Entscheidung (2026-06-24):** linguaflow.app bleibt dauerhaft in **Konto A**.
