#!/usr/bin/env python3
"""
Aggiunge link alle entità (PNG, Fazioni, Lore) nei capitoli della wiki.
Strategia: prima menzione per capitolo — solo la prima occorrenza di ogni entità.
Non tocca: link già esistenti, [[]], intestazioni, blockquote, codice.
"""
import re, os, sys

BASE = "/home/federico/volos-guide-to-pp/docs"
CHAPTERS_DIR = os.path.join(BASE, "sessioni/strahd")

# (ancora, label, [pattern ordinati per lunghezza decrescente], link_path)
ENTITIES = [
    # --- PNG ---
    ("strahd-von-zarovich", "Strahd", ["Strahd von Zarovich", "Strahd"], "../../../png/strahd/"),
    ("ireena-kolyana", "Ireena", ["Ireena Kolyana", "Ireena"], "../../../png/strahd/"),
    ("tatyana", "Tatyana", ["Tatyana"], "../../../png/strahd/"),
    ("sergei", "Sergei", ["Sergei von Zarovich", "Sergei"], "../../../png/strahd/"),
    ("ismark", "Ismark", ["Ismark Kolyanovich", "Ismark"], "../../../png/strahd/"),
    ("madam-eva", "Madam Eva", ["Madam Eva"], "../../../png/strahd/"),
    ("van-richten", "Van Richten", ["Rudolph van Richten", "Van Richten"], "../../../png/strahd/"),
    ("rictavio", "Rictavio", ["Rictavio"], "../../../png/strahd/"),
    ("ezmeralda", "Ezmeralda", ["Ezmeralda d'Avenir", "Ezmeralda"], "../../../png/strahd/"),
    ("baba-lysaga", "Baba Lysaga", ["Baba Lysaga"], "../../../png/strahd/"),
    ("kasimir", "Kasimir", ["Kasimir Velikov", "Kasimir"], "../../../png/strahd/"),
    ("vladimir", "Vladimir", ["Vladimir Horngaard", "Vladimir"], "../../../png/strahd/"),
    ("sir-godfrey", "Sir Godfrey", ["Sir Godfrey Gwilym", "Sir Godfrey", "Godfrey"], "../../../png/strahd/"),
    ("vargas-vallakovich", "Vargas", ["Vargas Vallakovich", "Vargas"], "../../../png/strahd/"),
    ("victor-vallakovich", "Victor", ["Victor Vallakovich", "Victor"], "../../../png/strahd/"),
    ("fiona-watcher", "Fiona Wachter", ["Dame Fiona Wachter", "Fiona Wachter", "Fiona", "Wachter"], "../../../png/strahd/"),
    ("padre-lucian", "Padre Lucian", ["Padre Lucian Petrovich", "Padre Lucian", "Lucian"], "../../../png/strahd/"),
    ("danika-martikov", "Danika", ["Danika Martikov", "Danika"], "../../../png/strahd/"),
    ("urwin-martikov", "Urwin", ["Urwin Martikov", "Urwin"], "../../../png/strahd/"),
    ("izek", "Izek", ["Izek Strazni", "Izek"], "../../../png/strahd/"),
    ("henrik", "Henrik", ["Henrik"], "../../../png/strahd/"),
    ("bluto", "Bluto", ["Bluto"], "../../../png/strahd/"),
    ("dimitri-krezkov", "Dimitri", ["Dimitri Krezkov", "Dimitri"], "../../../png/strahd/"),
    ("abbate", "Abbate", ["L'Abbate", "Abbate"], "../../../png/strahd/"),
    ("odjek", "Odjek", ["Odjek"], "../../../png/strahd/"),
    ("davian-martikov", "Davian", ["Davian Martikov", "Davian"], "../../../png/strahd/"),
    ("muriel", "Muriel", ["Muriel Vinshaw", "Muriel"], "../../../png/strahd/"),
    ("luvash", "Luvash", ["Luvash"], "../../../png/strahd/"),
    ("arrigal", "Arrigal", ["Arrigal"], "../../../png/strahd/"),
    ("arabelle", "Arabelle", ["Arabelle"], "../../../png/strahd/"),
    ("rahadin", "Rahadin", ["Rahadin"], "../../../png/strahd/"),
    ("escher", "Escher", ["Escher"], "../../../png/strahd/"),
    ("ludmilla", "Ludmilla", ["Ludmilla"], "../../../png/strahd/"),
    ("anastrasya", "Anastrasya", ["Anastrasya"], "../../../png/strahd/"),
    ("volenta", "Volenta", ["Volenta"], "../../../png/strahd/"),
    ("gertruda", "Gertruda", ["Gertruda"], "../../../png/strahd/"),
    ("xenia", "Xenia", ["Xenia"], "../../../png/strahd/"),
    ("morgantha", "Morgantha", ["Morgantha"], "../../../png/strahd/"),
    ("vasili-von-holtz", "Vasili", ["Vasili Von Holtz", "Vasili"], "../../../png/strahd/"),
    ("sarek", "Sarek", ["Sarek"], "../../../png/strahd/"),
    ("helga", "Helga", ["Helga"], "../../../png/strahd/"),
    ("rina", "Rina", ["Rina"], "../../../png/strahd/"),
    ("gnemo", "Gnemo", ["Gnemo"], "../../../png/strahd/"),
    ("donavich", "Donavich", ["Padre Donavich", "Donavich"], "../../../png/strahd/"),
    ("doru", "Doru", ["Doru"], "../../../png/strahd/"),
    ("naso", "Naso", ["Naso"], "../../../png/strahd/"),
    ("maddok", "Maddok", ["Maddok"], "../../../png/strahd/"),
    # --- LORE ---
    ("barovia", "Barovia", ["Barovia"], "../../../lore/strahd/"),
    ("castle-ravenloft", "Castle Ravenloft", ["Castle Ravenloft"], "../../../lore/strahd/"),
    ("tempio-ambra", "Tempio d'Ambra", ["Tempio d'Ambra"], "../../../lore/strahd/"),
    ("argynvostholt", "Argynvostholt", ["ArcaynVostholt", "Argynvostholt"], "../../../lore/strahd/"),
    ("polla-di-tser", "Polla di Tser", ["Polla di Tser"], "../../../lore/strahd/"),
    ("yester-hill", "Yester Hill", ["Yester Hill"], "../../../lore/strahd/"),
    ("berez", "Berez", ["Berez"], "../../../lore/strahd/"),
    ("krezk", "Krezk", ["Krezk"], "../../../lore/strahd/"),
    ("abbazia-san-markovia", "Abbazia di San Markovia", ["Abbazia di San Markovia"], "../../../lore/strahd/"),
    ("mulino-bonegrinder", "Mulino di Bonegrinder", ["Mulino di Bonegrinder", "Mulino di Bonegrinder"], "../../../lore/strahd/"),
    ("vallaki", "Vallaki", ["Vallaki"], "../../../lore/strahd/"),
    ("torre-van-richten", "Torre di Van Richten", ["Torre di Van Richten", "Torre di Baratok", "torre di Baratok"], "../../../lore/strahd/"),
    ("lago-zarovich", "Lago Zarovich", ["Lago Zarovich", "lago Zarovich"], "../../../lore/strahd/"),
    ("witchlight-carnival", "Witchlight Carnival", ["Witchlight Carnival"], "../../../lore/strahd/"),
    # --- FAZIONI ---
    ("custodi-delle-piume", "Custodi delle Piume", ["Custodi delle Piume", "custodi delle piume"], "../../../fazioni/strahd/"),
    ("cavalieri-dargento", "Cavalieri d'Argento", ["Cavalieri d'Argento", "cavalieri d'argento"], "../../../fazioni/strahd/"),
    ("vistani", "Vistani", ["Vistani", "vistani"], "../../../fazioni/strahd/"),
    ("chiesa-santandral", "Chiesa di Sant'Andral", ["Chiesa di Sant'Andral", "chiesa di Sant'Andral", "Sant'Andral", "sant'Andral"], "../../../fazioni/strahd/"),
    ("famiglia-vallakovich", "Famiglia Vallakovich", ["Famiglia Vallakovich", "famiglia Vallakovich"], "../../../fazioni/strahd/"),
    ("famiglia-wachter", "Famiglia Wachter", ["Famiglia Wachter", "famiglia Wachter"], "../../../fazioni/strahd/"),
    ("druidi-collina-selvaggia", "Druidi della Collina Selvaggia", ["Druidi della Collina Selvaggia", "druidi della Collina Selvaggia"], "../../../fazioni/strahd/"),
    ("streghe-di-ravenloft", "Streghe di Ravenloft", ["Streghe di Ravenloft", "streghe di Ravenloft"], "../../../fazioni/strahd/"),
    ("megere-di-bonegrinder", "Megere di Bonegrinder", ["Megere di Bonegrinder", "megere di Bonegrinder"], "../../../fazioni/strahd/"),
]

def esc(s):
    """Escape per regex."""
    return re.escape(s)

def is_already_linked(text, pos, name, link_path, ancora):
    """Controlla se a pos c'è già un link markdown o [[]]."""
    # Guarda indietro per [ o [[
    before = text[max(0,pos-1):pos]
    if before == '[':
        # Potrebbe essere [Name](...) o [[Name]]
        rest = text[pos:pos+len(name)]
        after = text[pos+len(name):pos+len(name)+1] if pos+len(name) < len(text) else ''
        if after == ']':
            after2 = text[pos+len(name)+1:pos+len(name)+2] if pos+len(name)+1 < len(text) else ''
            if after2 == '(':
                # [Name](...)
                return True
            elif after2 == ']':
                # [[Name]]
                return True
    return False

def process_chapter(path):
    """Aggiunge link (prima menzione) a un file capitolo."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    
    original = text
    changes = []
    
    # Prepara: per ogni entità, trova la prima occorrenza non linkata
    for ancora, label, patterns, link_path in ENTITIES:
        found = False
        for pattern in patterns:
            if found:
                break
            # Cerca il pattern con word boundary
            rx = re.compile(r'(?<!\w)(' + esc(pattern) + r')(?!\w)')
            for m in rx.finditer(text):
                pos = m.start()
                name = m.group(1)
                
                # Salta se già in un link markdown
                if is_already_linked(text, pos, name, link_path, ancora):
                    continue
                
                # Salta se in [[]] (wikilink)
                if pos > 0 and text[pos-1] == '[' and pos + len(name) < len(text) and text[pos+len(name)] == ']':
                    continue
                
                # Salta se in intestazione (###)
                line_start = text.rfind('\n', 0, pos) + 1
                line_prefix = text[line_start:pos].strip()
                if line_prefix.startswith('#'):
                    continue
                
                # Salta se in blockquote
                if line_prefix.startswith('>'):
                    continue
                
                # Prima occorrenza valida → linkala
                link = f"[{name}](<{link_path}#{ancora}>)"
                text = text[:pos] + link + text[pos+len(name):]
                changes.append(f"  {label} → #{ancora}")
                found = True
                break
    
    if changes != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return changes
    return []

chapters = sorted(f for f in os.listdir(CHAPTERS_DIR) if f.endswith(".md"))
total_changes = 0

for fname in chapters:
    path = os.path.join(CHAPTERS_DIR, fname)
    changes = process_chapter(path)
    if changes:
        print(f"=== {fname} ===")
        for c in changes:
            print(c)
        total_changes += len(changes)
        print()

print(f"Totale link aggiunti: {total_changes}")