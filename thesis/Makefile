.PHONY: thesis viewthesis clean
thesis:
	latexmk -xelatex -interaction=nonstopmode -halt-on-error thesis.tex
viewthesis: thesis
	latexmk -pv thesis.tex
clean:
	latexmk -c thesis.tex
