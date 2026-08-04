# Feature – Preissektion auf der Startseite

## Ziel
Nutzer sollen **vor dem App-Download transparent sehen**, was die Pro-Variante von LinguaFlow kostet, und welcher Preisvorteil im Jahresabo steckt.

## Status
✅ **Umgesetzt am 2026-04-23**

## Umsetzung
- Neue Sektion `#preise` in `index.html` zwischen "Sprachen" und "Download-CTA".
- Drei Karten nebeneinander (Desktop) bzw. untereinander (Mobile, <1024 px):
  - **Wöchentlich** – 9,99 € / Woche (≈ 43 €/Monat)
  - **Quartalsweise** – 54,99 € / 3 Monate (≈ 18 €/Monat)
  - **Jährlich** – 109,99 € / Jahr (≈ 9 €/Monat) – **hervorgehoben als "Bester Preis"** (Teal-Purple-Gradient, gelber Badge).
- Pro Karte: Titel, Subtitle, Preis, Monatsäquivalent, 3 Bullet-Points (u. a. Preisersparnis-Hinweis).
- Nav-Link "Preise" in der Hauptnavigation ergänzt.
- CSS in `styles.css` unter "Pricing / Preise" ergänzt, inkl. Responsive-Regel im 1024 px-Breakpoint.

## Disclaimer-Text unter der Sektion
> Preise in Euro, inkl. MwSt. Kauf und Abrechnung erfolgen über den Apple App Store bzw. Google Play. Die Preise können je nach Land und Währung abweichen – der aktuelle, für dich gültige Preis wird dir vor dem Kauf im Store angezeigt. Preisänderungen vorbehalten.

## Warum so?
- **Transparenz** schafft Vertrauen (siehe DECISIONS.md, 2026-04-23).
- Alle drei Varianten nebeneinander stellen den Preisvorteil des Jahresabos deutlich heraus (~79 % günstiger als wöchentlich).
- Der Disclaimer schützt rechtlich, falls Apple / Google regional andere Preise setzen.

## Wartung / Bei Preisänderungen
Wenn Apple oder Google die Preise in der App anpassen:
1. `index.html` → Sektion `#preise` → Zahlen in allen drei Karten aktualisieren.
2. **WICHTIG:** Die Preis-Spans MÜSSEN das Attribut `translate="no"` behalten, sonst zerlegt DeepL den Preis im Englischen (siehe DECISIONS.md, 2026-05-01).
3. Monatsäquivalent (`pricing-equivalent`) und Prozent-Vergleiche neu ausrechnen:
   - Wöchentlich × 52 ÷ 12 = Monats-Äquivalent
   - Quartalsweise ÷ 3 = Monats-Äquivalent
   - Jährlich ÷ 12 = Monats-Äquivalent
   - Ersparnis % = 1 − (Jahres-Monatspreis ÷ Wochen-Monatspreis)
4. `TODO.md` Änderungsprotokoll aktualisieren.

## i18n / Übersetzung
- Die deutsche `index.html` ist die einzige Quelle der Wahrheit.
- Bei jedem Push auf `main` läuft die GitHub Action `translate-site.yml` und übersetzt automatisch in 33 Sprachen via DeepL Pro.
- Alle Preis-Werte sind mit `translate="no"` markiert, damit DeepL sie nicht anfasst (siehe DECISIONS.md, 2026-05-01).
- Die Texte (Titel, Subtitle, Bullet Points, Disclaimer) werden korrekt übersetzt.

## Offene Ideen / später evtl.
- [ ] Bei Lebenszeit- oder Familien-Abo → vierte Karte ergänzen.
- [ ] FAQ-Frage "Wie kündige ich?" in `hilfe.html` verlinken.
- [ ] A/B-Test: Jahres-Badge "Bester Preis" vs. "Empfohlen" vs. "-79 %".
