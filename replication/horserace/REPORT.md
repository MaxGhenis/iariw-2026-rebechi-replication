# “What is the treatment?” horse race

_Verification report; computations and source retrieval performed in-session on 2026-08-23._

## Status

Priority 1 is complete. Priority 2 randomization and descriptive checks are in progress. This file is updated and committed after each coherent step.

## Data and design

The supplied `panel_state_year.csv` contains simulated state income-tax outcomes (×100) for 51 jurisdictions and 2004–2021. The requested analytic sample drops Colorado, South Dakota, Nebraska, and Louisiana, leaving 47 jurisdictions and 846 state-year observations.

## Results

### Baseline reproduction

The baseline matches the supplied targets. Estimates below use state and year fixed effects, CR1 standard errors clustered over 47 jurisdictions, and cluster-_t_ inference (46 df).

| Outcome | CU × CorpUnion | CU × CorpOnly | N |
|---|---:|---:|---:|
| Top-1% ATR | −0.673 (0.286) | 0.199 (0.317) | 846 |
| Redistribution slope (`rs`) | −0.089 (0.035) | 0.023 (0.046) | 846 |
| Top-5% ATR | −0.580 (0.251) | 0.179 (0.235) | 846 |
| `beta` | −0.679 (0.219) | 0.357 (0.396) | 846 |

### Priority 1 horse race

The tables report coefficient (state-clustered SE). Stars use cluster-_t_ p-values: `***` p<0.01, `**` p<0.05, `*` p<0.10. Full-sample tests use 46 cluster df and restricted-sample tests use 38. “Move toward zero” is
`100 × (|baseline CorpUnion| − |specification CorpUnion|) / |baseline CorpUnion|`; a negative number means the coefficient grows in absolute value. All specifications include state and year fixed effects. The lagged models lose 2004 because pre-panel 2003 trifecta status is unavailable. The restricted models retain the 13 CorpUnion states and 26 controls, dropping the eight CorpOnly states.

#### Primary outcomes

| Specification | CU×CorpUnion | CU×CorpOnly | Added term(s) | N | Move toward zero |
|---|---:|---:|---|---:|---:|
| (a) Baseline | −0.673** (0.286) | 0.199 (0.317) | — | 846 | 0.0% |
| (b) + acquisition wave | −0.565* (0.303) | 0.169 (0.309) | CU×Acquirer: −0.281 (0.246) | 846 | 16.1% |
| (c) + R trifecta, year _t_ | −0.640** (0.292) | 0.210 (0.313) | R trifecta(_t_): −0.147 (0.125) | 846 | 4.8% |
| (c-L) + R trifecta, year _t−1_ | −0.602** (0.279) | 0.214 (0.305) | R trifecta(_t−1_): −0.205 (0.124) | 799 | 10.5% |
| (d) + REDMAP | −0.736** (0.336) | 0.199 (0.318) | CU×REDMAP: 0.138 (0.509) | 846 | −9.5% |
| (e) + acquisition wave + REDMAP | −0.673* (0.369) | 0.165 (0.309) | CU×Acquirer: −0.322 (0.219); CU×REDMAP: 0.268 (0.503) | 846 | 0.0% |
| (f) acquisition wave + REDMAP; no ban terms | — | — | CU×Acquirer: −0.444** (0.199); CU×REDMAP: −0.249 (0.386) | 846 | — |
| (g) restricted + R trifecta(_t_) | −0.649** (0.293) | — | R trifecta(_t_): −0.105 (0.139) | 702 | 3.5% |
| (g-L) restricted + R trifecta(_t−1_) | −0.616** (0.279) | — | R trifecta(_t−1_): −0.143 (0.138) | 663 | 8.5% |

_Outcome: top-1% ATR (`atr_top1`)._

| Specification | CU×CorpUnion | CU×CorpOnly | Added term(s) | N | Move toward zero |
|---|---:|---:|---|---:|---:|
| (a) Baseline | −0.089** (0.035) | 0.023 (0.046) | — | 846 | 0.0% |
| (b) + acquisition wave | −0.072* (0.036) | 0.018 (0.045) | CU×Acquirer: −0.045 (0.031) | 846 | 19.5% |
| (c) + R trifecta, year _t_ | −0.083** (0.036) | 0.025 (0.045) | R trifecta(_t_): −0.028* (0.015) | 846 | 7.0% |
| (c-L) + R trifecta, year _t−1_ | −0.078** (0.034) | 0.027 (0.045) | R trifecta(_t−1_): −0.039** (0.016) | 799 | 13.1% |
| (d) + REDMAP | −0.085** (0.038) | 0.023 (0.046) | CU×REDMAP: −0.010 (0.061) | 846 | 5.1% |
| (e) + acquisition wave + REDMAP | −0.075* (0.044) | 0.018 (0.045) | CU×Acquirer: −0.047 (0.028); CU×REDMAP: 0.009 (0.061) | 846 | 15.5% |
| (f) acquisition wave + REDMAP; no ban terms | — | — | CU×Acquirer: −0.060** (0.025); CU×REDMAP: −0.049 (0.048) | 846 | — |
| (g) restricted + R trifecta(_t_) | −0.085** (0.036) | — | R trifecta(_t_): −0.020 (0.016) | 702 | 4.9% |
| (g-L) restricted + R trifecta(_t−1_) | −0.080** (0.034) | — | R trifecta(_t−1_): −0.028 (0.017) | 663 | 10.4% |

_Outcome: redistribution slope (`rs`)._

The acquisition-wave control produces the largest primary-outcome attenuation: 16.1% for top-1% ATR and 19.5% for `rs`, well below the pre-specified 40% threshold. Both coefficients remain significant at 10% but not 5% in (b). With contemporaneous or lagged trifecta status they remain significant at 5%; REDMAP barely changes them. In (e), magnitudes again remain close to baseline, though larger clustered SEs leave both significant only at 10%. Within the CorpUnion-versus-control sample, trifecta timing attenuates just 3.5%–10.4%. The lag movements in the tables compare the 2005–21 model with the requested full-period (a); against a same-2005–21 baseline they are smaller: 6.8% for top-1% ATR and 9.8% for `rs` (and 4.7%/7.0% in restricted models). **The CorpUnion coefficient therefore survives the partisan-control horse race in magnitude; its exact 5% significance is specification-dependent.**

The partisan terms nevertheless pick up real outcome variation when ban terms are omitted. In single-term no-ban models, CU×Acquirer is −0.520 (0.242) for top-1% ATR and −0.075 (0.031) for `rs`; lagged R-trifecta status is −0.267 (0.119) and −0.047 (0.015), respectively. With both acquisition and REDMAP terms but no bans, the acquisition coefficients are −0.444 (0.199) and −0.060 (0.025), while REDMAP is imprecise. Thus partisan control explains some of the same broad post-2010 tax-cut variation, but it does not absorb most of the CorpUnion contrast.

This is a decomposition/proxy check, not a clean causal test. Trifecta status may itself be an outcome of _Citizens United_, making it a post-treatment “bad control” in a mediation sense. Survival means the paper's pre-2010 ban-type contrast is not merely a proxy for the measured 2011–13 Republican-trifecta wave or the supplied REDMAP set; it does not establish that ban type is the causal channel. Had the coefficient fallen by more than 40% and lost significance, that would instead have suggested that the ban-type label was largely capturing the partisan-control/REDMAP wave.

#### Secondary outcomes

| Outcome/specification | CU×CorpUnion | CU×CorpOnly | Added term(s) | N | Move toward zero |
|---|---:|---:|---|---:|---:|
| Top-5% ATR: (a) | −0.580** (0.251) | 0.179 (0.235) | — | 846 | 0.0% |
| Top-5% ATR: (b) | −0.496* (0.266) | 0.156 (0.229) | CU×Acquirer: −0.217 (0.215) | 846 | 14.4% |
| Top-5% ATR: (c) | −0.557** (0.257) | 0.187 (0.233) | R trifecta(_t_): −0.102 (0.108) | 846 | 3.9% |
| Top-5% ATR: (c-L) | −0.530** (0.246) | 0.185 (0.226) | R trifecta(_t−1_): −0.154 (0.108) | 799 | 8.5% |
| Top-5% ATR: (d) | −0.628** (0.299) | 0.179 (0.236) | CU×REDMAP: 0.105 (0.455) | 846 | −8.4% |
| Top-5% ATR: (e) | −0.579* (0.325) | 0.152 (0.229) | CU×Acquirer: −0.249 (0.193); CU×REDMAP: 0.206 (0.448) | 846 | 0.1% |
| Top-5% ATR: (f), no bans | — | — | CU×Acquirer: −0.355* (0.177); CU×REDMAP: −0.241 (0.347) | 846 | — |
| Top-5% ATR: (g) | −0.563** (0.258) | — | R trifecta(_t_): −0.077 (0.123) | 702 | 2.9% |
| Top-5% ATR: (g-L) | −0.539** (0.247) | — | R trifecta(_t−1_): −0.111 (0.121) | 663 | 6.9% |
| `beta`: (a) | −0.679*** (0.219) | 0.357 (0.396) | — | 846 | 0.0% |
| `beta`: (b) | −0.533** (0.232) | 0.317 (0.382) | CU×Acquirer: −0.379* (0.223) | 846 | 21.5% |
| `beta`: (c) | −0.622*** (0.220) | 0.378 (0.389) | R trifecta(_t_): −0.258** (0.110) | 846 | 8.4% |
| `beta`: (c-L) | −0.578*** (0.214) | 0.375 (0.385) | R trifecta(_t−1_): −0.346*** (0.120) | 799 | 14.8% |
| `beta`: (d) | −0.678*** (0.241) | 0.357 (0.397) | CU×REDMAP: −0.002 (0.339) | 846 | 0.2% |
| `beta`: (e) | −0.598** (0.265) | 0.315 (0.382) | CU×Acquirer: −0.403* (0.221); CU×REDMAP: 0.161 (0.349) | 846 | 11.9% |
| `beta`: (f), no bans | — | — | CU×Acquirer: −0.531** (0.223); CU×REDMAP: −0.321 (0.291) | 846 | — |
| `beta`: (g) | −0.630*** (0.222) | — | R trifecta(_t_): −0.219* (0.112) | 702 | 7.1% |
| `beta`: (g-L) | −0.587*** (0.215) | — | R trifecta(_t−1_): −0.306** (0.130) | 663 | 13.6% |

### Priority 2: assignment placebo and descriptive changes

The seeded placebo (`seed=20260823`, 10,000 draws per outcome) uniformly partitions the 47 states into 13 fake CorpUnion, eight fake CorpOnly, and 26 fake control states. I residualize outcomes and post interactions on state and year fixed effects. “Trifecta-only” is FE + CU×Acquirer; each random-ban model is FE + the two randomized post interactions. The first comparison is the share of random two-term ban models with partial within-_R²_ no greater than the real one-term trifecta model—i.e., how often trifecta-only explains at least as much. An adjusted-within-_R²_ sensitivity accounts for the random model's extra regressor. The shrinkage comparison adds the real CU×Acquirer term to each randomized ban model and measures `|fake union baseline| − |fake union adjusted|`.

| Outcome | Trifecta-only partial within-R² | Actual-ban partial within-R² | Random-ban median [5th, 95th pct.] | Random ≤ trifecta | Random ≥ actual bans | Observed union shrinkage | Random shrinkage ≥ observed |
|---|---:|---:|---:|---:|---:|---:|---:|
| Top-1% ATR | 0.0474 | 0.0878 | 0.0165 [0.0013, 0.0689] | 87.1% | 2.0% | 0.1082 | 8.5% |
| `rs` | 0.0570 | 0.0863 | 0.0160 [0.0012, 0.0664] | 92.5% | 1.7% | 0.0174 | 5.9% |
| Top-5% ATR | 0.0470 | 0.0961 | 0.0169 [0.0012, 0.0703] | 86.2% | 1.4% | 0.0836 | 9.9% |
| `beta` | 0.0623 | 0.0967 | 0.0151 [0.0011, 0.0594] | 95.6% | 0.6% | 0.1456 | 6.0% |

The degrees-of-freedom-adjusted “random ≤ trifecta” frequencies are nearly identical: 87.8%, 92.8%, 86.9%, and 95.9%. The acquisition wave therefore explains more tax variation than most arbitrary 13/8 labels and produces more CorpUnion shrinkage than most arbitrary labelings. But the actual two-ban-group fit is also unusually large relative to random assignments, and the observed shrinkage remains only 16%–20% of the primary coefficients. These are permutation diagnostics, **not randomization-test p-values**: historical labels were not randomly assigned, and the partisan variable is potentially post-treatment.

For the descriptive, I first form one equally weighted state-level `atr_top1(2021) − atr_top1(2009)` change. Mutually exclusive groups are: the strict R-trifecta acquirers; non-acquirers with a Democratic governor and both Democratic chambers in at least one year of the matching 2011–13 window; and all others. (The first two happen not to overlap.)

| Partisan group | All states | CorpUnion | CorpOnly | Controls |
|---|---:|---:|---:|---:|
| R-trifecta acquirers | −0.592 (15) | −0.770 (8) | −0.493 (1) | −0.372 (6) |
| D trifecta in 2011–13 | 0.364 (15) | −0.585 (1) | 0.696 (4) | 0.326 (10) |
| Others | −0.422 (17) | −0.396 (4) | −0.486 (3) | −0.413 (10) |

_Cells report mean top-1% ATR change (number of states). The one-state D-trifecta/CorpUnion and R-acquirer/CorpOnly cells are not stable group comparisons._

### Partisan-control panel and treatment overlap

`partisan_control.csv` contains 51 jurisdictions × 18 years = 918 unique state-years. For each state, I transcribed the annual component codes in Ballotpedia's governor/Senate/House tables into full party names and computed `rep_trifecta` from those three fields. Ballotpedia explicitly assigns general-election changes to the following calendar year because officeholders take office in December or January. Nebraska's chamber fields and indicator are missing; DC receives the requested Democratic/not-Republican-trifecta analytic override.

I implement “having not been one in 2009–2010” literally: both 2009 and 2010 must be zero, and at least one of 2011–2013 must be one. The full-panel acquirers are **AK, AL, IN, KS, LA, ME, MI, MS, NC, OH, OK, PA, TN, VA, WI, WY** (16); dropping LA leaves 15 in the analytic sample. Florida is not included: it was an R trifecta in 2009, lost that status when Gov. Charlie Crist became independent in April 2010, and regained it for 2011. An alternative “not in 2010 only” rule would add Florida.

| `rep_trifecta_acq` | CorpUnion (13) | CorpOnly (8) | Controls (26) |
|---|---:|---:|---:|
| 1 | 8 | 1 | 6 |
| 0 | 5 | 7 | 20 |

Thus 61.5% of CorpUnion states, versus 12.5% of CorpOnly states and 23.1% of controls, belong to the strict 2011–13 acquisition wave. This is substantial treatment overlap and makes the requested proxy/decomposition check informative.

All specified checks pass: Michigan, Ohio, Oklahoma, Pennsylvania, and Wisconsin switch to R trifectas in 2011; North Carolina switches in 2013; Kansas is one throughout 2011–17; Minnesota is a D trifecta in 2013–14; Connecticut is a D trifecta from 2011 onward; and Texas, Utah, Idaho, and North Dakota are R trifectas throughout 2004–21.

## Sources and reproducibility

Baseline command:

```bash
UV_CACHE_DIR="$PWD/.cache/uv" \
UV_FIND_LINKS="$PWD/.cache/local-wheels" \
uv run --offline --with pandas,numpy,statsmodels,requests,lxml,bs4 \
  python horserace.py
```

The local cache variables are required only because this sandbox blocks writes to the normal uv cache and blocks DNS/PyPI. The normal cache contained `beautifulsoup4` but not the tiny `bs4` meta-package, so `.cache/local-wheels` supplies workspace-local compatibility metadata; no analysis code imports it.

The exact baseline formula is `outcome ~ cu_x_corp_only + cu_x_corp_union + C(state) + C(year)`. Added terms are appended to that formula; no-ban models remove both ban terms, and restricted models omit CorpOnly states and their term. `results/baseline.csv`, `results/horserace_models.csv`, `results/horserace_tidy.csv`, `results/key_models.csv`, and `results/no_ban_models.csv` contain full-precision coefficients, CR1 clustered SEs, cluster-_t_ p-values, sample sizes, cluster counts, and exact formulas.

Priority 2 is generated by the same command. `results/placebo_summary.csv` records the seed, draw count, benchmarks, quantiles, and frequencies; `results/placebo_draws.csv` records all 40,000 outcome-draw results; `results/state_changes.csv` and `results/descriptive_changes.csv` record state-level and grouped changes.

Direct shell network retrieval was attempted first as ordered, but DNS is disabled in the execution sandbox (`curl: (6) Could not resolve host: ballotpedia.org`). Historical sources are therefore being inspected through the environment's read-only web retrieval fallback; annual URLs and limitations will be reported with the partisan panel.

Partisan sources (retrieved 2026-08-23):

- Ballotpedia, [State government trifectas](https://ballotpedia.org/State_government_trifectas): component histories for governor, upper chamber, and lower chamber; this URL is recorded on every non-DC row/year.
- Ballotpedia, [Historical and potential changes in trifectas](https://ballotpedia.org/Historical_and_potential_changes_in_trifectas): annual timing rule and dated change log, including the 2010–13 wave, Louisiana's February 2011 change, and Florida's 2010 interruption.
- NCSL, [State Partisan Composition](https://www.ncsl.org/about-state-legislatures/state-partisan-composition): definitions and Nebraska's nonpartisan exclusion; also recorded for the task-specified DC rows.
- Klarner's legacy [State Partisan Balance Data, 1937–2011](https://doi.org/10.7910/DVN/LZHMG3) was identified but not used: shell access to Harvard Dataverse failed at DNS and its coverage cannot supply 2012–21. This source is **not verified from its data in this session**.

The web fallback would not open Ballotpedia's advertised frozen `oldid=11275745` query URL, so the data file records the mutable page actually fetched on 2026-08-23. Every annual row has nonempty `source` and `source_url` fields; this limitation is explicit rather than presenting the frozen revision as fetched.
