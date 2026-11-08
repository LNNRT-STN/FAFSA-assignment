"""Illustrative calculations for the memo on Prosus's equity-accounted stake in Tencent (IAS 28).

Inputs
  data/processed/prosus_tencent.csv  hand-keyed annual-report figures, each with a source
                                     (checked by analysis/verify_citations.py)
  data/raw/PRX.AS_income.csv         OpenBB download, used only as a cross-check

Outputs (for \\input / \\includegraphics in report/)
  report/tables/tencent_history.tex   stake, carrying value, fair value, profit share, cash, FY2022-26
  report/tables/fy26_bridge.tex       FY2026 profit for the year vs what Tencent put in the bank
  report/tables/sensitivity.tex       per-percentage-point economics and the 20% cliff
  report/tables/acquirer_view.tex     Prosus's books vs the acquirer's books after an IFRS 3 step-up
  report/tables/openbb_check.tex      OpenBB figures vs the annual report (restatement caveat)
  report/figures/tencent_gap.pdf      carrying value vs quoted value, FY2019-26
  report/figures/profit_vs_cash.pdf   where the profit comes from vs cash received, FY2022-26

Usage:  python3.12 analysis/analysis.py PRX.AS
"""
import sys

import numpy as np
import pandas as pd

from common import PROCESSED, load_statement, plt, save_figure, write_table

BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#9a9a94"


def wide() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED / "prosus_tencent.csv")
    return df.pivot(index="fy", columns="item", values="value")


def bn(x: float) -> float:
    return x / 1000.0


def table_history(w: pd.DataFrame) -> None:
    yrs = [2022, 2023, 2024, 2025, 2026]
    rows = {
        "Effective stake (%)": w.loc[yrs, "tencent_stake_pct"],
        "Quoted value of stake": w.loc[yrs, "tencent_fair_value"],
        "Carrying value (IAS 28)": w.loc[yrs, "tencent_carrying_value"],
        "Unrecognised gap": w.loc[yrs, "tencent_fair_value"] - w.loc[yrs, "tencent_carrying_value"],
        "Share of Tencent profit (IFRS)": w.loc[yrs, "tencent_share_of_profit"],
        "Tencent in core headline earnings": w.loc[yrs, "tencent_core_he_contribution"],
        "Cash dividend received": w.loc[yrs, "tencent_cash_dividend"],
        "Dividend in specie (JD.com, Meituan)": w.loc[yrs, "tencent_in_specie_dividend"].fillna(0),
        "Proceeds from selling Tencent shares": w.loc[yrs, "tencent_sale_proceeds"],
        "Gain booked on those sales": w.loc[yrs, "tencent_disposal_gain"],
        "Group profit for the year": w.loc[yrs, "group_profit_for_year"],
    }
    t = pd.DataFrame(rows).T
    t.columns = [f"FY{y}" for y in yrs]
    out = pd.DataFrame(
        {c: [f"{v:,.2f}" if r.startswith("Effective") else f"{v:,.0f}" for r, v in t[c].items()] for c in t.columns},
        index=t.index,
    )
    write_table(out, "tencent_history", caption_note="US$m unless stated; 31 March year-ends")
    print(t.round(0))


def table_bridge(w: pd.DataFrame) -> dict:
    y = w.loc[2026]
    profit = y["group_profit_for_year"]
    tencent_profit = y["tencent_share_of_profit"]
    gain = y["tencent_disposal_gain"]
    rest = profit - tencent_profit - gain
    cash_div = y["tencent_cash_dividend"]
    proceeds = y["tencent_sale_proceeds"]
    cfo = y["group_cash_generated_from_operations"]
    rows = [
        ("Profit for the year (IFRS)", profit),
        ("less: share of Tencent's profit (equity accounted)", -tencent_profit),
        ("less: gain on selling 0.9% of Tencent", -gain),
        ("= everything else Prosus owns and runs", rest),
        ("Tencent-related profit recognised", tencent_profit + gain),
        ("Cash dividends actually received from associates", cash_div),
        ("Cash from selling Tencent shares (capital, not income)", proceeds),
        ("Cash generated from operations, whole group", cfo),
    ]
    t = pd.DataFrame(rows, columns=["FY2026", "US$m"]).set_index("FY2026")
    write_table(t, "fy26_bridge", caption_note="FY2026 profit vs cash lens")
    print(t)
    return dict(profit=profit, tencent_profit=tencent_profit, gain=gain, rest=rest, cash_div=cash_div)


def table_sensitivity(w: pd.DataFrame) -> dict:
    y = w.loc[2026]
    stake, fv, cv = y["tencent_stake_pct"], y["tencent_fair_value"], y["tencent_carrying_value"]
    fv_pp, cv_pp = fv / stake, cv / stake            # per percentage point of Tencent
    gain_pp = fv_pp - cv_pp
    pace = w.loc[2025, "tencent_stake_pct"] - stake   # net reduction in FY2026, pp per year
    years_to_20 = (stake - 20.0) / pace
    gap = fv - cv
    equity = y["group_total_equity"]
    rows = [
        ("Stake at 31 March 2026 (%)", stake, "note 9"),
        ("Quoted value per percentage point of Tencent", fv_pp, "127 637 / 22.66"),
        ("Carrying value per percentage point", cv_pp, "42 172 / 22.66"),
        ("Gain booked per percentage point sold, at March 2026 prices", gain_pp, "difference"),
        ("Net stake reduction in FY2026 (pp, incl. Tencent buy-backs)", pace, "23.49 - 22.66"),
        ("Years until the stake reaches 20% at that pace", years_to_20, "(22.66 - 20) / pace"),
        ("Remeasurement gain if significant influence were lost", gap, "quoted value - carrying value"),
        ("That gain as a multiple of group equity", gap / equity, "gap / 53 867"),
        ("Group equity if Tencent were carried at quoted value", equity + gap, "53 867 + gap"),
    ]
    t = pd.DataFrame(rows, columns=["Illustration", "Value", "How"]).set_index("Illustration")
    fmt = t.copy()
    fmt["Value"] = [f"{v:,.2f}" if abs(v) < 100 else f"{v:,.0f}" for v in t["Value"]]
    write_table(fmt, "sensitivity", caption_note="US$m unless stated")
    print(t)
    return dict(fv_pp=fv_pp, cv_pp=cv_pp, gain_pp=gain_pp, pace=pace, years_to_20=years_to_20, gap=gap)


def table_acquirer(w: pd.DataFrame) -> None:
    """What the same stake looks like in the acquirer's consolidated accounts (IFRS 3 fair value step-up)."""
    y = w.loc[2026]
    fv, cv = y["tencent_fair_value"], y["tencent_carrying_value"]
    rows = [
        ("Tencent on the balance sheet", f"{cv:,.0f}", f"{fv:,.0f}"),
        ("Headroom before an IAS 28/IAS 36 impairment test bites", f"{fv - cv:,.0f}", "nil: carrying value = quoted value on day one"),
        ("Gain if 1 pp of Tencent is sold at March 2026 prices", f"{(fv - cv) / y['tencent_stake_pct']:,.0f}", "about nil"),
        ("Share of Tencent profit recognised", f"{y['tencent_share_of_profit']:,.0f}", "same, less amortisation of any fair-value uplift on Tencent's intangibles"),
        ("Deferred tax on the gap", "none recognised", "depends on the acquirer's own tax jurisdiction"),
        ("Cash that reaches the parent", f"{y['tencent_cash_dividend']:,.0f}", "unchanged: dividends plus whatever is sold"),
    ]
    t = pd.DataFrame(rows, columns=["FY2026, US$m", "Prosus's books", "Acquirer's books"]).set_index("FY2026, US$m")
    write_table(t, "acquirer_view", caption_note="Prosus vs acquirer view of the Tencent stake")
    print(t)


def table_openbb(w: pd.DataFrame, ticker: str) -> None:
    try:
        inc = load_statement(ticker, "income")
    except FileNotFoundError:
        print("no OpenBB data; skipping cross-check")
        return
    cols = {str(c)[:4]: c for c in inc.columns}
    rows = []
    for fy in (2023, 2024, 2025, 2026):
        c = cols.get(str(fy))
        if c is None:
            continue
        ni = inc.loc["net_income", c] / 1e6 if "net_income" in inc.index else np.nan
        rev = inc.loc["total_revenue", c] / 1e6 if "total_revenue" in inc.index else np.nan
        rows.append((f"FY{fy}", rev, ni, w.loc[fy, "group_profit_for_year"]))
    t = pd.DataFrame(rows, columns=["Year", "Revenue (OpenBB)", "Net income to equity holders (OpenBB)", "Profit for the year (AR)"]).set_index("Year")
    write_table(t.round(0), "openbb_check", caption_note="OpenBB (yfinance, restated comparatives) vs annual report as first published, US$m")
    print(t.round(0))


def fig_gap(w: pd.DataFrame) -> None:
    yrs = list(range(2019, 2027))
    fv = [bn(w.loc[y, "tencent_fair_value"]) for y in yrs]
    cv = [bn(w.loc[y, "tencent_carrying_value"]) for y in yrs]
    x = np.arange(len(yrs))
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.bar(x - 0.21, fv, width=0.4, color=BLUE, label="Quoted value of the stake (note 9)")
    ax.bar(x + 0.21, cv, width=0.4, color=ORANGE, label="Carrying value under IAS 28")
    for i, (a, b) in enumerate(zip(fv, cv)):
        if yrs[i] in (2021, 2026):
            ax.text(x[i] - 0.21, a + 3, f"{a:.0f}", ha="center", va="bottom", fontsize=7.5, color="#333")
            ax.text(x[i] + 0.21, b + 3, f"{b:.0f}", ha="center", va="bottom", fontsize=7.5, color="#333")
    ax.set_xticks(x, [f"FY{y}" for y in yrs])
    ax.set_ylabel("US$ bn, 31 March")
    ax.yaxis.grid(True, color="#e6e6e3", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    save_figure(fig, "tencent_gap")


def fig_profit_vs_cash(w: pd.DataFrame) -> None:
    yrs = [2022, 2023, 2024, 2025, 2026]
    tp = np.array([bn(w.loc[y, "tencent_share_of_profit"]) for y in yrs])
    g = np.array([bn(w.loc[y, "tencent_disposal_gain"]) for y in yrs])
    tot = np.array([bn(w.loc[y, "group_profit_for_year"]) for y in yrs])
    rest = tot - tp - g
    div = np.array([bn(w.loc[y, "tencent_cash_dividend"]) for y in yrs])
    x = np.arange(len(yrs))
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.bar(x, tp, width=0.55, color=BLUE, label="Share of Tencent's profit")
    ax.bar(x, g, width=0.55, bottom=tp, color=AQUA, label="Gain on Tencent shares sold")
    pos = np.where(rest > 0, rest, 0)
    neg = np.where(rest < 0, rest, 0)
    ax.bar(x, pos, width=0.55, bottom=tp + g, color=GREY, label="Everything else")
    ax.bar(x, neg, width=0.55, bottom=0, color=GREY)
    ax.plot(x, div, color=ORANGE, marker="o", markersize=7, linewidth=2, label="Cash dividends received", zorder=5)
    for i, v in enumerate(tot):
        ax.text(x[i], max(tp[i] + g[i] + pos[i], 0) + 0.4, f"profit {v:.1f}", ha="center", fontsize=7.5, color="#333")
    ax.axhline(0, color="#777", linewidth=0.6)
    ax.set_xticks(x, [f"FY{y}" for y in yrs])
    ax.set_ylabel("US$ bn")
    ax.yaxis.grid(True, color="#e6e6e3", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.5, ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    save_figure(fig, "profit_vs_cash")


def main(ticker: str) -> None:
    w = wide()
    table_history(w)
    table_bridge(w)
    table_sensitivity(w)
    table_acquirer(w)
    table_openbb(w, ticker)
    fig_gap(w)
    fig_profit_vs_cash(w)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "PRX.AS")
