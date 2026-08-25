#!/bin/bash
# Cerca nei capitoli nomi che hanno un'ancora ma non sono linkati
# Percorso base dei capitoli
CHAPTERS_DIR="/home/federico/volos-guide-to-pp/docs/sessioni/strahd"

# Pattern per ogni entità: "nome" -> "ancora"
# Formato: nome_da_cercare|path_relativo_del_link|ancora
# L'ordine conta: match_più_lunghi prima

ENTRIES=(
  # PNG
  "Strahd von Zarovich|../../../png/strahd/|#strahd-von-zarovich"
  "Strahd|../../../png/strahd/|#strahd-von-zarovich"  
  "Ireena Kolyana|../../../png/strahd/|#ireena-kolyana"
  "Ireena|../../../png/strahd/|#ireena-kolyana"
  "Tatyana|../../../png/strahd/|#tatyana"
  "Sergei von Zarovich|../../../png/strahd/|#sergei"
  "Sergei|../../../png/strahd/|#sergei"
  "Ismark Kolyanovich|../../../png/strahd/|#ismark"
  "Ismark|../../../png/strahd/|#ismark"
  "Madam Eva|../../../png/strahd/|#madam-eva"
  "Van Richten|../../../png/strahd/|#van-richten"
  "Rictavio|../../../png/strahd/|#rictavio"
  "Ezmeralda d'Avenir|../../../png/strahd/|#ezmeralda"
  "Ezmeralda|../../../png/strahd/|#ezmeralda"
  "Baba Lysaga|../../../png/strahd/|#baba-lysaga"
  "Kasimir Velikov|../../../png/strahd/|#kasimir"
  "Kasimir|../../../png/strahd/|#kasimir"
  "Vladimir Horngaard|../../../png/strahd/|#vladimir"
  "Vladimir|../../../png/strahd/|#vladimir"
  "Sir Godfrey|../../../png/strahd/|#sir-godfrey"
  "Godfrey|../../../png/strahd/|#sir-godfrey"
  "Vargas Vallakovich|../../../png/strahd/|#vargas-vallakovich"
  "Vargas|../../../png/strahd/|#vargas-vallakovich"
  "Victor Vallakovich|../../../png/strahd/|#victor-vallakovich"
  "Victor|../../../png/strahd/|#victor-vallakovich"
  "Fiona Wachter|../../../png/strahd/|#fiona-watcher"
  "Fiona|../../../png/strahd/|#fiona-watcher"
  "Lucian|../../../png/strahd/|#padre-lucian"
  "Padre Lucian|../../../png/strahd/|#padre-lucian"
  "Danika Martikov|../../../png/strahd/|#danika-martikov"
  "Danika|../../../png/strahd/|#danika-martikov"
  "Urwin Martikov|../../../png/strahd/|#urwin-martikov"
  "Urwin|../../../png/strahd/|#urwin-martikov"
  "Izek Strazni|../../../png/strahd/|#izek"
  "Izek|../../../png/strahd/|#izek"
  "Henrik|../../../png/strahd/|#henrik"
  "Bluto|../../../png/strahd/|#bluto"
  "Dimitri Krezkov|../../../png/strahd/|#dimitri-krezkov"
  "L'Abbate|../../../png/strahd/|#abbate"
  "Abbate|../../../png/strahd/|#abbate"
  "Odjek|../../../png/strahd/|#odjek"
  "Odjek|../../../png/strahd/|#odjek"  # duplicate, won't matter
  "Davian Martikov|../../../png/strahd/|#davian-martikov"
  "Muriel Vinshaw|../../../png/strahd/|#muriel"
  "Muriel|../../../png/strahd/|#muriel"
  "Luvash|../../../png/strahd/|#luvash"
  "Arrigal|../../../png/strahd/|#arrigal"
  "Arabelle|../../../png/strahd/|#arabelle"
  "Rahadin|../../../png/strahd/|#rahadin"
  "Escher|../../../png/strahd/|#escher"
  "Ludmilla|../../../png/strahd/|#ludmilla"
  "Anastrasya|../../../png/strahd/|#anastrasya"
  "Volenta|../../../png/strahd/|#volenta"
  "Gertruda|../../../png/strahd/|#gertruda"
  "Xenia|../../../png/strahd/|#xenia"
  "Morgantha|../../../png/strahd/|#morgantha"
  "Vasili|../../../png/strahd/|#vasili-von-holtz"
  "Sarek|../../../png/strahd/|#sarek"
  "Helga|../../../png/strahd/|#helga"
  "Rina|../../../png/strahd/|#rina"
  "Gnemo|../../../png/strahd/|#gnemo"
  "Donavich|../../../png/strahd/|#donavich"
  "Padre Donavich|../../../png/strahd/|#donavich"
  "Doru|../../../png/strahd/|#doru"
  "Naso|../../../png/strahd/|#naso"
  "Maddok|../../../png/strahd/|#maddok"
  "Maddok|../../../png/strahd/|#maddok"

  # LORE
  "Barovia|../../../lore/strahd/|#barovia"
  "Castle Ravenloft|../../../lore/strahd/|#castle-ravenloft"
  "Tempio d'Ambra|../../../lore/strahd/|#tempio-ambra"
  "Argynvostholt|../../../lore/strahd/|#argynvostholt"
  "Polla di Tser|../../../lore/strahd/|#polla-di-tser"
  "Yester Hill|../../../lore/strahd/|#yester-hill"
  "Berez|../../../lore/strahd/|#berez"
  "Krezk|../../../lore/strahd/|#krezk"
  "Abbazia di San Markovia|../../../lore/strahd/|#abbazia-san-markovia"
  "Mulino di Bonegrinder|../../../lore/strahd/|#mulino-bonegrinder"
  "Bonerginder|../../../lore/strahd/|#mulino-bonegrinder"
  "Vallaki|../../../lore/strahd/|#vallaki"
  "Torre di Van Richten|../../../lore/strahd/|#torre-van-richten"
  "Lago Zarovich|../../../lore/strahd/|#lago-zarovich"
  "Witchlight Carnival|../../../lore/strahd/|#witchlight-carnival"

  # FAZIONI
  "Custodi delle Piume|../../../fazioni/strahd/|#custodi-delle-piume"
  "Cavalieri d'Argento|../../../fazioni/strahd/|#cavalieri-dargento"
  "Vistani|../../../fazioni/strahd/|#vistani"
  "Chiesa di Sant'Andral|../../../fazioni/strahd/|#chiesa-santandral"
  "Famiglia Vallakovich|../../../fazioni/strahd/|#famiglia-vallakovich"
  "Famiglia Wachter|../../../fazioni/strahd/|#famiglia-wachter"
  "Druidi della Collina Selvaggia|../../../fazioni/strahd/|#druidi-collina-selvaggia"
  "Streghe di Ravenloft|../../../fazioni/strahd/|#streghe-di-ravenloft"
  "Megere di Bonegrinder|../../../fazioni/strahd/|#megere-di-bonegrinder"
)

# Crea pattern di link per escludere quelli già linkati
# Il link sarebbe: [Nome](<../../../.../#anchor>)

check_chapter() {
  local file="$1"
  local chapter=$(basename "$file" .md)
  local found=0

  for entry in "${ENTRIES[@]}"; do
    IFS='|' read -r name link_path anchor <<< "$entry"

    # Crea il pattern del link completo per escluderlo
    # Escape per grep: [ e ] e ( e ) sono speciali
    local link_pattern="\\[$name\\]\\(<$link_path$anchor\\)"

    # Trova occorrenze del nome NON linkate
    # Usa grep -P per lookahead negativi
    while IFS= read -r line; do
      # Estrai numero riga
      local lineno=$(echo "$line" | cut -d: -f1)
      local text=$(echo "$line" | cut -d: -f2-)

      # Conta occorrenze totali del nome
      local total=$(echo "$text" | grep -oP "(?<![\\w])$(echo "$name" | sed 's/\([][()\.^$*+?{}|]\)/\\\1/g')(?![\\w])" | wc -l)

      # Conta occorrenze già linkate
      local linked=$(echo "$text" | grep -oP "\\[$(echo "$name" | sed 's/\([][()\.^$*+?{}|]\)/\\\1/g')\\]\\(<$link_path$anchor\\)" | wc -l)

      if [ "$total" -gt "$linked" ]; then
        local unlinked=$((total - linked))
        if [ $found -eq 0 ]; then
          echo ""
          echo "=== $chapter ==="
          found=1
        fi
        echo "  $name → $anchor ($unlinked occorrenze non linkate, riga $lineno)"
      fi
    done < <(grep -n "$name" "$file" 2>/dev/null || true)
  done

  if [ $found -eq 0 ]; then
    echo -n ""
  fi
}

echo "=== Controllo capitoli per nomi non linkati ==="
echo "Legenda: nome → ancora (quante occorrenze non linkate)"
echo "Capitoli in sessioni/strahd/:"
for f in "$CHAPTERS_DIR"/*.md; do
  check_chapter "$f"
done
echo ""
echo "=== Fine ==="