#!/bin/bash
set -e

BASE_URL="https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets"
TARGETS=("442s")
DIST_DIR="dist"

LOCAL_MODE=false
if [[ "$1" == "--local" ]]; then
  LOCAL_MODE=true
fi

mkdir -p "$DIST_DIR"

if [ "$LOCAL_MODE" = true ]; then
  for bsp in raw/*.bsp; do
    target=$(basename "$bsp" .bsp)
    if [[ "$target" == *"_minified" ]]; then
      continue
    fi
    
    echo "Minifying $target.bsp..."
    cd raw
    ../exe/spkmerge "$target.cmd"
    cd ..
    
    mv "raw/${target}_minified.bsp" "$DIST_DIR/"
    echo "Done: ${target}_minified.bsp"
  done
else
  for target in "${TARGETS[@]}"; do
    echo "Downloading de$target.bsp..."
    curl -Lko "raw/de$target.bsp" "$BASE_URL/de$target.bsp"
    
    echo "Minifying de$target.bsp..."
    cd raw
    ../exe/spkmerge de$target.cmd
    cd ..
    
    mv "raw/de${target}_minified.bsp" "$DIST_DIR/"
    rm -f "raw/de$target.bsp"
    echo "Done: de${target}_minified.bsp"
  done
fi