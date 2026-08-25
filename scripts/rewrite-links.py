#!/usr/bin/env python3
"""
Rewrite png/strahd/index.md, fazioni/strahd/index.md, lore/strahd/index.md
with ### heading sections + anchors + cross-links.
Add first-mention links in all 22 chapters with CORRECT relative paths.
"""

import os, re, glob

DOCS = "/home/federico/volos-guide-to-pp/docs"
CH_DIR = f"{DOCS}/sessioni/strahd"

# (name, display_name, anchor, desc, [(ref_name, rel_path)])
# rel_path: "" = same page, otherwise absolute category path from root
# e.g. from png/strahd/ to fazioni/strahd/ = "../../fazioni/strahd/"
# from chapter sessioni/strahd/X/ to png/strahd/ = "../../../png/strahd/"

PNG = [
 ("Strahd","Strahd von Zarovich","strahd-von-zarovich","Il Conte vampiro, signore indiscusso di Barovia. Elegante, crudele, immortale.",
  [("Barovia","../../lore/strahd/"),("Ireena",""),("Castle Ravenloft","../../lore/strahd/"),("Tatiana","")]),
 ("Ireena","Ireena Kolyana","ireena-kolyana","La giovane dal destino segnato, reincarnazione di Tatyana. Oggetto dell'ossessione di Strahd.",
  [("Strahd",""),("Ismark",""),("Barovia","../../lore/strahd/")]),
 ("Tatiana","Tatyana","tatyana","L'amata perduta di Strahd, reincarnata in Ireena. La sua morte ha scatenato la maledizione del Conte.",
  [("Ireena",""),("Strahd",""),("Sergei","")]),
 ("Sergei","Sergei von Zarovich","sergei","Fratello di Strahd, ucciso dal Conte per gelosia. La sua anima è legata alla Sunsword.",
  [("Strahd",""),("Ireena",""),("Tatiana","")]),
 ("Ismark","Ismark Kolyanovich","ismark","Figlio del borgomastro di Barovia, detto \"il Grande\". Nuovo borgomastro dopo la morte del padre.",
  [("Ireena",""),("Barovia","../../lore/strahd/")]),
 ("Madam Eva","Madam Eva","madam-eva","Misteriosa veggente Vistani, sorellastra di Strahd. Ha letto le carte del destino ai personaggi.",
  [("Strahd",""),("Vistani","../../fazioni/strahd/"),("Polla di Tser","../../lore/strahd/")]),
 ("Van Richten","Rudolph van Richten","van-richten","Leggendario cacciatore di vampiri. Invecchiato, segnato da tragedie, ma letale. Sotto copertura come Rictavio.",
  [("Rictavio",""),("Ezmeralda",""),("Barovia","../../lore/strahd/")]),
 ("Rictavio","Rictavio","rictavio","Misterioso bardo mezz'elfo con un carro da circo. In realtà Van Richten sotto copertura.",
  [("Van Richten",""),("Ezmeralda","")]),
 ("Ezmeralda","Ezmeralda d'Avenir","ezmeralda","Cacciatrice di vampiri mezz'elfa, ex allieva di Van Richten. Determinata e coraggiosa.",
  [("Van Richten",""),("Rahadin",""),("Torre di Van Richten","../../lore/strahd/")]),
 ("Baba Lysaga","Baba Lysaga","baba-lysaga","Strega antica di Berez, nutrice di Strahd. Vive in una casa sulla gamba di gallina nella palude.",
  [("Strahd",""),("Berez","../../lore/strahd/")]),
 ("Kasimir","Kasimir Velikov","kasimir","Elfo drow anziano, cerca vendetta contro Strahd per aver ucciso sua sorella Patrina. Diventa Sir Kasimir, cavaliere d'argento.",
  [("Strahd",""),("Cavalieri d'Argento","../../fazioni/strahd/"),("Sarek","")]),
 ("Vladimir","Vladimir Horngaard","vladimir","Cavaliere spettrale, comandante dei Cavalieri d'Argento caduti. Guardiano di Argynvostholt, consumato dall'odio.",
  [("Cavalieri d'Argento","../../fazioni/strahd/"),("Argynvostholt","../../lore/strahd/"),("Sir Godfrey","")]),
 ("Sir Godfrey","Sir Godfrey Gwilym","sir-godfrey","Ex capitano dei cavalieri d'argento, tra i pochi ancora legati alla luce.",
  [("Vladimir",""),("Cavalieri d'Argento","../../fazioni/strahd/"),("Argynvostholt","../../lore/strahd/")]),
 ("Vargas Vallakovich","Vargas Vallakovich","vargas-vallakovich","Borgomastro di Vallaki. Convinto che il buonumore forzato tenga lontana la nebbia.",
  [("Vallaki","../../lore/strahd/"),("Izek",""),("Victor Vallakovich",""),("Famiglia Vallakovich","../../fazioni/strahd/")]),
 ("Victor Vallakovich","Victor Vallakovich","victor-vallakovich","Figlio del barone, mago in erba. Tortura Randal con esperimenti magici.",
  [("Vargas Vallakovich",""),("Vallaki","../../lore/strahd/")]),
 ("Fiona Watcher","Dame Fiona Wachter","fiona-watcher","Nobildonna di Vallaki, devota a Strahd. Guida una fazione segreta. Prende il potere dopo la rivolta.",
  [("Strahd",""),("Vallaki","../../lore/strahd/"),("Famiglia Wachter","../../fazioni/strahd/")]),
 ("Padre Lucian","Padre Lucian Petrovich","padre-lucian","Il prete di Vallaki, custode delle ossa di Sant'Andral.",
  [("Vallaki","../../lore/strahd/"),("Chiesa di Sant'Andral","../../fazioni/strahd/")]),
 ("Danika","Danika Martikov","danika-martikov","Locandiera della Blue Water Inn, membro dei Custodi delle Piume.",
  [("Custodi delle Piume","../../fazioni/strahd/"),("Urwin Martikov",""),("Vallaki","../../lore/strahd/")]),
 ("Urwin Martikov","Urwin Martikov","urwin-martikov","Proprietario del Gatto Morto, membro dei Custodi delle Piume.",
  [("Danika",""),("Custodi delle Piume","../../fazioni/strahd/"),("Vallaki","../../lore/strahd/")]),
 ("Izek","Izek Strazni","izek","Capitano della guardia di Vallaki. Braccio demoniaco deforme. Muore e rinasce come Sir Kasimir.",
  [("Vallaki","../../lore/strahd/"),("Vargas Vallakovich",""),("Kasimir","")]),
 ("Henrik","Henrik","henrik","Il becchino di Vallaki. Corrotto da una donna in rosso, nasconde vampiri nelle bare.",
  [("Vallaki","../../lore/strahd/")]),
 ("Bluto","Bluto","bluto","Pescatore ubriaco di Krezk, disposto a tutto per compiacere Strahd.",
  [("Krezk","../../lore/strahd/"),("Strahd","")]),
 ("Dimitri Krezkov","Dimitri Krezkov","dimitri-krezkov","Borgomastro di Krezk, uomo austero ma giusto.",
  [("Krezk","../../lore/strahd/")]),
 ("L'Abbate","L'Abbate","abbate","Enigmatico custode dell'Abbazia di San Markovia. Angelo del Signore del Mattino, ossessionato dalla perfezione.",
  [("Abbazia di San Markovia","../../lore/strahd/"),("Strahd",""),("Krezk","../../lore/strahd/")]),
 ("Odjek","Odjek","odjek","Cacciatore di Krezk, innamorato di Yana.",
  [("Krezk","../../lore/strahd/")]),
 ("Davian Martikov","Davian Martikov","davian-martikov","Patriarca dei Martikov, gestore del Vigneto del Mago dei Vini.",
  [("Custodi delle Piume","../../fazioni/strahd/"),("Danika",""),("Urwin Martikov","")]),
 ("Muriel","Muriel Vinshaw","muriel","Corvo mannaro, membro dei Custodi delle Piume. Salva Randal al Lago Zarovich.",
  [("Custodi delle Piume","../../fazioni/strahd/"),("Lago Zarovich","../../lore/strahd/")]),
 ("Luvash","Luvash","luvash","Capo del campo Vistani alla Polla di Tser. Padre di Arabelle.",
  [("Vistani","../../fazioni/strahd/"),("Arabelle",""),("Polla di Tser","../../lore/strahd/")]),
 ("Arrigal","Arrigal","arrigal","Fratello di Luvash, abile assassino e spia Vistana.",
  [("Vistani","../../fazioni/strahd/"),("Luvash","")]),
 ("Arabelle","Arabelle","arabelle","Giovane figlia di Luvash, salvata dalle acque del Lago Zarovich.",
  [("Luvash",""),("Lago Zarovich","../../lore/strahd/")]),
 ("Rahadin","Rahadin","rahadin","Ciambellano di Strahd, elfo dalla pelle scura. Elegante, sinistro, impeccabile.",
  [("Strahd",""),("Castle Ravenloft","../../lore/strahd/")]),
 ("Escher","Escher","escher","Vampiro, consorte e servitore di Strahd. Sconfitto nel Tempio d'Ambra.",
  [("Strahd",""),("Castle Ravenloft","../../lore/strahd/"),("Tempio d'Ambra","../../lore/strahd/")]),
 ("Ludmilla","Ludmilla","ludmilla","Sposa di Strahd, elegante e composta.",
  [("Strahd",""),("Castle Ravenloft","../../lore/strahd/")]),
 ("Anastrasya","Anastrasya","anastrasya","Sposa di Strahd, bellissima e provocatrice. Guida l'attacco alla chiesa di Vallaki.",
  [("Strahd",""),("Vallaki","../../lore/strahd/"),("Yester Hill","../../lore/strahd/")]),
 ("Volenta","Volenta","volenta","Sposa di Strahd, minuta come una ragazzina, sadica.",
  [("Strahd",""),("Castle Ravenloft","../../lore/strahd/")]),
 ("Gertruda","Gertruda","gertruda","Figlia di Mary, la donna piangente di Barovia. Ospite a Castle Ravenloft.",
  [("Castle Ravenloft","../../lore/strahd/"),("Laszlo","")]),
 ("Xenia","Xenia","xenia","Acrobata del Witchlight Carnival, ex-PG diventata PNG. Rivaleggia con Luth.",
  [("Witchlight Carnival","../../lore/strahd/"),("Castle Ravenloft","../../lore/strahd/")]),
 ("Morgantha","Morgantha","morgantha","La vecchia del Mulino di Bonegrinder, strega notturna (night hag).",
  [("Mulino di Bonegrinder","../../lore/strahd/"),("Megere di Bonegrinder","../../fazioni/strahd/")]),
 ("Vasili Von Holtz","Vasili Von Holtz","vasili-von-holtz","Misterioso mercante gentile. Nessuno sa dove abiti.",
  [("Vallaki","../../lore/strahd/")]),
 ("Sarek","Sarek","sarek","Nipote di Kasimir. Giura di combattere Strahd.",
  [("Kasimir",""),("Strahd",""),("Yester Hill","../../lore/strahd/")]),
 ("Helga","Helga","helga","Cameriera di Castle Ravenloft. Lascia un biglietto a Nezuko.",
  [("Castle Ravenloft","../../lore/strahd/")]),
 ("Rina","Rina","rina","Strega napoletana che aiuta Nezuko nel Tempio d'Ambra.",
  [("Tempio d'Ambra","../../lore/strahd/")]),
 ("Gnemo","Gnemo","gnemo","Compagno del gruppo. Sopravvive all'assalto finale.",
  [("Strahd",""),("Castle Ravenloft","../../lore/strahd/")]),
 ("Donavich","Padre Donavich","donavich","Sacerdote della chiesa di Barovia. Ha nutrito suo figlio vampiro con la carne degli abitanti.",
  [("Doru",""),("Barovia","../../lore/strahd/")]),
 ("Doru","Doru","doru","Figlio di Donavich, trasformato in vampiro. Il primo scomparso di Barovia.",
  [("Donavich",""),("Barovia","../../lore/strahd/")]),
 ("Naso","Naso","naso","Agente teatrale del Witchlight Carnival. Tyrannico ma efficace.",
  [("Witchlight Carnival","../../lore/strahd/")]),
 ("Maddok","Maddok","maddok","Kenku medico del Witchlight Carnival. Comunica scrivendo su una lavagnetta.",
  [("Witchlight Carnival","../../lore/strahd/")]),
]

FAZIONI = [
 ("Custodi delle Piume","I Custodi delle Piume","custodi-delle-piume","Rete di spie di corvi mannari. Operano nell'ombra per proteggere Barovia. Guidati dalla famiglia Martikov.",
  [("Danika","../../png/strahd/"),("Davian Martikov","../../png/strahd/"),("Muriel","../../png/strahd/"),("Barovia","../../lore/strahd/")]),
 ("Cavalieri d'Argento","I Cavalieri d'Argento","cavalieri-dargento","Ordine cavalleresco devoto alla protezione di Barovia. Guidati da Sir Vladimir Horngaard, giurarono fedeltà al drago Argynvost.",
  [("Vladimir","../../png/strahd/"),("Sir Godfrey","../../png/strahd/"),("Argynvostholt","../../lore/strahd/")]),
 ("Vistani","I Vistani","vistani","Popolo nomade, viaggiatori tra i piani. Unici a poter entrare e uscire da Barovia. Legati a Strahd da un patto antico.",
  [("Madam Eva","../../png/strahd/"),("Luvash","../../png/strahd/"),("Polla di Tser","../../lore/strahd/"),("Strahd","../../png/strahd/")]),
 ("Chiesa di Sant'Andral","La Chiesa di Sant'Andral","chiesa-santandral","Chiesa di Vallaki, dedicata a Sant'Andral, protettore contro il vampirismo.",
  [("Padre Lucian","../../png/strahd/"),("Vallaki","../../lore/strahd/")]),
 ("Famiglia Vallakovich","La Famiglia Vallakovich","famiglia-vallakovich","Casata regnante di Vallaki. Il barone Vargas governa col terrore e i festival forzati.",
  [("Vargas Vallakovich","../../png/strahd/"),("Victor Vallakovich","../../png/strahd/"),("Vallaki","../../lore/strahd/")]),
 ("Famiglia Wachter","La Famiglia Wachter","famiglia-wachter","Nobile famiglia rivale dei Vallakovich. Dame Fiona guida una setta segreta di Strahd.",
  [("Fiona Watcher","../../png/strahd/"),("Vallaki","../../lore/strahd/")]),
 ("Druidi della Collina Selvaggia","I Druidi della Collina Selvaggia","druidi-collina-selvaggia","Druidi che venerano il Tempio d'Ambra e le sue vestigia oscure. Guidano rituali a Yester Hill.",
  [("Yester Hill","../../lore/strahd/"),("Tempio d'Ambra","../../lore/strahd/")]),
 ("Streghe di Ravenloft","Le Streghe di Ravenloft","streghe-di-ravenloft","Tre streghe al servizio diretto di Strahd a Castle Ravenloft.",
  [("Castle Ravenloft","../../lore/strahd/")]),
 ("Megere di Bonegrinder","Le Megere di Bonegrinder","megere-di-bonegrinder","Tre streghe notturne (night hags) al Mulino di Bonegrinder. Trasformano bambini in pasticcini magici.",
  [("Morgantha","../../png/strahd/"),("Mulino di Bonegrinder","../../lore/strahd/")]),
]

LORE = [
 ("Barovia","Barovia","barovia","Dominio della Nebbia, terra strappata dal suo piano. Divisa in tre insediamenti: il Villaggio di Barovia, Vallaki e Krezk.",
  [("Strahd","../../png/strahd/"),("Vallaki",""),("Krezk",""),("Castle Ravenloft","")]),
 ("Castle Ravenloft","Castle Ravenloft","castle-ravenloft","Fortezza di Strahd su un picco di roccia. Labirinto di torri, cripte e sale da ballo. Al suo cuore pulsa il Cuore del Dolore.",
  [("Strahd","../../png/strahd/"),("Barovia",""),("Rahadin","../../png/strahd/")]),
 ("Tempio d'Ambra","Il Tempio d'Ambra","tempio-ambra","Antica fortezza dove sono imprigionate le Vestigia, esseri oscuri e potenti.",
  [("Barovia",""),("Exethanter","../../png/strahd/"),("Neferon","../../png/strahd/")]),
 ("Argynvostholt","Argynvostholt","argynvostholt","Magione dei Cavalieri d'Argento, dove riposa l'anima del drago Argynvost. Il suo faro si riaccende quando il teschio viene restituito.",
  [("Cavalieri d'Argento","../../fazioni/strahd/"),("Vladimir","../../png/strahd/"),("Sir Godfrey","../../png/strahd/")]),
 ("Polla di Tser","La Polla di Tser","polla-di-tser","Accampamento Vistani dove Madam Eva legge le carte del destino.",
  [("Madam Eva","../../png/strahd/"),("Vistani","../../fazioni/strahd/")]),
 ("Yester Hill","Yester Hill","yester-hill","Collina sacra ai druidi. Qui Strahd punisce Anastrasya, Sarek e Kasimir.",
  [("Druidi della Collina Selvaggia","../../fazioni/strahd/"),("Strahd","../../png/strahd/")]),
 ("Berez","Berez","berez","Villaggio sommerso dalla palude. Covo di Baba Lysaga.",
  [("Baba Lysaga","../../png/strahd/")]),
 ("Krezk","Krezk","krezk","Insediamento più occidentale di Barovia, arroccato su una collina. Oltre le mura sorge l'Abbazia di San Markovia.",
  [("Dimitri Krezkov","../../png/strahd/"),("Abbazia di San Markovia",""),("Barovia","")]),
 ("Abbazia di San Markovia","L'Abbazia di San Markovia","abbazia-san-markovia","Un tempo luogo sacro, ora in mani oscure. L'Abbate vi conduce esperimenti raccapriccianti.",
  [("L'Abbate","../../png/strahd/"),("Krezk","")]),
 ("Mulino di Bonegrinder","Il Mulino di Bonegrinder","mulino-bonegrinder","Mulino abbandonato sulla strada per Vallaki, covo delle megere.",
  [("Megere di Bonegrinder","../../fazioni/strahd/"),("Morgantha","../../png/strahd/")]),
 ("Vallaki","Vallaki","vallaki","Città più vivace di Barovia, governata dal barone Vargas Vallakovich con pugno di ferro e festival forzati.",
  [("Vargas Vallakovich","../../png/strahd/"),("Fiona Watcher","../../png/strahd/"),("Chiesa di Sant'Andral","../../fazioni/strahd/"),("Barovia","")]),
 ("Torre di Van Richten","La Torre di Van Richten","torre-van-richten","Torre sul Lago Baratok, rifugio di Van Richten. Protetta da gargoyle e fulmini magici.",
  [("Van Richten","../../png/strahd/"),("Ezmeralda","../../png/strahd/")]),
 ("Lago Zarovich","Il Lago Zarovich","lago-zarovich","Gigantesco lago di Barovia con un'isoletta. Qui Arabelle viene salvata dalle acque.",
  [("Arabelle","../../png/strahd/"),("Muriel","../../png/strahd/")]),
 ("Witchlight Carnival","Il Witchlight Carnival","witchlight-carnival","Circo itinerante da cui provengono i PG. Punto di partenza dell'avventura.",
  [("Naso","../../png/strahd/"),("Maddok","../../png/strahd/"),("Xenia","../../png/strahd/")]),
]

# Build master name map
# name -> (rel_path_from_chapter, anchor, cross_refs_list)
MASTER = {}
for cat, entries in [("png", PNG), ("fazioni", FAZIONI), ("lore", LORE)]:
    for e in entries:
        # From chapters: ../../../cat/strahd/
        MASTER[e[0]] = (f"../../../{cat}/strahd/", e[2], e[1], e[3], e[4])

SORTED_NAMES = sorted(MASTER.keys(), key=lambda n: -len(n))

def make_link(name, path, anchor):
    return f"[{name}](<{path}#{anchor}>)"

# ── STEP 1: WRITE REFERENCE PAGES WITH CORRECT CROSS-LINKS ──────────────
def write_page(cat, entries, title, subtitle):
    path = f"{DOCS}/{cat}/strahd/index.md"
    # Build entity map by name -> anchor
    emap = {e[0]: e[2] for e in entries}
    
    lines = [f"# {title}\n", f"{subtitle}\n", "---\n"]
    for name, display, anchor, desc, xrefs in entries:
        d = desc
        for rn, rp in xrefs:
            if rn in emap:
                # Same-page link: #anchor
                ra = emap[rn]
                repl = f"[{rn}](<#{ra}>)"
                pat = re.compile(r'(?<!\[)\b' + re.escape(rn) + r'\b(?!\])')
                d = pat.sub(repl, d, count=1)
        lines.append(f"### {display} {{#{anchor}}}\n")
        lines.append(f"{d}\n")
    lines.append("---\n")
    lines.append(f"*[Torna all'indice](/{cat}/)*\n")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  {path} ({len(entries)} sezioni)")

# ── STEP 2: PROCESS CHAPTERS ───────────────────────────────────────────
def process_chapters():
    chapters = sorted(glob.glob(f"{CH_DIR}/*.md"))
    for ch in chapters:
        bn = os.path.basename(ch)
        if bn == "index.md":
            continue
        with open(ch, "r") as f:
            content = f.read()
        
        seen = set()
        modified = False
        lines = content.split("\n")
        
        for i, line in enumerate(lines):
            s = line.strip()
            if s.startswith("```") or s.startswith("#") or s.startswith(">"):
                continue
            
            for name in SORTED_NAMES:
                if name in seen:
                    continue
                # Skip if already a wikilink
                if f"[[{name}]]" in line:
                    path, anchor, _, _, _ = MASTER[name]
                    link = make_link(name, path, anchor)
                    lines[i] = line.replace(f"[[{name}]]", link, 1)
                    seen.add(name)
                    modified = True
                    break
                # Check for standalone occurrence NOT inside [[...]]
                pat = re.compile(r'(?<!\[)\b' + re.escape(name) + r'\b(?!\])')
                m = pat.search(line)
                if m:
                    path, anchor, _, _, _ = MASTER[name]
                    link = make_link(name, path, anchor)
                    lines[i] = line[:m.start()] + link + line[m.end():]
                    seen.add(name)
                    modified = True
                    break
        
        if modified:
            content = "\n".join(lines)
            with open(ch, "w") as f:
                f.write(content)
            print(f"  {bn}: ✓ ({len(seen)} link: {', '.join(sorted(seen))})")
        else:
            print(f"  {bn}: —")

# ── MAIN ────────────────────────────────────────────────────────────────
print("=== Step 1: Riscrittura pagine di riferimento ===")
write_page("png", PNG, "PNG — Curse of Strahd",
    "I personaggi non giocanti incontrati durante l'avventura in Barovia.")
write_page("fazioni", FAZIONI, "Fazioni — Curse of Strahd",
    "Le organizzazioni e i gruppi incontrati durante l'avventura in Barovia.")
write_page("lore", LORE, "Lore — Curse of Strahd",
    "I luoghi, la storia e i segreti di Barovia.")

print("\n=== Step 2: Aggiunta link nei capitoli ===")
process_chapters()

print("\n=== Fatto! ===")