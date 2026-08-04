# Feature: Marketing-Backlog (Sichtbarkeit & Wachstum)

**Status:** Backlog – noch nicht gestartet
**Ziel:** Mehr organische Sichtbarkeit für LinguaFlow

---

## 1. App-Verzeichnisse eintragen
**Aufwand:** 3–5 h
**Impact:** Hoch (Backlinks + direkte Sichtbarkeit)

### Plattformen (Priorität: oben = wichtigster zuerst)
- [ ] **Product Hunt** – einmaliger Launch-Effekt, hohe Reichweite bei Tech-Usern
- [ ] **AlternativeTo** – stark SEO-relevant, User suchen "Alternative zu Duolingo / Babbel"
- [ ] **Capterra** – B2B / Bildungs-Kontext, eher sekundär
- [ ] **G2** – ähnlich wie Capterra, B2B
- [ ] Weitere: AppAdvice, TheAppStore, AppAgg.com, GetApp

### Wichtige Felder die immer gebraucht werden
- Kurzbeschreibung (1 Satz)
- Lange Beschreibung (mehrere Absätze – "Birkenbihl-Methode" gut erklären)
- Screenshots (liegen in `img/`)
- App-Store & Play-Store-Links (siehe CLAUDE.md)
- Logo / Icon
- Kategorie: Education, Language Learning
- Ziel: sauber auf Deutsch UND Englisch vorbereiten

### Offene Fragen
- [ ] Wollen wir Product Hunt als klassischen Launch (einmalig, gebündelt) oder laufend?
- [ ] Welche Kategorie / Tags auf AlternativeTo? Alternativen zu welchen Apps nennen?

---

## 2. Free Tool auf der Domain (Wort-für-Wort-Demo)
**Aufwand:** 5–15 h
**Impact:** Sehr hoch (SEO + Conversion)

### Idee
Eine kleine Web-Demo direkt auf der Website, mit der man die **Birkenbihl-Dekodierung** live ausprobieren kann – ohne App-Download. User gibt einen Satz ein, bekommt Wort-für-Wort-Übersetzung. Das erzeugt:
- Direkte Nutzererfahrung → stärkeres "aha"-Gefühl vor dem Download
- Suchmaschinen lieben Tools (bessere Rankings)
- Teilen in Sozialen Netzen wird leichter

### Technische Optionen
- **Option A:** Reines Frontend mit bestehendem Übersetzungs-API (DeepL / Google Translate / eigenem Backend). Schneller, aber API-Kosten.
- **Option B:** Reines Frontend mit einer Wörter-Liste für wenige Sprachen (kein API). Billig, aber limitiert.
- **Option C:** Nutzt die selbe Engine wie die App (falls Backend existiert).

### Offene Fragen
- [ ] Gibt es schon ein Backend / eine API der App, die wir anzapfen können?
- [ ] Welche Sprach-Paare sollen im Free Tool gehen? (Alle 30? Oder nur DE↔EN?)
- [ ] Sollen wir nach 2–3 Anfragen einen soften Push Richtung App-Download einbauen?

---

## 3. Blog-Sektion starten
**Aufwand:** laufend (pro Artikel 2–5 h)
**Impact:** Hoch (Long-Tail-SEO)

### Idee
Eigener `/blog`-Bereich auf der Website mit Artikeln zum Thema Sprachenlernen, Birkenbihl-Methode, Produktivität beim Lernen etc.

### Technische Umsetzung
- **Option A:** Reine HTML-Dateien (wie aktueller Rest der Site) – einfachster Start, skaliert aber schlecht
- **Option B:** Statischer Generator (Hugo / Eleventy / Astro) – mehr Aufwand, aber beste Performance
- **Option C:** WordPress-Blog auf Subdomain – passt zum Hosting, aber technisch getrennt

### Erste Artikel-Ideen
- "Warum Vokabeln pauken nicht funktioniert"
- "Die Birkenbihl-Methode in 5 Minuten erklärt"
- "Mit welcher Sprache fängt man am besten an?"
- "Warum Passiv-Hören im Alltag so mächtig ist"

### Offene Fragen
- [ ] Welche Blog-Umsetzung (A / B / C)?
- [ ] Soll der Blog mehrsprachig (DE + EN) oder erstmal nur DE?
- [ ] Wer schreibt die Artikel? (Christian alleine / mit Claude / extern)

---

## Priorisierung (Vorschlag)
1. **Jetzt:** DMARC abschließen (läuft bereits)
2. **Diese Woche:** App-Verzeichnisse – schneller Impact, klar abgrenzbarer Task
3. **Nächste Woche:** Entscheidung Blog-Stack + erster Artikel
4. **Danach:** Free Tool – das ist die größte Investition, aber auch das größte Wachstumspotenzial
