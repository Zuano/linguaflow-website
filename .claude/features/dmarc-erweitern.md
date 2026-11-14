# Feature: DMARC-Record erweitern

**Status:** Freigegeben, aber noch NICHT geschrieben (2026-11-14). Christian hat „Ja, ändern" gesagt; der Schreibzugriff über den WordPress.com-Connector wurde vom Berechtigungssystem der Claude-Session abgelehnt. Eintrag steht weiter auf `p=none`. Nächster Schritt siehe „So wird es fertig".
**Ort der Umsetzung:** DNS der Domain `linguaflow.app` bei WordPress.com (per WordPress.com-Connector, siehe Memory „DNS bei WordPress.com")
**Aufwand:** ca. 5 Minuten
**Kategorie:** E-Mail-Sicherheit / Reputation

---

## Ziel
Fake-Mails (Phishing, Spoofing) im Namen von `linguaflow.app` sollen automatisch im Spam landen. Zusätzlich wollen wir Reports bekommen, wer versucht, in unserem Namen Mails zu verschicken.

## Aktuelle Situation (geprüft 2026-11-14, Zone frisch gelesen + `dig`)

| Eintrag | Wert |
|---|---|
| `_dmarc` TXT (TTL 3600) | `v=DMARC1; p=none; rua=mailto:hello@linguaflow.app` |
| SPF (TXT am Apex) | `v=spf1 include:_spf.mlsend.com include:_spf.google.com ~all` |
| DKIM Google | `google._domainkey` TXT vorhanden |
| DKIM MailerLite | `litesrv._domainkey` CNAME → `litesrv._domainkey.mlsend.com` |
| MX | `1 smtp.google.com` |

### Wer verschickt Mails im Namen der Domain – und bestehen sie DMARC?

DMARC besteht, wenn SPF **oder** DKIM zur Absender-Domain passt („aligned").

| Versender | SPF aligned | DKIM aligned | Beleg |
|---|---|---|---|
| **Google Workspace** (Postfach `christian@`, Aliase `hello@`, `quittung@`) | ja | ja, laut Admin-Konsole | Fastmail-Bericht 13.09.2026: SPF `linguaflow.app` pass. DKIM damals noch Googles Ersatzschlüssel (`d=linguaflow-app.20251104.gappssmtp.com`). Admin-Konsole am 14.11.2026 (geprüft durch die Hauptsession): „E-Mails werden über DKIM authentifiziert", Selektor `google`, Schlüssel identisch mit dem DNS-Eintrag. **Noch kein Bericht, der `d=linguaflow.app` für Google zeigt** – siehe Nachkontrolle. |
| **Automatische Trial-Erinnerungen** (Firebase-Erweiterung `firestore-send-email`) | wie Google | wie Google | Versand über `smtp.gmail.com` (Skill `kunden-erinnerung`), also Google Workspace – kein eigener Versender. |
| **MailerLite** (Newsletter, Double-Opt-in) | nein (Umschlag-Absender `mlsend.com`) | **ja** | Seznam-Bericht 08.11.2026: DKIM `d=linguaflow.app`, Selektor `litesrv`, pass → DMARC bestanden. |

Weitere Versender wurden in den Postfächern der letzten 20 Tage nicht gefunden.

## Neuer DMARC-Eintrag (von Christian am 26.10.2026 grundsätzlich gewählt: „erst Google prüfen", dann umstellen)

| Feld | Wert |
|------|------|
| Typ | `TXT` |
| Name | `_dmarc` |
| Wert | `v=DMARC1; p=quarantine; rua=mailto:hello@linguaflow.app` |
| TTL | `3600` |

Es ändert sich nur `p=none` → `p=quarantine`. Vorgehen: alten Eintrag mit exakt den gelesenen Feldern entfernen, neuen hinzufügen, sonst nichts in der Zone anfassen.

### Bewusst NICHT übernommen (Vorschlag vom Juni 2026)
- `adkim=s` / `aspf=s` (strenger Abgleich): unnötiges Risiko, MailerLite besteht SPF nur „entspannt" gar nicht und hängt allein an DKIM.
- `ruf=` (Einzelfall-Berichte): wird von den großen Anbietern kaum verschickt, bringt nichts.
- `dmarc@linguaflow.app` als Berichtsadresse: Die Berichte kommen bereits an `hello@` an.
- `pct=100`: ist ohnehin der Standardwert.

## So wird es fertig (zwei Wege, einer genügt)

**Weg A – Christian selbst, ca. 2 Minuten:** wordpress.com → Upgrades → Domains → `linguaflow.app` → DNS-Einträge → Eintrag `_dmarc` (TXT) bearbeiten → im Wert nur `p=none` durch `p=quarantine` ersetzen → speichern. Ergebnis muss exakt lauten: `v=DMARC1; p=quarantine; rua=mailto:hello@linguaflow.app`.

**Weg B – Claude macht es:** Christian schreibt die Freigabe direkt in die Session, die den Eintrag ändern soll (nicht über eine andere Session weitergereicht), oder erlaubt das Werkzeug `wpcom-domain-update-dns-records` in seinen Claude-Einstellungen. Dann: alten Eintrag (`TXT`, Name `_dmarc`, TTL 3600, alter Wert) entfernen, neuen hinzufügen.

Danach in beiden Fällen den Check unten ausführen, den TODO-Punkt abhaken und den DECISIONS-Eintrag um das Datum der Umstellung ergänzen.

## Check nach der Umstellung
- `dig +short TXT _dmarc.linguaflow.app @ns1.wordpress.com` und `@8.8.8.8` zeigen den neuen Wert.
- MX, SPF und beide DKIM-Einträge unverändert.

## Nachkontrolle (nach der Umstellung)
- Nächsten DMARC-Bericht an `hello@` abwarten, in dem eine **Google**-Mail vorkommt: DKIM muss `d=linguaflow.app`, Selektor `google`, `pass` zeigen. Steht dort weiter `gappssmtp.com`, in der Google-Admin-Konsole die Authentifizierung neu starten.
- In den Berichten auf `disposition=quarantine` bei eigenen Mails achten. Kommt das vor: sofort zurück auf `p=none` und Ursache suchen.

## Risiken / Seiteneffekte
- **Risiko:** Legitime Mails landen im Spam, wenn ein Dienst ohne korrekte SPF/DKIM im Namen der Domain verschickt. → Abgesichert durch die Tabelle oben; `p=quarantine` statt `p=reject`; Berichte beobachten.
- **Rückweg:** Eintrag zurück auf `p=none`, wirkt binnen einer Stunde (TTL 3600).
- **Kein Risiko für die Website** – reine DNS-Änderung.
