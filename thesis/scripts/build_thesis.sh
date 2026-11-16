#!/usr/bin/env bash
set -euo pipefail
thesis_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$thesis_root"
mkdir -p build/thesis output/pdf
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build/thesis thesis.tex
cp build/thesis/thesis.pdf thesis.pdf
cp build/thesis/thesis.pdf output/pdf/thesis.pdf
printf '%s\n' "$thesis_root/thesis.pdf"
