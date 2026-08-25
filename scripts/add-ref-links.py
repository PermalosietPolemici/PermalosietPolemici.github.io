#!/usr/bin/env python3
"""
Aggiunge link (prima menzione) nelle pagine di riferimento PNG, Fazioni, Lore.
Linka entità menzionate in una pagina che hanno ancora in un'altra pagina.
Path: ../../ (da png/strahd/ a lore/strahd/, ecc.)
"""
import re, os

BASE = "/home/federico/volos-guide-to-pp/docs"

# Per ogni pagina di riferimento, lista di (pattern_da_cercare, ancora_target, link_path)
# link_path è relativo alla root docs/ (poi lo script calcola il path relativo dal file)
# Le entità sono ordinate per specificità (pattern più lunghi prima)

# Entità con i loro target e path dalla root docs/
ENTITIES = {
    # PNG target
    "strahd-von-zarovich": ("../../../png/strahd/", ["Strahd von Zarovich", "Strahd"]),
    "vladimir": ("../../../png/strahd/", ["Vladimir Horngaard", "Vladimir"]),
    "vargas-vallakovich": ("../../../png/strahd/", ["Vargas Vallakovich", "Vargas"]),
    "fiona-watcher": ("../../../png/strahd/", ["Dame Fiona Wachter", "Fiona Wachter", "Fiona"]),
    "madam-eva": ("../../../png/strahd/", ["Madam Eva"]),
    "baba-lysaga": ("../../../png/strahd/", ["Baba Lysaga"]),
    "abbate": ("../../../png/strahd/", ["L'Abbate", "Abbate"]),
    "van-richten": ("../../../png/strahd/", ["Van Richten"]),
    "arabelle": ("../../../png/strahd/", ["Arabelle"]),
    "anastrasya": ("../../../png/strahd/", ["Anastrasya"]),
    "sarek": ("../../../png/strahd/", ["Sarek"]),
    "kasimir": ("../../../png/strahd/", ["Kasimir Velikov", "Kasimir"]),
    "davian-martikov": ("../../../png/strahd/", ["Davian Martikov", "Davian"]),
    "donavich": ("../../../png/strahd/", ["Donavich", "Padre Donavich"]),
    "doru": ("../../../png/strahd/", ["Doru"]),
    "naso": ("../../../png/strahd/", ["Naso"]),
    "maddok": ("../../../png/strahd/", ["Maddok"]),
    "xenia": ("../../../png/strahd/", ["Xenia"]),
    "gertruda": ("../../../png/strahd/", ["Gertruda"]),
    "helga": ("../../../png/strahd/", ["Helga"]),
    "ludmilla": ("../../../png/strahd/", ["Ludmilla"]),
    "volenta": ("../../../png/strahd/", ["Volenta"]),
    "escher": ("../../../png/strahd/", ["Escher"]),
    "rina": ("../../../png/strahd/", ["Rina"]),
    "gnemo": ("../../../png/strahd/", ["Gnemo"]),
    "izek": ("../../../png/strahd/", ["Izek Strazni", "Izek"]),
    "muriel": ("../../../png/strahd/", ["Muriel Vinshaw", "Muriel"]),
    "bluto": ("../../../png/strahd/", ["Bluto"]),
    "dimitri-krezkov": ("../../../png/strahd/", ["Dimitri Krezkov", "Dimitri"]),
    "odjek": ("../../../png/strahd/", ["Odjek"]),
    "sergei": ("../../../png/strahd/", ["Sergei von Zarovich", "Sergei"]),
    "tatyana": ("../../../png/strahd/", ["Tatyana"]),
    "ireena-kolyana": ("../../../png/strahd/", ["Ireena Kolyana", "Ireena"]),
    "ismark": ("../../../png/strahd/", ["Ismark Kolyanovich", "Ismark"]),
    "rahadin": ("../../../png/strahd/", ["Rahadin"]),
    "henrik": ("../../../png/strahd/", ["Henrik"]),
    "vasili-von-holtz": ("../../../png/strahd/", ["Vasili Von Holtz", "Vasili"]),
    "morgantha": ("../../../png/strahd/", ["Morgantha"]),
    "padre-lucian": ("../../../png/strahd/", ["Padre Lucian Petrovich", "Padre Lucian", "Lucian"]),
    "victor-vallakovich": ("../../../png/strahd/", ["Victor Vallakovich", "Victor"]),
    "rictavio": ("../../../png/strahd/", ["Rictavio"]),
    "ezmeralda": ("../../../png/strahd/", ["Ezmeralda d'Avenir", "Ezmeralda"]),
    "sir-godfrey": ("../../../png/strahd/", ["Sir Godfrey Gwilym", "Sir Godfrey", "Godfrey"]),
    "luvash": ("../../../png/strahd/", ["Luvash"]),
    "arrigal": ("../../../png/strahd/", ["Arrigal"]),
    "danika-martikov": ("../../../png/strahd/", ["Danika Martikov", "Danika"]),
    "urwin-martikov": ("../../../png/strahd/", ["Urwin Martikov", "Urwin"]),
    # LORE target
    "barovia": ("../../../lore/strahd/", ["Barovia"]),
    "vallaki": ("../../../lore/strahd/", ["Vallaki"]),
    "krezk": ("../../../lore/strahd/", ["Krezk"]),
    "berez": ("../../../lore/strahd/", ["Berez"]),
    "castle-ravenloft": ("../../../lore/strahd/", ["Castle Ravenloft", "Ravenloft"]),
    "witchlight-carnival": ("../../../lore/strahd/", ["Witchlight Carnival"]),
    "mulino-bonegrinder": ("../../../lore/strahd/", ["Mulino di Bonegrinder"]),
    "tempio-ambra": ("../../../lore/strahd/", ["Tempio d'Ambra"]),
    "lago-zarovich": ("../../../lore/strahd/", ["Lago Zarovich"]),
    "argynvostholt": ("../../../lore/strahd/", ["Argynvostholt"]),
    "polla-di-tser": ("../../../lore/strahd/", ["Polla di Tser"]),
    "abbazia-san-markovia": ("../../../lore/strahd/", ["Abbazia di San Markovia"]),
    "yester-hill": ("../../../lore/strahd/", ["Yester Hill"]),
    "torre-van-richten": ("../../../lore/strahd/", ["Torre di Van Richten"]),
    # FAZIONI target
    "cavalieri-dargento": ("../../../fazioni/strahd/", ["Cavalieri d'Argento", "cavalieri d'argento", "Ordine cavalleresco"]),  # ordine non è unico
    "custodi-delle-piume": ("../../../fazioni/strahd/", ["Custodi delle Piume", "custodi delle piume"]),
    "vistani": ("../../../fazioni/strahd/", ["Vistani", "vistani"]),
    "chiesa-santandral": ("../../../fazioni/strahd/", ["Chiesa di Sant'Andral", "Sant'Andral"]),
    "famiglia-vallakovich": ("../../../fazioni/strahd/", ["Famiglia Vallakovich", "famiglia Vallakovich"]),
    "famiglia-wachter": ("../../../fazioni/strahd/", ["Famiglia Wachter", "famiglia Wachter"]),
    "druidi-collina-selvaggia": ("../../../fazioni/strahd/", ["Druidi della Collina Selvaggia"]),
    "streghe-di-ravenloft": ("../../../fazioni/strahd/", ["Streghe di Ravenloft"]),
    "megere-di-bonegrinder": ("../../../fazioni/strahd/", ["Megere di Bonegrinder", "megere"]),
}

def esc(s):
    return re.escape(s)

def is_already_linked(text, pos, name):
    """Controlla se a pos c'è già un link markdown o [[]]."""
    before = text[max(0,pos-2):pos]
    if '[[' in before:
        return True
    if '[' in before and pos + len(name) < len(text) and text[pos+len(name)] == ']':
        return True
    return False

def process_file(path, file_label):
    """Processa un file di riferimento."""
    filename = os.path.basename(path)
    dirpath = os.path.dirname(path)
    
    # Calcola il path relativo dal file alla root
    # png/strahd/ → ../../
    # sessioni/strahd/ → ../../
    depth = len(dirpath.replace(BASE, '').strip('/').split('/'))
    if depth == 0:
        to_root = "./"
    else:
        to_root = "../" * depth
    
    with open(path, encoding="utf-8") as f:
        text = f.read()
    
    original = text
    changes = []
    
    # Per ogni entità, cerca la prima menzione non linkata
    for ancora, (target_path, patterns) in ENTITIES.items():
        # Calcola path relativo dal file all'ancora
        # target_path è dalla root, to_root è dalla root al file
        # Quindi da file a target: to_root rimuove depth, target_path aggiunge
        # Se file è in png/strahd/ e target è ../../../lore/strahd/:
        # to_root = ../../ (arriva a root), target_path = ../../../lore/strahd/ (parte da root)
        # Ma poiché target_path è già relativo a root, e to_root parte dal file:
        # path rel = to_root + target_path.replace('../../../', '')
        # Più semplice: costruisco il path relativo dalla directory del file
        
        # Entrambi sono dalla root: ../../
        # Se il file è in png/strahd/ (depth=2), to_root = ../../
        # devo arrivare a root, poi alla target
        # Quindi: to_root + target_path.replace('../../../', '')
        # target_path è ../../../lore/strahd/ → diventa lore/strahd/
        rel_path = to_root + target_path.replace('../../../', '')
        
        for pattern in patterns:
            # Cerca con word boundary
            rx = re.compile(r'(?<!\w)(' + esc(pattern) + r')(?!\w)')
            for m in rx.finditer(text):
                pos = m.start()
                name = m.group(1)
                
                # Salta se già linkato
                if is_already_linked(text, pos, name):
                    continue
                
                # Salta se in intestazione (###)
                line_start = text.rfind('\n', 0, pos) + 1
                line_prefix = text[line_start:pos].strip()
                if line_prefix.startswith('#'):
                    continue
                
                # Salta se in blockquote
                if line_prefix.startswith('>'):
                    continue
                
                # Salta se è il titolo della sezione stessa (es. "### Strahd" → non linkare)
                after_header = text[line_start:pos+len(name)]
                if after_header.startswith('###') and pattern in after_header:
                    continue
                
                # Prima occorrenza valida → linkala
                link = f"[{name}](<{rel_path}#{ancora}>)"
                text = text[:pos] + link + text[pos+len(name):]
                changes.append(f"  {name} → {rel_path}#{ancora}")
                break  # passa all'ancora successiva
            if changes and changes[-1].startswith(f"  {pattern}"):
                break
    
    if text != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return changes
    return []

# Processa le tre pagine di riferimento
ref_files = [
    os.path.join(BASE, "png/strahd/index.md"),
    os.path.join(BASE, "lore/strahd/index.md"),
    os.path.join(BASE, "fazioni/strahd/index.md"),
]

total = 0
for path in ref_files:
    label = os.path.relpath(path, BASE)
    changes = process_file(path, label)
    if changes:
        print(f"=== {label} ===")
        for c in changes:
            print(c)
        total += len(changes)
        print()

print(f"Totale link aggiunti nelle pagine di riferimento: {total}")