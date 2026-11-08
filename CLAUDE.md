# Take-home project: accounting issue analysis (Vlerick)

The brief is in `brief/Final Project - Take-home.pdf`. In short: advise an acquirer on one material, tricky accounting issue at a real listed company (not Thomas Cook, NVIDIA, BMW Group or Solvay).

## Deliverable constraints
- A single PDF: A4, at least 12pt, margins of at least 2 cm. Name, student number and a URL to the financial statements go on page 1.
- Page 1 is the executive summary, with exactly three headings: What is the issue? / Why is it relevant? / What should we do?
- Pages 2–4 are the technical memo: the standard(s), measurement, judgement, disclosures, and implications, plus illustrative numbers.
- The AI-use note comes after the memo and doesn't count toward the 4 pages.
- Every important figure is cited in a footnote (report year, note, page).
- The final prose must be in the student's own voice; 3 of the 20 marks are for "not sounding like AI". Claude helps with understanding, analysis, numbers and LaTeX, and doesn't write the report prose unless asked to.

## Layout
- The chosen issue: Prosus's 22.66% stake in Tencent equity-accounted under IAS 28 (carrying US$42.2bn vs quoted US$127.6bn at 31 March 2026). The argument, numbers and page citations are in `report/notes/tencent_issue.md`.
- `analysis/`: Python. `fetch_financials.py` pulls statements via OpenBB, `analysis.py` does the calculations, `common.py` holds paths and the table/figure helpers. `verify_citations.py` checks every row of `data/processed/prosus_tencent.csv` against the cited PDF page with pdftotext (run it after editing the CSV; rows without a `pdf_page` get candidate pages printed).
- `data/raw/`: OpenBB downloads (gitignored, regenerable). `data/processed/`: hand-keyed annual-report figures with a `source` column and a `pdf_page` column (PDF page index, not the printed number).
- Printed vs PDF page numbers: FY2026/FY2025/FY2021 printed = PDF − 1; FY2022/FY2020 printed = PDF − 2; FY2023 is a two-page spread (one PDF page = two printed pages); FY2024 uses section/page numbering like "5/133" (PDF page = 134).
- LaTeX: `\footnote` inside a `table`/`figure` float does not print, so table citations go in the `\par\footnotesize` source line under the table; footnotes work in body prose.
- `sources/`: annual report PDFs and other filings.
  - `sources/prosus/`: Prosus N.V. (IFRS, fiscal year ends 31 March). `pdf/` holds the annual reports FY2020–26, summary consolidated FS, and results booklets (interim statements). `kpi/` holds the KPI datasheets. `md/` holds the markitdown conversions of both. `SOURCES.txt` maps each file to its prosus.com URL.
  - Caveat on `md/`: the markdown has no page markers. The printed page number appears as a bare line (e.g. `139`) near the page header. Two-column statements come out jumbled, so verify any figure against the PDF page before citing it.
  - `analysis/verify_sources.py prosus` checks number recall (PDF/xlsx vs md). It was 98–100% on every file. The only weak pages are headcount charts.
- OpenBB for Prosus: `make data` (ticker PRX.AS) writes `data/raw/PRX.AS_*.csv`. Coverage is FY2023–FY2026 annual only: FY2022 is empty and there's no half-year data. Values are in US$, Prosus's reporting currency, even though the PRX.AS listing trades in EUR. The data uses the most recent restated comparatives, not figures as first reported; e.g. FY2023 revenue is 4,947 (restated in the FY2024 AR) vs 5,765 in the FY2023 AR. EPS fields are zero/NaN, so don't use them. `total_debt` is a Yahoo-derived aggregate, not a Prosus line item.
- `report/`: LaTeX. `main.tex` plus `sections/*.tex`. Generated `tables/*.tex` and `figures/*.pdf` come from the analysis scripts.

## Tooling (installed globally, no venv)
- Python: `/opt/homebrew/bin/python3.12`. Use the full path, because the uv `python3.12` in `~/.local/bin` comes earlier on PATH. Packages were installed with `pip install --break-system-packages`.
- OpenBB 5.0 with the `openbb-equity` and `openbb-yfinance` extensions: `obb.equity.fundamental.{income,balance,cash}(symbol=..., provider="yfinance")`. After installing a new OpenBB extension, run `python3.12 -c "import openbb; openbb.build()"`.
- LaTeX: Tectonic (`brew install tectonic`), which fetches packages on demand.

## Commands
- `make data TICKER=XYZ` downloads statements.
- `make analysis TICKER=XYZ` writes tables and figures.
- `make report` builds `report/build/main.pdf`.
- `make all TICKER=XYZ` runs all three.
