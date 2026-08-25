#!/usr/bin/env python3
"""Scanner: entità con ancora in png/fazioni/lore che compaiono nei capitoli ma non sono MAI linkate."""
import re, os, sys

BASE = "/home/federico/volos-guide-to-pp/docs"
CHAPTERS_DIR = os.path.join(BASE, "sessioni/strahd")

# (ancora, label, [pattern da cercare])
ENTITIES = [
    # --- PNG ---
    ("strahd-von-zarovich", "Strahd", ["Strahd von Zarovich", "Strahd"]),
    ("ireena-kolyana", "Ireena", ["Ireena Kolyana", "Ireena"]),
    ("tatyana", "Tatyana", ["Tatyana"]),
    ("sergei", "Sergei", ["Sergei von Zarovich", "Sergei"]),
    ("ismark", "Ismark", ["Ismark Kolyanovich", "Ismark"]),
    ("madam-eva", "Madam Eva", ["Madam Eva"]),
    ("van-richten", "Van Richten", ["Rudolph van Richten", "Van Richten"]),
    ("rictavio", "Rictavio", ["Rictavio"]),
    ("ezmeralda", "Ezmeralda", ["Ezmeralda"]),
    ("baba-lysaga", "Baba Lysaga", ["Baba Lysaga"]),
    ("kasimir", "Kasimir", ["Kasimir Velikov", "Kasimir"]),
    ("vladimir", "Vladimir", ["Vladimir Horngaard", "Vladimir"]),
    ("sir-godfrey", "Sir Godfrey", ["Sir Godfrey", "Godfrey"]),
    ("vargas-vallakovich", "Vargas Vallakovich", ["Vargas Vallakovich", "Vargas"]),
    ("victor-vallakovich", "Victor Vallakovich", ["Victor Vallakovich", "Victor"]),
    ("fiona-watcher", "Fiona Wachter", ["Fiona Wachter", "Fiona", "Wachter"]),
    ("padre-lucian", "Padre Lucian", ["Padre Lucian", "Lucian"]),
    ("danika-martikov", "Danika Martikov", ["Danika Martikov", "Danika"]),
    ("urwin-martikov", "Urwin Martikov", ["Urwin Martikov", "Urwin"]),
    ("izek", "Izek", ["Izek"]),
    ("henrik", "Henrik", ["Henrik"]),
    ("bluto", "Bluto", ["Bluto"]),
    ("dimitri-krezkov", "Dimitri Krezkov", ["Dimitri Krezkov", "Dimitri"]),
    ("abbate", "L'Abbate", ["L'Abbate", "Abbate"]),
    ("odjek", "Odjek", ["Odjek"]),
    ("davian-martikov", "Davian Martikov", ["Davian Martikov", "Davian"]),
    ("muriel", "Muriel", ["Muriel"]),
    ("luvash", "Luvash", ["Luvash"]),
    ("arrigal", "Arrigal", ["Arrigal"]),
    ("arabelle", "Arabelle", ["Arabelle"]),
    ("rahadin", "Rahadin", ["Rahadin"]),
    ("escher", "Escher", ["Escher"]),
    ("ludmilla", "Ludmilla", ["Ludmilla"]),
    ("anastrasya", "Anastrasya", ["Anastrasya"]),
    ("volenta", "Volenta", ["Volenta"]),
    ("gertruda", "Gertruda", ["Gertruda"]),
    ("xenia", "Xenia", ["Xenia"]),
    ("morgantha", "Morgantha", ["Morgantha"]),
    ("vasili-von-holtz", "Vasili", ["Vasili von Holtz", "Vasili"]),
    ("sarek", "Sarek", ["Sarek"]),
    ("helga", "Helga", ["Helga"]),
    ("rina", "Rina", ["Rina"]),
    ("gnemo", "Gnemo", ["Gnemo"]),
    ("donavich", "Donavich", ["Padre Donavich", "Donavich"]),
    ("doru", "Doru", ["Doru"]),
    ("naso", "Naso", ["Naso"]),
    ("maddok", "Maddok", ["Maddok"]),
    # --- LORE ---
    ("barovia", "Barovia", ["Barovia"]),
    ("castle-ravenloft", "Castle Ravenloft", ["Castle Ravenloft"]),
    ("tempio-ambra", "Tempio d'Ambra", ["Tempio d'Ambra"]),
    ("argynvostholt", "Argynvostholt", ["Argynvostholt"]),
    ("polla-di-tser", "Polla di Tser", ["Polla di Tser"]),
    ("yester-hill", "Yester Hill", ["Yester Hill"]),
    ("berez", "Berez", ["Berez"]),
    ("krezk", "Krezk", ["Krezk"]),
    ("abbazia-san-markovia", "Abbazia di San Markovia", ["Abbazia di San Markovia"]),
    ("mulino-bonegrinder", "Mulino di Bonegrinder", ["Mulino di Bonegrinder"]),
    ("vallaki", "Vallaki", ["Vallaki"]),
    ("torre-van-richten", "Torre di Van Richten", ["Torre di Van Richten", "Torre di Baratok"]),
    ("lago-zarovich", "Lago Zarovich", ["Lago Zarovich"]),
    ("witchlight-carnival", "Witchlight Carnival", ["Witchlight Carnival"]),
    # --- FAZIONI ---
    ("custodi-delle-piume", "Custodi delle Piume", ["Custodi delle Piume"]),
    ("cavalieri-dargento", "Cavalieri d'Argento", ["Cavalieri d'Argento"]),
    ("vistani", "Vistani", ["Vistani"]),
    ("chiesa-santandral", "Chiesa di Sant'Andral", ["Chiesa di Sant'Andral", "Sant'Andral"]),
    ("famiglia-vallakovich", "Famiglia Vallakovich", ["Famiglia Vallakovich", "famiglia Vallakovich"]),
    ("famiglia-wachter", "Famiglia Wachter", ["Famiglia Wachter", "famiglia Wachter"]),
    ("druidi-collina-selvaggia", "Druidi della Collina Selvaggia", ["Druidi della Collina Selvaggia"]),
    ("streghe-di-ravenloft", "Streghe di Ravenloft", ["Streghe di Ravenloft"]),
    ("megere-di-bonegrinder", "Megere di Bonegrinder", ["Megere di Bonegrinder"]),
]

def esc(s):
    return re.escape(s)

# Pre-compila pattern: (ancora, label, regex alternation con word boundary, lista pattern per mostrare)
compiled = []
for ancora, label, patterns in ENTITIES:
    rx = re.compile(r"(?<!\w)(?:" + "|".join(esc(p) for p in patterns) + r")(?!\w)")
    compiled.append((ancora, label, rx, patterns))

def count_occ(text, rx):
    return len(rx.findall(text))

def has_link_to(text, ancora):
    # link markdown: [testo](<.../#ancora>) o (#ancora)
    rx = re.compile(r"\(\s*<[^)]*#" + re.escape(ancora) + r"\s*\)")
    return len(rx.findall(text)) > 0

chapters = sorted(f for f in os.listdir(CHAPTERS_DIR) if f.endswith(".md"))

print("Entità che COMPAIONO in un capitolo ma non hanno NESSUN link all'ancora:\n")
for fname in chapters:
    path = os.path.join(CHAPTERS_DIR, fname)
    text = open(path, encoding="utf-8").read()
    misses = []
    for ancora, label, rx, patterns in compiled:
        occ = count_occ(text, rx)
        if occ > 0 and not has_link_to(text, ancora):
            # escludi casi in cui l'ancora stessa è nel testo (frontmatter/nav) — irrilevante
            misses.append((label, ancora, occ))
    if misses:
        chapter = fname.replace(".md", "")
        print(f"=== {chapter} ===")
        for label, ancora, occ in misses:
            print(f"  - {label}  [{occ} occorrenze]  →  #{ancora}")
print("\nFine.")