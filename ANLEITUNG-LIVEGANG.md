# Anleitung: Nice to Eat live schalten (Netlify)

Der Prototyp bleibt im Repo, wie er ist. `werkzeuge/livegang.py` baut daraus eine
Kopie in `fertig/` und packt sie als `fertig.zip`. Diese ZIP wird auf Netlify
hochgeladen. `fertig/` und `fertig.zip` ignoriert Git.

Stand der Anleitung: 20.10.2026.

## Schritt 1: Vorher klären (mit dem Kunden)

| Punkt | Wo es fehlt | Blockiert |
|---|---|---|
| Domain (z. B. `nicetoeat.ch`) gekauft, Zugang zum DNS | - | alles |
| Name der verantwortlichen Person, Rechtsform, E-Mail | `impressum.html`, Abschnitt `id="offene-angaben"` | `--sichtbar` |
| Empfänger-Adresse für Anfragen aus dem Formular | Netlify (Schritt 5) | `--formular` |
| Datenschutz auf Netlify umstellen | `datenschutz.html` nennt heute GitHub als Hosting | Livegang |

Offene Punkte stehen in `00_Task/aufgaben.json`. Nur dort führen.

## Schritt 2: Prototyp prüfen

```powershell
cd C:\Github\nice-to-eat-prototyp
git pull
python werkzeuge/links_pruefen.py           # erwartet: 0 Fehler
python 00_Task/pdf_erzeugen.py --pruefen
```

## Schritt 3: Inhalte nachtragen

1. Impressum: fehlende Angaben eintragen. Danach den ganzen Abschnitt
   `<h2 id="offene-angaben">` mit seinem Text löschen. Solange die `id` noch
   in der Datei steht, verweigert das Skript `--sichtbar`.
2. Datenschutz: Hosting von GitHub auf Netlify (Netlify, Inc., USA) ändern.
   Mit Formular zusätzlich: Anfragen werden bei Netlify gespeichert und per
   E-Mail weitergeleitet.
3. Committen und pushen.

## Schritt 4: Live-Version bauen

Variante je nach Stand:

```powershell
# Nur Seite, Formular aus, Suchmaschinen gesperrt
python werkzeuge/livegang.py --domain nicetoeat.ch

# Mit Formular (erst wenn die Empfänger-Adresse feststeht)
python werkzeuge/livegang.py --domain nicetoeat.ch --formular

# Endstand: Formular an, für Google sichtbar
python werkzeuge/livegang.py --domain nicetoeat.ch --formular --sichtbar
```

Das Skript erledigt automatisch:
- entfernt den Prototyp-Balken und Verweise auf `was-fehlt.html`
- setzt `canonical` und `og:url` auf die Domain (im Prototyp zeigen sie auf Instagram)
- schreibt `sitemap.xml` auf die Domain und das heutige Datum um
- `--formular`: verdrahtet `kontakt.html` für Netlify Forms, legt `danke.html` an
- `--sichtbar`: entfernt `noindex`, öffnet `robots.txt` mit Sitemap-Verweis

Ergebnis: `C:\Github\nice-to-eat-prototyp\fertig.zip`.

Kurz prüfen: `fertig\index.html` im Browser öffnen, durchklicken.

## Schritt 5: Auf Netlify hochladen

Erstes Mal:
1. https://app.netlify.com anmelden.
2. **Add new site → Deploy manually**, `fertig.zip` (oder den Ordner `fertig`)
   ins Feld ziehen.
3. Netlify vergibt eine Adresse `irgendwas.netlify.app`. Dort testen.
4. **Site configuration → Change site name**, z. B. `nicetoeat`.

Jedes weitere Mal: Site öffnen → **Deploys** → neue `fertig.zip` ins
Drag-&-Drop-Feld ziehen. Ältere Deploys bleiben dort und lassen sich mit
**Publish deploy** zurückholen.

Mit `--formular` zusätzlich:
1. **Forms → Enable form detection** einschalten. Ohne diesen Schalter erkennt
   Netlify das Formular nicht. Danach die ZIP **erneut** hochladen, weil die
   Erkennung nur beim Deploy läuft.
2. Unter **Forms** muss jetzt `anfrage` erscheinen.
3. **Site configuration → Notifications → Emails and webhooks → Form submission
   notifications → Add notification → Email notification**: Empfänger-Adresse
   eintragen, Formular `anfrage` wählen. Ohne diesen Eintrag landen Anfragen
   nur im Netlify-Konto, und niemand bekommt eine Mail.
4. Testanfrage abschicken: Erscheint `danke.html`, kommt die Mail an?
   Spam-Ordner prüfen.

## Schritt 6: Domain verbinden

1. **Domain management → Add a domain**, `nicetoeat.ch` eintragen.
2. DNS beim Domain-Anbieter, eine der beiden Varianten:
   - **Nameserver auf Netlify umstellen** (Netlify zeigt die vier Nameserver an).
     Am einfachsten. Achtung: Bestehende E-Mail-Einträge (MX) der Domain müssen
     dann bei Netlify nachgetragen werden, sonst geht die Mail kaputt.
   - **Nur Einträge setzen**, Nameserver bleiben:
     `A  @    75.2.60.5` und `CNAME  www  <sitename>.netlify.app`.
     Die genauen Werte zeigt Netlify unter Domain management an. Die dortigen
     Werte gelten, falls sie von hier abweichen.
3. Warten (Minuten bis einige Stunden). Netlify holt das HTTPS-Zertifikat
   selbst. Unter **Domain management → HTTPS** prüfen.
4. `https://nicetoeat.ch` und `https://www.nicetoeat.ch` testen.

## Schritt 7: Nach dem Livegang

- Mit `--sichtbar`: In der Google Search Console die Domain anlegen und
  `https://nicetoeat.ch/sitemap.xml` einreichen.
- Instagram-Profil: Link auf die neue Domain setzen.
- Erledigte Punkte in `00_Task/aufgaben.json` abhaken,
  `python 00_Task/pdf_erzeugen.py` laufen lassen.

## Fehler und Abbrüche des Skripts

| Meldung | Bedeutung |
|---|---|
| `Impressum hat noch 'Offene Angaben'` | Schritt 3.1 nicht erledigt. Ohne `--sichtbar` bauen oder Impressum ergänzen. |
| `kontakt.html: <form> nicht eindeutig gefunden` | Formular-Markup wurde geändert. `kontakt.html` von Hand prüfen. |
| `Verweis auf was-fehlt.html uebrig in: ...` | Eine Seite verlinkt noch die gelöschte Seite. Link im Prototyp entfernen. |
