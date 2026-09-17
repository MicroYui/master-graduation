#!/usr/bin/env bash
set -euo pipefail
thesis_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
thesis_build="$thesis_root/build/thesis"
mkdir -p "$thesis_build" "$thesis_root/output/pdf"
cd "$thesis_root"
if command -v tectonic >/dev/null 2>&1; then
  tectonic --keep-logs --keep-intermediates --outdir "$thesis_build" thesis.tex
elif command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="$thesis_build" thesis.tex
else
  xelatex -interaction=nonstopmode -halt-on-error -output-directory="$thesis_build" thesis.tex
  (cd "$thesis_build" && BIBINPUTS="$thesis_root:" bibtex thesis)
  xelatex -interaction=nonstopmode -halt-on-error -output-directory="$thesis_build" thesis.tex
  xelatex -interaction=nonstopmode -halt-on-error -output-directory="$thesis_build" thesis.tex
fi
cp "$thesis_build/thesis.pdf" "$thesis_root/output/pdf/thesis.pdf"
printf '%s\n' "$thesis_root/output/pdf/thesis.pdf"
