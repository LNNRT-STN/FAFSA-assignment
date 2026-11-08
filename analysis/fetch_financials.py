"""Download annual financial statements for a ticker via OpenBB (yfinance provider).

Usage:  python3.12 analysis/fetch_financials.py ASML [--limit 5]

Note: OpenBB/yfinance data is a convenience for trends and cross-checks. Every figure
quoted in the report must still be traced to the company's annual report (year, note,
page) and cited in a footnote.
"""
import argparse

from openbb import obb

from common import RAW

STATEMENTS = {
    "income": obb.equity.fundamental.income,
    "balance": obb.equity.fundamental.balance,
    "cash": obb.equity.fundamental.cash,
}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("ticker")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--provider", default="yfinance")
    args = p.parse_args()

    for name, fn in STATEMENTS.items():
        df = fn(symbol=args.ticker, provider=args.provider, period="annual", limit=args.limit).to_df()
        df = df.set_index("period_ending").T  # rows = line items, columns = fiscal years
        out = RAW / f"{args.ticker}_{name}.csv"
        df.to_csv(out)
        print(f"{name:8s} {df.shape[0]:3d} items x {df.shape[1]} years -> {out.relative_to(RAW.parents[1])}")

    profile = obb.equity.profile(symbol=args.ticker, provider=args.provider).to_df()
    profile.T.to_csv(RAW / f"{args.ticker}_profile.csv")
    print(f"profile  -> data/raw/{args.ticker}_profile.csv")


if __name__ == "__main__":
    main()
