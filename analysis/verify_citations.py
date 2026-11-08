"""Check every hand-keyed figure in data/processed/<dataset>.csv against its cited PDF page.

For rows with a `pdf_page`, the page is extracted with pdftotext and searched for the value
(space-separated thousands, e.g. 127 637, or comma-separated). Rows without a page are
searched across the whole report and candidate pages are printed, so the page can be filled in.

Usage:  python3.12 analysis/verify_citations.py <company> <dataset>

The `source` column starts with the period and document, e.g. "FY2025 FD note 18" or "H1-2026 HFR ...":
FD -> FY<yyyy>_financial-documents.pdf, URD -> FY<yyyy>_urd.pdf, HFR -> H1-<yyyy>_financial-report.pdf
(all in sources/<company>/pdf/).
"""
import re
import subprocess
import sys
from functools import lru_cache

import pandas as pd

from common import PROCESSED, ROOT

DOCS = {"FD": "financial-documents", "URD": "urd", "HFR": "financial-report"}


@lru_cache(maxsize=None)
def pages_of(company: str, report: str) -> list[str]:
    pdf = ROOT / "sources" / company / "pdf" / f"{report}.pdf"
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    return txt.split("\f")


def variants(value: float, unit: str) -> list[str]:
    if unit == "%":
        return [f"{value:.2f}", f"{value:.1f}"]
    v = int(round(value))
    out = [f"{v:,}".replace(",", " "), f"{v:,}", str(v)]
    if value != v:  # e.g. US$570.7m
        out.append(f"{value:.1f}m")
    if v % 10 == 0 and v >= 1000:  # rounded "US$6.5bn" / "US$12.34bn" / "US$17bn" figures
        out += [f"{v / 1000:.1f}bn", f"{v / 1000:.2f}bn", f"{v // 1000}bn" if v % 1000 == 0 else ""]
        out = [o for o in out if o]
    if value != v and unit.endswith("bn"):  # e.g. "12.6" in an EUR billions table
        out.append(f"{value:.1f}")
    if v < 0:  # negatives printed in parentheses
        out += [f"({-v:,})".replace(",", " "), f"({-v:,})", f"({-v})"]
    return out


def main(company: str, dataset: str) -> None:
    df = pd.read_csv(PROCESSED / f"{dataset}.csv")
    ok = missing = unknown = 0
    for _, r in df.iterrows():
        m = re.match(r"((?:FY|H1-)\d{4}) (FD|URD|HFR)\b", str(r.source))
        if not m:
            unknown += 1
            print(f"  (skip) {r.fy} {r["item"]}: not a report citation -> {r.source}")
            continue
        report = f"{m.group(1)}_{DOCS[m.group(2)]}"
        pages = pages_of(company, report)
        needles = variants(r.value, r.unit)
        if pd.notna(r.pdf_page):
            page = int(r.pdf_page)
            text = re.sub(r"\s+", " ", pages[page - 1])
            hit = any(n in text for n in needles)
            ok += hit
            missing += not hit
            print(f"{'ok ' if hit else 'MISSING'} {r.fy} {r["item"]}={r.value} on {report} pdf p.{page} ({r.source})")
        else:
            cands = [i + 1 for i, p in enumerate(pages) if any(n in re.sub(r"\s+", " ", p) for n in needles)]
            unknown += 1
            print(f"  (no page) {r.fy} {r["item"]}={r.value}: candidate pdf pages in {report}: {cands[:12]}")
    print(f"\n{ok} verified, {missing} missing, {unknown} without a checkable page")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: verify_citations.py <company> <dataset>")
    main(*sys.argv[1:])
