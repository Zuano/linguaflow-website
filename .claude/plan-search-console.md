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
| 11 | `www.linguaflow.app` existiert nicht (kein DNS). | curl → 000 | Nur verlorene Tipp-Besucher. |

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
3. **`funktionen.html`:** Variante A (empfohlen): die 8 `href="funktion-….html"` durch Sprungmarken (`#buecher` …) ersetzen oder „Mehr erfahren“ entfernen; identisch per `sed` in `en/funktionen.html`; Cache-Hash für `funktionen.html` aktualisieren (Memory „Übersetzungs-Cache-Trick“). Variante B: 8 Detailseiten bauen (eigenes Projekt).
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

### Schritt 5 — HTTPS erzwingen (Christian, 5 Minuten)

GitHub → `Zuano/linguaflow-website` → Settings → Pages → **Enforce HTTPS**. Alternativ `gh api -X PUT repos/Zuano/linguaflow-website/pages -f https_enforced=true` (nach Freigabe).

→ **Check:** `curl -sI http://linguaflow.app/` → `301` auf `https://`.

### Schritt 6 — Inhalt: Aussprache-Seite (neues Feature, Entscheidung nötig)

Eine Seite `aussprache.html` („Deutsche Aussprache lernen und verbessern – mit App“) für die Suchanfragen aus #8: Chorsprechen, Wort-Schleife, 0,5×-Tempo, Karaoke-Hervorhebung als Antwort auf „aussprache verbessern app“. Den alten Stub `/deutsch-aussprache-lernen-…/` dann auf diese Seite statt auf `/` umleiten (er hat noch 1.257 Impressionen). Nur DE + EN (Nachfrage ist deutsch), Nav-Eintrag unter Ratgeber. Kosten: ~0,50 € DeepL (EN).

→ **Check:** Seite indexiert; in der GSC taucht sie bei „deutsche aussprache app“ auf; CTR dieser Anfragen > 2 % nach 6 Wochen.

### Schritt 7 — Core Web Vitals (Startseite)

Font-Fallback mit `size-adjust` in `styles.css` oder `display=optional`; `width`/`height` an allen `<img>`; `fetchpriority="high"` + kleinere `srcset`-Variante fürs Hero-Bild. Änderungen an `index.html` nur mit Cache-Trick oder per `sed` in alle 34 Fassungen.

→ **Check:** Chrome-Trace CLS < 0,1; LCP-Discovery „fetchpriority PASSED“; Lighthouse SEO bleibt 100.

### Schritt 8 — `/zurueck-in-deinen-beruf/` nachbessern (nach Schritt 1–4 beobachten)

Wenn der Hub nach 4 Wochen weiter „Gecrawlt – nicht indexiert“ ist: Indexierung beantragen, interne Links aus `ratgeber.html` und den beiden Unterseiten auf den Hub prüfen, ggf. Text des Hubs stärker von den Unterseiten abgrenzen (Google wertet ihn sonst als dünne Zwischenseite).

→ **Check:** GSC „URL ist bei Google“.

### Schritt 9 — Barrierefreiheit (optional, Design-Entscheidung) und Schritt 10 — www (optional)

Wie in der ersten Fassung: Türkis für Text ≥ 4,5:1 (`#0a8f7c`), Grau `#6b6b80`, `<main>`, Footer-Überschriften; `CNAME www → zuano.github.io`.

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

## Offene Fragen an Christian

1. **Schritt 2.3:** Links auf die acht Funktionsseiten entfernen/umlenken (A) — oder die Detailseiten bauen (B)?
2. **Schritt 3:** 5–6 € DeepL für alle 33 Sprachen freigeben, oder zuerst nur EN + PL/HU/SK/IT/ES/TR (≈ 1,20 €)?
3. **Schritt 5:** Darf ich „Enforce HTTPS“ per `gh api` setzen, oder machst du das Häkchen selbst?
4. **Schritt 6:** Aussprache-Seite bauen — ja/nein, und nur DE+EN?
5. **Schritt 9:** Türkis für Text dunkler erlaubt (Markenfarbe), oder nur die grauen Preis-Untertitel?
6. **Schritt 10:** `www` einrichten — wo liegt das DNS?

## Nach der Umsetzung

Diese Datei nach `.claude/done/` verschieben (mit Christians Bestätigung); GSC-Zahlen vor/nach (Klicks, CTR EN-Ratgeber, 404-Anzahl, Status `/methode.html`) in `TODO.md` eintragen.
