# Replication audit: Rebechi & Van Kerm (2026), "What Can Money Buy?"

**Status: COMPLETE** (2026-08-22, ~2h15m wall-clock; see NOTES.md for the running log).
One-day, public-data, best-effort replication of the paper's core estimate: the effect of
Citizens United (2010) on simulated state income-tax progressivity, DiD across states
2004–2021 (paper Table 4). Every number labeled "mine" was computed in this session by
the scripts in `scripts/`; paper numbers are transcribed from the paper text.

## Summary

**The headline replicates.** From scratch — public SCF 2010 summary extract (the LWS
"2011" dataset; no 2011 SCF exists), NBER TAXSIM-35 run locally (WebAssembly) for all 50
states + DC × 2004–2021 × 6,482 fixed households (~5.9M simulated returns), the paper's
outcome definitions, and TWFE eq. (7) on N=846:

| corp&union β2 (×100) | mine | paper |
|---|---|---|
| ATR top 1% | **−0.67\*\* (0.29)** | −0.53\*\* (0.24) |
| Reynolds–Smolensky | **−0.09\*\* (0.03)** | −0.11\*\* (0.04) |
| diff (corp&union − corp-only), top 1% | **−0.87\*\* (0.38)** | −0.83\*\* (0.35) |

Corp-only arm: positive, never significant (mine 0.14–0.20; paper 0.01–0.30) ✓. B-1
(income-tax states only): amplifies to −0.95\*\*/−0.12\*\*\* (paper −0.77\*\*/−0.12\*\*) ✓.
Robust to dropping DC and to dating CU from 2011. Randomization inference (5,000
permutations, group sizes fixed): p=0.013; wild cluster bootstrap: p=0.030 (top-1%),
0.016 (RS). Group-mean top-1% ATR level ≈3.7% around 2010, inside the paper's ~3.5–5%.

**What doesn't replicate:** the paper's clean zero on overall ATR (−0.01; mine −0.35\*\*).
My simulated tax levels are too high overall (their Fig C-2 levels ≈2.5–3% for legible
states vs my 4.7–5.6%) because the public summary extract forces: no itemized deductions,
all Social Security treated as taxable pensions, cohabitants filing jointly. These inflate
middle-class taxable income, so across-the-board cuts move my overall ATR where theirs
concentrates at the top. Top-1%/RS — the paper's headline — is insensitive to this.

**What the audit adds:**
1. **Concentration.** Per-state DiDs: OH −2.01, ND −1.98, NC −1.83, RI −1.73, OK −1.00pp
   carry the effect; five corp&union states (AK TX WY NH PA) are mechanical ~zeros
   (no/flat income tax); WI and MI are opposite-signed. **Dropping NC+ND+OH: β2 = −0.29
   (SE 0.24, p=0.22)** — the headline does not survive the three biggest reformers.
2. **Pre-trend.** The treated-control top-1% gap was already widening before CU: −1.56
   (2004) → −2.03 (2009) → −2.55 (2021); pre-slope ≈ post-slope. Joint pre-tests don't
   reject (p≈0.40) only because clustered SEs are wide. Independently corroborates the
   paper's own admission that state-specific trends "substantially attenuate" the effect.
3. **Incidence.** Micro heterogeneity (fixed sample ⇒ group ATRs ≡ saturated micro reg):
   monotone gradient from +0.21pp (n.s.) for the bottom quintile to −0.67\*\* for the top
   1% ≈ **−$9,000/yr per top-1% household** (2010$); capital-heavy and high-wage top
   households hit alike (across-the-board top-rate cuts, not capital carve-outs).
4. **Mechanism check.** Pre-2010 union density is balanced across ban groups (11.5 vs
   12.4 vs 11.5%) and the effect does not scale with density within the corp&union group
   (p=0.57) — no dose-response for a "silenced unions" story; CU×density itself is
   *positive* (high-union states raised top taxes post-2010).
5. Corp-only states' positive coefficient is CT (+1.63) and MN (+1.40) raising top rates.

**Bottom-line read for a discussant:** the paper's numbers are honestly reproducible from
public data — signs, magnitudes, significance, and the corp-only/corp&union asymmetry all
come out. But the causal claim rests on ~5 state tax-reform episodes (OH ND NC RI OK)
inside a 13-state group with a pre-existing differential trend, and the significance
disappears when the three biggest reformers are removed. It is a valid group-mean
contrast, not a broad-based treatment response.

## 1. What I did (pipeline)

1. **Data.** The paper uses "the LWS version of the SCF for the year 2011" with all pre-tax
   incomes treated as 2010 values (paper fn. 8). There is no 2011 SCF (triennial survey);
   the LWS 2011 label corresponds to the Fed's **2010 wave**. I used the Fed's public
   summary extract `rscfp2010.dta` (no state identifiers — irrelevant here, since the paper
   runs the same national sample through every state's tax law). Implicate 1 only,
   n = 6,482 households, SCF weights.
2. **Dollar units.** The published extract is inflation-adjusted to 2022 dollars. From the
   Fed's own generator code (`bulletin.macro.txt`): published = nominal × (3198/3147
   income-year lag) × (4376/3204 Sept CPI-U-RS rescale). I multiplied all dollar values by
   3204/4376, recovering the Fed's "2010 dollars" convention (income already lagged
   2009→2010). Cross-check: weighted median income becomes $45,727 vs. the Fed Bulletin's
   published $45.8k (2010$) — matches.
3. **TAXSIM.** NBER TAXSIM-35 run **locally** via the R package `usincometaxes` 0.7.1
   (bundled WebAssembly; no server). All 50 states + DC × all years 2004–2021 × 6,482
   households ≈ 5.95M simulated returns. Incomes scaled to year t by CPI-U(t)/CPI-U(2010);
   all 18 CPI values verified against the BLS API.
4. **Outcomes** per state-year (weighted): ATR = Σ siitax/Σ AGI (AGI = TAXSIM federal AGI,
   v10); ATR of top 5%/1% by AGI and by SCF net worth; Reynolds–Smolensky =
   Gini(AGI) − Gini(AGI − siitax) (negatives clipped to 0 in Gini); β = ATR(top20) −
   ATR(bottom20). All ×100.
5. **Estimation.** TWFE per paper eq. (7): CU_t×CorpOnly_s + CU_t×CorpUnion_s + state FE +
   year FE, CU_t = 1{year ≥ 2010}, SEs clustered by state (t dist, G−1 dof for the
   difference row). Samples: main 47 units (incl. DC) N=846; excl.-DC N=828; B-1 drops the
   8 no-income-tax states, N=702. Sensitivity: CU_t = 1{year ≥ 2011}.

### Input mapping (SCF summary extract → TAXSIM), with known compromises
- mstat: married/cohabiting → joint (SCF `married==1` includes cohabitants); else single.
  TAXSIM treats single-with-dependents as head of household.
- page = head's age; sage = head's age if married (spouse age absent from extract).
- depx = KIDS; dependent ages set to 10 (all CTC/EITC-qualifying).
- pwages/swages = WAGEINC × 0.6/0.4 if married, else all primary.
- psemp = BUSSEFARMINC (includes rents/royalties X5714 — extract cannot separate).
- dividends = intrec = 0.5 × INTDIVINC each.
- ltcg = KGINC (negatives kept).
- pensions = SSRETINC + PENACCTWD. **Social Security cannot be separated from pensions in
  the extract**; treating all of it as taxable pension income overstates state tax for
  retirees in states that exempt SS but tax pensions.
- transfers = max(TRANSFOTHINC,0); negative remainder → otherprop. UI inside transfers
  (not separable) → treated as nontaxable; understates tax slightly.
- No itemized deductions (property tax, mortgage, charity = 0): overstates taxable income
  levels; mostly absorbed by year/state FE unless itemization policy changed differentially.

## 2. Results: mine vs. paper

### Table 4 (state taxes only, main sample N=846, coeffs ×100, clustered SEs)

| outcome | mine β1 corp-only | paper β1 | mine β2 corp&union | paper β2 | mine diff | paper diff |
|---|---|---|---|---|---|---|
| ATR | 0.14 (0.12) | 0.01 (0.10) | **−0.35\*\* (0.17)** | −0.01 (0.13) | −0.49\*\*\* (0.17) | −0.02 (0.12) |
| ATR top 5% | 0.18 (0.24) | 0.14 (0.14) | −0.58\*\* (0.25) | −0.33 (0.20) | −0.76\*\* (0.30) | −0.47\*\* (0.20) |
| **ATR top 1%** | 0.20 (0.32) | 0.30 (0.30) | **−0.67\*\* (0.29)** | **−0.53\*\* (0.24)** | **−0.87\*\* (0.38)** | **−0.83\*\* (0.35)** |
| ATR top 5% nw | 0.18 (0.24) | 0.07 (0.13) | −0.58\*\* (0.25) | −0.25 (0.17) | −0.76\*\* (0.31) | −0.32\* (0.17) |
| ATR top 1% nw | 0.16 (0.30) | 0.10 (0.19) | −0.66\*\* (0.28) | −0.36\* (0.19) | −0.82\*\* (0.36) | −0.46\* (0.23) |
| **RS** | 0.02 (0.05) | 0.07 (0.07) | **−0.09\*\* (0.03)** | **−0.11\*\* (0.04)** | −0.11\*\* (0.05) | −0.18\*\* (0.07) |

Robustness (mine): excluding DC (N=828) or dating CU from 2011 changes nothing material
(top-1% β2: −0.68 and −0.65). Table B-1 sample (drop 8 no-income-tax states, N=702):
top-1% β2 = −0.95\*\* (0.36) vs paper −0.77\*\* (0.30); RS −0.12\*\*\* (0.04) vs paper
−0.12\*\* (0.06); diff top-1% −1.20\*\* vs paper −1.13\*\*\* — same amplification pattern.

### Levels (sanity vs paper's SDID trend figures)
- Corp&union group mean top-1% ATR: mine 3.7–3.8% around 2010 (paper figures ≈3.5–5%). ✓
- RS ×100 for corp&union states: mine ≈0.3–0.9 (OH 0.83→0.65, NC 0.67→0.43, WI 0.86);
  paper ≈0.4–0.7. ✓ Corp-only: MN 1.03→1.32, CT 0.65→1.01 (paper ≈0.6–0.9). ✓
- Zero-income-tax states: ATR exactly 0 all years ✓; NH/TN ≈0.15 (I&D taxes only) ✓;
  NC top-1% falls 7.35→5.69 across the 2013 reform ✓; Kansas Brownback dip 2013–16 and
  2017–18 restoration ✓; OH 2005–11 phase-down ✓.

### Event study (2009 omitted, corp&union, top-1% ATR)
Pre: +0.47, +0.48, +0.45, +0.37, +0.22 (2004–08) — a monotone decline INTO treatment.
Post: −0.03 (2010) drifting to −0.52 (2021). Joint pre-trend test does NOT reject
(p=0.40 top-1%; p=0.40 RS) because clustered SEs are wide — but the point pattern shows
the treated-control gap was already widening pre-2010: raw gap −1.56 (2004) → −2.03
(2009) → −2.55 (2021). The pre-period slope (≈−0.09/yr) is comparable to the post-period
slope (≈−0.045/yr), which is why the paper's own state-specific-trend robustness check
"substantially attenuates" the effect. My joint post-period test for top-1% does NOT
reject (p=0.52; RS p=0.23), unlike the paper's Table 5 claim of joint post significance —
the pooled TWFE coefficient is significant, the 12 individual-year coefficients jointly
are not, in my replication.

## 3. What reproduced, what didn't

**Reproduced (signs, magnitudes, significance):**
1. The headline: corp&union top-1% ATR effect ≈ −0.5 to −0.7pp, significant at 5%;
   RS ≈ −0.09 to −0.11, significant; corp-only arm positive and never significant;
   difference row top-1% ≈ −0.85\*\* — mine −0.87 vs paper −0.83, nearly exact.
2. The asymmetry mechanism is visible in raw simulated data: post-2010 top-tax CUTS in
   corp&union states (OH, ND, NC, RI, OK) vs top-tax INCREASES in corp-only states
   (CT 2009/2011, MN 2013).
3. B-1 (income-tax states only) amplification; robustness to DC, CU-dating.

**Did not reproduce:**
1. Overall ATR: paper finds a clean zero for corp&union (−0.01); I find −0.35\*\* — in my
   simulation the big reformers cut ATRs across the whole distribution (across-the-board
   rate cuts: OH −0.98pp overall 2012→15, ND −1.30 2008→15, NC −0.70 2012→15), so the
   "effect concentrated at the top with nothing overall" pattern in the paper is only
   partially present (my top-1% effect is ~2× my overall effect; theirs is ~50×).
   Diagnosis from the paper's own Figure C-2 (viewed in the PDF): their overall-ATR
   levels top out around 2.5–3% for the corporate-ban states whose y-axis is legible,
   whereas my levels for the same states are 4.7–5.6% — my simulated liabilities are
   systematically larger relative to AGI. That is exactly what the mapping compromises
   predict (no itemized deductions; all Social Security treated as taxable pensions;
   cohabitants filed jointly): they inflate taxable income mostly in the broad middle,
   so across-the-board rate cuts move my overall ATR when theirs barely moves. Top-1%
   levels (where deductions/exclusions are relatively smaller) match the paper's SDID
   figures well, which is why the top-1% and RS rows replicate closely.
2. Paper's Table 5 joint post-period significance for top-1%/RS (see above).
3. My corp&union effects are uniformly ~25–60% larger in magnitude than the paper's
   (e.g., top5 −0.58 vs −0.33; top5nw −0.58 vs −0.25); my top5-by-networth ≈ top5-by-AGI
   almost exactly, while the paper's networth effects are notably smaller than its AGI
   effects. Their LWS net-worth ranking evidently overlaps less with the income ranking
   than my SCF-extract ranking does.

## 4. Inference beyond clustered SEs (main sample, corp&union β2)

| method | ATR top 1% | RS |
|---|---|---|
| cluster-robust t (46 dof) | p = 0.023 | p = 0.014 |
| randomization inference, 5,000 permutations of the 8/13 labels | p = 0.013 | p = 0.013 |
| wild cluster bootstrap (Rademacher, B=9,999) | p = 0.030 | p = 0.016 |
| RI for the difference row | p = 0.012 | p = 0.018 |

The significance is not an artifact of few-cluster asymptotics.

**But it is concentrated:** per-state DiDs vs never-ban controls (top-1% ATR, pp):
OH −2.01, ND −1.98, NC −1.83, RI −1.73, OK −1.00; then AZ −0.23, and AK/TX/WY/NH/PA
≈ −0.07 (five states with no/flat income tax that mechanically cannot respond), and
MI +0.13, WI +0.27 opposite-signed. The 13-state mean (= β2 exactly) is −0.67.
Leave-one-out keeps β2 in [−0.75, −0.56]; **dropping NC+ND+OH jointly gives
β2 = −0.29 (SE 0.24, p = 0.22)** — the top-1% headline does not survive removing the
three biggest tax reformers (RS: −0.039, SE 0.025, p = 0.12). The estimate is a
group-mean of ~5 real reform episodes diluted by 8 near-mechanical zeros.

## 4b. Who got the cuts? (micro heterogeneity, not in the paper)

Because the household sample is identical in every state-year cell, a fully saturated
micro regression is equivalent to computing group-level ATRs (the paper's Φ for
subgroups) and running the same TWFE per group (`scripts/09_micro_heterogeneity.py`,
`results/micro_heterogeneity.csv`). Corp&union β2, main sample:

| group | β2 (pp) | p | mean AGI (2010$) | $ per hh/yr |
|---|---|---|---|---|
| AGI bottom 20% | **+0.21** | 0.13 | 8,649 | +18 |
| AGI 20–80 | −0.19 | 0.15 | 47,929 | −91 |
| AGI 80–95 | −0.33 | 0.06 | 132,064 | −434 |
| AGI 95–99 | −0.48 | 0.03 | 329,408 | −1,595 |
| AGI top 1% | −0.67 | 0.02 | 1,340,002 | **−9,014** |
| net worth top 1% | −0.66 | 0.02 | 957,239 | −6,336 |
| capital-share>50% (AGI>50k) | −0.53 | 0.02 | 411,063 | −2,179 |
| wage-share>90% in top 5% | −0.54 | 0.02 | 467,640 | −2,543 |
| age 65+ | −0.31 | 0.07 | 63,039 | −194 |
| married with kids | −0.36 | 0.05 | 106,511 | −382 |

A clean monotone gradient: nothing (or a slight increase) at the bottom, −$9k/yr for the
average top-1% household. Capital-heavy and wage-heavy top households are hit almost
identically — consistent with across-the-board top-rate cuts (OH, ND, NC, RI, OK) rather
than capital-income carve-outs.

## 4c. Union-density moderator (bonus)

Hirsch–Macpherson (unionstats.com) state panel, pre-2010 (2004–09) mean membership
density, demeaned (`scripts/10_union_density.py`). Density is balanced across groups
(corp&union 11.5%, corp-only 12.4%, controls 11.5%), so it cannot confound the ban
contrast. CU×density enters **positive** (top-1% ATR +0.065 per density point, p≈0.003:
high-union states raised top taxes after 2010), the ban coefficients are unchanged when
it is added (β2 −0.677 vs −0.673), and within the corp&union group the effect does NOT
scale with pre-period density (interaction −0.023, p=0.57). The treated-group effect is
not proxying for union-density differences, but there is also no within-group dose
response for the "silenced unions" mechanism.

## 5. Exact rerun commands

```bash
bash scripts/01_download.sh                    # SCF 2010 extract + Fed macro (needs UA header)
Rscript -e 'install.packages("usincometaxes", repos="https://cloud.r-project.org", lib="~/Rlibs")'
uv run --with pandas,pyreadstat,numpy python scripts/02_build_inputs.py
Rscript scripts/03_run_taxsim.R 2004 2021      # ~11 min single-process; or 3 parallel chunks
uv run --with pandas,numpy python scripts/04_outcomes.py
uv run --with pandas,numpy,statsmodels,scipy python scripts/05_did.py
uv run --with pandas,numpy,statsmodels,scipy,matplotlib python scripts/06_event_study.py
uv run --with pandas,numpy python scripts/07_inference.py
uv run --with pandas,numpy python scripts/08_reforms.py
uv run --with pandas,numpy,statsmodels,scipy python scripts/09_micro_heterogeneity.py
uv run --with pandas,pyreadstat,numpy,statsmodels,scipy python scripts/10_union_density.py
```
Software: R 4.3.0, usincometaxes 0.7.1 (bundled TAXSIM-35 WebAssembly), Python 3.14 via
uv (pandas/statsmodels/scipy/wildboottest). Runtime: full pipeline ≈ 25 min wall-clock.

## 6. Caveats / not done

- Single SCF implicate (1 of 5); the paper does not state its implicate handling.
  Sampling variation across implicates is NOT reflected in my SEs (nor in the paper's —
  both treat the simulated panel as data).
- Summary extract instead of LWS harmonization: LWS separates spouse wages,
  interest vs dividends, SS vs pensions; my mapping cannot. Levels of overall ATR are
  visibly higher than the paper's as a result (Section 3).
- TAXSIM vintage: today's TAXSIM-35 wasm vs whatever the authors ran; NBER revises
  state law encodings.
- `siitax` excludes local income taxes (NYC etc.) — same limitation as the paper.
- The wild bootstrap used Rademacher weights via `wildboottest` 0.3.x; the RI permutation
  holds group sizes (8/13) fixed, which is the assignment-consistent scheme.
- Not done: SDID re-estimation (paper's Fig 4/C-9/C-10); Appendix D (after-federal-tax
  base); state-trend specifications (paper reports attenuation — my pre-trend series
  independently corroborates why); multiple implicates; formal Table 5 joint-test
  replication beyond the three outcomes reported above.
- The paper's N=846 with "46 states" is consistent with 47 units × 18 years; my results
  are near-identical with and without DC, so the DC question is immaterial.
