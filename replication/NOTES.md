# NOTES — running log

Replication audit of Rebechi & Van Kerm (2026), "What Can Money Buy? Inequality and
Fiscal Policy Implications of Citizens United v. FEC". Started 2026-08-22 ~17:20 local.

## Environment
- macOS 26.5.1 arm64; R 4.3.0 at /usr/local/bin/R; uv 0.11.7; python via uv.
- cwd `~/.cache/iariw287-replication` — fresh git repo initialized here (own sandbox repo;
  no pre-existing repo on the machine is touched, per hard rules).
- Prior delegate runs (delegate*.log, FINAL.result.json) all failed on API limits with zero
  output — nothing to reuse.

## Plan (from task)
P1: SCF2011 summary extract → TAXSIM-35 (R usincometaxes wasm) for 51 jurisdictions × 2004–2021
    → state-year panel of ATR / top-5% / top-1% (AGI & net-worth) / RS → TWFE Table 4 + B-1 + event study.
P2: RI permutation, wild bootstrap, leave-out, per-state DiD contributions, reform deltas.
P3: union density moderator; micro-level heterogeneity.

## Log
- 17:20 setup, git init, dirs created.
- 17:21 SCF download: scfp2011s.zip 404s — SCF is triennial, no 2011 wave. Paper says
  "LWS version of the SCF for the year 2011"; footnote 8 says all pre-tax incomes are
  2010 values → LWS label 2011 = Fed 2010 wave. Downloaded scfp2010s.zip (rscfp2010.dta).
- 17:24 rscfp2010.dta is in **2022 dollars** (Fed re-issue; site says "all dollar variables
  inflation-adjusted to 2022 dollars"). Verified via bulletin.macro.txt: published values =
  nominal × CPILAG(3198/3147, income only, 2009→2010$) × CPIADJ(4376/3204, Sept CPI-U-RS).
  Recover 2010$ by ×3204/4376 for ALL dollar vars. Cross-check: weighted median income
  62,457×3204/4376 = 45,727 ≈ Fed Bulletin's published $45.8k (2010$) ✓.
- 17:28 CPI-U 2004–2022 verified against BLS API — all 18 task values match; 2022=292.655.
- 17:30 usincometaxes 0.7.1 (wasm-only, local, no network). Smoke test passed incl.
  negative psemp/ltcg/otherprop, DC, NH (exactly 5%×(I&D−2400) ✓), TX=0 ✓.
- 17:35 base_households.csv built (implicate 1, n=6,482). Mapping documented in script.
- 17:38 full TAXSIM run launched: 3 parallel Rscript procs (6 years each), ~1.1s per
  state-year × 918 → ETA ~7 min.
- Paper verification: Table 4 numbers in task match paper text exactly (line ~700);
  eq (7) spec, clustered-by-state, coeffs ×100 confirmed; 21 treated states + CO/SD
  excluded confirmed from Table 2; B-1 drops the 8 no-income-tax states (line 1733).
- 17:45 all 18 years done (0.6 min/yr × 3 procs). Panel built; ALL sanity checks pass
  (zero-tax states exactly 0; NH=5%×(I&D−2400); NC 2014 reform; KS Brownback dip+repeal;
  OH phase-down; plausible CA/NY/OR/MN/NJ/HI levels).
- 17:50 Table 4 replicated (see REPORT). Biggest divergence: overall-ATR row.
- 17:55 event study: monotone pre-drift 2004–08 (+0.47→0), joint pre-test p=0.40 (wide
  SEs); post drifts to −0.52 by 2021; joint post p=0.52 (top1) — unlike paper Table 5.
- 18:00 RI (5,000 perms) p=0.013/0.013; wildboottest failed twice (results-object API,
  then numba typing on string clusters) — fixed with model object + integer cluster ids:
  p=0.030/0.016. LOO: NC+ND+OH drop → β2=−0.29 (p=0.22). Per-state DiD means ≡ β2 ✓.
- 18:05 reform deltas: NC −1.66, OH −1.84, ND −2.26, OK −1.50 vs CT +1.72, MN +2.27.
  RI (Rhode Island) −1.73 = 4th big contributor (2010 top-rate 9.9→5.99% reform).
- 18:10 micro heterogeneity: monotone gradient, top1 −$9,014/yr, bottom20 +$18 n.s.
- 18:15 unionstats.com: index/main pages are Word-export shells; found Stata panel at
  state/dta/state_1983_2025.dta. Density balanced across groups; no within-group dose
  response (p=0.57); CU×density positive (p=0.003).
- 18:20 PDF Fig C-2 axes show paper's overall-ATR levels ≈2.5–3% (corp-only panel) vs
  mine 4.7–5.6% → explains the overall-ATR divergence (no itemized deductions, SS→
  pensions inflate middle-class taxable income). Top-1% levels match (3.7 vs 3.5–5).
- 18:25 REPORT.md finalized; FINAL.md = summary copy.

## Failures / dead ends (for honesty)
- `scfp2011s.zip` 404 (no such wave); Fed blocks default curl UA (HTML error page).
- First SCF read assumed nominal dollars — caught 2022-dollar re-issue via weighted-median
  cross-check before anything downstream used it.
- BLS API v2 caps unregistered requests at 10 years — split into two calls.
- wildboottest: two API failures before success (see 18:00 entry).
- 07_inference.py leave-out crash: twfe helper read panel dims from closure — fixed.
- Prior delegate runs (delegate*.log): all failed on API rate limits, zero reusable output.
