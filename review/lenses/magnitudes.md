# Measurement & magnitudes: full arithmetic
Rebechi, Van Kerm, Paradowski, Lepinteur & Rohde (2026), "What Can Money Buy?" — IARIW 2026 draft (31 Jul 2026).
All table/figure references = the paper. External sources verified this session are listed at bottom; anything not verified is flagged UNVERIFIED.

## 0. Units
- Tables 4/6/8/B-1/D-1: "Coefficients and standard errors are multiplied by 100" (Table 4 notes, PDF p.17). So ATR coefficients are **percentage points** and RS coefficients are **Gini points ×100** (RS −0.11 ⇒ Gini −0.0011 on the 0–1 scale).
- Cross-check of RS scaling: Fig C-8 (p.58) plots per-state RS in raw units 0.000–0.02; Fig C-10(e) (p.62) plots the corp&union group mean at 0.38–0.45 ⇒ C-10 is the ×100 scale of the same object (group mean of ~0.004). Consistent.

## 1. Baseline levels read from the SDID trend charts (Figs C-9/C-10, PDF pp.61–62; y-axis in %)

### Corp & union ban group (13 states: AK AZ MI NH NC ND OH OK PA RI TX WI WY), Fig C-10
| outcome | treated 2004 | treated 2010/11 | treated 2021 | SDID control 2010/11 | control 2021 |
|---|---|---|---|---|---|
| ATR top 1% | 3.95 | ~3.50 (2010), 3.43 (2011) | 2.97 | ~5.10–5.14 | 5.03 |
| ATR top 5% | ~3.5 | ~3.05 | ~2.55 | ~4.75 | ~4.45 |
| RS (×100) | 0.385 | ~0.40 | ~0.445 | ~0.50–0.515 | ~0.665 |

Derived magnitudes for the headline TWFE effects (Table 4: top1 −0.53**, top5 −0.33, RS −0.11**):
- −0.53pp = **15% of the treated group's own 2010 top-1% ATR level** (3.5); **≈10% of the control level** (5.1); **≈32% of the pre-existing treated−control level gap** (~1.65pp at treatment; the gap is 2.06pp by 2021).
- Absolute post-period change in treated top-1% ATR: 3.43 → 2.97 = **−0.46pp over 2011–2021 (−13%)**; control −0.11pp.
- RS: −0.11 (×100) = **−0.0011 Gini**. Treated baseline ≈0.40 (×100) ⇒ the effect is **−27% of these states' own state-income-tax redistribution** — but note the treated RS **rose** in absolute terms post-2010 (0.40→0.445); the "decline in progressivity/higher post-tax inequality" is a shortfall relative to controls whose RS rose 0.50→0.665. For RS the result is entirely relative, not absolute.
- Slopes (from C-10(b) reads): pre-2010 treated −0.075/yr vs control −0.042/yr ⇒ differential **−0.033pp/yr pre**. Post-2010: treated −0.046/yr vs control −0.011/yr ⇒ differential **−0.035pp/yr post**. The differential slope barely changes at treatment; the DiD/SDID coefficient is ~the continuation of a pre-existing differential trend, which is exactly why state-specific linear trends (Fig 4) drive the corp&union effects toward zero.

### Corp-only ban group (8 states: CT IA KY MA MN MT TN WV), Fig C-9
- ATR top 1%: treated ~5.35 (2004) → ~5.2 (2008–10) → 5.55–5.65 (2012–16) → ~5.35 (2021); control ~5.3 → 5.1–5.2. (Positive coefficient +0.30/+0.32.)
- RS: treated 0.52 → ~0.65 (2010) → ~0.85 (2021); control 0.52 → 0.64 → ~0.78.
- Level contrast: corp-only treated levels ≈ control levels (~5.1–5.2 top-1% ATR — "normal" income-tax states); corp&union treated level is ~3.5 because **4 of its 13 states have no broad income tax** (AK NH TX WY) and PA is a 3.07% flat tax.

### Secular RS drift (both groups + controls)
Control RS rises 0.465→0.665 (+43%) over 2004–2021 **with a fixed micro sample**: with incomes CPI-indexed to year t, non-indexed state brackets/credits mechanically raise measured ATRs and RS (plus genuine blue-state top-rate increases: CA Prop 30, MN 2013, CT 2011/2015, NJ/NY). The treatment effect is measured against this rising counterfactual.

## 2. Dollarizing −0.53pp (verified anchors)

IRS SOI, Individual Income Tax Rates and Shares, 2011 (tables cover 2010; irs.gov/pub/irs-soi/14insprbultaxrateshares.pdf, extracted this session):
- Returns with positive AGI 2010: **135,033,492**; top 1% = **1,350,335 returns**; AGI floor **$369,691**; top-1% share of AGI **18.87%**; total AGI (all returns, less deficit) **$8,089.1B**; adding back the −$188.8B deficit of loss returns ⇒ positive-AGI total ≈ $8,277.9B.
- Top-1% AGI ≈ 0.1887 × 8,277.9 ≈ **$1,562B** ⇒ mean AGI per top-1% return ≈ **$1.157M** (2010$).

Per-household (per tax unit) effects:
- Table 4 corp&union top-1% ATR −0.53pp ⇒ **−$6,130/yr** per national-top-1% tax unit (0.0053 × $1.157M).
- DDD (corp&union − corp-only) −0.83pp ⇒ −$9,600/yr. Table B-1 (drop no-tax states) −0.77pp ⇒ −$8,900/yr. Table D-1 (after-federal base) −0.93pp ⇒ ≈−$8,000/yr on the smaller base (not directly comparable).
- NC state-specific SDID (Fig 5b, read ≈ −1.45pp) ⇒ ≈ **−$16,800/yr**; ND ≈ −1.5pp ⇒ −$17,400; OH ≈ −1.25pp ⇒ −$14,500.
- Order-of-magnitude corroboration: Policy Matters Ohio headline on the mid-2010s Ohio income-tax cut plan: "would cut taxes $6,000 a year on average for Ohio's most affluent" (title verified; body not fetched).

Revenue scale:
- −0.53pp on the top 1% alone = 0.0053 × 18.87% = **0.100% of a state's AGI per year**.
- NC anchor: individual income tax net collections FY2013 = **$11.068B** (Census Annual Survey of State Government Tax Collections via FRED NCINCTAX, read this session). NC collections ran 3.0–3.7% of NC personal income 1995–2009 (NCDOR Statistical Abstract Fig 25.1, fetched). NC AGI ≈ $230–270B in 2013 (approx: ~70% of ~$350–360B personal income — ratio UNVERIFIED) ⇒ a −0.53pp top-1% cut ≈ **$230–270M/yr ≈ 2–2.5% of NC's individual income tax revenue**.
- Observed reality check: NC collections fell **$11.068B (FY2013) → $10.391B (FY2014), −$678M (−6.1%)** in the first year of the 2013 reform (whole reform: all brackets to 5.8% flat + EITC repeal + base changes), rebounding to $11.198B by FY2015 (FRED NCINCTAX).

## 3. The −0.53 next to the actual statutory reforms (top state marginal rate on wages, $1.5M earner; NBER TAXSIM maxrate table, taxsim.nber.org/state-rates/maxrate.html, fetched this session)

| state | 2004 | 2009 | 2011 | 2013 | 2015 | 2021 | post-2010 Δ | notes |
|---|---|---|---|---|---|---|---|---|
| NC | 8.50 | 8.06 | 7.75 | 7.98¹ | 5.75 | 5.25 | **−2.50** | 2013 HB 998: 7.75/7/6 → flat 5.8 (2014), 5.75 (2015), 5.499 (2017), 5.25 (2019); EITC repealed for 2014+; sales-tax base broadened (verified) |
| OH | 7.50 | 6.24 | 5.92 | 5.42 | 5.00 | 3.99 | **−1.93** | 21% phase-down enacted **2005** (HB 66, pre-CU; −1.26pp of the total fell 2004–10); 2013 HB 59: −10% income + **sales tax 5.5%→5.75%** (verified) |
| ND | 5.41 | 4.68 | 3.84 | 3.21 | 2.90 | 2.90 | **−1.78** | first big cut **2009 = pre-treatment**; statutory top 5.54 (2008) → 2.90 (2015) |
| WI | 6.75 | 7.75 | 7.75 | 7.65 | 7.65 | 7.65 | −0.10 | top bracket **raised** 2009 (pre-CU); 2013 trim 7.75→7.65 |
| OK | 6.29 | 5.27 | 5.21 | 5.14 | 5.14 | 5.00 | ≈−0.2 | bulk of cuts 2005–09, pre-CU |
| RI | 9.28 | 6.50 | 5.99 | 5.99 | 5.99 | 5.99 | −0.51 | bulk pre-CU (2006 flat-tax option); 2010 reform → 5.99 in 2011 |
| MI | 3.95 | 4.35 | 4.35 | 4.25 | 4.25 | 4.25 | −0.10 | flat tax |
| AZ | 4.94 | 4.39 | 4.34 | 4.47 | 4.47 | 4.50 | ≈+0.15 | big cuts came 2022+, outside sample |
| PA | 3.07 | 3.07 | 3.07 | 3.07 | 3.07 | 3.07 | 0 | constitutionally flat |
| AK/NH/TX/WY | ~0 | ~0 | ~0 | ~0 | ~0 | ~0 | 0 | no broad income tax ⇒ mechanical zeros |

¹ TAXSIM 2013 NC value reflects interactions; statutory top was 7.75 through 2013.
(The TAXSIM maxrate page has an apparent error for MN — shows 6.75 post-2013 vs the verified statutory 9.85 — so statutory values above were cross-checked against statutes/coverage for NC, OH, ND, WI, KS, CT, MN; all except MN matched.)

Composition arithmetic (state-specific SDID ATTs read from Fig 5(b), p.22, x-axis −4..4):
CT +1.65, MN +1.6, MT +0.15, WV −0.05, TN −0.1, MA −0.2, KY −0.25, IA −0.25 (corp-only);
AZ +0.1, PA 0.0, WY 0.0, TX 0.0, AK 0.0, NH 0.0, MI −0.05, WI −0.15, OK −0.3, RI −0.7, OH −1.25, NC −1.45, ND −1.5 (corp&union).
- Mean of corp&union ATTs = −5.3/13 ≈ **−0.41** ✓ (pooled SDID −0.40, Table 6).
- **NC+ND+OH = −4.2/13 = −0.32, i.e. ~80% of the group effect**; RI adds most of the rest; 9 of 13 states ≈ 0 (four mechanically so).
- The paper says this itself ("Most of our results are driven by few outlying states", p.27) but still describes "a systematic pattern across treated states" (App. B).
- Corp-only mirror: the +0.30 pooled coefficient = CT and MN **raising** top rates (CT 5.0→6.5 (2009) →6.7 (2011) →6.99 (2015); MN 7.85→9.85 in 2013, verified) — 2 states drive it, other 6 ≈ 0/negative.
- Control-group contamination for context: **Kansas (a never-ban control) enacted the era's most famous top-rate cuts** (6.45→4.9 in 2013, →4.6 2015, reversed 2017; TAXSIM path verified) — of the five famous 2013-wave cutting states (KS NC ND OH WI), four are corp&union states and one is a control. Visible as the KS dip in Fig C-8(c).

So the "effect of CU on tax policy" in point-estimate terms = "NC, OH, ND (and partly RI) cut top rates by 1.3–1.5pp (SDID) while most treated and control states did nothing" — averaged over 13 states.

## 4. The "top 1%" is the national top 1% under each state's law
- Design: one fixed LWS/SCF-2011 national sample (income year 2010), run through TAXSIM under each state-year's law (900 datasets); "the only source of variation is the difference in tax-benefit schedules" (p.10). The public SCF has no state identifiers; the same national sample represents every state.
- So "ATR (top 1pct)" = the rate the **national** top 1% (mean AGI $1.157M) would pay under state s's law — a schedule characteristic, not the tax paid by state s's residents. State top-1% thresholds differ by ~3× across states; WV's actual top 1% is far poorer than the national top 1%, CT's much richer.
- Because $1.157M is deep inside every state's top bracket (NC's top bracket began ~$120k), the measure ≈ statutory top rate net of deductions: the paper's own NC series (Fig C-4) sits at ~7.6–7.7 when the statutory top rate was 7.75 and at ~5.2 when it was 5.25/5.499. The claimed advance over "specific parameters of the tax schedule 'in the books'" (p.9, and the contrast drawn with Slattery et al.'s "nominal parameters") is therefore thin for the top-1% outcomes; the genuine additions are base/credit effects (e.g., ND's capital-gains exclusion pulls its ATR ~0.8pp below its statutory rate) — and the RS outcome, which genuinely aggregates the whole schedule.
- ATR by net worth: same national sample re-sorted by SCF net worth. It is still the **income** tax of balance-sheet-wealthy households (states don't tax net worth; TAXSIM has no property/estate taxes), so it tracks the income-sorted columns at ~60–70% magnitude (−0.36 vs −0.53; −0.25 vs −0.33) rather than adding an independent "wealth" dimension.
- Group-mean dilution: 4 of 13 corp&union states contribute mechanical zeros to every outcome; dropping no-income-tax states (Table B-1) moves top-1% from −0.53 to −0.77 and the DDD to −1.13. The authors call the baseline "a lower bound" (App. B) — as a group-mean statement, but a mean over states with and without the instrument is hard to interpret as policy.

## 5. "Post-tax inequality" = RS restated
- With the pre-tax distribution fixed by construction, ΔGini(post) ≡ −ΔRS exactly (eq. 4 with fixed GINI(X); B≡0 in practice — TAXSIM has no benefits; state EITCs enter as negative tax). The paper reports RS in every table and separately narrates "higher post-tax inequality"/"post-government income inequality" (abstract; §4.1 "lower top-group tax rates, reduced progressivity, and higher post-tax inequality"; conclusions) and plots post-tax Gini (Fig C-7) and RS (Fig C-8) as separate exhibits. Nowhere does the text state that these are the same number with the sign flipped. Two findings are one finding.
- Scale: Gini +0.0011 on a post-tax Gini level of ≈0.6 (Fig C-7 axes ≈0.56–0.64) — a +0.2% relative change.
- Scope: "post-government" excludes benefits and all non-income taxes. The driver reforms were partly **income→consumption tax swaps** (OH 2013: −10% income tax + sales 5.5%→5.75%; NC 2013: sales base broadened to services; both verified), so measured income-tax progressivity declines overstate the net-regressivity shift on the tax side that a full state-fiscal RS would show — or understate it, since sales taxes are themselves regressive; either way, the income-tax-only lens cannot say. Also NC repealed its state EITC (2014+, verified): part of the measured RS decline is credits taken from the bottom, not rates cut at the top — which fits the paper's story but not its "top income tax rates" framing. The β measure (eq. 5, ATR top20 − ATR bottom20) that would separate the two ends is defined but never reported in any table.

## 6. Is −0.11 RS economically meaningful?
- State income taxes in these data redistribute 0.004–0.009 Gini points (Figs C-9/C-10(e), ×100 axis 0.4–0.9). CBO: means-tested transfers + federal taxes reduce the Gini by **0.090 (2016: 0.513→0.423) and 0.084 (2021 projected: 0.521→0.437)** (CBO Projected Changes in the Distribution of Household Income, 2016 to 2021, Dec 2019, quoted via PNHP; CBO 2021 actual after-T&T Gini 0.443, cbo.gov/publication/60706 snippet). The federal-taxes-only component ≈0.03–0.04 (UNVERIFIED split; CBO reports only the combined figure in what I could access).
- So: the **entire state-income-tax lever ≈ 5–10% of federal redistribution**; the CU effect (−0.0011) ≈ **1.2–1.3% of the combined federal effect** and ≈0.2% of the Gini level — but ≈ **27% of the treated states' own (small) state-tax redistribution**. Fair two-sided framing: a large proportional change in a small instrument. The paper never anchors RS against any external benchmark.

## 7. The "353-fold" (Table 1, p.7)
- Internal arithmetic checks: 1,411/4 = 353 ✓ (nominal). But the 2004 base ($4M "against Democrats"; $94M total outside spending) is an artifact of the reporting category: **527 committees — the era's dominant outside vehicle (Swift Boat, MoveOn) — raised/spent just over $500M in the 2003–04 cycle** (OpenSecrets 527 data / Northwestern JLSP; verified via search snippets) and are excluded from FEC "outside spending" totals. The text's "spending was less than $100 million" before the ruling is FEC-reportable outside spending only.
- Also nominal dollars: CPI-U rose ≈+66% 2004→2024 (BLS; approximate, UNVERIFIED exact), and total election spending roughly tripled, so a fair "rise in outside money" is closer to one order of magnitude than 353×.

## 8. What a household-level dollar table would add (constructive)
The 900 simulated datasets already contain household-level liabilities. A stacked household×state×year file would support:
- "Under NC's 2021 law vs its 2009 law, a national-top-1% household pays ≈$28k/yr less state tax (7.65%→5.2% of $1.157M); the median household ≈$300 less; a bottom-quintile EITC household pays MORE after the 2014 repeal" — dollar-denominated incidence by income, wealth, age, family type, capital vs wage income.
- Aggregation to revenue cost per state-year (multiply by represented population) — connecting the index movements to the $678M NC revenue drop actually observed.
- Decomposition of the RS change into top-rate vs bottom-credit vs base components (would reveal the EITC-repeal channel invisible in top-1% ATRs).
- DiD on dollar outcomes by group with state and year FE, clustered by state — same identification, interpretable units ("CU lowered simulated state taxes of filer type X by $Y").

## Verified sources (this session)
- IRS SOI, Individual Income Tax Rates and Shares, 2011 (2010 tables): https://www.irs.gov/pub/irs-soi/14insprbultaxrateshares.pdf (text-extracted; returns 135,033,492; top-1% 1,350,335; floor $369,691; share 18.87%; total AGI $8,089.1B)
- NBER TAXSIM top state rates: https://taxsim.nber.org/state-rates/maxrate.html (fetched; MN entry inconsistent with statute — flagged)
- NC collections: FRED NCINCTAX (Census Annual Survey of State Government Tax Collections): https://fred.stlouisfed.org/data/NCINCTAX (browser-read; FY2013 $11.068B, FY2014 $10.391B, FY2015 $11.198B)
- NCDOR Statistical Abstract Fig 25.1 (collections as % of personal income, 1995–2009): https://www.ncdor.gov/documents/reports/table25-4/open
- MN 9.85% fourth tier (2013): MN House Session Daily / Faegre Drinker summaries (search-verified)
- OH HB 66 (2005) 21% five-year cut: Ohio Dept. of Taxation history PDF / Policy Matters Ohio (search-verified); OH HB 59 (2013) −10% income + sales 5.5→5.75: Ohio House release/Policy Matters Ohio (search-verified)
- NC HB 998 (2013): Tax Foundation/Brooks Pierce/TCWF (flat 5.8% 2014, 5.75% 2015; EITC eliminated 2014+; sales base broadened) (search-verified)
- CBO combined Gini reduction: CBO "Projected Changes in the Distribution of Household Income, 2016 to 2021" (Dec 2019), quoted at pnhp.org (0.513→0.423 in 2016; 0.521→0.437 projected 2021); CBO 60706 snippet (2021 actual 0.443)
- 527s ≈ $500M+ in 2003–04: OpenSecrets 527 pages / Northwestern JLSP (search-verified)
- Tax Foundation FF: 2010 top-1% threshold $369,691, 18.9% of AGI, 37.4% of income tax (search-verified, matches SOI)
- UNVERIFIED items flagged inline: NC AGI level (~$230–270B), AGI/personal-income ratio, CPI +66%, federal-taxes-only Gini split (0.03–0.04), Policy Matters Ohio "$6,000" body text, NC 2013 fiscal note ($2.4B/5yr figure NOT used).
