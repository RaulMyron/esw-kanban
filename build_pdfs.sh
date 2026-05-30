#!/usr/bin/env bash
# Gera PDFs a partir dos arquivos Markdown (requer pandoc + wkhtmltopdf).
set -e
cd "$(dirname "$0")"
mkdir -p docs/pdf
CSS="docs/_style.css"
OPTS=(--from gfm --css "$CSS" --pdf-engine=wkhtmltopdf
      -V margin-top=18mm -V margin-bottom=18mm -V margin-left=18mm -V margin-right=18mm)

for f in docs/*.md infra/*.md; do
  [ -e "$f" ] || continue
  base=$(basename "${f%.md}")
  out="docs/pdf/${base}.pdf"
  echo "  -> $out"
  pandoc "$f" "${OPTS[@]}" -o "$out"
done
echo "PDFs gerados em docs/pdf/"
