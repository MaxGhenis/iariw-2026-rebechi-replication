# Citation and attribution check — Rebechi, Van Kerm, Paradowski, Lepinteur & Rohde (2026), "What Can Money Buy?"

All verifications performed 2026-08-22 via CrossRef API, publisher pages, NBER, arXiv, Harvard Dataverse, Fraser Institute, and open PDFs of the cited works. Items marked UNVERIFIED could not be confirmed this session.

## A. Real problems found

### A1. Adeel et al. (2020) is a COVID-19 paper, cited for a Citizens United conservatism claim (MISATTRIBUTION)
- Paper p. A-3: "these results suggest that the CU reform has increased the ideological conservatism within state legislatures, consistent with Adeel et al. (2020)".
- The bibliography entry (p. 28) is accurate as bibliography: Adeel, A.B., Catalano, M., Catalano, O., Gibson, G., Muftuoglu, E., Riggs, T., Sezgin, M.H., Shvetsova, O., Tahir, N., VanDusky-Allen, J., et al. (2020), "COVID-19 Policy Response and the Rise of the Sub-National Governments," *Canadian Public Policy* 46(4):565–584. VERIFIED: DOI 10.3138/cpp.2020-101 — the paper builds a "Protective Policy Index" of pandemic responses in the US and Canada. It contains nothing about Citizens United, campaign finance, ideology, or conservatism.
- Almost certainly a BibTeX-key slip for Abdul-Razzak et al. (2020) (adjacent alphabetically, same year), whose verified abstract does say the regulatory changes "increase the electoral success of Republican candidates, thereby leading to more ideologically conservative legislatures"; Harvey & Mattia (2022) would also fit.

### A2. "Caughey and Sekhon (2017)" — wrong year AND wrong paper for the claims it supports (used 3×)
- Bibliography (p. 29): "Caughey, D. and Sekhon, J. S. (2017). Elections and the Regression Discontinuity Design: Lessons from Close U.S. House Races, 1942–2008. *Political Analysis*, 19(4):385–408."
- VERIFIED via CrossRef (DOI 10.1093/pan/mpr032): print publication year is **2011** (vol. 19, iss. 4). Cambridge re-registered the article online on 2017-01-04 when Political Analysis changed platforms — the likely source of the wrong year.
- That paper is a *methods* paper on whether close US House races are as-good-as-random for RDD. The paper cites it three times for claims it does not make:
  1. p. 23: "party discipline and partisan control serve as key predictors of policy adoption and mechanisms of policy diffusion, particularly for policies affecting tax burdens and welfare benefits (Caughey and Sekhon, 2017; DellaVigna and Kim, 2022; Bucchianeri et al., 2025)";
  2. p. A-8: "Following the literature on policy diffusion and political polarization (Caughey and Sekhon, 2017; …)";
  3. p. A-9: "Previous studies have attributed the growing polarization of state legislatures to a pronounced rightward shift of the Republican Party, followed by a leftward shift of the Democratic Party (Caughey and Sekhon, 2017; …)".
- The intended reference is almost surely **Caughey, Warshaw & Xu (2017), "Incremental Democracy: The Policy Effects of Partisan Control of State Government," *Journal of Politics* 79(4):1342–1358** (VERIFIED, DOI 10.1086/692669 — partisan control of state government → policy, 1936–2014).

### A3. Footnote 5 mischaracterizes Slattery, Tazhitdinova & Robinson (2023) — a precise null becomes "a moderate effect"
- Paper footnote 5 (p. 10): "Slattery et al. (2023) examines state-level corporate taxation, finding only a moderate effect of CU."
- VERIFIED abstract (NBER WP 30352, final; published as *JPubE* 221:104859, 2023 — bibliographic details verified via CrossRef): "Ten years after the ruling and for a wide range of outcomes, **we are not able to identify economically or statistically significant effects** of corporate independent expenditures on state tax policy, including tax rates, discretionary tax breaks, and tax revenues."
- The word "moderate" appears in the earlier SSRN abstract only as what confidence intervals *cannot rule out*: results "allow for a moderate economic effect on corporate tax rates and revenues, but suggest economically insignificant effects."
- So the closest prior paper found a null on statutory tax policy; the footnote converts it into a positive-but-moderate finding. This matters for positioning: the conclusion (p. 29) states "Most research to date has found no impact on actual policy. In contrast, we find evidence of a persistent impact on taxation policy" — the contrast with Slattery is real and should be stated as null-vs-effect, and reconciled (their pooled-treatment statutory outcomes vs. this paper's by-ban-type simulated ATRs; note this paper's own pooled/aggregate ATR effect is also ≈0).

### A4. Missing: Gilens, Patterson & Haines (2021, APSR) — the closest prior study of CU → state policy, which SUPPORTS the paper's thesis
- Gilens, M., Patterson, S. Jr., & Haines, P. (2021). "Campaign Finance Regulations and Public Policy." *American Political Science Review* 115(3):1074–1081. VERIFIED via Cambridge Core.
- It uses the same natural experiment (CU striking IE bans in 23 states) and finds treated states "adopted more corporate-friendly policies," most strongly corporate tax rates and tort law, with no effect on non-corporate issues (abortion, guns).
- Not in the reference list (only Gilens & Page 2014 is cited). Its existence also falsifies the blanket claim "Most research to date has found no impact on actual policy" (p. 29) — awkwardly, in the authors' favor. Citing it would strengthen the paper and force a sharper statement of what is new (distributional incidence via simulated liabilities, and the corp-only vs corp&union split).

### A5. SpeechNow.org v. FEC called a Supreme Court ruling in the introduction
- p. 1: "two Supreme Court rulings – 'Citizens United v. FEC' and 'SpeechNow.org v. FEC'".
- VERIFIED: SpeechNow.org v. FEC, 599 F.3d 686 (D.C. Cir. 2010) (en banc), decided March 26, 2010 by the U.S. Court of Appeals for the D.C. Circuit; certiorari denied. Sources: Campaign Legal Center case page; Justia; Quimbee.
- The paper's own Section 2.3 (p. 6) states it correctly ("this time by the D.C. Circuit Court of Appeals") — an internal inconsistency, trivially fixable.

### A6. The Figure 2 map "reproduced from Klumpp et al. (2016)" silently drops the source's New Hampshire caveat
- Klumpp, Mialon & Williams' own map marks "NH (1979\*)" and the note explains: "\* Corporate ban repealed in 2000 and replaced with a $5,000 cap, the same as applies to individuals (NH AG Opinion 143270)." Their footnote 16: "we classify New Hampshire as a state with both a corporate and union ban prior to Citizens United. Our results are robust to instead classifying New Hampshire separately…" (VERIFIED from the authors' posted PDF, sites.ualberta.ca/~klumpp/docs/cu.pdf).
- Abdul-Razzak, Prato & Wolton (2020) likewise write "By November 2010, all states (with the possible exception of New Hampshire) had complied… (we nonetheless perform robustness tests excluding New Hampshire)" (VERIFIED from the LSE open-access PDF; their Table A.1 has no NH date).
- Rebechi et al.'s Figure 2 reproduces the map without the asterisk; Table 2 lists NH as "N/A" and asserts "this does not affect the treatment coding." NH is 1 of the 13 corporate-and-union treated states (and one of the no-income-tax ones). Both source papers flagged NH and ran NH-exclusion robustness; this paper reproduces their materials without the caveat and (as far as the text shows) never drops NH specifically.

### A7. Stansel et al. EFNA reference is internally impossible; cited edition cannot be the data plotted
- Bibliography (p. 30): "Stansel, D., Torra, J., McMahon, F., and Carrión-Tavárez, Á. (2025). Economic freedom of north america 2022."
- VERIFIED: *Economic Freedom of North America 2022* was published in **2022** by exactly those four authors, with data through **2020** (Fraser Institute). *EFNA 2025* (published Dec 2, 2025) is by Stansel, Torra, **Mitchell** & Carrión-Tavárez, data through 2023.
- Figure 7(a) plots the index to ≈2023, so the data must come from the 2024/2025 edition — i.e., the reference's title/authors (2022 edition) do not match the year given (2025) or the data actually used.

## B. Related mischaracterization worth a note (kept out of the findings cap)

- p. 2: "This line of research shows that tax policy adoption is often constrained by political factors rather than purely economic considerations (Robinson and Tazhitdinova, 2023, 2024)." VERIFIED abstract of NBER WP 31268 (2023) finds close to the opposite emphasis: "the timing and magnitude of tax changes are **not** driven by economic needs, state politics, institutional rules, neighbor competition, or demographics," with those factors explaining <20% of variation. The 2024 SSRN paper (4852670, verified) does document rising partisan polarization of income/corporate/cigarette taxes — partial support — but 2023 is being cited against its own headline result. (Also self-relevant: if state politics explains so little of tax setting, the paper's politics→tax mechanism needs the 2024-style polarization channel, not the 2023 paper.)
- Bibliography entry "Raja, R. J. L. and Schaffner, B. F. (2015)" mangles La Raja's name (and the in-text cite renders as "Raja and Schaffner, 2015"); the 2014 article entry is correctly "La Raja". Book VERIFIED: *Campaign Finance and Political Polarization: When Purists Prevail*, University of Michigan Press, 2015.
- Table 3 is titled "Super PACs Outside Spending by Disclosure," but OpenSecrets' full/some/no-disclosure categories classify outside-spending groups generally (super PACs disclose committee donors by law — the paper's own §2.3 says disclosure requirements remained in place; "some/no disclosure" rows are largely 501(c)/shell-routed money). Numbers UNVERIFIED (OpenSecrets blocks automated access); the disclosure-decline direction is consistent with OpenSecrets reporting.
- Klumpp et al.'s posted text says "22 states had bans … 14 banned … by corporations and labor unions, and eight banned only corporate" while their own map shades 23 states (15+8, NH asterisked). Rebechi et al.'s "23 states" follows Abdul-Razzak et al. (verified: "23 states had restrictions") and Slattery et al. ("23 states"); no error charged, but the counts differ across the cited sources — worth one slide-footnote if classification comes up.
- Paper text says Shor–McCarty data are the "Individual State Legislator" file covering "1993–2020"; the bibliography cites the "Aggregate … January 2025 update," which covers 1993–2022 (both datasets VERIFIED on Harvard Dataverse: Individual DOI 10.7910/DVN/SGOQ7G, Aggregate DOI 10.7910/DVN/T53FFK, both published 2025-01-31). Trivial, but text and bib name different files and the stated end-year is stale relative to the cited release.
- Klarner: bibliography "State Legislative Election Returns, 1967-2022" matches the Harvard Dataverse dataset (DOI 10.7910/DVN/FJOGJB); body text says "(1968–2022)". Trivial.
- Intro spells "Hilary Clinton" (p. 4, §2.2); the film at issue was about Hillary Clinton. Cosmetic.
- Weschle (2021) in-text gloss "reduced incentives for the incumbents who left office to become lobbyists" garbles the mechanism slightly — the verified finding is that CU reduced the likelihood sitting legislators *leave for* lobbying (fundraising made staying more attractive). Direction consistent, wording off.

## C. Reference list — item-by-item verification

| Reference (as printed) | Status | Verified details / source |
|---|---|---|
| Abdul-Razzak, Prato & Wolton (2020), Electoral Studies 67:102190 | OK | CrossRef 10.1016/j.electstud.2020.102190; abstract confirms Republican-success + conservative-legislature finding and union-power/business-alignment mechanism; compliance dates in their Table A.1 match Rebechi Table 2 exactly (22 dates; NH none); "23 states" language confirmed (LSE OA PDF) |
| Adeel et al. (2020), Canadian Public Policy 46(4):565–584 | ENTRY OK, USE WRONG | 10.3138/cpp.2020-101; COVID-19 policy paper — see A1 |
| Arkhangelsky et al. (2021), AER 111(12):4088–4118 | OK | CrossRef 10.1257/aer.20190159 |
| Baker, Callaway, Cunningham, Goodman-Bacon & Sant'Anna (2026), JEL 64(2):498–557 | OK | CrossRef 10.1257/jel.20251650, exact match |
| Barber (2016), JOP 78(1):296–310 | OK | CrossRef 10.1086/683453 |
| Bassetti, Pavesi & Scotti (2020), mimeo | OK (exists) | Real working paper; authors at Padua/LIUC/UTS; public seminar record (2021) |
| Bonica (2016), Business and Politics 18(4):367–394 | OK | CrossRef 10.1515/bap-2016-0004 |
| Bucchianeri, Volden & Wiseman (2025), APSR 119(1):21–39 | OK | CrossRef 10.1017/s0003055424000042; note: paper is about legislative effectiveness — a loose fit where cited for polarization/candidate-entry/policy-diffusion claims |
| Caughey & Sekhon "(2017)", Political Analysis 19(4):385–408 | YEAR WRONG (2011); WRONG PAPER for claims | See A2; CrossRef 10.1093/pan/mpr032 |
| Ciccia (2024), arXiv 2407.09565 | OK | arXiv abs page; sdid_event |
| Cox (2023), SSRN 3794817 | OK | SSRN id correct; JMP (Oct 2022) abstract: super PACs "slightly help Republicans," "promote Republican challenger entry" — supports the in-text use; later revisions retitled "The Equilibrium Effects of Campaign Finance Deregulation on US Elections" |
| DellaVigna & Kim (2022), NBER WP 30142 | OK | nber.org/papers/w30142, June 2022 |
| Feenberg & Coutts (1993), JPAM 12(1):189–194 | OK | CrossRef 10.2307/3325474 |
| Gilens & Page (2014), Perspectives on Politics 12(3):564–581 | OK | CrossRef 10.1017/s1537592714001595 |
| Hacker & Pierson (2010), Simon and Schuster | OK (book, not re-verified) | Standard |
| Handan-Nader, Myers & Hall (2025), AJPS "1-18" | OK (early view) | CrossRef 10.1111/ajps.12973; now assigned 70(2):453–470 |
| Harvey & Mattia (2022), Public Choice 191(3):417–441 | OK | CrossRef 10.1007/s11127-019-00721-4 (191(3-4), online 2019, print 2022); abstract confirms CU → more Republican wins AND greater conservatism |
| Hirsch, Macpherson & Even (2026), union CPS data | OK | unionstats.com, updated annually, standard citation form |
| Kennickell (2008), IFC Bulletin 28:403–08 | OK | BIS IFC Bulletin vol. 28 (2008), pp. 403–408 (bis.org/ifc/publ/ifcb28zzn.pdf; RePEc bis:bisifc:28-47) |
| Klarner (2024), State Legislative Election Returns 1967–2022 | OK | Harvard Dataverse 10.7910/DVN/FJOGJB |
| Klumpp, Mialon & Williams (2016), JLE 59(1):1–43 | OK | CrossRef 10.1086/685691; map exists in source (their Figure 2 in posted version); NH caveat dropped in reproduction — see A6 |
| La Raja & Schaffner (2014), Electoral Studies 33:102–114 | OK | CrossRef 10.1016/j.electstud.2013.08.002; abstract confirms "limited, if any, effect" reading used in intro |
| Milanovic (2019), Harvard UP | OK (book) | Standard |
| Petrova, Simonov & Snyder (2019), mimeo | OK (exists) | On J. Snyder's Harvard working-papers page |
| Piketty (2020), Harvard UP | OK (book) | Standard |
| "Raja" & Schaffner (2015), U. Michigan Press | NAME GARBLED (should be La Raja) | Book verified (press.umich.edu) |
| Robinson & Tazhitdinova (2023), NBER 31268 | OK; use questionable | nber.org/papers/w31268 (May 2023); see B |
| Robinson & Tazhitdinova (2024), SSRN 4852670 | OK | SSRN page verified via search (posted June 2024) |
| Robinson & Tazhitdinova (2025), JPubE 241:105273 | OK | CrossRef 10.1016/j.jpubeco.2024.105273 |
| Ruger & Sorens (2023), Freedom in the 50 States | OK | Cato Institute, 7th edition (2023) |
| Shor (2025), Aggregate Shor-McCarty data, January 2025 update | OK | Harvard Dataverse 10.7910/DVN/T53FFK (2025-01-31); text/bib file-name mismatch — see B |
| Shor & McCarty (2011), APSR 105(3):530–551 | OK | CrossRef 10.1017/s0003055411000153 |
| Slattery, Tazhitdinova & Robinson (2023), JPubE 221:104859 | ENTRY OK; CHARACTERIZATION WRONG | CrossRef 10.1016/j.jpubeco.2023.104859; see A3 |
| Spencer & Wood (2014), Ind. LJ 89:315 | OK | Indiana Law Journal 89(1), art. 11 (repository.law.indiana.edu/ilj/vol89/iss1/11) |
| Stansel, Torra, McMahon & Carrión-Tavárez "(2025)", EFNA "2022" | YEAR/EDITION MISMATCH | See A7 |
| Weschle (2021), PSRM 9(2):365–379 | OK | CrossRef 10.1017/psrm.2019.46 |
| Wooldridge (2025), Empirical Economics 69(5):2545–2587 | OK | CrossRef 10.1007/s00181-025-02807-z (online Aug 2025) |

## D. Key in-text attributions

- Fig 2 map "reproduced from Klumpp et al. (2016)": TRUE (their posted Figure 2; identical layout/years; Abdul-Razzak et al. reproduce the same map with near-identical note wording) — but NH asterisk dropped (A6). State-by-state classification matches the source exactly (8 corp-only: CT IA KY MA MN MT TN WV; 15 corp&union incl. CO(2002), SD(2007)).
- Table 2 compliance dates "reproduced from Abdul-Razzak et al. (2020)": TRUE — all 22 dates match their Table A.1; NH N/A matches.
- "weaker unions … stronger ties between corporations and Republicans as possible mechanisms" (Abdul-Razzak et al.): ACCURATE — their heterogeneity analysis interacts union density and corporate-Republican alignment; effect "almost null in states with strong unions."
- Intro contrast (Abdul-Razzak find GOP gains; La Raja & Schaffner 2014 find little effect): ACCURATE per both abstracts.
- "87% vs 12% in the 2023-2024 federal election cycle according to opensecrets.org" (union giving): CONSISTENT with OpenSecrets-derived reporting ("almost 90 percent of labor sector contributions went to Democrats in 2024") and with Abdul-Razzak's earlier 86% figure; exact 87/12 UNVERIFIED (OpenSecrets blocks automated access).
- Footnote 1: top-100 donors "led by Elon Musk" gave $2.4B in 2024: Musk-as-top-donor VERIFIED (~$291M, OpenSecrets, Mar 2025); the $2.4B top-100 aggregate UNVERIFIED this session (plausible; no contradiction found).
- Table 1 outside-spending by cycle (OpenSecrets): UNVERIFIED line-by-line (site blocked); 2012 row sums to ≈$1.02B, consistent with known ≈$1.0B non-party outside spending in 2012; internal 2024/2004 ratios check out arithmetically (1,062/60≈18; 763/23≈33; 1,411/4≈353; 923/7≈132).
- Figure 1 timeline: SpeechNow correctly dated Mar 2010 and not called SCOTUS there; Austin (1990), McCutcheon (2014), FEC v. Ted Cruz for Senate (2022) all correctly placed. Intro's "two Supreme Court rulings" is the error (A5).
