# LVMH: the Diageo put over 34% of Moët Hennessy

Draft write-up of the analysis, 8 November 2026. Detailed workings and citations are in `nci-put-diageo.md`; every figure below is in `data/processed/lvmh_nci_put.csv` and verified against the cited PDF page.

Financial statements: LVMH Financial Documents, 31 December 2025, https://lvmh-com.cdn.prismic.io/lvmh-com/aXjqHgIvOtkhB_8I_Financialdocuments-December31%2C2025.pdf (cited as "FD 2025"; page numbers are PDF page indices).

---

## Executive summary

### What is the issue?

LVMH is the world's largest luxury group (revenue €80.8bn in 2025). Its Wines & Spirits arm, Moët Hennessy (Hennessy cognac, Moët & Chandon, Dom Pérignon, Veuve Clicquot, Krug), is 34% owned by Diageo and has been since 1994. LVMH consolidates it in full. Under the 1994 agreement Diageo can, at any time and with six months' notice, require LVMH to buy the 34% for 80% of Moët Hennessy's fair value (FD 2025 note 21, p. 56).

IAS 32 makes that promise a financial liability. LVMH shows it as "Purchase commitments for minority interests' shares": €6.3bn at end-2025, down from €11.9bn two years earlier (FD 2025 balance sheet, p. 26). No IFRS standard says what to do with the other side of the entry or with the yearly revaluation. LVMH's answer, a grandfathered French practice (note 1.13, p. 33), is to cancel Diageo's minority interest and book the difference, and every later change in it, in goodwill. The income statement is never touched.

### Why is it relevant?

- **The shrinking liability is not good news.** It records LVMH's own valuation of its drinks business falling from about €47bn (2021) to about €17bn (2025). The write-down was absorbed by a goodwill "plug" that went from €9.1bn to €0.4bn and is never impairment-tested. Wines & Spirits segment intangibles fell by €5.4bn in two years with no impairment charge.
- **Net debt is understated.** LVMH's net financial debt of €6.9bn excludes the put. With it, debt-like obligations are €13.2bn, and the put is callable on six months' notice.
- **The booked €4.7bn is 80% of a trough valuation.** A buyer who wants 100% of Moët Hennessy will pay at least €5.9bn at LVMH's own fair value, and far more if the cognac cycle turns first. At the 2023 valuation the same stake was worth €12.5bn.
- **The valuation is a management estimate that just changed method.** Through mid-2025 LVMH used peer multiples; in FY2025 it switched to its own DCF, with no reason given and no sensitivity. Diageo's books value the stake lower (around €13bn for 100%, with only a few hundred million dollars of headroom).
- **Earnings may soon swing with it.** In September 2026 the IASB tentatively decided (12 votes to 0) that remeasurement of such puts must go through profit or loss. On that basis FY2024 net profit would have been €16.9bn, not €12.6bn, and FY2021 €2.5bn lower.
- **The partner is not friendly and the contract is not disclosed.** A 2020 arbitration over €181m of withheld dividends, three distribution JVs terminated since, and change-of-control rights that LVMH's filings do not describe.

### What should we do?

1. Get the 20 January 1994 memorandum of understanding and shareholders' agreement into the data room before anything else: how "market value" is set and by whom, the six-month notice, change-of-control clauses on both sides, dividend rules, the "protections for Diageo as a non-controlling shareholder" that Diageo mentions but neither party spells out.
2. Treat the put as debt in the price: €4.7bn booked, €5.9bn at full fair value, €8–12bn in a recovered-cycle scenario. Model a ±€1–4bn per year remeasurement line in post-deal P&L and carve it out of covenants and earn-outs.
3. Value Wines & Spirits independently. Neither LVMH's €17bn nor Diageo's €13bn is an audited fair value; both are far below the €40–47bn carried in 2021–22.
4. Decide early whether to keep Diageo as a 34% partner, negotiate a buy-out as part of the deal (above 80% of fair value, probably at or above 100%), or sell Moët Hennessy to Diageo. The answer moves the funding need by €5–12bn.
5. Proceed, but on these terms. The liability is known, quantified and financeable, and the trough makes the timing favourable for a buyer who wants 100% of the drinks business. It changes the price, not the decision.

---

## Technical memo (condensed)

### The standard and LVMH's choice

IAS 32.23: a contract obliging an entity to buy its own equity instruments, including a subsidiary's shares held by a minority, is a financial liability for the present value of the redemption amount, whether or not exercise is likely. That part is settled. What is not settled is the debit entry and the remeasurement. IFRS 10.23 treats changes in ownership without loss of control as equity transactions; a plain reading of IFRS 9 would remeasure the liability through profit or loss. The IFRS Interpretations Committee proposed P&L remeasurement in 2012 (DI/2012/2), the IASB shelved it in 2013, and practice has diverged since. The IASB's FICE project (Exposure Draft, November 2023; redeliberations ongoing; no final date) is now heading towards P&L remeasurement, with the initial debit deducted from NCI.

LVMH, note 1.13 (FD 2025, p. 33): the commitment is a liability; the minority interest is cancelled; for commitments granted before 1 January 2010 the difference, "as are subsequent changes in this difference", goes to goodwill; for later commitments it goes to equity. The Diageo put is pre-2010, so it is the goodwill route. The resulting "goodwill arising on purchase commitments" is reported separately in note 4 (p. 40) and is not in the list of assets that note 5 says are impairment-tested.

### What the numbers say (EUR m)

| | 2021 | 2022 | 2023 | 2024 | 2025 | H1 2026 |
|---|---|---|---|---|---|---|
| Put liability (balance sheet) | 13,677 | 12,489 | 11,919 | 8,056 | 6,331 | 6,416 |
| of which goodwill counterpart | 9,070 | 6,899 | 5,682 | 1,239 | 386 | 382 |
| Diageo's share of Moët Hennessy equity | 3,775 | 4,265 | 4,281 | 4,332 | 4,341 | 4,369 |
| Implied Diageo put (sum of the two) | 12,845 | 11,164 | 9,963 | 5,571 | 4,727 | 4,751 |
| Implied fair value of 100% of Moët Hennessy | 47,224 | 41,044 | 36,629 | 20,482 | 17,379 | 17,467 |
| Goodwill movement, booked outside P&L | +2,467 | −2,204 | −1,235 | −4,378 | −900 | +6 |
| Net profit, Group share | 12,036 | 14,084 | 15,174 | 12,550 | 10,878 | |

Sources: balance sheets (PDF p. 26 of each year's FD; H1-2026 HFR p. 24), note 4 Goodwill (FD 2025 p. 40 and prior years), note 18 Minority interests (FD 2025 p. 53 and prior years), income statement (FD 2025 p. 24, FD 2023 p. 24). Implied fair value = put / 0.8 / 0.34; the goodwill line covers all pre-2010 commitments, "mainly" Diageo, so treat the implied values as approximate.

The operating cause is real: Wines & Spirits profit from recurring operations fell from €2,109m (2023) to €1,356m (2024) to €1,016m (2025) (FD 2025 p. 9–10); Diageo's summarised Moët Hennessy profit halved from $1.3bn (FY to June 2024) to $0.65bn (FY2025 and FY2026). Diageo's own test of its stake (AR 2026 note 6, p. 157) uses an EBITDA multiple, calls the investment "sensitive to reasonably possible changes", and discloses that a 1.0x lower multiple would cost $312m and 10% lower EBITDA $388m. Solving those gives a fair value of about $5.2bn for the 34%, roughly €13.3bn for 100%, versus €17.4bn on LVMH's DCF. On Diageo's basis LVMH's liability for the put would be about €3.6bn, €1.1bn below what is booked. Each €1bn of Moët Hennessy value moves the liability by €0.27bn.

### Pro-forma for the acquirer (FY2025, EUR m)

| | |
|---|---|
| Reported net financial debt | 6,857 |
| + put liability | 6,331 |
| = debt-like total | 13,188 |
| Diageo put as booked (80% of fair value) | 4,727 |
| Cost to buy Diageo out at 100% of LVMH's fair value | 5,909 |
| Diageo put on Diageo's own multiples basis | 3,607 |
| FY2024 net profit as reported | 12,550 |
| FY2024 net profit if the €4,378m goodwill movement had been a P&L gain | 16,928 |

### What LVMH discloses, and what it does not

Disclosed: the strike (80% of fair value), the notice period, the valuation technique (one sentence), Diageo's share of profit and equity, dividends paid to Diageo, Moët Hennessy's condensed balance sheet (equity €12.6bn, inventories €8.4bn), and the exclusion from net financial debt. Not disclosed: any sensitivity of the put value, the reason for the FY2025 change from multiples to DCF, the change-of-control terms, and the minority protections. The put is not a key audit matter; the auditors cover it only through the Wines & Spirits cash-flow forecasts used for impairment testing (URD 2025 p. 411), where the business group carries the lowest discount rate (6.9% post-tax) and the highest terminal growth range (2.1–3.5%) in the group (URD 2025 p. 357).

---

## Status of the project files

- `report/notes/nci-put-diageo.md`: full argument, citations, open points.
- `data/processed/lvmh_nci_put.csv`: 66 figures; the 61 LVMH figures verify against their PDF pages with `verify_citations.py lvmh lvmh_nci_put` (0 missing); the 5 Diageo figures were checked by hand in `sources/diageo/pdf/`.
- `analysis/analysis.py` writes `report/tables/nci_put_series.tex`, `report/tables/nci_put_proforma.tex`, `report/figures/nci_put_decomposition.pdf` and `report/figures/nci_put_pnl.pdf`.
- `report/sections/*.tex`: executive summary (page 1, three headings), technical memo (pages 2–4, five numbered subsections, two tables, one two-panel figure, 16 footnotes) and a draft AI-use note, written 8 November 2026. `make report` compiles to 5 pages (margins 2.05 cm, 12 pt).
- Still to do: student number in `main.tex`; review the first-person AI-use note; the two small checks at the end of the notes (wording of the IASB's 2013 decision; whether LVMH ever explained the FY2025 valuation-method change). Nothing is committed yet.
