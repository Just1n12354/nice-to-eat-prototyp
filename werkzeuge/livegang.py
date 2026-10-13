#!/usr/bin/env python3
"""livegang.py - baut aus dem Prototyp die Live-Version fuer Netlify.

Der Prototyp im Repo bleibt unveraendert. Das Skript schreibt eine Kopie nach
`fertig/` (von Git ignoriert) und packt sie als `fertig.zip` fuer den
Drag&Drop-Deploy auf Netlify.

    python werkzeuge/livegang.py --domain nicetoeat.ch
    python werkzeuge/livegang.py --domain nicetoeat.ch --formular
    python werkzeuge/livegang.py --domain nicetoeat.ch --formular --sichtbar

Was es immer tut:
- PROTOTYP-Balken und was-fehlt.html entfernen
- canonical und og:url auf die echte Domain setzen (im Prototyp zeigen sie
  auf Instagram - live waere das falsch: Google wuerde Instagram als
  Hauptadresse der Seite werten)
- sitemap.xml auf die Domain umschreiben

--formular  Kontaktformular fuer Netlify Forms verdrahten, danke.html dazu.
            Erst nehmen, wenn die Empfaenger-Adresse feststeht - Netlify
            schickt sonst keine Mail (siehe ANLEITUNG-LIVEGANG.md, Schritt 5).
--sichtbar  noindex entfernen und robots.txt fuer Suchmaschinen oeffnen.
            Verweigert, solange das Impressum noch "Offene Angaben" hat.

Entstanden am 13.10.2026 fuer den Termin beim Kunden.
"""
import argparse
import datetime
import pathlib
import re
import shutil
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "fertig"
MITNEHMEN = ["bilder", "schriften", "stil.css", "404.html", "index.html", "bilder.html",
             "kontakt.html", "impressum.html", "datenschutz.html", "robots.txt", "sitemap.xml"]

DANKE = """<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Danke für Ihre Anfrage</title>
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="stil.css">
</head>
<body>
<main id="inhalt">
<section class="s s--text s--eng s--laut">
<h1>Danke für Ihre Anfrage</h1>
<p>Nice to Eat meldet sich so bald wie möglich bei Ihnen. Eilt es, rufen Sie an: <a href="tel:+41795751558">+41 79 575 15 58</a>.</p>
<p><a class="knopf" href="index.html">Zur Startseite</a></p>
</section>
</main>
</body>
</html>
"""


def seite_url(domain, name):
    return f"https://{domain}/" if name in ("index.html", "404.html") else f"https://{domain}/{name}"


def umbauen(text, name, args):
    url = seite_url(args.domain, name)
    text = re.sub(r'<p class="prototyp">.*?</p>\n?', "", text)
    text = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', text)
    text = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', text)
    if args.sichtbar and name != "404.html":
        text = re.sub(r'<meta name="robots" content="noindex, nofollow">\n?', "", text)
    if args.formular and name == "kontakt.html":
        alt = "<form>"
        neu = ('<form name="anfrage" method="POST" action="danke.html" data-netlify="true" '
               'netlify-honeypot="website">\n<input type="hidden" name="form-name" value="anfrage">')
        if text.count(alt) != 1:
            sys.exit("kontakt.html: <form> nicht eindeutig gefunden - Formular von Hand pruefen")
        text = text.replace(alt, neu)
        text = re.sub(r'<p class="vorschau-hinweis">.*?</p>\n?', "", text)
        text = text.replace('<button class="knopf" type="button" disabled aria-disabled="true">',
                            '<button class="knopf" type="submit">')
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--domain", required=True, help="z. B. nicetoeat.ch (ohne www, ohne https)")
    ap.add_argument("--formular", action="store_true")
    ap.add_argument("--sichtbar", action="store_true")
    args = ap.parse_args()
    args.domain = args.domain.strip().removeprefix("https://").removeprefix("www.").strip("/")

    impressum = (WURZEL / "impressum.html").read_text(encoding="utf-8")
    if args.sichtbar and 'id="offene-angaben"' in impressum:
        sys.exit("Impressum hat noch 'Offene Angaben' - erst ergaenzen, dann --sichtbar.")

    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    ZIEL.mkdir()
    for eintrag in MITNEHMEN:
        quelle = WURZEL / eintrag
        if quelle.is_dir():
            shutil.copytree(quelle, ZIEL / eintrag)
        else:
            shutil.copy2(quelle, ZIEL / eintrag)

    for html in ZIEL.glob("*.html"):
        html.write_text(umbauen(html.read_text(encoding="utf-8"), html.name, args), encoding="utf-8")
    if args.formular:
        (ZIEL / "danke.html").write_text(DANKE, encoding="utf-8")

    heute = datetime.date.today().isoformat()
    sitemap = (ZIEL / "sitemap.xml").read_text(encoding="utf-8")
    sitemap = sitemap.replace("https://nice-to-eat-catering.invalid", f"https://{args.domain}")
    sitemap = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{heute}</lastmod>", sitemap)
    (ZIEL / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    if args.sichtbar:
        (ZIEL / "robots.txt").write_text(
            f"User-agent: *\nAllow: /\n\nSitemap: https://{args.domain}/sitemap.xml\n", encoding="utf-8")

    rest = [p.name for p in ZIEL.glob("*.html") if "was-fehlt.html" in p.read_text(encoding="utf-8")]
    if rest:
        sys.exit(f"Verweis auf was-fehlt.html uebrig in: {', '.join(rest)}")

    zip_pfad = shutil.make_archive(str(WURZEL / "fertig"), "zip", ZIEL)
    print(f"Fertig: {ZIEL}  und  {zip_pfad}")
    print(f"Domain {args.domain} · Formular {'an' if args.formular else 'aus'} · "
          f"Suchmaschinen {'offen' if args.sichtbar else 'gesperrt'}")


if __name__ == "__main__":
    main()
