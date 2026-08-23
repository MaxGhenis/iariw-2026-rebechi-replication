"""05: Re-estimate Table 4 (and B-1) TWFE DiD from the simulated panel.

Spec (paper eq. 7): Outcome_st = b1 CU_t x CorpBan_s + b2 CU_t x CorpUnionBan_s
                                 + state FE + year FE, SE clustered by state.
Outcomes already in percent (x100). CU_t = 1{year >= 2010} (sensitivity: >= 2011).
Samples: main = 50 states + DC minus CO SD NE LA (47 units, N=846); also excl. DC
(N=828); B-1 = additionally drop the 8 no-income-tax states (N=702).
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

CORP_UNION = ["AK","AZ","MI","NH","NC","ND","OH","OK","PA","RI","TX","WI","WY"]
CORP_ONLY  = ["CT","IA","KY","MA","MN","MT","TN","WV"]
EXCLUDE    = ["CO","SD","NE","LA"]
NO_INC_TAX = ["AK","FL","NV","NH","TN","TX","WA","WY"]
OUTCOMES   = ["atr","atr_top5","atr_top1","atr_top5nw","atr_top1nw","rs"]

panel = pd.read_csv("results/panel_state_year.csv")
panel["corp_only"]  = panel.state.isin(CORP_ONLY).astype(int)
panel["corp_union"] = panel.state.isin(CORP_UNION).astype(int)

def estimate(df, outcome, cu_from=2010):
    d = df.copy()
    d["cu"] = (d.year >= cu_from).astype(int)
    d["cu_co"] = d.cu * d.corp_only
    d["cu_cw"] = d.cu * d.corp_union
    m = smf.ols(f"{outcome} ~ cu_co + cu_cw + C(state) + C(year)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d.state}, use_t=True)
    b1, b2 = m.params["cu_co"], m.params["cu_cw"]
    se1, se2 = m.bse["cu_co"], m.bse["cu_cw"]
    V = m.cov_params()
    vd = V.loc["cu_cw","cu_cw"] + V.loc["cu_co","cu_co"] - 2*V.loc["cu_cw","cu_co"]
    diff, sed = b2 - b1, np.sqrt(vd)
    from scipy import stats
    G = d.state.nunique()
    pdiff = 2*(1 - stats.t.cdf(abs(diff/sed), df=G-1))
    return dict(b1=b1, se1=se1, p1=m.pvalues["cu_co"],
                b2=b2, se2=se2, p2=m.pvalues["cu_cw"],
                diff=diff, sed=sed, pdiff=pdiff, n=int(m.nobs), r2=m.rsquared)

def run_table(df, label, cu_from=2010):
    out = []
    for y in OUTCOMES:
        r = estimate(df, y, cu_from)
        r["outcome"] = y; r["sample"] = label; r["cu_from"] = cu_from
        out.append(r)
    return pd.DataFrame(out)

def stars(p): return "***" if p<.01 else "**" if p<.05 else "*" if p<.10 else ""

samples = {
    "main_846":   panel[~panel.state.isin(EXCLUDE)],
    "noDC_828":   panel[~panel.state.isin(EXCLUDE + ["DC"])],
    "B1_702":     panel[~panel.state.isin(EXCLUDE + NO_INC_TAX)],
}
res = []
for lab, df in samples.items():
    res.append(run_table(df, lab))
res.append(run_table(samples["main_846"], "main_cu2011", cu_from=2011))
res = pd.concat(res)
res.to_csv("results/table4_replication.csv", index=False)

PAPER_T4 = {  # from paper Table 4 (transcribed for comparison only)
 "atr":(0.01,0.10,-0.01,0.13,-0.02,0.12), "atr_top5":(0.14,0.14,-0.33,0.20,-0.47,0.20),
 "atr_top1":(0.30,0.30,-0.53,0.24,-0.83,0.35), "atr_top5nw":(0.07,0.13,-0.25,0.17,-0.32,0.17),
 "atr_top1nw":(0.10,0.19,-0.36,0.19,-0.46,0.23), "rs":(0.07,0.07,-0.11,0.04,-0.18,0.07)}

for lab in ["main_846","noDC_828","B1_702","main_cu2011"]:
    sub = res[res["sample"].eq(lab)] if lab != "main_cu2011" else res[res.cu_from.eq(2011)]
    print(f"\n=== {lab} (N={sub.n.iloc[0]}) ===")
    print(f"{'outcome':<11}{'b1 corpOnly':>16}{'b2 corpUnion':>18}{'diff':>16}")
    for _, r in sub.iterrows():
        line = (f"{r.outcome:<11}"
                f"{r.b1:8.2f}{stars(r.p1):<3}({r.se1:.2f})"
                f"{r.b2:9.2f}{stars(r.p2):<3}({r.se2:.2f})"
                f"{r['diff']:8.2f}{stars(r.pdiff):<3}({r.sed:.2f})")
        if lab == "main_846" and r.outcome in PAPER_T4:
            p = PAPER_T4[r.outcome]
            line += f"   | paper: {p[0]:.2f}({p[1]:.2f}) {p[2]:.2f}({p[3]:.2f}) {p[4]:.2f}({p[5]:.2f})"
        print(line)
