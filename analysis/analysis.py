"""Illustrative calculations for the memo: the Diageo put over 34% of Moët Hennessy.

Inputs
  data/processed/lvmh_nci_put.csv   hand-keyed figures from LVMH's Financial Documents, URD and
                                    half-year report, plus four Diageo figures (every LVMH row is
                                    checked by analysis/verify_citations.py lvmh lvmh_nci_put)
  data/raw/<TICKER>_*.csv           OpenBB downloads, not needed for this issue

Outputs (for \\includegraphics in report/; the series and pro-forma tables print to the console)
  report/figures/nci_put_entry.pdf           Dr = Cr blocks at end-2021 and end-2025, one scale
  report/figures/nci_put_flow.pdf            FY2024 flow: MH value -> put liability -> goodwill vs. P&L
  report/figures/nci_put_pnl.pdf             net profit as reported vs. with the goodwill movement in P&L
  report/figures/nci_put_fv.pdf              implied fair value of 100% of MH, LVMH vs. Diageo basis

Usage:  python3.12 analysis/analysis.py MC.PA
"""
import sys

import pandas as pd

from common import PROCESSED, plt, save_figure

DIAGEO_STAKE = 0.34
PUT_PRICE = 0.80          # Diageo can put at 80% of Moët Hennessy's fair value (FD note 21)
USD_EUR_JUN26 = 0.88      # Diageo AR 2026 note 6(b): $1 = EUR 0.88, closing rate for MH balance sheet at 30 June 2026 (0.86 is the income-statement rate)

# House palette, matched to the report (navy brand + muted copper accent for the put)
BLUE, ORANGE = "#1B365D", "#A65A24"
INK, MUTED = "#1A1D21", "#5A5F66"
GRID, AXIS, NEUTRAL = "#E3E6E9", "#B9BEC4", "#A9B4C2"
GREEN = "#2F7D5B"          # profit or loss (the IASB route); copper stays reserved for goodwill


def load() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED / "lvmh_nci_put.csv")
    wide = df.pivot_table(index="fy", columns="item", values="value", aggfunc="first")
    order = ["FY2019", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "H1-2026"]
    return wide.reindex(order)


def series_table(w: pd.DataFrame) -> pd.DataFrame:
    t = pd.DataFrame({
        "Put liability (balance sheet)": w.put_liability,
        "of which goodwill counterpart": w.goodwill_on_commitments,
        "Diageo's 34% of MH equity": w.diageo_accumulated_nci,
    })
    t["Implied Diageo put (sum)"] = t.iloc[:, 1] + t.iloc[:, 2]
    t["Implied FV of 100% of MH"] = t.iloc[:, 3] / PUT_PRICE / DIAGEO_STAKE
    t["Goodwill movement, outside P&L"] = w.goodwill_change_commitments
    t = t.loc["FY2021":].T
    t.columns.name = None
    return t


def proforma_table(w: pd.DataFrame) -> pd.DataFrame:
    y = w.loc["FY2025"]
    diageo_put = y.diageo_accumulated_nci + y.goodwill_on_commitments
    fv_mh = diageo_put / PUT_PRICE / DIAGEO_STAKE
    # Diageo's own test (AR 2026 note 6a) implies its 34% is worth about $5.2bn on a multiples basis:
    # a 10% EBITDA fall costs $388m: impairment = carrying - 0.9*FV = 5,107 - 0.9*FV = 388 -> FV = $5,243m
    # (the 1.0x multiple check, 5,107 - FV*(1 - 1/m) = 312, then gives m of about 11.7x EBITDA)
    diageo_fv_34 = (5107 - 388) / 0.9 * USD_EUR_JUN26
    fv_mh_diageo = diageo_fv_34 / DIAGEO_STAKE
    rows = {
        "Reported net financial debt": y.net_financial_debt,
        "+ put liability (all minority puts)": y.put_liability,
        "Diageo put as booked (80% of fair value)": diageo_put,
        "Cost to buy Diageo out at 100% of LVMH's fair value": diageo_put / PUT_PRICE,
        "Diageo put re-measured on Diageo's own multiples basis": fv_mh_diageo * DIAGEO_STAKE * PUT_PRICE,
        "FY2024 net profit, Group share, as reported": w.loc["FY2024"].net_profit_group_share,
        "FY2024 net profit if the EUR 4,378m goodwill movement were a P&L gain": (w.loc["FY2024"].net_profit_group_share
                                                        - w.loc["FY2024"].goodwill_change_commitments),
    }
    out = pd.DataFrame({"EUR m": pd.Series(rows)})
    out.attrs["fv_mh"] = fv_mh
    out.attrs["fv_mh_diageo"] = fv_mh_diageo
    return out


def _style(ax, ylim: tuple[float, float]) -> None:
    ax.set_ylabel("EUR bn", color=MUTED)
    ax.set_ylim(*ylim)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(colors=MUTED, length=0)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)




def entry_figure(w: pd.DataFrame):
    """The booking entry at end-2021 and end-2025, to one scale: Dr (minority interest + goodwill)
    = Cr (Diageo put liability). Shows that the goodwill block carries all of the fall in value."""
    from matplotlib.patches import FancyArrowPatch
    years = [("FY2021", "End-2021", 0.0), ("FY2025", "End-2025", 3.35)]
    bw, gap = 1.0, 0.34
    fig, ax = plt.subplots(figsize=(FIGSIZE[0], 2.0))
    def seg(x, y, value, name):
        """Block label: the amount, with the account name in smaller type under it."""
        ax.annotate(f"{value:,.0f}", (x, y), xytext=(0, 0.5), textcoords="offset points",
                    ha="center", va="bottom", color="white", fontsize=7.5, fontweight="semibold")
        ax.annotate(name, (x, y), xytext=(0, -0.5), textcoords="offset points",
                    ha="center", va="top", color="white", fontsize=6.5, linespacing=0.95)

    for fy, title, x0 in years:
        y = w.loc[fy]
        nci, gw = y.diageo_accumulated_nci, y.goodwill_on_commitments
        put = nci + gw
        fv = put / PUT_PRICE / DIAGEO_STAKE / 1000
        xc = x0 + bw + gap
        ax.bar(x0, nci, width=bw, align="edge", color=NEUTRAL, linewidth=0)
        ax.bar(x0, gw, bottom=nci, width=bw, align="edge", color=ORANGE, linewidth=0.8, edgecolor="white")
        ax.bar(xc, put, width=bw, align="edge", color=BLUE, linewidth=0)
        seg(x0 + bw / 2, nci * 0.63, nci, "minority\ninterest")
        if gw > 1500:
            seg(x0 + bw / 2, nci + gw / 2, gw, "goodwill")
        else:
            ax.annotate(f"{gw:,.0f} goodwill", xy=(x0 + bw / 2, put), xytext=(x0 + bw / 2 + 0.4, put + 1300),
                        ha="center", va="bottom", fontsize=7.5, color=ORANGE, fontweight="semibold",
                        arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6, shrinkA=0, shrinkB=0))
        seg(xc + bw / 2, put / 2 + 250, put, "put\nliability")
        ax.text(x0 + bw + gap / 2, put / 2, "=", ha="center", va="center", fontsize=11, color=MUTED)
        ax.text(x0 + bw / 2, -350, "Dr", ha="center", va="top", fontsize=7, color=MUTED)
        ax.text(xc + bw / 2, -350, "Cr", ha="center", va="top", fontsize=7, color=MUTED)
        # date heading above each pair, on one line across the figure
        ax.text(x0 + bw + gap / 2, 14250, title, ha="center", va="bottom",
                fontsize=9, color=INK, fontweight="semibold")
        ax.text(x0 + bw + gap / 2, 13350, f"MH ≈ €{fv:.0f}bn", ha="center", va="bottom",
                fontsize=7, color=MUTED)
    # the fall in the goodwill block, booked outside P&L
    d_gw = (w.loc["FY2025"].goodwill_on_commitments - w.loc["FY2021"].goodwill_on_commitments) / 1000
    ax.add_patch(FancyArrowPatch((2.42, 9600), (3.28, 4650), connectionstyle="arc3,rad=-0.35",
                                 arrowstyle="-|>,head_length=4,head_width=2.5", color=ORANGE, lw=1.3))
    ax.text(3.35, 11300, f"−€{-d_gw:.1f}bn goodwill", ha="left", va="top", fontsize=8,
            color=ORANGE, fontweight="semibold")
    ax.text(3.35, 10200, "€0 through P&L", ha="left", va="top", fontsize=8, color=INK, fontweight="semibold")
    ax.set_xlim(-0.05, 3.35 + 2 * bw + gap + 0.05)
    ax.set_ylim(-1100, 15500)
    ax.axis("off")
    return fig


def flow_figure(w: pd.DataFrame):
    """FY2024 as a flow: fall in MH value -> fall in the put liability -> two exits
    (LVMH: goodwill, P&L 0; IASB 2026 tentative: gain in P&L)."""
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
    y23, y24 = w.loc["FY2023"], w.loc["FY2024"]
    fv = lambda y: (y.diageo_accumulated_nci + y.goodwill_on_commitments) / PUT_PRICE / DIAGEO_STAKE / 1000
    fv23, fv24 = fv(y23), fv(y24)
    mv = -y24.goodwill_change_commitments / 1000          # 4.378: liability fall booked against goodwill

    fig = plt.figure(figsize=(FIGSIZE[0], 1.56))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIGSIZE[0]); ax.set_ylim(0, 1.56); ax.axis("off")
    cw = 0.82

    def card(x, y, h, head, big, foot, fc, ec, tc, bc, ls="-"):
        ax.add_patch(FancyBboxPatch((x, y), cw, h, boxstyle="round,pad=0,rounding_size=0.03",
                                    fc=fc, ec=ec, lw=0.9, ls=ls))
        ax.text(x + 0.06, y + h - 0.07, head, ha="left", va="top", fontsize=7.5, color=tc)
        ax.text(x + 0.06, y + h / 2 - 0.02, big, ha="left", va="center", fontsize=12, color=bc,
                fontweight="semibold")
        ax.text(x + 0.06, y + 0.07, foot, ha="left", va="bottom", fontsize=7.5, color=tc)

    mid = 0.78
    card(0.0, 0.40, 0.76, "MH value", f"−€{fv23 - fv24:.1f}bn", f"€{fv23:.0f}→{fv24:.0f}bn",
         "white", AXIS, MUTED, INK)
    card(1.215, 0.40, 0.76, "Put liability", f"−€{mv:.1f}bn", "owed to Diageo", BLUE, BLUE, "white", "white")
    card(2.43, 0.84, 0.70, "LVMH: goodwill", f"−€{mv:.1f}bn", "P&L: €0", ORANGE, ORANGE, "white", "white")
    card(2.43, 0.02, 0.70, "IASB: P&L", f"+€{mv:.1f}bn", "gain", "white", GREEN, GREEN, GREEN,
         ls=(0, (3, 2)))
    arrow = dict(arrowstyle="-|>,head_length=3,head_width=2", lw=1.6, shrinkA=1, shrinkB=1)
    ax.add_patch(FancyArrowPatch((0.83, mid), (1.205, mid), color=AXIS, **arrow))
    ax.text(1.0175, mid + 0.05, "× 34%", ha="center", va="bottom", fontsize=7.5, color=INK)
    ax.text(1.0175, mid - 0.05, "× 80%", ha="center", va="top", fontsize=7.5, color=INK)
    ax.add_patch(FancyArrowPatch((2.045, mid + 0.04), (2.42, 1.19), connectionstyle="arc3,rad=0.25",
                                 color=ORANGE, **arrow))
    ax.add_patch(FancyArrowPatch((2.045, mid - 0.04), (2.42, 0.37), connectionstyle="arc3,rad=-0.25",
                                 color=GREEN, **arrow))
    return fig


def pnl_figure(w: pd.DataFrame):
    """Right panel: net profit as reported vs. with the goodwill movement taken to P&L (FICE direction)."""
    d = w.loc["FY2021":"FY2025", ["net_profit_group_share", "goodwill_change_commitments"]] / 1000
    restated = d.net_profit_group_share - d.goodwill_change_commitments
    delta = -d.goodwill_change_commitments
    labels = [i.replace("FY", "") for i in d.index]
    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = list(range(len(d)))
    bw = 0.36
    ax.bar([i - bw / 2 - 0.02 for i in x], d.net_profit_group_share, width=bw, color=NEUTRAL, linewidth=0)
    ax.bar([i + bw / 2 + 0.02 for i in x], restated, width=bw, color=GREEN, linewidth=0)
    for i, (r, dl, rep) in enumerate(zip(restated, delta, d.net_profit_group_share)):
        ax.text(i + bw / 2 + 0.02, max(r, rep) + 0.3, f"{dl:+.1f}".replace("-", "\u2212"), ha="center", va="bottom", fontsize=8, color=INK)
    ax.set_xticks(x, labels, fontsize=8)
    _style(ax, (0, 26))
    ax.legend(["As reported", "Put remeasured through P&L"], frameon=False, fontsize=8, loc="upper left", ncol=2, handlelength=1, borderaxespad=0, columnspacing=1)
    return fig


FIGSIZE = (3.25, 1.75)   # one column of the two-column report


def diageo_basis_fv_mh() -> float:
    """100% of MH in EUR m on Diageo's multiples basis (AR 2026 note 6a): 5,107 - 0.9*FV34 = 388."""
    return (5107 - 388) / 0.9 * USD_EUR_JUN26 / DIAGEO_STAKE


def fv_figure(w: pd.DataFrame):
    """Implied fair value of 100% of Moët Hennessy (LVMH basis) and Diageo's own basis, Jun-2026."""
    d = (w.loc["FY2021":, "diageo_accumulated_nci"] + w.loc["FY2021":, "goodwill_on_commitments"]) \
        / PUT_PRICE / DIAGEO_STAKE / 1000
    labels = [i.replace("FY", "").replace("H1-2026", "H1 26") for i in d.index]
    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = list(range(len(d)))
    ax.plot(x, d.values, color=BLUE, linewidth=2, marker="o", markersize=5,
            markeredgecolor="white", markeredgewidth=1.2, zorder=3)
    for i in (0, 3):   # anchor the fall: start and the 2024 drop, up-right of the point
        ax.text(x[i] + 0.1, d.iloc[i] + 1.5, f"{d.iloc[i]:.0f}", ha="left", va="bottom", fontsize=8, color=INK)
    dg = diageo_basis_fv_mh() / 1000
    ax.plot([x[-1]], [dg], marker="D", markersize=5.5, color=ORANGE, markeredgecolor="white",
            markeredgewidth=1.2, linestyle="none", zorder=4)
    # Direct end labels, in series colour, right of each endpoint: name + value the text compares
    end = x[-1] + 0.22
    ax.text(end, d.iloc[-1] + 0.6, f"LVMH {d.iloc[-1]:.1f}", ha="left", va="bottom", fontsize=8,
            color=BLUE, fontweight="semibold")
    ax.text(end, dg - 0.6, f"Diageo {dg:.1f}", ha="left", va="top", fontsize=8,
            color=ORANGE, fontweight="semibold")
    ax.set_xticks(x, labels, fontsize=8)
    ax.set_xlim(-0.35, x[-1] + 1.35)
    ax.spines["bottom"].set_bounds(-0.35, x[-1] + 0.35)
    _style(ax, (0, 50))
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    return fig






def main(ticker: str) -> None:
    w = load()
    s = series_table(w)       # printed only: the figures carry these numbers in the report
    p = proforma_table(w)
    save_figure(entry_figure(w), "nci_put_entry")
    save_figure(flow_figure(w), "nci_put_flow")
    save_figure(pnl_figure(w), "nci_put_pnl")
    save_figure(fv_figure(w), "nci_put_fv")
    pd.set_option("display.width", 200)
    print(s.round(0).to_string())
    print()
    print(p.round(0).to_string())
    print(f"\nImplied FV of Moët Hennessy, LVMH basis FY2025: EUR {p.attrs['fv_mh']:,.0f}m; "
          f"Diageo multiples basis Jun-2026: EUR {p.attrs['fv_mh_diageo']:,.0f}m")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "MC.PA")
