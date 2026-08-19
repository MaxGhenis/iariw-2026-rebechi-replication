# Speaker notes — discussant presentation of Rebechi et al. (2026)

**Session:** Recent laws and their inequality implications · Fri 28 Aug 2026, 4:00–5:30pm, Room B (NBB Auditorium, Brussels)
**Paper:** "What Can Money Buy? Inequality and Fiscal Policy Implications of Citizens United v. FEC" — Rebechi (Tasmania), Van Kerm (Luxembourg/LIS), Paradowski (LIS), Lepinteur (Luxembourg), Rohde (Griffith). Final version 31 Jul 2026, 68pp.
**Format:** IARIW flipped — discussant presents the paper (~15 min), then author (Philippe Van Kerm) responds.
**Deck:** 24 slides. Slides 1–18 = the paper; 19–24 = discussion.

Timing guide (15 min): background 2–3 min (slides 2–5), approach 3 min (6–9), results 4 min (10–14), mechanisms + conclusions 2 min (15–18), discussion 4 min (20–24).

---

## 1 · Cover
Say who's who. Note the flipped format for anyone unfamiliar. Philippe responds after.

## 2 · Does money in politics change actual policy?
Frame: the political-science literature has a decade of evidence that CU shifted *who* gets elected (Republican vote share up, legislatures more conservative). What nobody has nailed down is whether that changed *what they legislate*. Quote from the paper's conclusion: "Most research to date has found no impact on actual policy." That's the gap.
Footnote 1: top-100 donors, $2.4B in the last presidential cycle (OpenSecrets).

## 3 · Timeline
Don't read the list. Two beats: (a) Austin v. Michigan 1990 is what let states ban corporate independent expenditures — that's why heterogeneity existed in 2010; (b) CU (Jan) + SpeechNow (Mar) 2010 are the two rulings the paper studies jointly, CU as the binding precedent.

## 4 · The natural experiment
23 states had bans; the map is from Klumpp et al. (2016). Two treatment groups: 13 corporate-and-union-ban states in the sample (AK AZ MI NH NC ND OH OK PA RI TX WI WY), 8 corporate-only (CT IA KY MA MN MT TN WV). All revised laws to comply by Nov 2010 (Table 2, from Abdul-Razzak et al. 2020). CO and SD excluded — bans adopted only 2002/2007, may still have been bedding in.

## 5 · What followed
Table 1 (OpenSecrets): outside spending 2004→2024. The 353-fold "against Democrats" figure is real but sits on a $4M base — I flag that in minor notes. Disclosure share fell from 77% to 33% (Table 3).

## 6 · This paper
Positioning vs Slattery, Tazhitdinova & Robinson (2023, JPubE): they look at statutory rates and aggregate revenue (macro, "in the books"); this paper looks at what households actually face — average rates by group and redistribution delivered. Preview the asymmetry.

## 7 · Measurement
The design: SCF 2011 (LWS-harmonized), TAXSIM, 50 states × 18 years (2004–2021) = 900 simulated datasets, one fixed household sample, incomes CPI-deflated to each year. Only legislation varies. Main text = state tax on pre-federal AGI; Appendix D = after-federal-tax income (results larger there).

## 8 · Outcomes
ATR; ATR top 5% and top 1% by income and by net worth (SCF's edge); β progressivity (ATR top 20% − bottom 20%); Reynolds–Smolensky = Gini(pre) − Gini(post). Emphasize: these summarize the *whole* schedule, not a statutory parameter.

## 9 · Identification
Eq. (7): TWFE with two interaction terms — CU × CorpBan and CU × CorpUnionBan — plus state and year FE. Event study (2009 omitted, leads/lags −6…+10). SDID (Arkhangelsky et al. 2021) in two variants: pooled by ban group, and state-by-state ATETs. Wooldridge (2025) TWFE as an alternative estimator (Table C-1). 46 states: drop CO, SD, NE (nonpartisan unicameral), LA (blanket primaries). SEs clustered by state; coefficients ×100.

## 10 · First stage
Appendix A replicates Abdul-Razzak et al. (2020) through 2022. Republican vote share +3.6 to +5.0pp (Table A-1; significant with trend controls). Median ideology (Shor–McCarty NPAT) +0.20 to +0.41 (Table A-2). Democratic legislative control −21pp** (spec 2, Table A-5); Republican trifectas +15pp* (spec 5, Table A-7). Majority parties more extreme, minority parties more moderate (Tables A-11/A-12). Polarization: little.

## 11 · Main result (Table 4) — THE slide
Corporate & union ban row: top 1% ATR −0.53** (SE 0.24); top 1% by wealth −0.36* (0.19); RS −0.11** (0.04). Overall ATR −0.01 (nothing). Corporate-only row: all positive, none significant (top 1% +0.30, SE 0.30). Difference row (triple-diff): top 5% −0.47**, top 1% −0.83**, RS −0.18**. N = 846.
Three takeaways: concentrated at the top; asymmetric by ban type; redistribution falls.

## 12 · Event studies (Fig. 3, Table 5)
No pre-trends: joint pre-treatment p-values all > 0.10 for both groups. Post-treatment jointly significant for corp&union: top 5% p=0.052, top 1% p=0.025, RS p=0.049. Ban-type differences post: p<0.01 for top 5%, top 1%, top 1% nw; 0.025 RS; only overall ATR not (0.086). Effects build gradually.

## 13 · Robustness
SDID (Table 6): signs hold; differences top 1% −0.72*, RS −0.13*. Wooldridge (Table C-1): −0.53**, −0.11** — identical. Leave-one-out (Figs B-1/B-2): stable. Drop the 8 no-income-tax states (Table B-1): corp&union top 1% −0.77**, RS −0.12**; difference top 1% −1.13***, RS −0.20** — so baseline is a lower bound. Appendix D (after federal tax, Table D-1): corp&union top 1% −0.93***, RS −0.17***; difference −1.27***, RS −0.24***.
Caveat: state-specific linear trends (Fig. 4) attenuate corp&union effects toward zero. Authors: trends can absorb gradual treatment effects — treat as robustness, not preferred spec.

## 14 · Heterogeneity (Fig. 5)
State-by-state SDID: CT and MN are the positive outliers in corporate-only (Dem/divided government); NC, ND, OH the most negative in corp&union (Republican after 2010). Authors' own words: "most of our results are driven by few outlying states" — but LOO shows no single state is decisive.

## 15 · Channels (Tables 7, 8, C-2)
Political outcomes → taxes: Republican Senate vote share → RS −0.14*; median ideology (Senate) → top 1% ATR −0.29**; Dem trifecta → top 1% +0.33**, RS +0.04*; Rep governor → top 1% −0.25*, RS −0.05** (Table C-2). Residualization (Table 8): after partialling out vote share/ideology/polarization, corp&union effects persist: top 1% −0.47 to −0.56 (all **), RS −0.08 to −0.10 (**/***). So electoral composition carries part; a residual points to lobbying/donor pressure/agenda-setting.

## 16 · Union counterweight (Fig. 6)
Unions ≈87% to Democrats vs 12% (2023–24, OpenSecrets). Union density highest in corporate-only-ban states (~12.5% in 2009 vs ~11.5% corp&union vs ~11% no-ban); the gap widens after 2010. Story: where unions could already spend, new corporate money met a counterweight; where both were banned (Republican-leaning, weaker unions), lifting both bans favored deeper pockets.

## 17 · Economic freedom (Fig. 7)
Fraser EFNA and Cato regulatory index rise most post-2010 in corp&union-ban states. Descriptive only.

## 18 · Conclusions
Persistently less progressive state income taxes where both bans fell; gradual; partly through composition, partly beyond. Closing quote with "wingnut welfare" — read it as theirs, not mine.

## 19 · Divider

## 20 · Comment 1 — measurement design
Praise first, and mean it: the fixed-population de jure panel is genuinely the exportable idea. Then the flip side: Φ^{st} is state s's law applied to a *national* fixed sample — the "top 1%" is the national top 1%, not the state's own. Right object for isolating legislation; not the realized state tax structure. Suggest a de facto companion: IRS SOI realized state ATRs, or CPS/ACS through TAXSIM, and put a dollar figure on it.

## 21 · Comment 2 — which fiscal margins
Personal income tax is one lever. Legislatures can also shift sales/excise mix, corporate rates (Slattery et al.: moderate), state EITC/CTC add-ons, and spending. Clarifying question for Philippe: Eq. (1) defines Φ over T and B — is B populated? (My read: TAXSIM = income taxes only, so no.) If other margins moved the same way, income-tax RS understates the total turn; if states substituted, could overstate. Suggest a total-fiscal-incidence extension via LIS/LWS.

## 22 · Comment 3 — inference + a sharper mechanism test
8 + 13 treated clusters, six correlated outcomes: wild-cluster bootstrap or randomization inference on the triple-diff. Ban type isn't random — corp&union group is disproportionately Republican (Fig. C-1); post-2010 decade is crowded (ACA surtaxes, ATRA 2013, TCJA 2017, fiscal recoveries). Trends attenuate — say which spec you believe and why.
The ask: interact CU with pre-2010 union density as a continuous moderator. If the counterweight story is right, effects scale with density *within* ban groups → turns Fig. 6 from description into identification.

## 23 · Comment 4 — magnitudes
Read off Figs C-9/C-10: corp&union treated top-1% state ATR ≈ 3.5–4% around 2010, so −0.53pp ≈ 1/7 of the burden. RS ≈ 0.4 (×100) → −0.11 ≈ a quarter. State income taxes redistribute little to start — say so. Dollarize one number.
Minor: 846 = 47 × 18 vs "46 states" (DC?); state the income concept in headline text; 353-fold on a $4M base; NH has no compliance date and no broad income tax.

## 24 · Close
Three floor questions: federal analogue (no counterfactual in Congress — do state results bound it?); the 2021–23 state tax-cut wave in many corp&union states after the 2021 sample end; direct democracy — does the legislature channel weaken in initiative states? Hand to Philippe.

---

## Numbers most likely to be challenged (all from the paper)
- N = 846 (Table 4); 612 / 702 (SDID Table 6, corp-only / corp&union samples).
- 23 ban states pre-2010; 21 in sample (13 + 8) after dropping CO, SD.
- Top 1% ATR corp&union: −0.53** (0.24). RS: −0.11** (0.04). Difference top 1%: −0.83** (0.35).
- SCF 2011; TAXSIM; 2004–2021; 900 datasets.
- Repub vote share effect: 0.036–0.050 (upper), 0.023–0.048 (lower), Table A-1.
- Union contributions ≈87% Dem (2023–24, OpenSecrets, per paper §5).
- Disclosure: full-disclosure share 77.3% (2010) → 33.2% (2024), Table 3.
