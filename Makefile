PY := /opt/homebrew/bin/python3.12
TICKER ?=

.PHONY: data analysis report all clean

data:        ## Pull financial statements via OpenBB: make data TICKER=XYZ
	$(PY) analysis/fetch_financials.py $(TICKER)

analysis:    ## Run calculations -> report/tables + report/figures
	$(PY) analysis/analysis.py $(TICKER)

report:      ## Compile the PDF -> report/build/main.pdf
	mkdir -p report/build
	cd report && tectonic -X compile main.tex --outdir build --synctex

all: data analysis report

clean:
	rm -rf report/build
