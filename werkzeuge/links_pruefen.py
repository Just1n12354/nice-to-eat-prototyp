#!/usr/bin/env python3
"""links_pruefen.py - prueft alle internen Verweise der Website.

Liest jede HTML-Datei (href, src, id) und jede CSS-Datei (url(...)) und
meldet Verweise auf fehlende Dateien oder fehlende Anker. Externe Links
(http, mailto, tel, data) werden nicht geprueft.

    python werkzeuge/links_pruefen.py    Exit 1, sobald ein Verweis ins Leere zeigt

Entstanden am 02.10.2026: Die Seite hatte keine Tests; das ist die einzige
Pruefung, die sich ohne Browser automatisch machen laesst.
"""
import pathlib
import re
import sys
from html.parser import HTMLParser

WURZEL = pathlib.Path(__file__).resolve().parent.parent
EXTERN = re.compile(r"^(https?:|mailto:|tel:|data:|//)")


class Seite(HTMLParser):
    def __init__(self):
        super().__init__()
        self.verweise = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.verweise.append(v)
            if k == "id" and v:
                self.ids.add(v)


def dateien(muster):
    return [f for f in WURZEL.rglob(muster) if ".git" not in f.parts]


def main():
    seiten = {}
    for f in dateien("*.html"):
        s = Seite()
        s.feed(f.read_text(encoding="utf-8"))
        seiten[f] = s
    verweise = [(f, v) for f, s in seiten.items() for v in s.verweise]
    for f in dateien("*.css"):
        for v in re.findall(r"url\(['\"]?([^'\")]+)", f.read_text(encoding="utf-8")):
            verweise.append((f, v))

    fehler, geprueft = [], 0
    for f, v in verweise:
        if EXTERN.match(v):
            continue
        geprueft += 1
        pfad, _, anker = v.partition("#")
        ziel = (f.parent / pfad).resolve() if pfad else f
        if not ziel.exists():
            fehler.append(f"{f.relative_to(WURZEL)}: {v} -> Datei fehlt")
        elif anker and ziel in seiten and anker not in seiten[ziel].ids:
            fehler.append(f"{f.relative_to(WURZEL)}: {v} -> Anker fehlt")

    print(f"{len(seiten)} HTML-Dateien, {geprueft} interne Verweise, {len(fehler)} Fehler")
    for x in fehler:
        print("  " + x)
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
