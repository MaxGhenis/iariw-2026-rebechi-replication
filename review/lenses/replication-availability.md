# Replication package and feasibility — Rebechi, Van Kerm, Paradowski, Lepinteur & Rohde (2026)

Lane: replicability question 1B (package availability + what a replicator needs). All external facts below verified 2026-08-22 via WebFetch/WebSearch/GitHub API/document downloads in this session. Paper citations are to the 31 Jul 2026 IARIW draft (pdftotext line numbers from scratchpad/paper.txt; page numbers from the PDF).

## 1. Bottom line

- **No replication package exists anywhere public, and the paper has no data/code availability statement.** Not on GitHub, Zenodo, OSF, SSRN, RePEc/IDEAS, the LIS/LWS working-paper series, the authors' sites, or the IARIW/III/LAGV conference sites. The paper's only pointers are footnote 6 (`http://www.lisdatacenter.org`, p.10) and footnote 7 (Feenberg & Coutts 1993).
- **Two earlier presentations exist but neither posted a PDF**, so version-to-version changes cannot be inspected: III (LSE) 10th Anniversary Conference, Session 4C "Policies & Institutions", Fri 19 Sept 2025 (programme PDF: lse.ac.uk/International-Inequalities/10th-Anniversary/III-10th-Anniversary-Conference-Programme.pdf, title listed with "vs." instead of "v."); 25th Journées LAGV, Aix-en-Provence, 10–12 June 2026 (acknowledgments, p.1 fn.*; lagv2026.sciencesconf.org's paper browser returns "No paper available").
- **Everything needed for an approximate replication is nonetheless public and free** (public SCF 2010 + NBER TAXSIM-35 + CPI-U + the ban lists reproduced in the paper's Table 2/Figure 2), so the core qualitative result should be reproducible in about a day — but the exact numbers are not, because the paper under-specifies the pipeline at ~10 decision points (Section 5) and one input layer (the LWS harmonization) is inspectable only through LIS's remote-execution system.
- The collapsed estimation panel (846 state-year rows of tax-schedule aggregates) is not confidential under LIS rules (aggregated output may be published); **the authors could make the entire econometric layer exactly replicable today by posting one small CSV plus estimation scripts**, even if the microsimulation layer stays gated.

## 2. Where I searched for a package or earlier version (all negative unless noted)

| Venue | Result |
|---|---|
| GitHub repo search: "citizens united taxsim", ""citizens united" state tax", "rebechi"; code search ""citizens united" taxsim" | 0 relevant hits (gh api, 2026-08-22) |
| Zenodo API: ""Citizens United" AND taxsim", "Rebechi" | 0 relevant records |
| OSF API: nodes filtered on "Citizens United" | none matching |
| SSRN / RePEc-IDEAS via web search (title, author combinations) | nothing; Van Kerm's IDEAS page (ideas.repec.org/e/pva19.html) surfaced but no such title |
| LIS & LWS working-paper series (lisdatacenter.org/working-papers, lwswps) | no Rebechi / Citizens United paper |
| iariw.org | paper #287 in the 39th General Conference program (Program-for-the-Web-08202026.docx: session "Recent Laws and their Inequality Implications", Fri 28 Aug 2026 4:00–5:30pm, Room A1, discussant Max Ghenis); the program docx contains **no per-paper download links** (only 3 external links total); no 2026 paper PDFs on iariw.org (unlike 2022, when e.g. Rebechi-Rohde-IARIW-2022.pdf was posted) |
| III 10th Anniversary Conference (LSE, 18–19 Sept 2025) | paper listed in programme PDF (Session 4C, Fri 19 Sept 9:15–10:45, CBG 2.02, same 5 authors) — **earliest documented version**; no paper link |
| LAGV 2026 (lagv2026.sciencesconf.org) | conference 10–12 June 2026; author/paper browser: "No paper available" |
| alessiorebechi.com | profile only, no publications list, no code links |
| vankerm.net | placeholder/JS shell, no content retrievable |
| Google Scholar | profile pages not fetchable by tooling; title searches via web search returned nothing (UNVERIFIED whether a Scholar entry links any draft) |

Implication: the IARIW draft is, as far as public evidence goes, the first and only inspectable artifact of this project. No numbers from earlier versions can be compared.

## 3. What the paper itself provides vs. omits (documentation audit)

Provided in the draft:
- Treated-state identities: Table 2 (p.8, reproduced from Abdul-Razzak et al. 2020) lists 23 states with compliance dates (Jan 21, 2010 – Oct 18, 2010 for those shown; New Hampshire "N/A"); CO and SD are excluded from estimation.
- Ban-type split (corp-only vs corp&union): **only via Figure 2, a map reproduced from Klumpp et al. (2016)** (p.6) — no state list by type appears in text; no state names appear anywhere in the running text except CT/MN/NC/ND/OH in the SDID discussion (lines 810–823).
- Data recipe (Section 3.1, pp.9–11): "We start with the LWS version of the SCF for the year 2011. We then run the NBER's TAXSIM model … using state-level tax-benefit parameters in place in all 50 US states and for all years from 2004 to 2021", 900 simulated datasets over "a fixed, representative sample"; footnote 8: "all 2010 pre-tax incomes are deflated to year t values on the basis of the CPI".
- Two tax-base strategies (state tax on AGI in main text; on after-federal-tax income in Appendix D).

Omitted (each item in Section 5 is something a replicator must guess):
- No data/code availability statement, no repository, no "available on request".
- No TAXSIM version, access route, or run date (the word "TAXSIM35" never appears; the only TAXSIM citation is Feenberg & Coutts 1993).
- No CPI series (CPI-U? C-CPI-U? R-CPI-U-RS? annual average?).
- No control-state list; no mention of DC; the unit count is internally inconsistent (Section 5.3).
- No mention of SCF implicates, survey weights, tax-unit construction, or the SCF→TAXSIM variable mapping.

## 4. What a replicator needs — verified infrastructure facts

### 4.1 Public SCF (Federal Reserve)
- Public SCF microdata + codebooks: federalreserve.gov/econres/scfindex.htm (SAS/Stata/ASCII/CSV, free, no registration). SCF is triennial: waves 2010 and 2013 bracket the paper's period; **there is no 2011 SCF wave**.
- **No state identifiers in the public file**: 2010 codebook (federalreserve.gov/econres/files/codebk2010.txt) states the public data set "does NOT include most variables related to the sample design, details of geography, or the 3-digit industry and occupation codes"; state-of-residence (X30029 "ALPHA STATE CODE: RESIDENCE") and even 4-level region (X30022) appear only in the restricted internal file; geographic linkage X8460 is marked "NOT INCLUDED IN THE PUBLIC DATA SET".
- SCF 2010: 6,492 interviews; public file has 6,482 families × 5 implicates = 32,410 records; **income questions reference calendar 2009** (codebook question text throughout: "…in 2009?", e.g. X3132 "total pre-tax net income in 2009").
- Consequence: the paper's fixed-national-sample design is the *only* design possible with the public SCF — and equally, a replicator needs no confidential data to mimic it.

### 4.2 LWS layer (LIS Data Center)
- LWS US series (lisdatacenter.org/our-data/lws-database/): datasets **US95, US98, US01, US04, US07, US10, US13, US16, US19, US22**, labeled by *wealth reference year* ("Year given is the wealth reference year"). LIS news confirms the sourcing convention: "US16 … based on the 2016 wave of the Survey of Consumer Finances". **There is no US11 dataset.**
- Access (lisdatacenter.org/data-access/): microdata **cannot be downloaded**; access is exclusively through **LISSY remote execution** (submit Stata/R/SAS/SPSS jobs; aggregated output returned; microdata printouts prohibited). Registration: free for students anywhere and researchers from contributing countries (incl. the US); €187.50–€750/quarter otherwise (lisdatacenter.org/data-access/lissy/eligibility/); approval takes a review cycle.
- LWS User Guide 2024 (lisdatacenter.org/wp-content/uploads/files/data-lws-guide.pdf): LWS files ship **all five SCF implicates** (hid × inum), instruct users to use multiple-imputation routines across the 5 implicates, and provide weights (hpopwgt/ppopwgt, normalized hwgt/pwgt) plus replicate weights in a separate R-file.
- **No documented way to run TAXSIM inside LISSY**: nothing on the LIS or NBER sites describes a LISSY–TAXSIM bridge (LISSY jobs run on LIS servers and return printed output). Two authors are LIS-affiliated (Paradowski: LIS; Van Kerm: LIS/University of Luxembourg), consistent with an internal execution channel outsiders do not have. The paper does not say how the LWS×TAXSIM link was executed.

### 4.3 NBER TAXSIM-35
Source: taxsim.nber.org/taxsim35/ (fetched this session).
- "As of 20 May 2022 TAXSIM35 incorporates **state income tax laws through 2021** and federal law through 2023 … State tax is 1977 through 2021 with 2022+ calculated using the 'real' value of the 2021 law." The paper's 2004–2021 window ends exactly at the last year of real state law.
- TAXSIM is "the NBER's FORTRAN program"; distributed as a service and compiled executables — access routes: web form; Stata .ado (NBER-server) and native local .ado (Windows/Linux/OSX); **R interface by Shane Orr** (CRAN `usincometaxes` v0.7.1, Jan 2024 — runs against the NBER server or a local WebAssembly file); low-level server interface for SAS/Python/R/Julia; local low-level interface; Julia (jo-fleck/Taxsim.jl); email; **WASM in-browser build by Aman Karmani** (tmm1/taxsim.js, tmm1/taxsim.app — recommended by NBER "for confidential data and for users with firewall problems"). PolicyEngine/policyengine-taxsim is an independent open-source emulator usable for cross-validation.
- Inputs: 27+ fields (taxsimid, year 1960–2023, state as **SOI code 1–51** (not FIPS), mstat, ages, pwages/swages, psemp/ssemp, dividends (qualified), intrec, stcg, ltcg, otherprop, nonprop, pensions, gssi, pui/sui, transfers, rentpaid, proptax, itemized-deduction items, mortgage, childcare...). State = 0 disables state calculation.
- **Versioning is a real problem**: taxsim.nber.org/taxsim35/changes.html reads, in full: "The change log was not maintained. Starting in January 2023 it will be maintained on github." State calculators are corrected over time, so TAXSIM-35 run in 2026 need not equal TAXSIM-35 run in (say) 2023 on identical inputs, and pre-2023 changes are unrecoverable. The paper records no version or run date.
- NBER's conversion library (taxsim.nber.org/to-taxsim/) lists **at least three distinct published SCF→TAXSIM mappings**: Kevin Moore (SAS, data + programs; taxsim32–35 era), Sabelhaus & Joshi (Stata, taxsim32–35), and William Gale et al. — mutually different codebases; the paper does not say whether it used any of them or a bespoke LWS-variable mapping.

### 4.4 CPI
- Paper: footnote 8 only ("the CPI"). If the sample is SCF 2010, incomes reference 2009, but the paper deflates "2010 pre-tax incomes"; CPI-U annual averages are 214.537 (2009) vs 218.056 (2010) (BLS, 1982-84=100), a 1.64% wedge in the level of all real incomes, hence in every bracket position. This washes out of the DiD (uniform across state-years) but blocks exact level-matching of the 846-cell panel.

## 5. Undocumented choices a replicator must guess (inventory)

1. **Which dataset, literally.** "LWS version of the SCF for the year 2011" names a dataset that does not exist: LWS has US10 and US13, no US11; SCF has no 2011 wave; and eq. (6)/fn. 8 call the incomes "2010". Most plausible reading: LWS **US10** = SCF 2010 (fieldwork mid-2010–early-2011; income year 2009), with "2011" a slip (release/fieldwork year) and "2010" the wealth year applied to incomes. But nothing in the paper settles it, and each reading changes the CPI base and the income vector.
2. **Implicate handling.** LWS ships 5 implicates (inum). Stack all 5? First implicate? Average outcomes across implicates (Rubin)? Sample size and Gini/top-share estimates differ.
3. **Weights.** SCF/LWS weights (hpopwgt) in the aggregations, top-group cutoffs, and Ginis — or unweighted? Never stated. (SCF oversamples the wealthy; unweighted top-1% would be a very different group.)
4. **Tax-unit construction.** SCF observation = primary economic unit (household); TAXSIM wants tax units. One filer per household? Spouse wage split (TAXSIM's pwages vs swages matter for FICA/EITC and some state schedules)? Dependents = children in PEU? Never stated.
5. **Income mapping.** SCF/LWS income categories → TAXSIM's 27 fields: qualified vs ordinary dividends; interest; **short- vs long-term capital gains split** (SCF collects gains without an ST/LT split; top-1% AGI is capital-gains-heavy, so this materially moves top-1% ATR levels); pensions vs Social Security; UI; property income. Whether the LWS harmonized variables even preserve enough detail (vs. the raw public SCF) is inspectable only inside LISSY.
6. **Deduction inputs.** TAXSIM state calculations respond to proptax, mortgage interest, rentpaid, childcare. Set to zero? Imputed from SCF balance-sheet data? Zeroing them changes state itemized-deduction behavior and hence ATR levels and progressivity.
7. **Definition of top groups.** Top 5%/1% "by AGI" — weighted percentiles of the national simulated sample, presumably fixed across state-years (AGI barely varies with state) — but AGI is *simulated output*; is the ranking re-done per state-year or fixed once? Ties/negative AGI at the bottom? Not stated.
8. **Negative incomes in the Gini/RS.** SCF has negative business/capital incomes; Gini with negatives is convention-dependent (drop, floor at 0, keep). Not stated; affects RS levels.
9. **Estimation sample.** Text says "46 states" (p.12, line 554) yet Table 4 N=846 = 47×18, and SDID Ns 612 = (8+26)×18 and 702 = (13+26)×18 imply 26 never-ban control units and 47 units total → an unnamed 47th unit, almost surely **DC**, which the paper never mentions. The 26 controls are never listed (25 never-ban states after dropping NE and LA, + DC). Ban-type assignment must be read off a reprinted map.
10. **Treatment timing.** CU_t "takes the value 1 after 2010" (line 571-2) — literally t≥2011 — but the event study normalizes 2009 (= j−1) and treats 2010 as j=0, implying post includes 2010. Whether 2010 is treated or control time changes β̂. (Compliance dates in Table 2 span Jan–Oct 2010, NH n/a; the design ignores staggering, which is defensible, but the binary cut must still be pinned down.)
11. **TAXSIM vintage** (Section 4.3) and **CPI series** (Section 4.4).
12. Loose ends that signal drift between framework and implementation: eq. (1)/(4) include benefits B, but TAXSIM computes no benefits (B≡0 throughout, so RS is taxes-only and ΔRS = −ΔGini_post exactly, pre-Gini being fixed); the β progressivity measure of eq. (5) (top-20 ATR − bottom-20 ATR) appears in no table. A replicator has no target numbers for either.

## 6. Feasibility verdict: can −0.53pp (corp&union, top-1% ATR) be reproduced in a day from public data?

**Sign and rough magnitude: yes, plausibly within a working day. Exact numbers: no.**

- Pipeline: download public SCF 2010 (minutes); map to TAXSIM inputs starting from Sabelhaus-Joshi or Moore's published conversions (hours); loop 50 states × 18 years, rescaling nominal incomes by CPI-U to year t; run via local/WASM TAXSIM-35 or batched server calls (900 runs × 32,410 records ≈ 29M record-calculations — well within a day on any route; the WASM/local path avoids server throttling); collapse to ATR/top-group ATR/RS per state-year; TWFE per eq. (7) with Table 2's states, Figure 2's type split, CO/SD/NE/LA dropped, cluster by state.
- Why the sign should replicate: the outcome is a **deterministic function of state tax law**, so the DiD is at bottom a coded-up statement about statutes: corp&union-ban states enacted large top-rate cuts after 2010 (NC's 2013 flat-tax reform 7.75%→5.8%→…, ND's successive cuts, OH cuts, WI, OK, MI), while the corp-only group contains the big post-2010 *raisers* (CT 2011/2015, MN 2013) — the paper's own Fig. 5 outliers. Any competent TAXSIM (or PolicyEngine) pipeline over any reasonable national sample should recover that contrast in sign and order of magnitude.
- Why exact replication fails: items 1–11 above (mapping, implicates, weights, base year, TAXSIM vintage, sample/timing definitions), plus inaccessibility of the LWS layer except via LISSY (registration lead time; no documented TAXSIM channel inside LISSY).
- Diagnostic value either way: if an independent public-SCF pipeline recovers ≈−0.5pp, the result is about state tax *law* and the SCF/LWS layer is mostly scenery; if it recovers the sign but a very different magnitude, the magnitude is an artifact of undocumented micro choices; if it fails to recover even the sign, that is a serious red flag given the statutory record. (A parallel lane of this review is running exactly this exercise; this section's judgment is independent of its outcome.)

## 7. Constructive asks (what would fix this)

1. **Post the 846-row state-year panel** (φ_st for all outcomes, both tax bases) + estimation do-files. This is aggregated output, publishable under LIS rules, and would make every table and figure exactly reproducible without touching microdata. Near-zero cost.
2. **Post the microsimulation scripts** (LWS variable mapping → TAXSIM inputs; TAXSIM call parameters; version/date of run; CPI series; implicate and weight conventions), even if the LWS extract itself cannot ship. LISSY users could then re-run them verbatim.
3. **Fix the dataset citation** ("LWS US10, SCF 2010, income reference year 2009" or whatever is true) and state the deflation base year.
4. **State the sample**: list the 26 control units (and DC's status), the ban-type lists by name, and whether 2010 is post.
5. Alternatively (or additionally), a **public-SCF companion package** would make the whole paper replicable end-to-end with zero confidential inputs — this paper is unusually well-suited to full open replication, which makes the current absence of any package unusually costly.

## 8. Source URLs (all fetched/verified 2026-08-22)

- taxsim.nber.org/taxsim35/ ; taxsim.nber.org/taxsim35/changes.html ; taxsim.nber.org/to-taxsim/
- cran.r-project.org/web/packages/usincometaxes/index.html (v0.7.1, 2024-01-11)
- github.com: tmm1/taxsim.js, tmm1/taxsim.app, PolicyEngine/policyengine-taxsim, jo-fleck/Taxsim.jl (gh api)
- federalreserve.gov/econres/scfindex.htm ; federalreserve.gov/econres/files/codebk2010.txt
- lisdatacenter.org/our-data/lws-database/ ; lisdatacenter.org/data-access/ ; lisdatacenter.org/data-access/lissy/eligibility/ ; lisdatacenter.org/wp-content/uploads/files/data-lws-guide.pdf ; lisdatacenter.org/news-and-events/united-states-one-new-dataset-in-lws/
- lse.ac.uk/International-Inequalities/10th-Anniversary/III-10th-Anniversary-Conference-Programme.pdf
- iariw.org/39th-iariw-general-conference/ ; iariw.org/wp-content/uploads/2026/08/Program-for-the-Web-08202026.docx
- lagv2026.sciencesconf.org (+ /browse/author)
- BLS CPI-U annual averages 2009/2010 (214.537 / 218.056), cross-checked via bls.gov releases and Minneapolis Fed CPI table
- Negative searches: GitHub repo+code search, Zenodo API, OSF API, SSRN/RePEc via web search, lisdatacenter working-paper series, alessiorebechi.com, vankerm.net
