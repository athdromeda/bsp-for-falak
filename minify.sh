#!/bin/bash
set -e

BASE_URL="https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets"
TARGETS=("442s")
DIST_DIR="dist"

mkdir -p "$DIST_DIR"

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