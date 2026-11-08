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
- The chosen company: LVMH Moët Hennessy Louis Vuitton SE (IFRS, EUR, calendar-year FY; ticker MC.PA; sources go in `sources/lvmh/`). The issue is not yet chosen. Put the argument, numbers and page citations in `report/notes/<issue>.md`.
- `analysis/`: Python. `fetch_financials.py` pulls statements via OpenBB, `analysis.py` does the calculations (currently a stub), `common.py` holds paths and the table/figure helpers. `verify_citations.py <company> <dataset>` checks every row of `data/processed/<dataset>.csv` against the cited PDF page with pdftotext (rows without a `pdf_page` get candidate pages printed). It expects annual reports at `sources/<company>/pdf/FY<yyyy>_annual-report.pdf` and a `source` like "FY2025 AR ...".
- `data/raw/`: OpenBB downloads (gitignored, regenerable). `data/processed/`: hand-keyed annual-report figures with a `source` column and a `pdf_page` column (PDF page index, not the printed number).
- LaTeX: `\footnote` inside a `table`/`figure` float does not print, so table citations go in the `\par\footnotesize` source line under the table; footnotes work in body prose.
- `sources/<company>/`: annual report PDFs (`pdf/`), other filings, markitdown conversions (`md/`), and a `SOURCES.txt` mapping each file to its URL. `analysis/verify_sources.py <company>` checks number recall (PDF/xlsx vs md). Markdown loses page markers and jumbles two-column pages, so verify any figure against the PDF page before citing it.
- `report/`: LaTeX. `main.tex` (fill in name, student number, company, framework, FS URL) plus `sections/*.tex`. Generated `tables/*.tex` and `figures/*.pdf` come from the analysis scripts.

## Tooling (installed globally, no venv)
- Python: `/opt/homebrew/bin/python3.12`. Use the full path, because the uv `python3.12` in `~/.local/bin` comes earlier on PATH. Packages were installed with `pip install --break-system-packages`.
- OpenBB 5.0 with the `openbb-equity` and `openbb-yfinance` extensions: `obb.equity.fundamental.{income,balance,cash}(symbol=..., provider="yfinance")`. After installing a new OpenBB extension, run `python3.12 -c "import openbb; openbb.build()"`.
- LaTeX: Tectonic (`brew install tectonic`), which fetches packages on demand.

## Commands
- `make data TICKER=XYZ` downloads statements.
- `make analysis TICKER=XYZ` writes tables and figures.
- `make report` builds `report/build/main.pdf`.
- `make all TICKER=XYZ` runs all three.
