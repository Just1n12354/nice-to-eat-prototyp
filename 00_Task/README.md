# Aufgaben im Repo nice-to-eat-prototyp

`aufgaben.json` ist die Arbeitsquelle für die Aufgaben dieses Repositories.
`Aufgaben.pdf` ist nur die Ausgabe zum Lesen und Ausdrucken — massgebend ist
allein die JSON-Datei.

Nach jeder Änderung an der JSON:

```powershell
python 00_Task/pdf_erzeugen.py            # PDF neu schreiben
python 00_Task/pdf_erzeugen.py --pruefen  # JSON-Inhalt und PDF-Stand prüfen
```

**Achtung, öffentlich:** Das Repo ist öffentlich, und GitHub Pages liefert den
ganzen Wurzelordner aus, also auch diesen Ordner. Hier gehört nur hinein, was
ohnehin auf der Website steht (vor allem `was-fehlt.html`), oder rein technische
Punkte. Keine Preise, Kundennamen oder Absprachen, bevor sie freigegeben sind.

## So arbeiten wir

1. Eine Aufgabe auswählen und auf `laeuft` setzen.
2. Den aktuellen Zustand prüfen.
3. Eine kleine Änderung durchführen und das Ergebnis dokumentieren.
4. Erst mit einem konkreten Nachweis (Commit, Prüfbefehl) auf `erledigt` setzen.

Kommt eine Angabe vom Kunden, die Website anpassen **und** den Punkt in
`was-fehlt.html` streichen — die Seite ist die Liste für den Kunden, diese
JSON die Arbeitsliste. Beide müssen zusammenpassen.

## Reihenfolge

- `hoch`: Rechte, Einwilligungen, gesetzliche Pflichtangaben.
- `mittel`: Inhalte, die für die fertige Website nötig sind.
- `tief`: Ordnung und Verbesserungen.
