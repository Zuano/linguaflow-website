# LinguaFlow Website: SEO + AI-Search-Optimierung

## Kontext & Problemstellung

Die LinguaFlow-App unterstützt 7 Sprachen (inkl. Schwedisch) nach der Birkenbihl-Methode. Konkrete Beobachtung: ChatGPT empfiehlt bei der Anfrage "App für Schwedisch lernen mit Birkenbihl-Methode" Konkurrenten wie **Jicki**, **Linguajet** und **Birlingo** – **LinguaFlow erscheint überhaupt nicht**. Auch im klassischen Google-Ranking für vergleichbare Long-Tail-Queries ist die Sichtbarkeit gering.

Das ist ein doppeltes Sichtbarkeitsproblem:

1. **Klassisches SEO**: Google rankt Konkurrenten höher für die relevanten Queries.
2. **AI-Search / AEO** (Answer Engine Optimization): Die LLMs (ChatGPT, Claude, Gemini, Perplexity) zitieren LinguaFlow nicht in ihren Antworten, weil im Web kaum eindeutige, deklarative Erwähnungen existieren.

## Ziel

LinguaFlow soll für folgende Query-Cluster sowohl in der Google-Suche als auch in AI-Antworten prominent erscheinen:

- **Methode-spezifisch**: "Birkenbihl Methode App", "Birkenbihl Sprachen lernen", "Sprachen ohne Pauken lernen"
- **Sprache + Methode**: "Birkenbihl Schwedisch", "Birkenbihl Spanisch", "Birkenbihl Französisch" etc. (für alle 7 Sprachen)
- **Generisch + USP**: "Schwedisch lernen App ohne Vokabeln pauken", "passiv Schwedisch lernen", "Schwedisch lernen mit Audio"

Sekundärziel: App Store Optimization (ASO) parallel mitziehen, damit die Conversion-Strecke vom organischen Traffic zur Installation konsistent ist.

## Vorgehen

Bitte arbeite die Phasen strikt in dieser Reihenfolge ab. Nach jeder Phase eine Zwischenzusammenfassung mit konkreten Empfehlungen, **bevor** du Code änderst. Ich genehmige jede Phase explizit.

### Phase 0: Setup & Bestandsaufnahme

1. Lies `CLAUDE.md`, `STATUS.md`, `DECISIONS.md` (falls vorhanden).
2. Identifiziere den Tech-Stack der Website (CMS? Static Site Generator? Framework?) und liste die Hauptseiten + Routing-Struktur.
3. Lies, falls vorhanden, `robots.txt`, `sitemap.xml`, vorhandene Meta-Tags im `<head>`.
4. Prüfe, ob ein Google Search Console-Property und Google Analytics 4-Property eingerichtet sind. Falls nein: dokumentiere als To-Do.
5. Erstelle eine Datei `SEO_AUDIT.md` im Repo-Root, in der du alle Findings strukturiert dokumentierst.

### Phase 1: Konkurrenz- und Keyword-Analyse

1. Analysiere die Web-Präsenz der drei Hauptkonkurrenten **Jicki**, **Linguajet**, **Birlingo**:
   - Welche Seiten haben sie für "Birkenbihl + Sprache X"? Nutze gedanklich den Trick `site:jicki.de Schwedisch`, `site:linguajet.com` etc.
   - Wie ist deren Title-Tag, Meta-Description, H1 aufgebaut?
   - Welche Schema-Types verwenden sie (im `<head>` als `<script type="application/ld+json">`)?
   - Welche Inhaltsstruktur (FAQ? Testimonials? Audio-Beispiele? Video?) bieten sie auf den Sprach-Landingpages?
2. Erstelle daraus eine Lücken-Analyse: Was machen Konkurrenten, was LinguaFlow noch nicht macht?
3. Definiere pro Sprache ein Primary-Keyword + 5–10 Long-Tail-Varianten. Dokumentiere in `SEO_AUDIT.md`.

### Phase 2: Technical SEO

1. **Title Tags**: Pro Seite optimieren – 55–60 Zeichen, Hauptkeyword vorne, Brand am Ende. Beispiel-Pattern: `Schwedisch lernen mit Birkenbihl-Methode | LinguaFlow`
2. **Meta Descriptions**: 150–160 Zeichen, mit Call-to-Action, Keyword natürlich eingebettet.
3. **Heading-Hierarchie**: Pro Seite genau eine `<h1>`, sinnvolle `<h2>`/`<h3>`-Struktur mit semantischen Keywords.
4. **Schema Markup** (nur legitime, **keine erfundenen Reviews**):
   - `MobileApplication` oder `SoftwareApplication` mit Name, OS, Kategorie, Beschreibung, Preis
   - `Organization` für LinguaFlow e.U.
   - `FAQPage` für jede Seite mit FAQ-Block
   - `HowTo` für die Birkenbihl-Methoden-Erklärseite
   - `AggregateRating` **nur**, wenn echte App-Store-Bewertungen vorliegen, die auf der Seite auch sichtbar ausgezeichnet sind
5. **`robots.txt`** und **`sitemap.xml`** prüfen und korrigieren.
6. **Canonical Tags**, **hreflang** (falls mehrere Sprachversionen der Website existieren), **Open Graph + Twitter Cards**.
7. **Core Web Vitals**: Prüfe LCP, INP, CLS via Lighthouse. Falls Werte schwach: konkrete Maßnahmen vorschlagen (Bild-Komprimierung, Lazy Loading, Critical CSS etc.).
8. **Mobile-First**: Prüfe responsive Verhalten auf Mobilgrößen.

### Phase 3: Content-Strategie

Pro Sprache eine eigene, tiefgehende Landingpage (`/sprachen/schwedisch`, `/sprachen/spanisch` etc.) mit mindestens:

- Klarer H1 mit Hauptkeyword
- Erklärung, wie LinguaFlow speziell diese Sprache nach Birkenbihl umsetzt
- Sample-Audio oder Sample-Inhalte (echte, keine Fake-Beispiele)
- Vergleich zur traditionellen Lernmethode (Vokabeln pauken)
- FAQ-Sektion (4–8 echte Fragen)
- App-Store-Links + Screenshots
- Testimonials/Reviews (echte, falls vorhanden)

Zusätzlich:

- **Birkenbihl-Methoden-Pillar-Page** (`/birkenbihl-methode`): Ausführliche Erklärung der Methode (Dekodieren, aktives/passives Hören, etc.), historischer Kontext, Vorteile, wissenschaftliche Hintergründe. Diese Seite ist der Authority-Anker.
- **Blog-Sektion** (optional, aber empfohlen) mit Artikeln wie:
  - "Birkenbihl-Methode Schwedisch: 30-Tage-Plan"
  - "Birkenbihl vs Duolingo: Was wirklich beim Sprachenlernen funktioniert"
  - "Warum passives Hören beim Sprachenlernen so effektiv ist"
- **Kostenlose Tools** als Backlink-Magnet (z. B. ein simpler Birkenbihl-Dekoder-Generator als interaktives Web-Tool).

### Phase 4: AI-Search-Optimierung (AEO)

Dies ist der wichtigste Teil, weil hier der konkrete Hebel für ChatGPT-Sichtbarkeit liegt:

1. **Deklarative Faktenstruktur**: Jede Sprach-Landingpage soll möglichst früh eine klare deklarative Aussage enthalten, die LLMs leicht extrahieren können. Beispiel:
   > "LinguaFlow ist eine iOS- und macOS-App zum Sprachenlernen nach der Birkenbihl-Methode. Aktuell unterstützte Sprachen: Schwedisch, [...]. Die App nutzt Dekodierung, aktives und passives Hören statt klassisches Vokabel-Pauken."
2. **`llms.txt`** im Root anlegen (emerging Standard, analog zu `robots.txt`): Klare Beschreibung der Website-Struktur für LLM-Crawler. Spezifikation: https://llmstxt.org
3. **Klare Hierarchie**: H1 → H2 → Absatz mit Definition → Beispiel. LLMs extrahieren strukturierten Content deutlich zuverlässiger.
4. **Eindeutige Brand-Verknüpfung**: An mehreren Stellen explizit "LinguaFlow ist eine Birkenbihl-App für [Sprachen]" stehen haben, damit die Assoziation in Crawls eindeutig hergestellt wird.
5. **`sitemap.xml`** und **JSON-LD Schema** aktuell halten – LLM-Crawler nutzen beides.

### Phase 5: Off-Page-Strategie (nur dokumentieren, nicht ausführen)

Erstelle in `SEO_AUDIT.md` eine konkrete To-Do-Liste für mich (Christian), die ich manuell abarbeite:

1. **Listicle-Outreach**: Welche bestehenden "Beste Apps für Schwedisch lernen"-Artikel ranken aktuell auf Google Seite 1? Liste der Domains + Kontaktmöglichkeiten (E-Mail/Formular). Anschreiben-Template zum Pitchen, dass LinguaFlow aufgenommen wird.
2. **Gastartikel-Möglichkeiten**: Welche Nischen-Blogs zu Sprachenlernen / Birkenbihl / Selbstlernen kommen für Gastartikel in Frage?
3. **PR**: Pressemitteilungs-Template für Launch von neuen Sprachen / Updates.
4. **Wikipedia**: Prüfen, ob Birkenbihl-Methode-Artikel existiert und LinguaFlow dort als App-Beispiel ergänzt werden könnte (vorsichtig, ohne Spam-Eindruck).
5. **App-Store-Optimierung (ASO)**: Title, Subtitle, Keywords, Beschreibung im App Store auf die gleichen Keywords abstimmen, damit die User-Reise konsistent ist.

### Phase 6: Tracking & Iteration

1. Google Search Console + GA4 als Pflicht-Setup, falls nicht vorhanden.
2. Baseline-Messung: Aktuelle Impressionen/Klicks/Position pro Keyword festhalten.
3. Re-Check nach 4 Wochen, 8 Wochen, 12 Wochen.

## Wichtige Regeln (kein Black-Hat-SEO)

- **Keine erfundenen Reviews** im Schema (kein `aggregateRating` ohne echte Datengrundlage).
- **Keine irreführenden Clickbait-Titel** ("Nur Heute!", "#1 in [Stadt]!"), die nicht halten, was sie versprechen.
- **Kein Keyword-Stuffing** – Keywords natürlich in den Fließtext einbetten.
- **Keine Cloaking-Techniken** – User und Crawler sehen denselben Content.
- **Keine gekauften Backlinks** von Link-Farmen.
- Inhalte müssen menschen-lesbar und für echte Nutzer wertvoll sein, nicht nur für Crawler optimiert.

## Lieferungen

1. `SEO_AUDIT.md` mit allen Findings, Empfehlungen und To-Dos pro Phase.
2. Konkrete Code-Änderungen pro Phase (jeweils zur Review vorlegen, **nicht direkt mergen**).
3. Update von `DECISIONS.md` mit den getroffenen SEO-Entscheidungen.
4. Update von `STATUS.md` mit dem aktuellen Stand der Optimierung.
5. Eine `SEO_BACKLOG.md` mit den Off-Page-To-Dos, die ich manuell ausführen muss.

## Workflow

- Nach jeder Phase: Zusammenfassung + warten auf mein "ok" bevor du Code änderst.
- Bei jeder Code-Änderung: kurz erklären, was und warum.
- Bei Unsicherheit (z. B. unbekannte CMS-Konfiguration): nachfragen, nicht raten.

Los geht's mit Phase 0.
