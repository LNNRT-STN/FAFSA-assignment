PY ?= $(firstword $(wildcard /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3.14) python3)
TICKER ?=

.PHONY: data analysis report all clean

data:        ## Pull financial statements via OpenBB: make data TICKER=XYZ
	$(PY) analysis/fetch_financials.py $(TICKER)

analysis:    ## Run calculations -> report/tables + report/figures
	$(PY) analysis/analysis.py $(TICKER)

report:      ## Compile the PDF -> report/build/main.pdf
	mkdir -p report/build
	@if command -v tectonic >/dev/null 2>&1; then \
		cd report && tectonic -X compile main.tex --outdir build --synctex; \
	else \
		cd report && latexmk -pdf -interaction=nonstopmode -halt-on-error -synctex=1 -outdir=build main.tex; \
	fi

all: data analysis report

clean:
	rm -rf report/build
