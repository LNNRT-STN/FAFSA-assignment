"""Illustrative calculations for the memo.

Inputs
  data/processed/<company>_<issue>.csv  hand-keyed annual-report figures, each with a source
                                        (checked by analysis/verify_citations.py)
  data/raw/<TICKER>_*.csv               OpenBB downloads, used only as a cross-check

Outputs (for \\input / \\includegraphics in report/)
  report/tables/*.tex
  report/figures/*.pdf

Usage:  python3.12 analysis/analysis.py <TICKER>
"""
import sys

import numpy as np  # noqa: F401
import pandas as pd  # noqa: F401

from common import PROCESSED, load_statement, plt, save_figure, write_table  # noqa: F401


def main(ticker: str) -> None:
    pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: analysis.py <TICKER>")
    main(sys.argv[1])
