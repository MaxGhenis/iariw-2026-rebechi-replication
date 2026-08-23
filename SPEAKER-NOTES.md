# Speaker notes — discussant presentation of Rebechi et al. (2026)

**Session:** Recent laws and their inequality implications · Fri 28 Aug 2026, 4:00–5:30pm, **Room A1** (NBB, Brussels; chair Diana Rojas — per the 20 Aug program; earlier notes said Room B). Same session: #326 D'Aguanno & Van Kerm (discussant Katsushi Imai) and #364 Ghenis/Ogorek/Makarchuk (discussant Castaldo).
**Paper:** "What Can Money Buy? Inequality and Fiscal Policy Implications of Citizens United v. FEC" — Rebechi (Tasmania), Van Kerm (Luxembourg/LIS), Paradowski (LIS), Lepinteur (Luxembourg), Rohde (Griffith). Version of 31 Jul 2026, 68 pp.
**Format:** IARIW flipped — discussant presents the paper (~15 min), then author (Philippe Van Kerm) responds.
**Deck:** 26 slides. 1–18 = the paper; 19 = divider; 20–23 = four comments; 24 = replication; 25 = literature; 26 = close.
**Backing:** `REVIEW.md` (findings with status), `replication/` (public-data replication, scripts + results), `review/lenses/` (source-by-source evidence).

Timing (15 min): paper 9 min (slides 2–18, ~30 s each — move fast, the room has the paper); discussion 6 min (20–25, ~1 min each); close 30 s.

---

## 1 · Cover
Who's who; flipped format; Philippe responds after.

## 2 · Does money in politics change actual policy?
The political effects of CU are documented; the policy effects are the open question. Quote the conclusion: "Most research to date has found no impact on actual policy." (Comment 4 will say that sentence is wrong — hold it.) Footnote 1: top-100 donors $2.4B (OpenSecrets).

## 3 · Timeline
Two beats: Austin (1990) is why state bans existed in 2010; CU (Jan) + SpeechNow (Mar, D.C. Circuit — the paper's p. 1 calls it a Supreme Court ruling; p. 6 gets it right).

## 4 · The natural experiment
23 ban states; map from Klumpp et al. (2016), who follow NCSL. Two groups: 13 corporate-and-union (AK AZ MI NH NC ND OH OK PA RI TX WI WY), 8 corporate-only (CT IA KY MA MN MT TN WV). CO, SD excluded. Don't belabour: NH's "ban" was a $5k cap since 2000 (Klumpp fn. 16) and has no broad income tax; Montana's ban came back Dec 2011–Jun 2012.

## 5 · What followed
Table 1 (federal outside spending). The 353-fold figure sits on a $4M base that excludes 2004's 527 committees (> $500M). Disclosure share 77% → 33% (Table 3).

## 6 · This paper
Positioning vs Slattery, Tazhitdinova & Robinson (2023): they study statutory rates and revenues; this paper simulates what households face. Preview the asymmetry.

## 7 · Measurement
SCF (LWS-harmonized) through TAXSIM, 50 states × 18 years = 900 datasets, one fixed household sample, CPI-deflated. Only legislation varies. Note the footnote: "2011" is the 2010 wave (LWS US10, incomes 2009) — the SCF is triennial. Main text = state tax on AGI; Appendix D = after federal tax.

## 8 · Outcomes
ATR; top 5%/1% by income and by net worth; β = ATR top 20% − bottom 20% (defined, never reported — comment 4); Reynolds–Smolensky = Gini(pre) − Gini(post).

## 9 · Identification
Eq. (7): TWFE with CU × CorpBan and CU × CorpUnionBan; event study (2009 omitted); SDID pooled and state-by-state; Wooldridge check. "46 states", N = 846 (= 47 × 18; DC is in the panel — replication slide). SEs clustered by state; coefficients × 100.

## 10 · First stage
Pooled (Table A-1/A-2): vote share +3.6 to +5.0pp, ideology +0.20 to +0.41, Dem control −21pp**, Rep trifectas +15pp*. Then the grey box — by ban type (Table A-4) vote share is n.s. in both groups and the ideology shift is significant only in corporate-only states. Say it neutrally here; it returns as comment 1.

## 11 · Main result (Table 4)
Corp&union: top 1% −0.53** (0.24); top 1% by wealth −0.36* (0.19); RS −0.11** (0.04); overall ATR −0.01. Corp-only: all positive, none significant (top 1% +0.30 (0.30)). Difference: top 5% −0.47**, top 1% −0.83**, RS −0.18**. N = 846. Three takeaways: concentrated at the top; asymmetric by ban type; redistribution falls.

## 12 · Event studies (Fig. 3, Table 5)
No *significant* pre-trends: joint pre p > 0.10 (corp&union RS 0.102, top 1% 0.166). Post corp&union: top 1% p = 0.025, RS 0.049, top 5% 0.052. Ban-type differences post: < 0.01 for the top-group rates, 0.025 RS; ATR 0.086. Effects build gradually.

## 13 · Robustness
SDID (Table 6): same signs; group estimates smaller and n.s. (top 1% −0.40, RS −0.07); differences −0.72*, −0.13* at 10% with SEs "assuming independence". Wooldridge (Table C-1): identical — expected with one adoption date and never-treated controls. LOO: no single state decisive. Drop 8 no-income-tax states (B-1): top 1% −0.77**, RS −0.12**. Appendix D: larger and sharper. Caveat box: state trends pull the corp&union effects toward zero (Fig. 4).

## 14 · Heterogeneity (Fig. 5)
CT, MN positive outliers (corp-only; Democratic/divided); NC, ND, OH most negative (corp&union; Republican after 2010). "Most of our results are driven by few outlying states."

## 15 · Channels (Tables 7, 8, C-2)
Political outcomes predict taxes (Rep Senate vote share → RS −0.14*; Senate ideology → top 1% −0.29**; Dem trifecta → top 1% +0.33**). Residualizing on vote share/ideology/polarization leaves corp&union effects at −0.47 to −0.56 → the authors assign the residual to lobbying, donor pressure, agenda-setting.

## 16 · Union counterweight (Fig. 6)
Unions ≈ 87% to Democrats (2023–24). Union density slightly higher in corporate-only states. Authors' story: where unions could already spend, new corporate money met a counterweight; where both bans fell (Republican-leaning, weaker unions), deeper pockets won.

## 17 · Economic freedom (Fig. 7)
Fraser EFNA and Cato indices rise most in corp&union states post-2010. Descriptive — and the Fraser index contains the top income-tax rate (fn. 9).

## 18 · Conclusions
Persistently less progressive state income taxes where both bans fell; gradual; partly via composition. The "wingnut welfare" quote is theirs.

## 19 · Divider
"Four comments and a public-data replication." Say in one sentence that we rebuilt their pipeline from the public SCF and TAXSIM so the comments come with numbers.

## 20 · Comment 1 — the finding is about the union ban
Left: Table 4 as a triple-difference — −0.83 is, under DiD logic, the extra effect of also lifting the *union* ban, the opposite of the unions-fund-Democrats prior. Table A-4: vote share n.s. in both groups; ideology shift significant only in corp-only states, where taxes rose. Table 8: residualization barely moves anything. Their resolution (weaker unions in corp&union states) rests on ≈ 1pp of density; in our replication pre-2010 density is 11.5 / 12.4 / 11.5 across the three groups and the corp&union group is bimodal (AK, MI, RI, WI, PA, OH high; NC, TX, OK, AZ, ND low).
Right, the asks: put the conditionality in the abstract; run CU × union density within ban groups (ours: interaction −0.02, p = 0.57; the density main effect is *positive*, p ≈ 0.003 — high-union states raised top taxes); a theory of change with names.
If challenged on density numbers: Hirsch–Macpherson, unionstats.com, 2004–09 means; script `replication/scripts/10_union_density.py`.

## 21 · Comment 2 — which −0.53 do you believe
Chart = our replication's group means. Gap −1.56 (2004) → −2.03 (2009) → −2.55 (2021); pre-period leads +0.46, +0.48, +0.45, +0.37, +0.22; joint pre-test p = 0.40 because SEs are wide. Consistent with the paper: trends spec → ≈ 0 (Fig. 4); SDID groups n.s. Slattery et al. fn. 11 and Gilens et al. both dropped level-DiD on this experiment for this reason. Asks: trends spec as co-equal; Rambachan–Roth bounds. Fairness line: RI p = 0.013, wild bootstrap p = 0.030 — not a few-cluster artifact.
Pre-2010 drivers of the decline (if asked): OH HB 66 (2005) phase-down, RI 2006 flat-tax option, OK 2005–07 cuts, ND 2009 cut, AZ 2007.

## 22 · Comment 3 — five reforms, not thirteen states
Chart = per-state DiDs: OH −2.01, ND −1.98, NC −1.83, RI −1.73, OK −1.00; AZ −0.23; AK TX WY NH PA ≈ 0 (no/flat tax); MI +0.13, WI +0.27. Drop NC+ND+OH: −0.29 (SE 0.24, p = 0.22). Timing: ND cut May 2009 (pre-CU, oil-financed); RI reform passed 4 June 2010 before RI's own compliance date; OH's 2011 step is the 2005 law; NC 2013 is the clean case. Asks: B-1 as the main sample; leave-three-out; tell the five stories.

## 23 · Comment 4 — model the tax function
Chart = incidence gradient: bottom 20% +0.21 (n.s.), 20–80 −0.19, 80–95 −0.33, 95–99 −0.48, top 1% −0.67 ≈ −$9,014 per household-year (2010 $; ≈ −$6,100 at their −0.53 and SOI means). Capital-heavy −0.53 vs wage-heavy −0.54. With a fixed sample the saturated micro regression *is* their Φ by subgroup. β (their eq. 5, never reported) is the most precise outcome: −0.68 (SE 0.22, t = 3.1). Asks: report β, dollars, the bottom quintile; say RS −0.11 = −0.0011 Gini on a lever of < 0.01; say B is empty.
Power question (Max asked): micro adds nothing for the average effect — identical coefficients and SEs; it adds precision for within-state-year contrasts because common schedule shocks cancel.

## 24 · Replication
Table: theirs vs ours. Say plainly: it reproduces — signs, magnitudes, stars, the asymmetry, B-1. DC: N = 846 only with DC. "SCF 2011" = 2010 wave (income 2009). What doesn't reproduce: overall ATR (−0.35 vs −0.01) — mapping compromises (no itemization; SS as pensions). 25 minutes of compute; one implicate. Ask for the 47 × 18 panel and code.

## 25 · Literature
Lead with Gilens, Patterson & Haines (2021, APSR): same experiment, policy effects, heterogeneity in the opposite direction, union counterweight hypothesized ex ante (H3) — uncited. Slattery et al.: a precise null including the top PIT rate, mischaracterized as "moderate". Klumpp: biggest electoral effects in MN, MT, IA — corporate-only states. Abdul-Razzak: Democratic-aligned groups still outspent Republican-aligned in treated states after CU. Hansen et al.: corporations weren't the source. Akey, Werner–Coleman, Farver: policy record mixed. Close the loop: the pooled effect they never report (≈ −0.2, n.s.) is Slattery's null.

## 26 · Close
Three floor questions: federal analogue; the 2021–23 state tax-cut wave (many corp&union states cut after the sample ends); who actually spent in the 13 states (their Table 1 is near parity at the federal level by 2020–24). Hand to Philippe.

---

## Numbers most likely to be challenged (all sourced)
- Paper: Table 4 top 1% −0.53** (0.24), RS −0.11** (0.04), difference −0.83** (0.35); N = 846; Table 6 SDID corp&union −0.40 (0.25), RS −0.07 (0.05); Table 5 pre p 0.166/0.102; Table A-4 vote share 0.05/0.01 n.s., ideology H 0.27** vs 0.18; Table 8 residual −0.47 to −0.56; B-1 −0.77**/−0.12**; D-1 −0.93***/−0.17***.
- Replication (`replication/results/`): top 1% −0.673 (0.286), RS −0.089 (0.035), diff −0.871 (0.380); B-1 −0.949; drop NC+ND+OH −0.293 (0.236, p 0.22); RI p 0.013; wild bootstrap p 0.030/0.016; gap −1.56/−2.03/−2.55; leads +0.46…+0.22; per-state DiDs as on slide 22; incidence as on slide 23; β −0.68 (0.22); union density 11.5/12.4/11.5, interaction p 0.57.
- Literature: Gilens et al. 2021 APSR 115(3):1074–81: −2.83 (1.06) p .01; corp-only −5.55 (0.35) p .001, "about twice as large". Slattery et al. 2023 JPubE 221:104859: "not able to identify economically or statistically significant effects … including tax rates"; top PIT ≈ −0.46pp n.s.; fn. 11 on levels. Klumpp et al. 2016 JLE 59(1): MN 14.2–21.7, MT 10.1–14.2, MI 6.6–13.7, OH 9.4–12.2, IA 6.3–11.7. Abdul-Razzak et al. 2020 Electoral Studies 67:102190, Table 7: $26.5M vs $21.7M. Hansen, Rocca & Ortiz 2015 JOP 77(2):535–45.
- Data facts: SCF waves 2007/2010/2013 (federalreserve.gov); LWS US10/US13 (lisdatacenter.org); IRS SOI 2010 top-1% threshold $369,691; no replication package found (GitHub/OSF/Zenodo/SSRN/RePEc/LIS WP, author site "work in progress").
