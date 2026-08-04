# Feature: DMARC-Record erweitern

**Status:** In Arbeit – DNS-Wert vorbereitet, Christian muss eintragen
**Ort der Umsetzung:** WordPress → DNS-Einstellungen der Domain `linguaflow.app`
**Aufwand:** ca. 5 Minuten
**Kategorie:** E-Mail-Sicherheit / Reputation

---

## Ziel
Fake-Mails (Phishing, Spoofing) im Namen von `linguaflow.app` sollen automatisch im Spam landen. Zusätzlich wollen wir Reports bekommen, wer versucht, in unserem Namen Mails zu verschicken.

## Aktuelle Situation (Annahme – bitte von Christian prüfen lassen)
- SPF-Record existiert
- DKIM ist vermutlich aktiv
- DMARC steht aktuell auf `p=none` (nur beobachten, keine Aktion)

## Geplanter neuer DMARC-Eintrag

**Im WordPress-DNS folgenden TXT-Record eintragen** (oder den bestehenden DMARC-TXT-Eintrag bearbeiten):

| Feld | Wert |
|------|------|
| Typ | `TXT` |
| Host / Name | `_dmarc` |
| Inhalt / Wert | `v=DMARC1; p=quarantine; rua=mailto:dmarc@linguaflow.app; ruf=mailto:dmarc@linguaflow.app; pct=100; adkim=s; aspf=s; fo=1` |
| TTL | `3600` (oder Standard lassen) |

### Was bedeuten die einzelnen Teile in Alltagssprache?
- `v=DMARC1` → Version (immer gleich)
- `p=quarantine` → **Verdächtige Mails kommen in den Spam-Ordner** (statt durchgelassen zu werden)
- `rua=mailto:...` → Sammel-Reports gehen an diese Adresse (**Report-Aggregate** – einmal pro Tag)
- `ruf=mailto:...` → **Forensik-Reports** bei einzelnen verdächtigen Mails
- `pct=100` → Regel gilt für 100% der Mails (nicht nur Stichprobe)
- `adkim=s` / `aspf=s` → **Strenger Abgleich** von DKIM / SPF
- `fo=1` → Forensik-Reports auch bei teilweisem Fehlschlag

### Wichtig bezüglich Report-Adresse
- Die Adresse `dmarc@linguaflow.app` muss **existieren** (auch als Alias ok). Falls du keine hast, kurz klären: entweder Alias auf Hauptadresse einrichten, oder statt `dmarc@linguaflow.app` direkt deine echte Adresse (z.B. `christian@linguaflow.app`) eintragen.

## Vorsichtsvariante (falls Unsicherheit)
Wenn du dir unsicher bist, ob alle legitimen Mails (Newsletter, Kontaktformular, Transactional Mails) korrekt signiert sind, kannst du mit `pct=25` starten – dann betrifft die Quarantäne nur 25% der Mails. Nach 1–2 Wochen ohne Probleme auf `pct=100` erhöhen.

## Schritte zur Umsetzung
1. Christian loggt sich im WordPress-Dashboard ein
2. Dort zu DNS-Einstellungen der Domain `linguaflow.app`
3. Bestehenden TXT-Eintrag mit Host `_dmarc` suchen
4. Entweder bearbeiten oder neuen anlegen mit dem Wert aus der Tabelle
5. Speichern
6. 1–48 h warten, bis DNS weltweit aktualisiert ist
7. Prüfen via: https://dmarcian.com/dmarc-inspector/ – Domain eingeben → sollte `p=quarantine` anzeigen

## Offene Fragen an Christian
- [ ] Existiert die Mail-Adresse `dmarc@linguaflow.app` schon, oder welche Adresse soll die Reports bekommen?
- [ ] Ist der aktuelle DMARC-Record tatsächlich auf `p=none`? Falls ja, seit wann? (Wenn schon länger stabil läuft, können wir direkt auf `p=quarantine` gehen)
- [ ] Willst du lieber vorsichtig mit `pct=25` starten oder direkt auf `pct=100`?

## Risiken / Seiteneffekte
- **Risiko:** Legitime Mails landen im Spam, wenn ein Dienst ohne korrekte SPF / DKIM in deinem Namen verschickt. → Mitigation: `p=quarantine` statt `p=reject`; `rua`-Reports beobachten
- **Kein Risiko für die Website** selbst – reine DNS-Änderung, keine Code-Änderung
