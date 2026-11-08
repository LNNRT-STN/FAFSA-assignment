"""Shared paths and helpers for the analysis scripts."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "report" / "tables"
FIGURES = ROOT / "report" / "figures"

for d in (RAW, PROCESSED, TABLES, FIGURES):
    d.mkdir(parents=True, exist_ok=True)

# Consistent, print-friendly figure style for the report
plt.rcParams.update({
    "figure.figsize": (6.0, 3.0),
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.bbox": "tight",
})


def load_statement(ticker: str, statement: str) -> pd.DataFrame:
    """Load a statement saved by fetch_financials.py (rows = line items, cols = periods)."""
    return pd.read_csv(RAW / f"{ticker}_{statement}.csv", index_col=0)


def write_table(df: pd.DataFrame, name: str, *, decimals: int = 0, caption_note: str = "") -> Path:
    """Write a booktabs tabular to report/tables/<name>.tex for \\input{} in the report.

    Only the tabular is written; captions and source footnotes stay in the .tex file,
    so the citation sits next to the text it supports.
    """
    path = TABLES / f"{name}.tex"
    df = df.copy()
    df.index.name = None
    body = df.to_latex(float_format=f"{{:,.{decimals}f}}".format, escape=True,
                       column_format="l" + "r" * df.shape[1])
    if caption_note:
        body = f"% {caption_note}\n" + body
    path.write_text(body)
    return path


def save_figure(fig, name: str) -> Path:
    path = FIGURES / f"{name}.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path
