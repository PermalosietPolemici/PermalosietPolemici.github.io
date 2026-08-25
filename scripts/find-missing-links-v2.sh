#!/bin/bash
# Trova entità che compaiono in un capitolo SENZA mai essere linkate
CHAPTERS_DIR="/home/federico/volos-guide-to-pp/docs/sessioni/strahd"

declare -A ENTITY_PATTERNS
declare -A ENTITY_ANCHORS

# PNG
ENTITY_PATTERNS["Strahd"]="Strahd"
ENTITY_ANCHORS["Strahd"]="png/strahd/#strahd-von-zarovich"
ENTITY_PATTERNS["Ireena"]="Ireena"
ENTITY_ANCHORS["Ireena"]="png/strahd/#ireena-kolyana"
ENTITY_PATTERNS["Tatyana"]="Tatyana"
ENTITY_ANCHORS["Tatyana"]="png/strahd/#tatyana"
ENTITY_PATTERNS["Sergei"]="Sergei"
ENTITY_ANCHORS["Sergei"]="png/strahd/#sergei"
ENTITY_PATTERNS["Ismark"]="Ismark"
ENTITY_ANCHORS["Ismark"]="png/strahd/#ismark"
ENTITY_PATTERNS["Madam Eva"]="Madam Eva"
ENTITY_ANCHORS["Madam Eva"]="png/strahd/#madam-eva"
ENTITY_PATTERNS["Van Richten"]="Van Richten"
ENTITY_ANCHORS["Van Richten"]="png/strahd/#van-richten"
ENTITY_PATTERNS["Rictavio"]="Rictavio"
ENTITY_ANCHORS["Rictavio"]="png/strahd/#rictavio"
ENTITY_PATTERNS["Ezmeralda"]="Ezmeralda"
ENTITY_ANCHORS["Ezmeralda"]="png/strahd/#ezmeralda"
ENTITY_PATTERNS["Baba Lysaga"]="Baba Lysaga"
ENTITY_ANCHORS["Baba Lysaga"]="png/strahd/#baba-lysaga"
ENTITY_PATTERNS["Kasimir"]="Kasimir"
ENTITY_ANCHORS["Kasimir"]="png/strahd/#kasimir"
ENTITY_PATTERNS["Vladimir"]="Vladimir"
ENTITY_ANCHORS["Vladimir"]="png/strahd/#vladimir"
ENTITY_PATTERNS["Sir Godfrey"]="Sir Godfrey"
ENTITY_ANCHORS["Sir Godfrey"]="png/strahd/#sir-godfrey"
ENTITY_PATTERNS["Vargas"]="Vargas"
ENTITY_ANCHORS["Vargas"]="png/strahd/#vargas-vallakovich"
ENTITY_PATTERNS["Victor"]="Victor"
ENTITY_ANCHORS["Victor"]="png/strahd/#victor-vallakovich"
ENTITY_PATTERNS["Fiona Wachter"]="Fiona Wachter"
ENTITY_ANCHORS["Fiona Wachter"]="png/strahd/#fiona-watcher"
ENTITY_PATTERNS["Padre Lucian"]="Padre Lucian"
ENTITY_ANCHORS["Padre Lucian"]="png/strahd/#padre-luci an"


#queti sono troppi, faccio diretamente da file

echo "Questa analisi è trop po complesa, faccio a mano"

exit 0