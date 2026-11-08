# LVMH: the Diageo put over 34% of Moët Hennessy

Working notes for the memo. Argument, numbers and page citations.

Citation convention: "FD" = LVMH Financial Documents (consolidated FS + notes) for the year; "URD" = Universal Registration Document; "HFR" = half-year financial report. Page numbers are **PDF page indices** (what `verify_citations.py` checks), not the printed folio. Printed folio = PDF index − 2 for the FY2025 FD and URD. Every LVMH figure below is in `data/processed/lvmh_nci_put.csv` and was verified against the PDF page with `python3.12 analysis/verify_citations.py lvmh lvmh_nci_put` (58 verified, 0 missing).

Financial statements URL (FY2025 FD): https://lvmh-com.cdn.prismic.io/lvmh-com/aXjqHgIvOtkhB_8I_Financialdocuments-December31%2C2025.pdf

---

## 1. What the issue is, in one paragraph

Since 1994 Diageo has owned 34% of Moët Hennessy (MH), the holding company for almost all of LVMH's Wines & Spirits business (Hennessy, Moët & Chandon, Dom Pérignon, Veuve Clicquot, Krug, etc.). LVMH consolidates MH at 100%. Under a 1994 memorandum of understanding Diageo can, at any time and with six months' notice, require LVMH to buy the 34% for **80% of MH's fair value at the exercise date** (FD 2025 note 21, p. 56; URD 2025 parent-company note 21.1, p. 443). IAS 32.23 says that a written put over a subsidiary's shares is a financial liability for the present value of the redemption amount, so LVMH carries a liability called "Purchase commitments for minority interests' shares": **€6,331m at 31 Dec 2025**, down from €11,919m two years earlier (FD 2025 balance sheet, p. 26). IFRS says nothing about what to do with the other side of the entry or with later remeasurements. LVMH's answer (note 1.13, p. 33) is a grandfathered French practice: cancel Diageo's minority interest, and book the difference between the put value and that minority interest as **goodwill**, with every subsequent change in the put value also going through goodwill, never through profit. That goodwill "plug" was €9,070m in 2021 and is €386m today. The result is that LVMH's own valuation of its drinks business fell by roughly €30bn in four years and not one euro of it touched the income statement, while the liability itself sits outside LVMH's definition of net financial debt.

Why this is "tricky, untested, uncertain": (i) no IFRS standard covers it and the IASB is, right now, re-deliberating a standard (FICE) that would push the remeasurement through profit or loss; (ii) the amount is a Level-3 management estimate of a private company's fair value, and LVMH changed the valuation technique in FY2025; (iii) a non-technical reader sees a shrinking liability and thinks "good news", when it actually records a collapse in value; (iv) for a buyer it is a €4–6bn cash call on six months' notice held by a third party whose relationship with LVMH is strained.

---

## 2. The standards

- **IAS 32.23**: a contract that obliges an entity to purchase its own equity instruments (including a subsidiary's shares held by NCI, per IFRS 10 the NCI is equity of the group) for cash gives rise to a financial liability for the present value of the redemption amount, even if the obligation is conditional on the counterparty exercising. Reclassified from equity on initial recognition.
- **IFRS 10.23 / B96**: changes in a parent's ownership interest that do not result in loss of control are equity transactions. This is the hook LVMH and most French groups use to keep remeasurements out of P&L (for post-2010 puts; LVMH books those in "Other reserves" within equity, note 1.13).
- **IFRS 9 / IAS 32**: on a plain reading the liability is a financial liability measured at amortised cost / remeasured, with changes through P&L. This is what the IFRS Interpretations Committee concluded in Draft Interpretation DI/2012/2 "Put Options Written on Non-controlling Interests" (May 2012): remeasure through P&L. After 68 comment letters the IC said the draft reflected existing IFRS but doubted the information was useful; in March 2013 the IASB took the issue over and did not finalise the interpretation. Diversity in practice has persisted since. (IASB agenda paper 8, March 2013: https://cdn.ifrs.org/content/dam/ifrs/meetings/2013/march/iasb/puts-written-on-a-non-controlling/ap8-feedbac-received-draft-ifric-interpretation-possible-paths-forward.pdf)
- **FICE project** (Exposure Draft "Financial Instruments with Characteristics of Equity", published November 2023, comments closed 29 March 2024; redeliberations ongoing). At its 22 September 2026 meeting the IASB tentatively decided, 12–0, that gains and losses on remeasuring an NCI-put liability go to **profit or loss**; 9–3 that the initial debit is deducted from NCI without derecognising it, shown as a separate line; 11–1 that on expiry of the put the difference between the liability and the NCI deduction goes to P&L. Measurement of the liability (80% of FV vs. full FV?) not yet decided. No date for final amendments. EFRAG's board (June 2026) disagreed with P&L remeasurement. Sources: IASB Update September 2026 (https://www.ifrs.org/content/ifrs/home/news-and-events/updates/iasb/2026/iasb-update-september-2026.html); project page (https://www.ifrs.org/projects/work-plan/financial-instruments-with-characteristics-of-equity/).
- **LVMH's policy, note 1.13 (FD 2025, p. 33)**, verbatim structure: "Pending specific guidance from IFRSs regarding this issue, the Group recognizes these commitments as follows: the value of the commitment at the balance sheet date appears in 'Purchase commitments for minority interests' shares', as a liability; the corresponding minority interests are canceled; for commitments granted prior to January 1, 2010, the difference between the amount of the commitments and canceled minority interests is maintained as an asset on the balance sheet under goodwill, as are subsequent changes in this difference. For commitments granted as from January 1, 2010, the difference ... is recorded in equity, under 'Other reserves'. This recognition method has no effect on the presentation of minority interests within the income statement." The Diageo put dates from 1994, so it is the pre-2010 "goodwill" method. Loro Piana (6%) and Middle-East distribution puts are post-2010, through equity.
- **Note 5 (FD 2025, p. 40)**: "Brands, trade names and other intangible assets with indefinite useful lives as well as the goodwill arising on acquisition were subject to annual impairment testing." The goodwill arising on purchase commitments is *not* in that sentence. It is not impairment-tested; it is simply re-plugged each year from the put valuation.
- **Net financial debt, note 19.1 (FD 2025, p. 53)**: "Net financial debt does not include purchase commitments for minority interests' shares (see Note 21) or lease liabilities (see Note 7)." Reported NFD €6,857m.
- **Disclosure of the valuation**: through H1-2025 the FV was "calculated by applying the share price multiples of comparable firms to Moët Hennessy's consolidated operating results" (FD 2021 note 21, p. 55; FD 2022 p. 56; FD 2023 p. 56; FD 2024 p. 57; HFR H1-2025). In FY2025 the wording became "based on Moët Hennessy's discounted future cash flows, calculated according to the method described in Note 1.16" (FD 2025 p. 56; HFR H1-2026 p. 45). A change of valuation technique with no reason given and no sensitivity disclosed. IFRS 13.93(d) and (h) ask for the technique, a description of any change in it and the reasons, and a narrative sensitivity for Level 3 measurements; the put is not in LVMH's fair-value hierarchy table at all (it is not a fair-value measurement in the IFRS 13 sense, LVMH would argue, because it is the redemption amount under IAS 32). Either way the reader gets no sensitivity.
- **Auditor**: the FY2025 key audit matters are intangible asset valuation, inventories and provisions (URD 2025, statutory auditors' report, p. 411). The put is not a KAM in its own right; it is covered only indirectly through the W&S cash-flow forecasts used for impairment testing.

---

## 3. The numbers

### 3.1 The series (EUR m)

| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | H1-2026 |
|---|---|---|---|---|---|---|
| Put liability (balance sheet) [a] | 13,677 | 12,489 | 11,919 | 8,056 | 6,331 | 6,416 |
| of which goodwill counterpart [b] | 9,070 | 6,899 | 5,682 | 1,239 | 386 | 382 |
| Diageo's share of MH equity, before the put [c] | 3,775 | 4,265 | 4,281 | 4,332 | 4,341 | 4,369 |
| Implied Diageo put = [b]+[c] | 12,845 | 11,164 | 9,963 | 5,571 | 4,727 | 4,751 |
| Implied FV of 100% of MH = put / 0.8 / 0.34 | 47,224 | 41,044 | 36,629 | 20,482 | 17,379 | 17,467 |
| Goodwill movement "Changes in purchase commitments" [d] | +2,467 | −2,204 | −1,235 | −4,378 | −900 | +6 |
| Net profit attributable to Diageo | 432 | 480 | 480 | 276 | 177 | 110 (H1) |
| Dividends paid to Diageo | 143 | 217 | 241 | 241 | 141 | 89 |
| Net profit, Group share | 12,036 | 14,084 | 15,174 | 12,550 | 10,878 | |

Earlier years: liability €10,735m (2019), €10,991m (2020); goodwill counterpart €6,597m (2020) (FD 2021, pp. 26, 41).

Sources, by row: [a] FD balance sheets, PDF p. 26 in each of FD 2021–2025; HFR H1-2026 p. 24. [b] and [d] FD note 4 "Goodwill": FD 2021 p. 41, FD 2022 p. 39–40, FD 2023 p. 40, FD 2024 p. 40, FD 2025 p. 40; HFR H1-2026 p. 30. [c] and the Diageo profit/dividend lines: FD note 18 "Minority interests" (note 17 in FD 2021): FD 2021 p. 52, FD 2022 p. 52, FD 2023 p. 52, FD 2024 p. 53, FD 2025 p. 53; HFR H1-2026 p. 42. Net profit: FD 2025 income statement p. 24 (2023–25); FD 2023 p. 24 (2021–22, from the same line; 12,036 and 14,084 appear at FD 2023 line "Net profit, Group share").

Caveat on the "implied" rows: the goodwill counterpart covers all pre-2010 commitments, which note 21 says are "mainly" the Diageo put, so [b]+[c] slightly overstates the Diageo put and the implied FV. The residual (liability minus [b]+[c]) is €0.8–2.5bn and covers Loro Piana (15% until 2024, 6% now) and Middle-East distributors. Treat the implied FV as "about", good to ±10%.

### 3.2 What the series says

1. **LVMH's own valuation of Moët Hennessy went from about €47bn (end-2021) to about €17bn (end-2025)**, i.e. roughly −€30bn, or −€20bn for LVMH's 66%. None of that is in the income statement. The mechanism: the put liability fell by €7.3bn over the period; €8.7bn of that fall (sum of [d] for 2022–25) was booked as a *reduction of goodwill*, the rest is Diageo's rising equity share. Compare: the group's total goodwill went from €25,904m (2021) to €18,315m (2025) (FD 2025 note 4, p. 40) and the W&S segment's "intangible assets and goodwill" went from €7,775m (2023) to €3,512m (2024) to €2,423m (2025) (FD 2025 note 24.1, pp. 61–63). A €5.4bn fall in a segment's intangibles with no impairment charge. The CFO's only comment (H1-2024 call, 23 July 2024): "Intangible assets declined due to the decrease in purchase commitments for minority interest."

2. **The operating reason is real.** W&S profit from recurring operations: €2,109m (2023), €1,356m (2024), €1,016m (2025) (FD 2025 management report 1.2, p. 9–10); revenue €5,358m in 2025, −9%. Cognac demand in the US and China collapsed, China imposed provisional anti-dumping deposits on EU brandy in Oct-2024 (final duties July 2025, Hennessy exempted via a price undertaking), US tariffs hit from 2025, and MH announced 1,200 job cuts in May 2025 (see `sources/lvmh/news/INDEX.md`). Diageo's own reported profit from the MH stake and related JVs went from $455m (FY to June 2023) to $219m (FY2025) (Reuters via Vinetur, 4 Aug 2026).

3. **The liability is "net-debt-like" and is excluded from net debt.** NFD €6,857m vs. put liability €6,331m: adding it almost doubles the figure to €13.2bn (and leases are another €16.0bn, FD 2025 BS p. 26). The put is exercisable at any time on six months' notice. LVMH SE's parent-company accounts show €6,913m of share purchase commitments off balance sheet (URD 2025 p. 443). Undrawn confirmed credit lines €10.8bn (URD 2025 p. 443), so liquidity is not the problem; price is.

4. **The 80% is a discount to LVMH, not to the buyer.** The liability is 80% of FV because that is the strike. If an acquirer wants to own 100% of MH (likely, since nobody buys LVMH to keep a 34% partner in its second-oldest business), it must negotiate: Diageo will not exercise at a 20% haircut (its CEO said in Aug-2026 he is not looking to sell "at this stage", Reuters). At LVMH's own FV the buy-out cost is €5.9bn (= 4,727 / 0.8), not €4.7bn; and the FV itself is a trough number (2024 and 2025 were the worst years for cognac in a decade). At the 2023 valuation the same 34% was worth €12.5bn. The acquirer's "true" cost of consolidating 100% of MH is somewhere between €4.7bn and €12bn depending on timing and negotiation. The balance sheet shows €4.7bn.

5. **Cross-check with Diageo's own books (Diageo Annual Report 2026, note 6, printed p. 157; `sources/diageo/pdf/FY2026_financial-statements.pdf` page 24; same text on EDGAR: https://www.sec.gov/Archives/edgar/data/835403/000162828026057527/dia045-arax2026annualrep.htm).** Diageo carries its 34% at $5,107m at 30 June 2026 ($5,149m at 30 June 2025, $4,608m at 30 June 2024) under the equity method, i.e. €4.4bn at the $1 = €0.86 rate it uses, against LVMH's €4,369m "share of accumulated minority interests" at the same date. The two books agree on Diageo's share of MH's *book* equity. Diageo's summarised MH results (its own policies, incl. brand fair-value adjustments): profit for the year $1,299m (FY to June 2024), $644m (2025), $668m (2026); net assets $15,215m. Diageo tests the stake at fair value less costs of disposal on an **EBITDA multiple**, says the investment "is sensitive to reasonably possible changes in assumptions", and discloses that a 1.0x drop in the multiple would cause a $312m impairment and a 10% EBITDA drop a $388m impairment. The same note says the 1994 arrangements "contain certain provisions for the protection of Diageo as a non-controlling shareholder in Moët Hennessy", without saying what they are. Solving: 5,107 − 0.9·FV = 388 gives FV of the 34% ≈ $5.24bn, i.e. a multiple of about 11.7x EBITDA and a fair value for 100% of MH of about **€13.3bn** on Diageo's basis vs **€17.4bn** on LVMH's DCF basis (different dates, FX and policies, so indicative only). On Diageo's basis LVMH's put liability for Diageo would be about **€3.6bn**, €1.1bn lower than booked. So a reasonable range of "fair value" from the two parties' own numbers is €13–17bn, and the liability moves €0.27bn for every €1bn of MH value. The point for the buyer is not which is right; it is that headroom on Diageo's side is a few hundred million dollars, i.e. the partner's own number sits at the bottom of the range, and that LVMH switched from multiples to DCF in the very year the multiples would have given the lowest answer.

6. **Earnings would look very different under the IASB's current proposal.** If remeasurement had gone through P&L (the Sept-2026 tentative FICE decision), the goodwill movements in [d] become gains/losses: FY2021 a €2.5bn loss (net profit €12.0bn would have been €9.6bn), FY2024 a €4.4bn gain (€12.6bn becomes €16.9bn, +35%), FY2025 a €0.9bn gain. Group net profit would have been more volatile by ±20–35% in three of the last five years from one line. For the acquirer: (i) forecast P&L for LVMH post-deal should include a line "remeasurement of the Diageo put", and (ii) any earnout, covenant or management incentive referencing IFRS net profit needs to carve it out. Also, under the FICE proposal the initial debit goes to equity (deducted from NCI, not to goodwill), so group equity would be lower by the goodwill plug: a trivial €0.4bn now, but it was €9.1bn in 2021. Pre-2010 grandfathering would almost certainly not survive a new standard.

7. **Cash leakage.** 34% of MH's dividends go out: €141m in 2025, €241m in 2023 and 2024. And the dispute history matters: in 2020 MH withheld €181m of 2019 dividends after Covid, Diageo started arbitration, the dividend was paid in 2021 (Reuters, Aug 2026). The partnership has since shed the French distribution JV (1 Jan 2025, Diageo paid $145m termination costs) and the Japan, Singapore and Thailand JVs (1 July 2026) (Diageo AR 2026 note 6). The relationship a buyer inherits is a contractual one, not a friendly one.

8. **Change-of-control terms are asymmetric and not disclosed by LVMH.** Diageo's directors' report ("Significant agreements – change of control") says that if a *Competitor* takes control of Diageo, defined as acquiring more than 34% of its votes or equity, LVMH may require Diageo to sell the MH and MHI interests to LVMH (Diageo AR 2026, printed p. 130; `sources/diageo/pdf/FY2026_annual-report.pdf` page 132). LVMH's filings say nothing about what happens if control of *LVMH* changes. Whether Diageo's put price, notice period or the "80%" changes on a change of control of LVMH is the first question for the data room.

### 3.3 Moët Hennessy's own balance sheet (FD 2025 note 18, p. 53; EUR bn)

PP&E and intangibles 6.5; inventories 8.4 (the ageing eaux-de-vie and champagne); cash 1.7; equity 12.6; short-term borrowings 2.0; total 19.2. Diageo's 34% of book equity = 4.3 = line [c]. So LVMH values MH at ~1.4x book, Diageo at ~1.05x book. For a business that reported €1.0bn of recurring operating profit and €2.1bn two years earlier, that is the whole debate.

### 3.4 Impairment-test assumptions for W&S (URD 2025 note 5, p. 357)

Post-tax discount rate 6.9% (pre-tax 9.3%), revenue growth 5.0% p.a. during the plan, terminal growth 2.1–3.5%. 2024: 6.9–7.4% and 4.8% / 2.0%. The 2025 terminal growth range (up to 3.5%) is the highest of any business group, and the discount rate is the lowest. The same DCF now drives the put. A 1-point higher discount rate or 0.5-point lower terminal growth typically moves a DCF of this profile by 15–20%, i.e. €2.5–3.5bn of MH value, €0.7–1.0bn of liability. LVMH gives the sensitivity only for Tiffany/TAG Heuer (URD 2025 p. 358), not for W&S or for the put.

---

## 4. What it means for the acquirer (the "so what")

**Misreading risk if the statements are taken at face value**

- *Net debt*: €6.9bn reported; €13.2bn with the put; the put is callable on six months' notice. Rating agencies and most sell-side models already add it back, but a headline EV/EBITDA using reported NFD is 0.3x too low.
- *Earnings quality*: none of the €30bn swing in LVMH's own valuation of its drinks arm is in P&L, and W&S intangibles fell €5.4bn with no impairment line. Reported net profit is clean of the problem; the balance sheet absorbed it silently. Under the IASB's current direction that changes, and the line would have swung net profit by −20% to +35% in recent years.
- *Equity / NCI*: "Minority interests" of €1,477m on the balance sheet exclude Diageo entirely (it is in the liability instead). Anyone computing "equity attributable to NCI" or a sum-of-the-parts that strips out minorities at book will miss the 34% of W&S.
- *Buy-out cost*: the liability (€4.7bn for Diageo) is 80% of a trough DCF. Owning 100% of MH will cost €6bn+ and could cost double that if the cognac cycle turns before the deal closes. Conversely, if Diageo's new CEO decides to exit at the trough, LVMH (and thus the acquirer) gets the 34% at a 20% discount: the put is an asset for the buyer in that scenario, and a reason for Diageo not to exercise.
- *Valuation of the W&S segment in the SOTP*: LVMH's own number (€17bn for 100%, €11.5bn for its 66%) and Diageo's (€13bn) are on the table; neither is audited as a fair value. Both are far below the €40–47bn LVMH was carrying in 2021–22. The acquirer should run its own DCF and multiple (Rémy Cointreau, Pernod, Diageo, Campari trade at 10–14x EBITDA in 2026) rather than lean on either.

**What the team should do next**

1. Data room request: the 20 Jan 1994 memorandum of understanding and shareholders' agreement with Diageo in full: strike mechanics ("market value" definition, who values, dispute mechanism), the six-month notice, change-of-control and competitor clauses on both sides, tag/drag rights, dividend policy (the 2020 dispute), non-compete (Diageo may not do champagne/cognac), and whether the put survives a change of control of LVMH.
2. Model the put as debt (€4.7bn booked, €5.9bn at 100% FV, scenario €8–12bn on a recovered cycle) and as a P&L line (±€1–4bn/yr) in the post-deal forecasts; carve it out of any covenant or earnout.
3. Rebuild MH's valuation independently: the DCF inputs (URD note 5), Diageo's multiples cross-check, and a bottom-up on cognac inventory (€8.4bn of MH inventories are mostly ageing stock whose value depends on the same demand assumptions).
4. Decide the strategic question early: keep Diageo as a 34% partner (and accept the cash leakage, the JV frictions and the overhang), negotiate a buy-out as part of the deal (price above 80% FV, probably at or above 100%), or offer Diageo the whole of MH (Diageo has reportedly wanted to go the other way; Bloomberg Jan 2025). The answer changes the deal's funding need by €5–12bn.
5. Watch the FICE timetable: if final amendments are issued before closing, the pro-forma P&L and equity presented to financing banks change.

**Does it change the decision to proceed?** Not on its own. It is a known, quantified, financeable liability, and the current trough valuation makes the timing favourable for a buyer who wants 100% of MH. But it moves the price: the acquirer should treat €5–6bn as the floor cost of owning the drinks business outright, price the W&S segment on its own numbers rather than LVMH's goodwill history, and not sign without the 1994 agreement in hand.

---

## 5. Illustrative calculations to put in the memo

(generated by `analysis/analysis.py`: `report/tables/nci_put_series.tex`, `report/tables/nci_put_proforma.tex`, `report/figures/nci_put_decomposition.pdf`)

- Decomposition chart: Diageo put = share of MH equity (flat ~€4.3bn) + goodwill plug (€9.1bn → €0.4bn), 2021–H1 2026.
- Pro-forma box (EUR m, FY2025): NFD 6,857 + put 6,331 = 13,188. Diageo put as booked 4,727; at 100% FV 5,909; on Diageo's multiples basis 3,607. FY2024 net profit 12,550 → 16,928 if the €4,378m goodwill movement had been a P&L gain.
- Implied FV path of MH: 47 → 41 → 37 → 20 → 17 (EUR bn, 2021–2025).

---

## 6. Things I checked that did not change the story

- Diageo's book value of the stake (€4.4bn) ≈ LVMH's cancelled NCI (€4.37bn): the two sets of books reconcile at book equity; the disagreement is only on fair value.
- Reuters (Aug 2026) quotes Diageo's MH interests as "worth about €4.3bn in 2025": that is the book equity figure from LVMH's note 18, not the put value.
- The Loro Piana and Middle-East puts are post-2010 and go through equity; the "Impact of changes in minority interests with purchase commitments" line in note 18 (−€88m in 2025, −€120m in 2024) is their annual reclassification, not a Diageo item.
- DFS: Mari-Cha's 39% stake has no put; DFS was classified as held for sale at 31 Dec 2025 (note 2). Not part of this issue.
- The H1-2026 liability rose slightly to €6,416m (goodwill plug flat at €382m), consistent with W&S organic sales +5% in H1 2026 and no further markdown.

## 7. Open points / to verify before the final draft

- (done) 2021 and 2022 net profit (12,036 and 14,084) verified on FD 2023 p. 24 and added to the CSV.
- (done) Diageo figures verified against the PDF (financial statements 2026, note 6, printed p. 157 = PDF page 24); the PDFs are in `sources/diageo/pdf/` with `SOURCES.txt`.
- The March 2013 IASB decision wording: cite the IASB Update March 2013 rather than the staff paper if possible.
- Whether LVMH's FY2025 change of valuation technique was mentioned anywhere (results call, URD): nothing found in the transcripts or the URD text search.
