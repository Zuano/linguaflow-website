# Plan: Google-Search-Console-Verbesserungen für linguaflow.app

Erstellt: 2026-10-24 · Session „Search Console Improvements“ (Branch `claude/search-console-improvements-0e67fd`)
Datenstand: GSC gelesen am 2026-10-24 (Domain-Property `sc-domain:linguaflow.app`, Zeitraum 16 Monate bis 22.10.2026, Vergleich letzte 3 Monate 23.07.–22.10.2026)

## Ziel

Die Website soll in der Google-Suche besser gefunden und häufiger angeklickt werden,
und die Google Search Console (GSC) soll möglichst keine Fehler mehr melden:
keine 404-Links, keine doppelten Seiten durch http/https, übersetzte
Suchergebnis-Texte in allen 33 Sprachen, eine vollständige und ehrliche Sitemap,
die Methode-Seite endlich im Index und saubere Core Web Vitals.

## Aktuelle Situation (Stand 2026-10-24)

### GSC-Zahlen

**Leistung 16 Monate:** 971 Klicks, 23.800 Impressionen, CTR 4,1 %, Ø Position 7,0 (497 Suchanfragen, 332 Seiten, 170 Länder).
**Leistung 3 Monate:** 551 Klicks, 14.500 Impressionen, CTR 3,8 %, Ø Position 6,8. Mehr als die Hälfte aller Klicks seit Juli 2025 kam also in den letzten drei Monaten — der Trend zeigt klar nach oben (Knick im Diagramm ab Mitte Mai 2026, also mit der statischen Seite + Ratgeber).

| Seite (3 Monate) | Klicks | Impr. | CTR | Pos. |
|---|---|---|---|---|
| `/` | 197 | 2.971 | 6,6 % | 5,8 |
| `/pl/` | 125 | 1.285 | 9,7 % | 4,1 |
| `/en/` | 33 | 806 | 4,1 % | 5,8 |
| `/en/ratgeber-anerkennung-auslaendischer-abschluss.html` | 14 | **1.563** | **0,9 %** | 6,4 |
| `/hu/` | 13 | 104 | 12,5 % | 3,3 |
| `/linguaflow-video-bibliothek/` (Redirect-Stub → `/youtube/`) | 8 | 45 | 17,8 % | 6,3 |
| `/hilfe.html` | 7 | 372 | 1,9 % | 10,4 |
| `/sk/ratgeber-anerkennung-auslaendischer-abschluss.html` | 6 | 200 | 3 % | 5,2 |
| `/en/hilfe.html` | 6 | 178 | 3,4 % | 8,3 |
| `/pl/hilfe.html` | 6 | 103 | 5,8 % | 6,1 |

| Suchanfrage (16 Monate) | Klicks | Impr. | CTR | Pos. |
|---|---|---|---|---|
| linguaflow | 89 | 935 | 9,5 % | 4,6 |
| metoda birkenbihl | 84 | 1.163 | 7,2 % | 4,7 |
| lingua flow | 38 | 220 | 17,3 % | 4,4 |
| birkenbihl sprachen app | 16 | 439 | 3,6 % | 5,2 |
| birkenbihl metoda | 12 | 137 | 8,8 % | 4,6 |
| birkenbihl app | 8 | 158 | 5,1 % | 7,0 |
| deutsche aussprache app | 1 | 178 | 0,6 % | 9,7 |
| lingua app | 0 | 118 | 0 % | 7,1 |
| aussprache verbessern software | 0 | 103 | 0 % | 15,7 |
| birkenbihl method (EN) | 0 | 92 | 0 % | 9,6 |
| deutsch aussprache app | 2 | 90 | 2,2 % | 9,6 |
| aussprache verbessern apps | 0 | 57 | 0 % | 14,2 |
| aussprache verbessern deutsch app kostenlos | 0 | 51 | 0 % | 7,9 |
| aussprache-tool deutsch lernen | 0 | 44 | 0 % | 15,7 |

**Länder (16 Monate):** Deutschland 310 Klicks / 5.661 Impr., **Polen 238 / 2.661 (CTR 8,9 %, Pos. 4,7)**, Österreich 87 / 2.377, Italien 25, Schweiz 24, Ungarn 21 (CTR 8,1 %), Spanien 19, Türkei 18, Slowakei 12 / 377, Tschechien 12. Polen ist mit Abstand der stärkste Nicht-DACH-Markt („metoda birkenbihl“), Ungarn hat die beste Klickrate.
**Geräte:** Mobil 585 Klicks (60 %), Computer 361, Tablet 25.

**Indexierung:** 272 indexiert, 199 nicht indexiert:
- 81 „Seite mit Weiterleitung“ → die Redirect-Stubs der alten WordPress-URLs. Erwartet, harmlos.
- **44 „Nicht gefunden (404)“** → vollständige Liste unten, mehrere echte Fehler.
- 28 „Alternative Seite mit richtigem kanonischen Tag“ → `/xx/index.html`-Varianten, `/datenschutz`, `/impressum` ohne `.html` und **`http://linguaflow.app/`**. Canonical greift, harmlos — der http-Eintrag bestätigt aber das fehlende HTTPS-Erzwingen (siehe #1).
- 1 „Soft 404“ → `/files/*` (WordPress-Rest, zuletzt gecrawlt 01.03.2026). Ignorieren.
- **34 „Gefunden – zurzeit nicht indexiert“** → **`/methode.html` in allen 33 Sprachen inklusive Deutsch und Englisch** (seit dem Launch am 28.08. nie gecrawlt!), dazu `/da/ratgeber.html`, `/sk/ratgeber.html`, `/zh/hilfe.html`.
- **11 „Gecrawlt – zurzeit nicht indexiert“** → **`/zurueck-in-deinen-beruf/`** (deutscher Hub, gecrawlt 21.08., nicht aufgenommen), `/tr/zurueck-in-deinen-beruf/` + `/akademiker/`, sechs gelöschte Bilder `img/screenshot-*.png/.webp`, `/eula/`, `/pt-pt/impressum.html`.

**Sitemap:** `sitemap.xml` eingereicht 22.04.2026, zuletzt gelesen 15.10.2026, Status „Erfolgreich“, 299 erkannte Seiten.
**Core Web Vitals:** Mobil 0 gute / 0 schlechte / 0 zu optimierende URLs, Computer „Nicht genügend Nutzungsdaten“ — der Bericht ist leer, es gibt keine Felddaten.
**HTTPS-Bericht:** 85 HTTPS-URLs, 0 Nicht-HTTPS-URLs, „keine Probleme“.

### Die 44 URLs mit 404 (vollständig), nach Ursache gruppiert

**A — Echte Fehler durch relative Footer-Links in den Sprachversionen (laufend neue 404s):**
`/pl/was-ist-neu.html`, `/pl/newsletter.html`, `/bg/newsletter.html`. Ursache: Der Footer jeder der 31 Nicht-DE/EN-Sprachversionen verlinkt relativ auf `newsletter.html` und `was-ist-neu.html`, die es nur in DE und EN gibt. Potenzial: 62 weitere 404-URLs, Google hat erst drei davon gefunden.

**B — Rechtstexte ohne Stub in den Sprachordnern (alte Links, inzwischen absolut `/agb.html`, `/widerruf.html`):**
`/en/agb.html`, `/en/widerruf.html`, `/it/agb.html`, `/pt-pt/agb.html`, `/da/agb.html`, `/lt/agb.html`, `/lt/widerruf.html`, `/da/widerruf.html`, `/uk/widerruf.html`, `/fr/widerruf.html`, `/pl/widerruf.html`. Für `datenschutz/eula/impressum` gibt es in jedem Sprachordner einen Stub, für `agb`/`widerruf` nicht.

**C — Alte WordPress-URLs ohne Redirect-Stub (echte Lücken):**
`/hilfe/` (gecrawlt 22.07.), `/unterstutzte-sprachen/` (21.07., die Suchanfrage „unterstützte sprachen“ hat 10 Impressionen), `/en/linguaflow-video-bibliothek/` (15.08.).

**D — Alte WordPress-URLs, die seit 12.07.2026 einen Stub haben, aber von Google vorher zuletzt gecrawlt wurden (nur Neu-Crawl nötig):**
`/startseite/`, `/kontakt/`, `/about/`, `/agb/`, `/impressum/`, `/studien/`, `/datenschutzerklaerung/`, `/terms-of-service/`, `/deutsch-aussprache-lernen-…/`, `/bessere-jobchancen-…/`, `/en/startseite/`, `/en/kontakt/`, `/en/about/`, `/en/agb/`, `/en/impressum/`, `/en/studien/`, `/en/datenschutzerklaerung/`, `/en/terms-of-service/`, `/en/eula/`, `/en/category/uncategorized/`, `/en/deutsch-aussprache-lernen-…/`, `/en/bessere-jobchancen-…/`, `/en/startseite/?from=AppAgg.com…`.

**E — WordPress-Müll, soll 404 bleiben:** `/feed/`, `/about/feed/`, `/wp-content/*`, `/wp-login.php?…`.

### Was gut ist (keine Aktion nötig)

- Lighthouse Startseite mobil: **SEO 100, Best Practices 100**, Barrierefreiheit 92; LCP 275 ms, TTFB 43 ms.
- Alle 299 Sitemap-URLs existieren; robots.txt erlaubt alles; 404-Seite liefert echten 404 + `noindex`.
- JSON-LD gültig (DE/EN/FR/JA/PL geprüft); hreflang 35 + x-default konsistent; canonical überall korrekt; Titel in allen Sprachen übersetzt; 1 H1 je Seite.
- Redirect-Stubs (Meta-Refresh) bleiben, GitHub Pages kann keine 301 (Entscheidung 2026-07-12).
- `/hilfe` vs. `/hilfe.html`, `/index.html` vs. `/`: canonical regelt es, GSC bestätigt („Alternative Seite mit richtigem kanonischen Tag“).

### Gefundene Probleme (nach Wirkung sortiert)

| # | Befund | Beleg | Wirkung |
|---|--------|-------|---------|
| 1 | **`/methode.html` ist in keiner Sprache indexiert** — auch nicht DE/EN. Status „Gefunden – zurzeit nicht indexiert“ = Google kennt die URL aus der Sitemap, hat sie aber seit dem 28.08. nie abgerufen. | GSC-Liste (34 URLs) | Die aufwändigste Seite der Website (12–15 € + ElevenLabs) ist für Google unsichtbar. |
| 2 | **Meta-Description in ALLEN 33 Sprachversionen deutsch** — auf allen Seiten, auch `/en/`. Gleiches gilt für `og:description`, `twitter:description` und `alt`-Texte. | `en/ratgeber-anerkennung…html`: Titel englisch, Description „Ausländischer Abschluss? So läuft die Anerkennung…“ | Messbar: diese Seite hat **1.563 Impressionen bei 0,9 % CTR** (Seitenschnitt 3,8 %). Englische Suchende sehen deutschen Text unter dem Treffer. |
| 3 | **Laufend neue 404s durch relative Footer-Links** (Gruppe A), dazu fehlende Stubs (B, C). | 44 URLs in GSC, 62 weitere absehbar | Fehlerliste wächst, Crawl-Budget geht in Sackgassen. |
| 4 | **8 tote Links auf `funktionen.html` + `en/`** (`funktion-*.html` existieren nicht). Noch nicht in der GSC, weil `funktionen.html` nicht in der Hauptnavigation ist — kommt aber. | live 404 | Besucher landen auf der Fehlerseite. |
| 5 | **HTTP wird nicht auf HTTPS umgeleitet** (`https_enforced: false`). | GSC listet `http://linguaflow.app/` als Alternativseite | Google sortiert es per canonical richtig ein, trotzdem unnötige Duplikate und ein Sicherheitssignal. 5-Minuten-Fix. |
| 6 | **Sitemap unvollständig, `lastmod` unglaubwürdig.** Fehlen: `/youtube/`, `agb.html`, `widerruf.html`, `datenschutz-extension.html`, `privacy-extension.html`; alle 299 Einträge tragen das Laufdatum. | `build_sitemap()` | `/youtube/` wird nur über den alten Stub `/linguaflow-video-bibliothek/` gefunden (der 8 Klicks in 3 Monaten bringt!). |
| 7 | **`/zurueck-in-deinen-beruf/` gecrawlt, aber nicht indexiert** (21.08.). | GSC | Google hält den Hub (noch) nicht für wertvoll genug; Unterseiten `/pflege/`, `/akademiker/` sind nicht gelistet, also vermutlich indexiert. |
| 8 | **Themenlücke „Aussprache“**: ~600 Impressionen auf Suchanfragen wie „deutsche aussprache app“, „aussprache verbessern app/software/tool“ bei 0–2 % CTR und Position 8–16. Ranking kommt vom alten WordPress-Artikel `/deutsch-aussprache-lernen-…/`, der jetzt nur noch auf `/` umleitet. | Suchanfragen-Tabelle | Fertige Nachfrage ohne passende Seite. |
| 9 | **Layout-Verschiebung CLS 0,12** (Grenze 0,10), Font-Swap + fehlende Bildmaße; Hero-Bild ohne `fetchpriority`, 65 kB zu groß. | Chrome-Trace | Kein Felddaten-Bericht in der GSC (zu wenig Traffic), aber günstig zu beheben. |
| 10 | **Barrierefreiheit 92**: Türkis `#0fb49b` auf Weiß 2,61:1, Grau `#9494a8` 2,71:1, kein `<main>`, Footer-`h4`. | Lighthouse | Design-Entscheidung (Markenfarbe). |
| 11 | `https://www.linguaflow.app` scheitert mit TLS-Fehler. DNS existiert (Nameserver bei WordPress.com, `www` ist CNAME auf `linguaflow.app`), `http://www` leitet GitHub korrekt per 301 um — aber GitHubs Zertifikat deckt nur `linguaflow.app` ab, weil der `www`-CNAME nicht auf `zuano.github.io` zeigt. | `openssl s_client` → SAN nur `linguaflow.app`; `curl http://www` → 301 | Wer `https://www…` tippt oder einen alten https-www-Link klickt, sieht einen Zertifikatsfehler. Fürs Tracking irrelevant: gezählt wird nach der Umleitung vom Cloudflare-Snippet. |

## Geplante Schritte

### Schritt 1 — Indexierung der Methode-Seite anstoßen (Christian, 10 Minuten, sofort)

GSC → URL-Prüfung → „Indexierung beantragen“ für `/methode.html`, `/en/methode.html`, `/pl/methode.html`, `/hu/methode.html` (die vier stärksten Sprachen; Tageslimit ~10 Anfragen). Zusätzlich Sitemaps → Sitemap erneut einreichen. Danach prüfen, ob `methode.html` von der Startseite aus mit normalem `<a href>` verlinkt ist (ja: Navbar + Sektions-Knopf) — falls Google trotzdem nicht crawlt, nach Schritt 5 einen Link aus `hilfe.html` und `ratgeber.html` ergänzen.

→ **Check:** GSC URL-Prüfung zeigt „URL ist bei Google“ für `/methode.html` innerhalb von 1–2 Wochen; Leistung → Seiten listet `/methode.html` mit Impressionen.

### Schritt 2 — 404-Quellen schließen (Code, 0 € DeepL)

1. **Stubs anlegen** nach dem Muster von `fr/eula.html` (Meta-Refresh + canonical, `lang`-Attribut passend):
   - `<lang>/newsletter.html` und `<lang>/was-ist-neu.html` → `/en/newsletter.html` bzw. `/en/was-ist-neu.html` für alle 31 Nicht-DE/EN-Sprachordner (62 Dateien).
   - `<lang>/agb.html` und `<lang>/widerruf.html` → `/agb.html` bzw. `/widerruf.html` für alle 33 Sprachordner inkl. `en` (66 Dateien; EN bekommt kein eigenes AGB, Entscheidung „Rechtstexte nur DE+EN“ bleibt — AGB/Widerruf gibt es nur auf Deutsch).
   - `hilfe/index.html` → `/hilfe.html`; `unterstutzte-sprachen/index.html` → `/#sprachen`; `en/linguaflow-video-bibliothek/index.html` → `/youtube/`.
   Erzeugung per kleinem Skript `scripts/make-stubs.py` (einmalig, idempotent), damit es beim nächsten Sprach-Zuwachs wiederholbar ist.
2. **Ursache dauerhaft beheben:** In `adjust_html()` (`scripts/translate-site.py`) die Footer-Links `newsletter.html` / `was-ist-neu.html` für Sprachen außerhalb `languages_for()` auf `/en/…` umschreiben — sonst entstehen die 404s beim nächsten Übersetzungslauf erneut, auch wenn Stubs sie auffangen.
3. **`funktionen.html` (Entscheidung Christian 2026-10-25: Kacheln ohne Link):** Die acht `<a class="fn-tile" href="funktion-….html">` werden zu `<div class="fn-tile">`, die Zeile `<span class="fn-more">Mehr erfahren →</span>` entfällt, Hover-Effekt (`.fn-tile:hover`) raus. Identisch per `sed` in `en/funktionen.html` („Learn more →“); Cache-Hash für `funktionen.html` aktualisieren (Memory „Übersetzungs-Cache-Trick“). Hinweis: Die Seite hängt nur am Footer der Methode-Seite, nicht in der Hauptnavigation.
4. Gruppe D und E brauchen **keinen Code**: In der GSC bei „Nicht gefunden (404)“ auf **„Fehlerbehebung überprüfen“** klicken, Google crawlt die Stubs dann neu.

→ **Check:** Link-Checker über alle 430 HTML-Dateien meldet 0 fehlende Ziele (auch relative Links in Sprachordnern); `curl -o /dev/null -w "%{http_code}"` für `/pl/newsletter.html`, `/it/agb.html`, `/hilfe/`, `/unterstutzte-sprachen/` → 200; GSC-404-Zahl sinkt nach Validierung auf ≤ 5 (nur Gruppe E).

### Schritt 3 — Meta-Description, og:/twitter:description und alt-Texte nachübersetzen

Neues, manuell startbares Skript `scripts/retrofit-meta.py` nach dem Vorbild von `scripts/retrofit-jsonld.py`:

1. Je Sprachversion die `content`-Werte von `meta[name=description]`, `og:description`, `twitter:description` und alle `alt="…"` aus der deutschen Quelle als **reinen Text** an DeepL schicken und einsetzen; Dry-Run; Fallback auf Deutsch bei jedem Fehler; HTML-Escaping der Rückgabe.
2. Dieselbe Logik in den regulären Übersetzungslauf einbauen (`adjust_html()`), `SCRIPT_VERSION` **nicht** erhöhen.
3. Optional Workflow `retrofit-meta.yml` (Kopie von `retrofit-jsonld.yml`, nur `workflow_dispatch`).
4. **Reihenfolge nach Wirkung:** zuerst EN (1.563 Impressionen auf dem Anerkennungs-Ratgeber), PL, HU, SK, IT, ES, TR — dann der Rest.

Kosten: ~20 Seiten × 33 Sprachen × ~400 Zeichen ≈ 260.000 Zeichen ≈ **5–6 € DeepL**; nur EN+6 Sprachen ≈ 1,20 €.

→ **Check:** `grep -o 'name="description" content="[^"]*"' en/ratgeber-anerkennung-auslaendischer-abschluss.html` ist englisch; `es/index.html` spanisch; hreflang-Anzahl (35) und canonical in Stichproben unverändert; JSON-LD weiterhin gültig. Nach 4 Wochen: CTR der EN-Ratgeberseite in der GSC > 2 %.

### Schritt 4 — Sitemap vervollständigen und `lastmod` ehrlich machen

In `build_sitemap()`: feste Zusatzliste `youtube/`, `agb.html`, `widerruf.html`, `datenschutz-extension.html`, `privacy-extension.html`; `lastmod` je Datei aus `git log -1 --format=%cs -- <datei>` (Fallback Dateidatum, nie „heute für alle“); im Workflow `translate-site.yml` `fetch-depth: 0`. Option `--sitemap-only`, damit die Sitemap ohne DeepL-Lauf neu gebaut werden kann.

→ **Check:** 304 `<loc>`; `lastmod` variiert; XML parst; GSC → Sitemaps zeigt nach Neueinreichung 304 erkannte Seiten.

### Schritt 5 — HTTPS erzwingen (Claude per `gh api`, Freigabe Christian 2026-10-25)

`gh api -X PUT repos/Zuano/linguaflow-website/pages -f https_enforced=true` in der Umsetzungs-Session ausführen, danach mit `gh api repos/Zuano/linguaflow-website/pages --jq .https_enforced` gegenprüfen.

→ **Check:** `curl -sI http://linguaflow.app/` → `301` auf `https://`.

### Schritt 6 — Inhalt: Aussprache-Seite (neues Feature, Entscheidung nötig)

Eine Seite `aussprache.html` („Deutsche Aussprache lernen und verbessern – mit App“) für die Suchanfragen aus #8: Chorsprechen, Wort-Schleife, 0,5×-Tempo, Karaoke-Hervorhebung als Antwort auf „aussprache verbessern app“. Den alten Stub `/deutsch-aussprache-lernen-…/` dann auf diese Seite statt auf `/` umleiten (er hat noch 1.257 Impressionen). **Entscheidung Christian 2026-10-25: in allen 33 Sprachen** (reguläre Aufnahme in `SOURCE_FILES`, Übersetzungs-Workflow übernimmt den Rest; in den Sprachversionen geht es dann um die Aussprache der jeweiligen Zielsprache, der Text muss sprachneutral formuliert sein — „deine Zielsprache“ statt „Deutsch“ außer im DE-Titel/Keyword-Block). Nav-Eintrag unter Ratgeber. Kosten: ~8–10 € DeepL.

→ **Check:** Seite indexiert; in der GSC taucht sie bei „deutsche aussprache app“ auf; CTR dieser Anfragen > 2 % nach 6 Wochen.

### Schritt 7 — Core Web Vitals (Startseite)

Font-Fallback mit `size-adjust` in `styles.css` oder `display=optional`; `width`/`height` an allen `<img>`; `fetchpriority="high"` + kleinere `srcset`-Variante fürs Hero-Bild. Änderungen an `index.html` nur mit Cache-Trick oder per `sed` in alle 34 Fassungen.

→ **Check:** Chrome-Trace CLS < 0,1; LCP-Discovery „fetchpriority PASSED“; Lighthouse SEO bleibt 100.

### Schritt 8 — `/zurueck-in-deinen-beruf/` nachbessern (nach Schritt 1–4 beobachten)

Wenn der Hub nach 4 Wochen weiter „Gecrawlt – nicht indexiert“ ist: Indexierung beantragen, interne Links aus `ratgeber.html` und den beiden Unterseiten auf den Hub prüfen, ggf. Text des Hubs stärker von den Unterseiten abgrenzen (Google wertet ihn sonst als dünne Zwischenseite).

→ **Check:** GSC „URL ist bei Google“.

### Schritt 9 — Barrierefreiheit (Entscheidung Christian 2026-10-25: nur Grau)

Markenfarbe Türkis bleibt unverändert. Nur die grauen Preis-Untertitel (`#9494a8` auf `#f4f4f8`) auf ein dunkleres Grau (`#6b6b80`, ≥ 4,5:1) in `styles.css`; dazu die kostenlosen Struktur-Punkte `<main>` um den Seiteninhalt und Footer-`h4` → `h2` mit kleiner Optik (nur wenn `index.html` ohnehin per Cache-Trick angefasst wird, Schritt 7).

→ **Check:** Lighthouse `color-contrast` meldet nur noch die Türkis-Elemente; Preis-Untertitel bestehen.

### Schritt 10 — `https://www` reparieren (Christian im WordPress.com-DNS, 5 Minuten)

Im DNS bei WordPress.com (Nameserver `ns1–3.wordpress.com`) den Eintrag `www` von `CNAME → linguaflow.app` auf `CNAME → zuano.github.io` ändern. GitHub Pages erkennt dann die www-Variante, stellt voraussichtlich ein Zertifikat auch für `www.linguaflow.app` aus und leitet weiter auf `linguaflow.app`. Nichts am Repo nötig (`CNAME`-Datei bleibt `linguaflow.app`). Fürs Tracking ändert sich nichts: Besucher landen nach der Umleitung auf Seiten mit dem Cloudflare-Analytics-Snippet.

→ **Check:** nach 1–24 h `curl -sI https://www.linguaflow.app/` → `301` auf `https://linguaflow.app/` ohne TLS-Fehler. Falls GitHub kein www-Zertifikat ausstellt: Punkt dokumentieren und schließen (http-Umleitung funktioniert bereits).

## Betroffene Dateien

| Datei / Ort | Schritt | Änderung |
|---|---|---|
| GSC (kein Code) | 1, 2.4 | Indexierung beantragen, Sitemap neu einreichen, 404-Validierung starten |
| `scripts/make-stubs.py` (neu) + ~131 Stub-Dateien in Sprachordnern, `hilfe/`, `unterstutzte-sprachen/`, `en/linguaflow-video-bibliothek/` | 2 | Redirect-Stubs |
| `scripts/translate-site.py` | 2.2, 3, 4 | Footer-Link-Umschreibung in `adjust_html()`, Attribut-Übersetzung, `build_sitemap()` |
| `funktionen.html`, `en/funktionen.html`, `scripts/.translation-cache.json` | 2.3 | tote Links, Cache-Hash |
| `scripts/retrofit-meta.py` (neu), ggf. `.github/workflows/retrofit-meta.yml` | 3 | Nachübersetzung |
| `.github/workflows/translate-site.yml` | 4 | `fetch-depth: 0` |
| `sitemap.xml` | 4 | 304 URLs, echte Daten |
| GitHub-Pages-Einstellung | 5 | Enforce HTTPS |
| `aussprache.html` (neu), `en/aussprache.html`, Stub `deutsch-aussprache-lernen-…/index.html`, Nav in allen Seiten (Cache-Trick) | 6 | neue Seite |
| `index.html` + 33 Sprachversionen, `styles.css`, `img/screens/*/decoding.webp`, `scripts/build-screenshots.py` | 7 | CWV |
| `.claude/TODO.md`, `.claude/DECISIONS.md` | alle | Doku |

## Risiken / Seiteneffekte

- **DeepL-Kosten durch versehentliche Neuübersetzung:** Jede Änderung an einer deutschen Quelldatei auf `main` löst den Workflow aus (`index.html` ≈ 27 €). Quellseiten nur per `sed` gleichzeitig in alle Sprachversionen ändern + Cache-Hash nachziehen, oder vorher mit gemocktem DeepL simulieren (wie am 2026-08-21). Stubs und `styles.css` sind kostenlos.
- **Attribut-Übersetzung kann HTML brechen:** escapen, Fallback, Dry-Run, Parser-Durchlauf, Regressionstest hreflang/canonical.
- **Stubs sind 200er-Seiten mit Meta-Refresh:** Sie wandern in der GSC von „404“ nach „Seite mit Weiterleitung“ — das ist der gewollte Zustand, die Zahl „nicht indexiert“ sinkt dadurch nicht, nur die Fehler verschwinden.
- **HTTPS erzwingen:** risikolos, aber Konto-Einstellung → nur nach Freigabe.
- **Font-Änderung:** beim ersten Besuch kurz Systemschrift sichtbar; optisch prüfen.
- **Aussprache-Seite** ist neuer Inhalt mit Marken-Wording („inspiriert von der Birkenbihl-Methode“, kein Anbieter-Name für die Sprachausgabe, siehe CONTEXT.md).

## Entscheidungen Christian (2026-10-25) — keine offenen Fragen mehr

1. **Schritt 2.3 Funktionen-Seite:** Kacheln bleiben, aber ohne Link und ohne „Mehr erfahren“. Keine Detailseiten.
2. **Schritt 3 Nachübersetzung:** alle 33 Sprachen, ~5–6 € DeepL freigegeben.
3. **Schritt 5 HTTPS:** Claude setzt `https_enforced` per `gh api`.
4. **Schritt 6 Aussprache-Seite:** ja, in allen 33 Sprachen (~8–10 € DeepL).
5. **Schritt 9 Kontrast:** Markenfarbe Türkis bleibt, nur graue Preis-Untertitel werden dunkler.
6. **Schritt 10 www:** Christian ändert den CNAME im WordPress.com-DNS (Anleitung oben); Tracking-Frage geklärt — DNS-Ort ist dafür egal.

**Reihenfolge für die Umsetzungs-Session:** 1 (Christian, sofort) → 2 → 4 → 5 → 3 → 7 + 9 → 6 → 8 beobachten; 10 parallel durch Christian.

## Agenten-Einsatz je Schritt (Wunsch Christian 2026-10-25)

Grundsatz: **Mechanisches und Prüfendes an günstige Subagenten** (Modell Sonnet oder Haiku, Typ `general-purpose` bzw. `Explore`), **alles mit DeepL-Kosten, Inhalt oder Markenwording bleibt in der Hauptsession** (Fable/Opus) und bekommt vor dem Push eine zweite Meinung durch einen Review-Subagenten, der den Diff ohne die Begründung der Hauptsession liest. Subagenten laufen im Hintergrund, die Hauptsession wartet auf das Ergebnis statt parallel dieselben Dateien anzufassen. Checks sind immer ein eigener Agentenlauf, nie der Agent, der die Änderung gemacht hat.

| Schritt | Wer | Modell | Warum |
|---|---|---|---|
| 1 Indexierung beantragen, Sitemap neu einreichen | Christian in der GSC | — | Braucht eingeloggten Browser, 10 Minuten Klickarbeit |
| 2.1 ~131 Redirect-Stubs + `scripts/make-stubs.py` | Subagent `general-purpose` | **Haiku** | Rein mechanisch, Vorlage `fr/eula.html` existiert, Ergebnis per Skript reproduzierbar |
| 2.1 **Check**: Link-Checker über alle 430 HTML-Dateien, `curl` auf Stub-URLs | Subagent `Explore` | **Haiku** | Nur lesen und melden |
| 2.2 Footer-Link-Umschreibung in `adjust_html()` | Hauptsession | Fable | Greift in das Übersetzungsskript ein — ein Fehler dort kostet beim nächsten Lauf echtes Geld |
| 2.3 `funktionen.html`-Kacheln entlinken + Cache-Hash | Subagent `general-purpose` | **Sonnet** | Kleine Textersetzung, aber Cache-Trick muss exakt stimmen (Hash-Berechnung wie in `translate-site.py`) |
| 3 `scripts/retrofit-meta.py` schreiben | Hauptsession | Fable | Kostenrelevant (DeepL), HTML-Escaping, Fallback-Logik, Regressionstest hreflang/canonical |
| 3 **Review** des Skripts vor dem ersten echten Lauf | Subagent `general-purpose` (Review-Auftrag: „suche Fälle, in denen das Skript HTML oder JSON kaputt macht oder doppelt übersetzt“) | **Opus** | Gewissenhaft: zweite Meinung ohne Vorannahmen, bevor Geld ausgegeben wird |
| 3 Dry-Run auswerten, dann echter Lauf | Hauptsession | Fable | Kostenentscheidung |
| 3 **Check**: Stichproben in 10 Sprachen, Attribute übersetzt, JSON-LD gültig, hreflang 35 | Subagent `Explore` | **Haiku** | Nur lesen und melden |
| 4 `build_sitemap()`: Zusatz-URLs, `lastmod` aus Git, `--sitemap-only`, `fetch-depth: 0` | Subagent `general-purpose` | **Sonnet** | Überschaubare Python-Änderung mit klarem Prüfkriterium (304 URLs, XML parst) |
| 4 **Check**: XML parsen, URL-Zahl, `lastmod`-Streuung | Subagent `Explore` | **Haiku** | Nur lesen |
| 5 `gh api … https_enforced=true` + Gegenprüfung | Hauptsession | Fable | Konto-Einstellung, ein Befehl, Verantwortung bleibt hier |
| 6 Aussprache-Seite: Text und Struktur | Hauptsession | Fable | Inhalt, Markenwording („inspiriert von der Birkenbihl-Methode“, Glossar in `CONTEXT.md`), SEO-Titel, Aufnahme in `SOURCE_FILES` |
| 6 **Review** Text vor dem Push (Wording, Glossar, keine Anbieter-Nennung, sprachneutrale Formulierung für 33 Sprachen) | Subagent `general-purpose` (Review-Auftrag) | **Opus** | Gewissenhaft: Seite wird 33-fach übersetzt, Fehler kosten 8–10 € pro Korrektur |
| 6 **Check** nach dem Übersetzungslauf: 5 Sprachversionen live 200, canonical, hreflang, Nav | Subagent `Explore` | **Haiku** | Nur lesen |
| 7 CWV: `width`/`height`, `fetchpriority`, `srcset`, Font-Fallback in 34 Dateien per `sed` | Subagent `general-purpose` | **Sonnet** | Mechanisch über viele Dateien, Cache-Trick wie 2.3 |
| 7 **Check**: Chrome-Trace CLS < 0,1, Lighthouse SEO 100 | Hauptsession mit `chrome-devtools` | Fable | Braucht die Browser-Werkzeuge der Hauptsession |
| 8 `/zurueck-in-deinen-beruf/` beobachten, ggf. Hub-Text schärfen | Hauptsession | Fable | Inhaltliche Entscheidung |
| 9 Grau `#6b6b80` in `styles.css`, `<main>`, Footer-`h4` | Subagent `general-purpose` | **Haiku** | Zwei Zeilen CSS, eine Struktur-Klammer |
| 10 www-CNAME | Christian bei WordPress.com | — | Fremdes Dashboard |
| Abschluss: Doku (`TODO.md`, `DECISIONS.md`, Feature-Datei), Commit, Push | Hauptsession | Fable | Pflicht nach jeder Änderung, in derselben Antwort |

Nicht einsetzen: `ios-geraetetester` (nur Apps), Workflows/Multi-Agent-Orchestrierung (Christian hat das nicht angefordert, und die Schritte hängen voneinander ab).

## Nach der Umsetzung

Diese Datei nach `.claude/done/` verschieben (mit Christians Bestätigung); GSC-Zahlen vor/nach (Klicks, CTR EN-Ratgeber, 404-Anzahl, Status `/methode.html`) in `TODO.md` eintragen.
