# Feature: Erste Facebook-/Instagram-Werbekampagne (LinguaFlow)

**Status:** Kampagne als **Entwurf** angelegt, NICHT veröffentlicht.
**Angelegt:** 2026-08-15/16 · **Zuletzt bearbeitet:** 2026-08-26

> ⛔️ **Der eingestellte Zeitraum ist abgelaufen.** Der Entwurf steht auf
> 16.08. 05:00 → 23.08. 23:59; heute ist der 26.08. **Vor dem Veröffentlichen
> Start- und Enddatum neu setzen**, sonst verweigert Meta die Auslieferung.

## Ziel
Erster bezahlter Traffic-Test für linguaflow.app. Kleines Budget, drei
Textvarianten gegeneinander, um zu lernen welche Ansprache zieht.

## Was schon existiert (nicht neu anlegen!)

| | |
|---|---|
| Business-Portfolio | **LinguaFlow App** (ID `664639840066263`) |
| Werbekonto | **LinguaFlow App** (ID `1724098535586816`) — am 16.08. NEU angelegt |
| Währung / Zeitzone | **EUR / Europe/Vienna** — unveränderlich, bewusst so gesetzt |
| Facebook-Seite | LinguaFlow App (existierte bereits, 1 Follower) |
| Instagram | `linguaflow.app` (3 Follower), ist in der Anzeige verknüpft |
| Zahlungsmittel | von Christian hinterlegt |

Christians persönliches Werbekonto „Christian Nouza" (`922566344556976`)
hat 3 fremde Kampagnen (Tempur-Matratze u. a.) — **nicht anfassen.**

## Kampagnen-Einstellungen (Entwurf, alles gespeichert)

- **Kampagne:** `LinguaFlow – Traffic Test August 2026`, Ziel **Traffic**, Auktion,
  manuell konfiguriert (nicht die „empfohlene Einrichtung")
- **Anzeigengruppe:** `AT/DE/CH – Sprachenlernen 25-60`
  - Conversion-Ort **Website** (Meta hatte „Messaging" vorausgewählt — umgestellt!)
  - Performance-Ziel: Landingpage-Aufrufe maximieren
  - Budget **10 €/Tag**, Laufzeit **16.08. 05:00 → 23.08. 23:59** (= 8 Tage, max. 80 €)
  - Standorte: Österreich, Deutschland, Schweiz
  - Interessen: **Fremdsprache**, **Fremdsprachenunterricht** (Zielgruppe 3,1–3,6 Mio)
  - Advantage+ Audience bleibt AN, Interessen nur als Vorschlag → bei 10 €/Tag
    liefert hartes Einschränken schlechter aus
  - EU-Pflichtangabe Werbetreibender: **LinguaFlow e.U.** (öffentlich in der Meta-Werbebibliothek)
- **Anzeige A** `A – Problem zuerst (Vokabelpauken)`: Ziel-URL gesetzt auf
  `https://linguaflow.app/?utm_source=facebook&utm_medium=cpc&utm_campaign=traffic-test-0816`

## Erkenntnis: Birkenbihl lässt sich NICHT targetieren
Facebook führt weder „Birkenbihl" noch „Vera F. Birkenbihl" als Interesse
(zweimal sauber geprüft — beim ersten Versuch aktualisierte sich die Vorschlagsliste
gar nicht, der Test war wertlos; bei „Fremdsprache" kamen echte Treffer, bei
„Birkenbihl" nichts). **Werbeanzeigen können außerdem grundsätzlich nicht auf
bestimmte Facebook-Gruppen ausgerichtet werden.** Wer Birkenbihl-Gruppen erreichen
will, muss dort organisch posten (Gruppenregeln beachten, viele verbieten Werbung).

## Anzeigentexte (abgestimmt, noch nicht eingetragen)

**A – Problem zuerst**
> Du hast jahrelang Vokabeln gepaukt – und trotzdem fehlen dir im Gespräch die Worte?
> Das liegt nicht an dir, das liegt an der Methode. LinguaFlow lernt Sprachen so,
> wie dein Gehirn es ohnehin tut: verstehen statt auswendig lernen.
> Überschrift: *Sprachen lernen ohne Vokabelpauken* · Beschreibung: *Inspiriert von der Birkenbihl-Methode*

**B – Neugier auf die Methode**
> Kinder lernen ihre Muttersprache ohne eine einzige Vokabelliste. LinguaFlow nutzt
> genau dieses Prinzip: Jeder Text wird Wort für Wort dekodiert, du hörst mit –
> und die Grammatik kommt von allein.
> Überschrift: *So lernt dein Gehirn Sprachen wirklich* · Beschreibung: *30+ Sprachen, iOS & Android*

**C – Alltagsnutzen**
> 10 Minuten am Tag. Kein Vokabelheft, keine Grammatikregeln. LinguaFlow übersetzt
> jeden Text Wort für Wort – du hörst zu und verstehst. Auch nebenbei beim Kochen oder Autofahren.
> Überschrift: *Sprachen lernen nebenbei* · Beschreibung: *Jetzt kostenlos ausprobieren*

Alle drei gleichzeitig schalten — Meta verteilt das Budget nach ein paar Tagen
automatisch auf die beste Variante, das kostet nicht extra.

## Werbebilder
1080×1080, App-Screenshot mittig auf Markenviolett `#7C5CFC`
(erzeugt mit `sips -Z 980` + `sips --padToHeightWidth 1080 1080 --padColor 7C5CFC`).
Quellen sind die **aktuellen** Screenshots (15.08. bzw. 09.08.) — die erste Fassung
stammte versehentlich aus den veralteten Website-Bildern von Juli.

> ⚠️ Die Dateien liegen noch im Scratchpad einer beendeten Session und sind
> **verloren**. Vor der Weiterarbeit neu erzeugen (Befehl oben) aus:
> `NEU 2026-08 Roh-Screenshots/iOS/04-Decoded-View.png`,
> `Blanke Screenshots für Website 2026-08-15/01-startseite-uebersicht.png`,
> `… /03-lernweg-lektion-dekodiert.png`

## Offene Punkte / nächste Schritte
1. **BLOCKER: verifizierte Telefonnummer** fürs Werbekonto (Meta-Fehler `#3858013`,
   Button „Telefonnummer hinzufügen" im Ads Manager). Ohne das keine Auslieferung.
   Muss Christian selbst machen (SMS-Code).
2. Werbebild in Anzeige A einfügen — **Christian per Drag & Drop**: Meta erzeugt das
   `input[type=file]` erst beim Klick, und der öffnet einen nativen Dateidialog,
   den der Agent nicht bedienen kann (gleiches Muster wie beim Play-Store-Upload).
3. Primärtext / Überschrift / Beschreibung / Button für A eintragen
4. Anzeigen B und C als Duplikate anlegen
5. **Start-/Enddatum neu setzen** — der Entwurf steht auf 16.–23.08., das ist
   vorbei. Christians ursprüngliche Vorgabe war: Start früh am Morgen (05:00),
   Ende um Mitternacht, rund eine Woche Laufzeit bei 10 €/Tag
6. Erst danach „Veröffentlichen" — **nur nach ausdrücklicher Freigabe von Christian**

## Hinweise fürs Weiterarbeiten
- `adsmanager.facebook.com`, `business.facebook.com` und `facebook.com` mussten in
  der Claude-Chrome-Erweiterung einzeln freigegeben werden; der eingebaute
  Claude-Browser darf Facebook gar nicht öffnen (Richtlinie).
- Meta setzt gern Voreinstellungen, die nicht passen: Conversion-Ort „Messaging",
  Zeitzone Los Angeles, Währung USD, Budget 20 €/Tag, Start „in 20 Minuten".
  Jedes Feld einzeln kontrollieren.
