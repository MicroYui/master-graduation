$ErrorActionPreference = 'Stop'
$thesisRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $thesisRoot
try {
    New-Item -ItemType Directory -Path 'build/thesis', 'output/pdf' -Force | Out-Null
    & latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build/thesis thesis.tex
    if ($LASTEXITCODE -ne 0) { throw 'Thesis compilation failed.' }
    Copy-Item -LiteralPath 'build/thesis/thesis.pdf' -Destination 'thesis.pdf' -Force
    Copy-Item -LiteralPath 'build/thesis/thesis.pdf' -Destination 'output/pdf/thesis.pdf' -Force
    Write-Output (Join-Path $thesisRoot 'thesis.pdf')
} finally {
    Pop-Location
}
