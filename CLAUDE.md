# Take-home project: accounting issue analysis (Vlerick)

The brief is in `brief/Final Project - Take-home.pdf`. In short: advise an acquirer on one material, tricky accounting issue at a real listed company (not Thomas Cook, NVIDIA, BMW Group or Solvay).

## Deliverable constraints
- A single PDF: A4, at least 12pt, margins of at least 2 cm. Name, student number and a URL to the financial statements go on page 1.
- Page 1 is the executive summary, with exactly three headings: What is the issue? / Why is it relevant? / What should we do?
- Pages 2–4 are the technical memo: the standard(s), measurement, judgement, disclosures, and implications, plus illustrative numbers.
- The AI-use note comes after the memo and doesn't count toward the 4 pages.
- Every important figure is cited in a footnote (report year, note, page).
- Claude helps with understanding, analysis, numbers and LaTeX, and doesn't write the report prose unless asked to.

## Layout
- The chosen company: LVMH Moët Hennessy Louis Vuitton SE (IFRS, EUR, calendar-year FY; ticker MC.PA; sources go in `sources/lvmh/`). The chosen issue is the put option Diageo holds over its 34% of Moët Hennessy ("Purchase commitments for minority interests' shares", IAS 32.23 / LVMH note 1.13 and note 21). The argument, numbers and page citations are in `report/notes/nci-put-diageo.md`; the hand-keyed figures are in `data/processed/lvmh_nci_put.csv` (verified with `verify_citations.py lvmh lvmh_nci_put`).
- `analysis/`: Python. `fetch_financials.py` pulls statements via OpenBB, `analysis.py` writes the four memo figures (`figures/nci_put_{entry,flow,pnl,fv}.pdf`; the report uses figures, not tables) and prints the series and pro-forma numbers to the console, `common.py` holds paths and the table/figure helpers. `verify_citations.py <company> <dataset>` checks every row of `data/processed/<dataset>.csv` against the cited PDF page with pdftotext (rows without a `pdf_page` get candidate pages printed). It expects annual reports at `sources/<company>/pdf/FY<yyyy>_annual-report.pdf` and a `source` like "FY2025 AR ...".
- `data/raw/`: OpenBB downloads (gitignored, regenerable). `data/processed/`: hand-keyed annual-report figures with a `source` column and a `pdf_page` column (PDF page index, not the printed number).
- LaTeX: `\footnote` inside a `table`/`figure` float does not print, so table citations go in the `\par\footnotesize` source line under the table; footnotes work in body prose.
- `sources/lvmh/`: `pdf/` holds Financial Documents FY2021–25 (consolidated FS + notes, the main citation source), Universal Registration Documents FY2020, FY2022–25 (no English 2021 URD on lvmh.com), first-half financial reports H1 2021–26, and results presentations/press releases. `md/` holds markitdown conversions, `SOURCES.txt` maps each PDF to its lvmh.com URL, `transcripts/` and `news/` hold call transcripts and press coverage (each with an `INDEX.md`). The FY2022–24 and H1 2024–25 results decks are image-only (no text layer), so their .md is near-empty.
- `sources/diageo/`: Diageo's FY2026 (June year-end) annual report and financial statements, for the other side of the Moët Hennessy put (note 6, printed p. 157; change-of-control clause p. 130). `SOURCES.txt` has the URLs and page pointers.
- Citation `source` strings: "FY2025 FD note X", "FY2025 URD ...", "H1-2026 HFR ..." (what `verify_citations.py` parses). `analysis/verify_sources.py <company>` checks number recall (PDF/xlsx vs md). Markdown loses page markers and jumbles two-column pages, so verify any figure against the PDF page before citing it.
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
