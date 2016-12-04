all:	report.pdf

report.pdf:	clean
	pdflatex report.tex && bibtex report.aux && pdflatex report.tex && pdflatex report.tex

clean:
	rm -f *.aux *.lof *.log *.lol *.lot *.out *.toc *.bbl *.blg *.tab report.pdf