"""Check that the markitdown conversions in sources/<co>/md kept the numbers from the originals.

Usage:  python3.12 analysis/verify_sources.py [prosus]

For each PDF, numbers are pulled from every page's text layer (pypdfium2). For each xlsx,
numbers are pulled from every numeric cell. We then check whether each number also
appears in the matching .md file. Low recall means figures were lost or mangled.
Writes data/processed/<co>_md_verification.csv.
"""
import re
import sys
from pathlib import Path

import pandas as pd
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
# Numbers with 3+ significant chars; Prosus uses a space as the thousands separator ("5 104")
NUM = re.compile(r"(?<![\d.,])\(?\d{1,3}(?:[  ]\d{3})+(?:[.,]\d+)?\)?|(?<![\d.,])\d{3,}(?:[.,]\d+)?|(?<![\d.,])\d+[.,]\d+")


def norm(text: str) -> str:
    text = text.replace(" ", " ").replace("|", " ")
    return re.sub(r"\s+", " ", text)


def numbers(text: str) -> list[str]:
    return [n.strip("()") for n in NUM.findall(norm(text))]


def check_pdf(pdf: Path, md_text: str) -> dict:
    doc = pdfium.PdfDocument(pdf)
    total = found = 0
    empty_pages, weak_pages = [], []
    for i in range(len(doc)):
        txt = doc[i].get_textpage().get_text_range()
        if len(txt.strip()) < 20:
            empty_pages.append(i + 1)
            continue
        nums = numbers(txt)
        hit = sum(n in md_text for n in nums)
        total += len(nums)
        found += hit
        if len(nums) >= 20 and hit / len(nums) < 0.9:
            weak_pages.append(f"{i + 1}:{hit / len(nums):.0%}")
    return dict(pages=len(doc), numbers=total, recall=found / total if total else None,
                no_text_pages=len(empty_pages), weak_pages=" ".join(weak_pages[:15]))


def fmt_cell(v: float) -> set[str]:
    """String forms a numeric cell might take in the markdown."""
    forms = {str(v), repr(v)}
    if float(v).is_integer():
        forms.add(str(int(v)))
    forms |= {f"{v:.{d}f}" for d in range(0, 4)}
    return forms


def check_xlsx(xlsx: Path, md_text: str) -> dict:
    sheets = pd.read_excel(xlsx, sheet_name=None, header=None)
    total = found = 0
    for df in sheets.values():
        for v in pd.to_numeric(df.stack(), errors="coerce").dropna():
            total += 1
            found += any(f in md_text for f in fmt_cell(float(v)))
    return dict(pages=len(sheets), numbers=total, recall=found / total if total else None,
                no_text_pages=0, weak_pages="")


def main(company: str = "prosus") -> None:
    src = ROOT / "sources" / company
    rows = []
    for f in sorted([*src.glob("pdf/*.pdf"), *src.glob("kpi/*")]):
        md = src / "md" / f"{f.stem}.md"
        md_text = norm(md.read_text()) if md.exists() else ""
        res = check_pdf(f, md_text) if f.suffix == ".pdf" else check_xlsx(f, md_text)
        rows.append(dict(file=f.name, **res))
        print(f"{f.name:38s} pages={res['pages']:4d} nums={res['numbers']:7d} "
              f"recall={res['recall'] or 0:6.1%} no_text={res['no_text_pages']:3d} {res['weak_pages']}")
    out = ROOT / "data" / "processed" / f"{company}_md_verification.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"-> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
