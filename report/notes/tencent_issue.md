# Working notes: Prosus and the equity-accounted stake in Tencent (IAS 28)

These are analysis notes for writing the memo, not memo prose. Every number below is in
`data/processed/prosus_tencent.csv` with its source, and `analysis/verify_citations.py`
confirms each annual-report figure appears on the cited PDF page. Page references are the
printed page numbers of each annual report (AR); FY2024 uses the report's own "section/page"
numbering (e.g. 5/133). All amounts US$m unless stated. Prosus's year ends 31 March.

## 1. The issue in one paragraph

Prosus owns 22.66% of Tencent. It does not control Tencent, so it uses the equity method:
the stake sits on the balance sheet at US$42.2bn (cost plus Prosus's share of Tencent's
retained profits, less dividends), while the same shares were quoted at US$127.6bn on
31 March 2026. Prosus's consolidated profit of US$11.65bn is almost entirely Tencent: a
US$7.26bn share of Tencent's profit that never arrives as cash, plus a US$4.7bn "gain" that is
simply the quoted/carrying gap crystallising on the 0.9% of Tencent sold during the year.
Cash dividends from associates were US$1.24bn and the group generated US$472m from
operations. Everything a buyer would normally read off the statements (earnings, tax rate,
equity, gains) is shaped by one accounting choice that is itself resting on a judgement
(significant influence) that gets thinner every year Prosus sells.

## 2. The numbers (31 March)

| | FY2022 | FY2023 | FY2024 | FY2025 | FY2026 |
|---|---|---|---|---|---|
| Stake (%) | 28.81 | 26.16 | 24.61 | 23.49 | 22.66 |
| Quoted value | 132,311 | 122,952 | 90,213 | 138,167 | 127,637 |
| Carrying value | 34,837 | 29,827 | 30,138 | 36,544 | 42,172 |
| Gap | 97,474 | 93,125 | 60,075 | 101,623 | 85,465 |
| Share of Tencent profit (IFRS) | 9,863 | 6,994 | 4,072 | 6,306 | 7,262 |
| Tencent in core headline earnings | 5,413 | 4,326 | 5,387 | 7,263 | 8,117 |
| Cash dividend | 571 | 565 | 759 | 1,001 | 1,237* |
| Dividend in specie | 3,900 (JD.com) | 4,500 (Meituan) | – | – | – |
| Tencent shares sold, proceeds | 14,600 | 10,700 | 7,200 | 8,500 | 6,500 |
| Gain booked on those sales | 12,340 | 7,600 | 5,100 | 6,000 | 4,700 |
| Group profit for the year | 18,594 | 10,022 | 6,590 | 12,366 | 11,650 |

*FY2026 figure is dividends from all associates (cash flow statement, p.143); the liquidity
note says US$1.2bn came from Tencent.

Sources: FY2026 AR note 9 pp.155–156; FY2025 AR note 9 pp.147–149; FY2024 AR note 9
pp.5/133–5/135; FY2023 AR note 9 pp.206–208; FY2022 AR note 9 pp.172–174 and note 6 p.163;
IFRS profit share and core HE contribution from the KPI datasheets ("Contribution by Tencent")
and FY2026 AR segment note p.168 and APM reconciliation p.233.

Composition of the FY2026 carrying value (note 9, p.156): share of Tencent's net assets
35,547 + "goodwill" 6,625 = 42,172. Tencent's own numbers (calendar 2025, as used by Prosus):
net profit 31,792; closing net assets after NCI 157,056; Prosus's 22.66% of that is 35,547.

Group context FY2026 (income statement p.140, balance sheet p.139, cash flow p.143):
revenue 9,705; operating loss (173); share of associates' results 6,871; gains on partial
disposal of associates 4,858; profit before tax 11,778; tax (117); profit 11,650; total
assets 79,075; equity 53,867; investments in associates 44,848; cash generated from
operations 472; cash from partial disposals of associates 6,866. Financial review p.35:
US$12.5bn cash incl. short-term investments, net of US$17bn interest-bearing debt.

## 3. The accounting (memo section 1)

* **Standard.** IAS 28 *Investments in Associates and Joint Ventures*. Significant influence is
  presumed at 20% or more of the votes (IAS 28.5) and Prosus's chair sits on Tencent's board
  (FY2026 AR p.86: the chair "receives no compensation for serving on the board of Tencent").
  Prosus accounts for Tencent as an associate (note 9, p.155) and the auditor treats it as a key
  audit matter (p.223), as does the audit committee (pp.58–59).
* **Measurement.** Equity method (IAS 28.10): cost, plus share of post-acquisition profit and OCI,
  less distributions. The reconciliation in note 9 (p.156) shows the moving parts for the year:
  share of results 6,889, share of OCI/NAV changes (303), dividends (1,237), FX translation
  2,058, partial disposal (1,866), goodwill and intangibles recognised 2,370 (this last one is the
  re-allocation of Tencent's net assets when Tencent buys back its own shares above book value,
  footnote 2; the goodwill inside the carrying amount went from 2,354 in FY2024 to 6,625 in FY2026).
* **Lag.** Tencent closes in December, Prosus in March. Prosus uses a lag of up to three months
  and adjusts for "significant transactions and events" in the gap (note 3, p.145); the auditor
  tested the lag adjustments against Tencent's Q1 2026 results (p.223). So Prosus's FY2026 share
  of profit is essentially Tencent's calendar-2025 profit at Prosus's average stake and
  US$/RMB 7.08 (KPI datasheet).
* **Partial disposals.** Selling shares while keeping significant influence: derecognise the
  proportionate carrying amount, recognise proceeds less that amount as a gain, recycle the
  proportionate FX reserve (IAS 28.25). FY2026: 95,572,900 shares sold for 6.5bn, gain 4.7bn
  (note 5 p.145; note 9 p.156). The gain per percentage point sold at March 2026 prices is
  about 3.8bn (5,633 quoted less 1,861 carrying).
* **Dilution.** Tencent's buy-backs raise Prosus's percentage; employee share issues lower it.
  Net dilution gain 4 in FY2026, loss 318 in FY2025 (income statement p.140; note 9 p.156).
* **Impairment.** IAS 28.40–43 route the test through IAS 36 at the level of the whole
  investment; a quoted price is a Level 1 fair value (note 9 p.155). Headroom is 85bn, so no
  test could ever bite at Prosus. Management's indicator check compares market price and
  analyst consensus with carrying value per share (audit committee p.59).
* **Deferred tax.** None on associates: "distributions from associates do not have tax
  consequences" (note 9 p.156). Dutch participation exemption on the shares held through
  MIH Internet Holdings B.V.; Tencent is Cayman-incorporated and Hong Kong-listed, so no
  capital-gains tax or dividend withholding at source. Effective tax rate on the group's
  11,778 pre-tax profit: 1%.

## 4. Where judgement enters (memo section 2)

1. **Significant influence at 22.66% and falling.** Net reduction in FY2026 was 0.83 pp
   (23.49 to 22.66) even after Tencent's own buy-backs helped. At that pace the stake reaches
   20% in about 3.2 years; sales continued after year end (11,303,000 shares for US$675m,
   April to 24 June 2026, p.205). Prosus does not list "significant influence over Tencent"
   among its critical judgements in note 3 (only the lag-period judgement is listed). The
   indicators in IAS 28.6: board representation (one seat, the Prosus chair), participation in
   policy decisions (no evidence), material transactions (no), interchange of staff (no),
   essential technical information (no). The 20% line is a rebuttable presumption, not a rule,
   so the judgement can go either way near 20%, and that is precisely where it becomes an
   accounting cliff.
2. **What happens if influence is judged lost (IAS 28.22).** The retained interest is remeasured
   to fair value through profit or loss: a one-off gain of roughly 85bn at March 2026 values,
   1.6 times group equity. The shares then become an IFRS 9 financial asset. Prosus's own
   precedent in FY2026 is Delivery Hero: when it lost significant influence it elected FVOCI
   (note 6, p.150ff; loss of 648m incl. recycled FX). Under FVOCI, later price moves never touch
   profit; only dividends do. Reported profit would fall from ~12bn to ~1bn with nothing
   economic having changed, and the "gain on partial disposal" machine would stop.
3. **Lag-period adjustments.** Management "exercises significant judgement when determining
   the transactions and events for which adjustments are made" (note 3 p.145). The KPI datasheet
   notes that the IFRS share includes "material gains and losses during the 3 month lag period".
   This is where a Tencent impairment or fair-value swing in January to March can be pulled
   into, or left out of, Prosus's year.
4. **Core headline earnings.** Prosus's headline metric (p.233) starts from Tencent's IFRS profit
   (7,262) and adds back Tencent's equity-settled share-based payments (920), amortisation
   (371) and impairments/fair-value items. Tencent's contribution is 8,117 of group core HE of
   8,340, i.e. 97%. An acquirer reading "core HE up 13%" is reading Tencent, with Tencent's
   stock compensation treated as if it were free.
5. **Impairment indicators** are judged by management against market price and consensus; a
   mechanical exercise today, but see section 6 for why it stops being mechanical the moment a
   buyer steps up the stake to fair value.
6. **Dividends in specie.** JD.com shares (3.9bn, FY2022) and Meituan shares (4.5bn, FY2023)
   were received as dividends, reduced the carrying amount, and were then held at FVOCI and sold.
   Big returns of capital that never went through profit; useful illustration of how little of
   Tencent's value transfer shows up in the income statement.

## 5. What Prosus discloses, and what it doesn't (memo section 3)

Discloses: accounting policy and lag policy (note 3 p.145); significant transactions incl. the
share counts and proceeds (note 5 p.145, note 6); associate table with effective interest,
Level 1 fair values, summarised Tencent financials, the carrying-amount reconciliation and the
no-deferred-tax statement (note 9 pp.155–156); Tencent's share of results in the segment note
(p.168); the core HE bridge (p.233) and, in the KPI datasheet, a full reconciliation from
Tencent's annual report to Prosus's core HE; the auditor's key audit matter (p.223) and the
audit committee's view (pp.58–59); post-balance-sheet sales (p.205).

Does not disclose: the reasoning for significant influence at 22.66% (not in the critical
judgements); the size of the lag-period adjustments; any sensitivity of the carrying amount or
of profit to the Tencent share price (none is needed under IAS 28, which is the point); the tax
that would arise if the shares were held in a different structure; what Prosus would do at 20%.

## 6. What it means for a buyer (memo section 4)

* **Earnings multiples on consolidated profit are meaningless.** FY2026: profit 11,650 =
  Tencent profit share 7,262 + Tencent disposal gain 4,700 + everything else (312) loss.
  Dividends received 1,237; cash from operations 472. The disposal gain is old appreciation being
  realised; it recurs only as long as Prosus keeps selling. Strip both out and the operated
  businesses lose money (JET and Despegar were consolidated this year).
* **Value on net asset value, not on book equity.** Book equity 53,867 excludes an 85,465 gap.
  The acquirer pays for the quoted 127,637 (plus the rest of the portfolio) whatever the
  carrying value says. Any "price-to-book" or "return on equity" screen is wrong by a factor of
  roughly 2.6 on the denominator (139,332 vs 53,867).
* **The acquirer's own accounts will look nothing like Prosus's.** Under IFRS 3 the acquirer
  measures the Tencent stake at fair value on the acquisition date (about 127.6bn at March 2026
  prices). Consequences: (i) no more "gains on partial disposal": selling Tencent at market
  produces roughly nil; (ii) no impairment headroom: a fall like FY2024 (quoted value down 27%
  from 122,952 to 90,213) becomes a possible "significant or prolonged decline" indicator and an
  impairment test against value in use; (iii) the share of Tencent's profit continues, but net of
  amortising any fair-value uplift allocated to Tencent's identifiable intangibles; (iv) deferred
  tax on the step-up depends on the acquirer's jurisdiction. Reported earnings will be lower and
  far more volatile than what Prosus shows today.
* **Tax is the biggest number in the room.** Prosus books no deferred tax because the Dutch
  participation exemption makes dividends and gains exempt and Tencent's home jurisdictions tax
  neither at source. A buyer must confirm that its structure keeps this: acquiring Prosus N.V.
  and leaving the shares inside MIH Internet Holdings B.V. versus moving them up; home-country
  CFC or minimum-tax rules; South African angles via Naspers. Illustration only: a 20% tax on the
  85bn gap is 17bn, more than the whole of Prosus's non-Tencent portfolio.
* **You buy an income you cannot direct.** Tencent sets its dividend (yield about 1% on the
  quoted value) and its buy-backs. Prosus's percentage moves with Tencent's capital actions
  (dilution loss 318 in FY2025, gain 4 in FY2026). The only lever Prosus has is to sell, which
  is what it has done every year since June 2022: 939,992,619 Prosus shares bought back for
  US$32.8bn funded by Tencent sales (results booklet). A buyer either continues selling Tencent
  to fund itself, or stops and lives on a 1.2bn dividend against 17bn of debt.
* **Leverage sits on the quoted value.** 17bn of bonds against 12.5bn cash after JET; the
  investment-grade rating is explicitly a commitment (p.35). Lenders look at loan-to-value on
  the 127.6bn, not at the 42.2bn in the accounts; a 30% Tencent drawdown changes LTV by more
  than any operating development.
* **The 20% cliff is on a three-year fuse.** If the buyer keeps the sale programme going, the
  question "do we still have significant influence?" arrives around FY2029. The accounting
  answer flips reported profit by tens of billions in either direction; the economic answer is
  that nothing changed. Decide in advance which it will be and what covenants, incentive plans
  and dividend policies key off reported profit.
* **Control chain.** Naspers controls Prosus; free-float holders' effective economic interest in
  Prosus is 56.7% (note 5 p.145). A bid needs Naspers, and Naspers funds its own buy-backs by
  selling Prosus shares.

Due-diligence list: Tencent's own December accounts and the Q1 lag adjustments; a look-through
NAV model (Tencent at market, other listed associates at market, unlisted at fair value,
operated businesses on their own cash flows) in place of consolidated P/E; a tax-structuring
opinion on preserving the participation exemption and on the 85bn gap; the Tencent board seat
and any shareholder arrangements; an IFRS 3 purchase-price model showing the acquirer's
post-deal earnings and impairment sensitivity to the Tencent price; debt covenants and rating
triggers expressed in LTV terms; the Naspers chain and South African approvals.

## 7. Things to double-check before citing

* FY2023 pages come from a two-page spread PDF; the fair-value table is on p.206 and the
  carrying-value table on p.208 (confirmed visually).
* FY2024 report has no conventional page numbers; cite "FY2024 AR, note 9, p.5/133" style.
* The 1,237 dividend figure is the group total from associates; Tencent's own is "US$1.2bn"
  (FY2026 AR liquidity note). Use 1.2bn when attributing to Tencent.
* OpenBB net income (11,638 for FY2026) is profit attributable to equity holders, not profit
  for the year (11,650). FY2023 revenue in OpenBB (4,947) is the restated figure.
