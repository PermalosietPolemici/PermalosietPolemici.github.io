#!/usr/bin/env python3
"""
Script per creare pagine individuali PNG, Fazioni e Lore di Strahd,
e aggiungere [[wikilink]] alla prima menzione per capitolo.
"""

import os
import re
import glob

DOCS = "/home/federico/volos-guide-to-pp/docs"
CHAPTERS_DIR = f"{DOCS}/sessioni/strahd"

# ─── ENTITY DEFINITIONS ───────────────────────────────────────────────────────

PNG = [
    ("Strahd", "strahd-von-zarovich", "Strahd von Zarovich", "Il Conte vampiro, signore indiscusso di Barovia.", "png/strahd"),
    ("Ireena", "ireena-kolyana", "Ireena Kolyana", "La giovane dal destino segnato, reincarnazione di Tatyana.", "png/strahd"),
    ("Ismark", "ismark-kolyanovich", "Ismark Kolyanovich", "Figlio del borgomastro di Barovia, detto \"il Grande\".", "png/strahd"),
    ("Madam Eva", "madam-eva", "Madam Eva", "Misteriosa veggente Vistani, sorellastra di Strahd.", "png/strahd"),
    ("Van Richten", "van-richten", "Rudolph van Richten", "Leggendario cacciatore di vampiri.", "png/strahd"),
    ("Ezmeralda", "ezmeralda", "Ezmeralda d'Avenir", "Cacciatrice di vampiri mezz'elfa, ex allieva di Van Richten.", "png/strahd"),
    ("Baba Lysaga", "baba-lysaga", "Baba Lysaga", "Strega antica di Berez, nutrice di Strahd.", "png/strahd"),
    ("Kasimir", "kasimir-velikov", "Kasimir Velikov", "Elfo drow anziano, cerca vendetta contro Strahd.", "png/strahd"),
    ("Vladimir", "vladimir-horngaard", "Vladimir Horngaard", "Cavaliere spettrale, comandante dei Cavalieri d'Argento.", "png/strahd"),
    ("Vargas Vallakovich", "vargas-vallakovich", "Vargas Vallakovich", "Borgomastro di Vallaki.", "png/strahd"),
    ("Victor Vallakovich", "victor-vallakovich", "Victor Vallakovich", "Figlio del barone, mago in erba.", "png/strahd"),
    ("Fiona Watcher", "fiona-watcher", "Dame Fiona Wachter", "Nobildonna di Vallaki, devota a Strahd.", "png/strahd"),
    ("Padre Lucian", "padre-lucian", "Padre Lucian Petrovich", "Il prete di Vallaki.", "png/strahd"),
    ("Danika", "danika-martikov", "Danika Martikov", "Locandiera della Blue Water Inn, Custode delle Piume.", "png/strahd"),
    ("Urwin Martikov", "urwin-martikov", "Urwin Martikov", "Proprietario del Gatto Morto, Custode delle Piume.", "png/strahd"),
    ("Izek", "izek-strazni", "Izek Strazni", "Capitano della guardia di Vallaki.", "png/strahd"),
    ("Rictavio", "rictavio", "Rictavio", "Bardo misterioso, Van Richten sotto copertura.", "png/strahd"),
    ("Henrik", "henrik", "Henrik", "Il becchino di Vallaki.", "png/strahd"),
    ("Bluto", "bluto", "Bluto", "Pescatore ubriaco di Krezk.", "png/strahd"),
    ("Dimitri Krezkov", "dimitri-krezkov", "Dimitri Krezkov", "Borgomastro di Krezk.", "png/strahd"),
    ("L'Abbate", "abbate", "L'Abbate", "Custode dell'Abbazia di San Markovia.", "png/strahd"),
    ("Odjek", "odjek", "Odjek", "Cacciatore di Krezk, innamorato di Yana.", "png/strahd"),
    ("Davian Martikov", "davian-martikov", "Davian Martikov", "Patriarca dei Martikov, vignaiolo.", "png/strahd"),
    ("Muriel", "muriel-vinshaw", "Muriel Vinshaw", "Corvo mannaro, Custode delle Piume.", "png/strahd"),
    ("Luvash", "luvash", "Luvash", "Capo del campo Vistani alla Polla di Tser.", "png/strahd"),
    ("Arrigal", "arrigal", "Arrigal", "Fratello di Luvash, assassino Vistano.", "png/strahd"),
    ("Arabelle", "arabelle", "Arabelle", "Figlia di Luvash, salvata dalle acque del Lago Zarovich.", "png/strahd"),
    ("Sir Godfrey", "sir-godfrey", "Sir Godfrey Gwilym", "Ex capitano dei cavalieri d'argento.", "png/strahd"),
    ("Exethanter", "exethanter", "Exethanter", "Lich decaduto del Tempio d'Ambra.", "png/strahd"),
    ("Neferon", "neferon", "Neferon", "Arcilich che veglia sul Tempio d'Ambra.", "png/strahd"),
    ("Rahadin", "rahadin", "Rahadin", "Ciambellano di Strahd.", "png/strahd"),
    ("Escher", "escher", "Escher", "Vampiro, servitore di Strahd.", "png/strahd"),
    ("Ludmilla", "ludmilla", "Ludmilla", "Sposa di Strahd.", "png/strahd"),
    ("Anastrasya", "anastrasya", "Anastrasya", "Sposa di Strahd.", "png/strahd"),
    ("Volenta", "volenta", "Volenta", "Sposa di Strahd, sadica.", "png/strahd"),
    ("Gertruda", "gertruda", "Gertruda", "Figlia di Mary, ospite a Castle Ravenloft.", "png/strahd"),
    ("Xenia", "xenia", "Xenia", "Acrobata del Witchlight Carnival.", "png/strahd"),
    ("Morgantha", "morgantha", "Morgantha", "Strega del Mulino di Bonegrinder.", "png/strahd"),
    ("Vasili Von Holtz", "vasili-von-holtz", "Vasili Von Holtz", "Misterioso mercante.", "png/strahd"),
    ("Sarek", "sarek", "Sarek", "Nipote di Kasimir.", "png/strahd"),
    ("Helga", "helga", "Helga", "Cameriera di Castle Ravenloft.", "png/strahd"),
    ("Rina", "rina", "Rina", "Strega napoletana.", "png/strahd"),
    ("Gnemo", "gnemo", "Gnemo", "Compagno del gruppo.", "png/strahd"),
    ("Donavich", "donavich", "Padre Donavich", "Sacerdote della chiesa di Barovia.", "png/strahd"),
    ("Doru", "doru", "Doru", "Figlio di Donavich, vampiro.", "png/strahd"),
    ("Naso", "naso", "Naso", "Agente teatrale del Witchlight Carnival.", "png/strahd"),
    ("Maddok", "maddok", "Maddok", "Kenku medico del circo.", "png/strahd"),
]

FAZIONI = [
    ("Custodi delle Piume", "custodi-delle-piume", "I Custodi delle Piume", "Rete di spie di corvi mannari.", "fazioni/strahd"),
    ("Cavalieri d'Argento", "cavalieri-dargento", "I Cavalieri d'Argento", "Ordine cavalleresco un tempo devoto a proteggere Barovia.", "fazioni/strahd"),
    ("Vistani", "vistani", "I Vistani", "Popolo nomade, viaggiatori tra i piani.", "fazioni/strahd"),
    ("Chiesa di Sant'Andral", "chiesa-santandral", "La Chiesa di Sant'Andral", "Chiesa di Vallaki, protettore contro il vampirismo.", "fazioni/strahd"),
    ("Famiglia Vallakovich", "famiglia-vallakovich", "La Famiglia Vallakovich", "Casata regnante di Vallaki.", "fazioni/strahd"),
    ("Famiglia Wachter", "famiglia-wachter", "La Famiglia Wachter", "Nobile famiglia rivale dei Vallakovich.", "fazioni/strahd"),
    ("Druidi della Collina Selvaggia", "druidi-collina-selvaggia", "I Druidi della Collina Selvaggia", "Druidi che venerano il Tempio d'Ambra.", "fazioni/strahd"),
    ("Streghe di Ravenloft", "streghe-di-ravenloft", "Le Streghe di Ravenloft", "Tre streghe al servizio di Strahd.", "fazioni/strahd"),
    ("Megere di Bonegrinder", "megere-di-bonegrinder", "Le Megere di Bonegrinder", "Streghe notturne al Mulino di Bonegrinder.", "fazioni/strahd"),
]

LORE = [
    ("Barovia", "barovia", "Barovia", "Dominio della Nebbia, la valle maledetta di Strahd.", "lore/strahd"),
    ("Castle Ravenloft", "castle-ravenloft", "Castle Ravenloft", "Fortezza di Strahd, labirinto di torri e cripte.", "lore/strahd"),
    ("Tempio d'Ambra", "tempio-ambra", "Il Tempio d'Ambra", "Antica fortezza dove sono imprigionate le Vestigia.", "lore/strahd"),
    ("Argynvostholt", "argynvostholt", "Argynvostholt", "Magione dei Cavalieri d'Argento.", "lore/strahd"),
    ("Polla di Tser", "polla-di-tser", "La Polla di Tser", "Accampamento Vistani di Madam Eva.", "lore/strahd"),
    ("Yester Hill", "yester-hill", "Yester Hill", "Collina sacra ai druidi.", "lore/strahd"),
    ("Berez", "berez", "Berez", "Villaggio sommerso dalla palude, covo di Baba Lysaga.", "lore/strahd"),
    ("Krezk", "krezk", "Krezk", "Insediamento occidentale di Barovia con l'Abbazia.", "lore/strahd"),
    ("Mulino di Bonegrinder", "mulino-bonegrinder", "Il Mulino di Bonegrinder", "Covo delle megere.", "lore/strahd"),
    ("Vallaki", "vallaki", "Vallaki", "Città più vivace di Barovia, governata dal barone Vallakovich.", "lore/strahd"),
    ("Torre di Van Richten", "torre-van-richten", "La Torre di Van Richten", "Rifugio e laboratorio di Van Richten.", "lore/strahd"),
    ("Abbazia di San Markovia", "abbazia-san-markovia", "L'Abbazia di San Markovia", "Luogo sacro caduto in mani oscure.", "lore/strahd"),
    ("Lago Zarovich", "lago-zarovich", "Il Lago Zarovich", "Gigantesco lago di Barovia.", "lore/strahd"),
    ("Witchlight Carnival", "witchlight-carnival", "Il Witchlight Carnival", "Circo itinerante da cui provengono i PG.", "lore/strahd"),
]

def create_page_file(category_dir, filename, title, description):
    """Create an individual page file for an entity."""
    path = f"{DOCS}/{category_dir}/{filename}.md"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    content = f"""# {title}

{description}

---

*[Torna all'indice](/{category_dir}/)*
"""
    with open(path, "w") as f:
        f.write(content)
    return path

def create_all_pages():
    """Create all individual entity pages."""
    created = []
    for name, filename, title, desc, cat_dir in PNG:
        path = create_page_file(cat_dir, filename, title, desc)
        created.append((name, filename, cat_dir))
    for name, filename, title, desc, cat_dir in FAZIONI:
        path = create_page_file(cat_dir, filename, title, desc)
        created.append((name, filename, cat_dir))
    for name, filename, title, desc, cat_dir in LORE:
        path = create_page_file(cat_dir, filename, title, desc)
        created.append((name, filename, cat_dir))
    return created

def add_first_mention_links(chapter_path, entity_names):
    """
    Process a chapter file: add [[wikilink]] at first mention of each entity.
    Only the first occurrence in the entire chapter gets linked.
    """
    with open(chapter_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    modified = False
    seen = set()
    
    # We need to find the first occurrence of each name across the whole file
    # Build a list of (line_index, position, name) for all candidate matches
    candidates = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Skip code blocks, headers, blockquotes 
        if stripped.startswith('```') or stripped.startswith('#') or stripped.startswith('>'):
            continue
        for name in entity_names:
            if name in seen:
                continue
            # Skip if already has a wikilink
            if f'[[{name}]]' in line:
                seen.add(name)
                continue
            # Find standalone occurrence (not inside [[...]] already)
            pattern = r'(?<!\[)\b' + re.escape(name) + r'\b(?!\])'
            for m in re.finditer(pattern, line):
                candidates.append((i, m.start(), name, m))
                break  # Only first occurrence per line per name
    
    # Sort by line, then position
    candidates.sort(key=lambda x: (x[0], x[1]))
    
    # Apply first occurrence for each name
    seen.clear()
    for line_idx, pos, name, match in candidates:
        if name in seen:
            continue
        seen.add(name)
        line = lines[line_idx]
        lines[line_idx] = line[:match.start()] + f'[[{name}]]' + line[match.end():]
        modified = True
    
    if modified:
        content = '\n'.join(lines)
        with open(chapter_path, 'w') as f:
            f.write(content)
        return True, seen
    return False, set()

def main():
    print("=== Creazione pagine individuali ===")
    created = create_all_pages()
    print(f"Create {len(created)} pagine individuali")
    
    # Build entity list sorted by length (longest first for greedy matching)
    all_entities = PNG + FAZIONI + LORE
    entity_names = sorted([e[0] for e in all_entities], key=len, reverse=True)
    
    print("\n=== Aggiunta wikilink ai capitoli ===")
    chapters = sorted(glob.glob(f"{CHAPTERS_DIR}/*.md"))
    for ch in chapters:
        basename = os.path.basename(ch)
        if basename == "index.md":
            continue
        result, linked = add_first_mention_links(ch, entity_names)
        linked_str = ', '.join(sorted(linked)) if linked else '—'
        print(f"  {basename}: {'✓' if result else '—'} ({len(linked)} link: {linked_str})")
    
    print("\n=== Fatto! ===")

if __name__ == "__main__":
    main()