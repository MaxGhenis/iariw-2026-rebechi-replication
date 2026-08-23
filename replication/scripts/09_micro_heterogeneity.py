"""09: Which household types got the state-tax cuts? (micro version of eq. 7)

Because the household sample is IDENTICAL in every state-year cell, a micro
regression of household ATR on CU x ban-type x group with household controls is
equivalent to computing the group-level ATR per state-year (the paper's own
Phi_2 for subgroup g) and running the same TWFE per group. We do the latter:
group ATR_st = 100 * sum(w*siitax)/sum(w*AGI) within group, then
ATR_st = b1 CUxCorpOnly + b2 CUxCorpUnion + state FE + year FE, cluster by state.
Dollar effect = b2/100 * group weighted-mean AGI (2010$).

Groups (fixed over states/years; AGI groups use 2010 weighted quantiles):
  AGI: q1 (bottom 20), q2-q4 (20-80), p80-95, p95-99, top1
  Net worth: top 5, top 1
  Capital share of AGI (div+int+ltcg)/AGI among AGI>50k: >50% vs <10%
  Age: head 65+; family type: married w/ kids
"""
import glob
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

CORP_UNION = ["AK","AZ","MI","NH","NC","ND","OH","OK","PA","RI","TX","WI","WY"]
CORP_ONLY  = ["CT","IA","KY","MA","MN","MT","TN","WV"]
EXCLUDE    = ["CO","SD","NE","LA"]

base = pd.read_csv("data/base_households.csv").set_index("hhid")

def wq(x, w, q):
    o = np.argsort(x); x, w = x[o], w[o]
    c = np.cumsum(w)
    return np.interp(q * c[-1], c, x)

# 2010 AGI for group definitions (fixed groups, like the paper's fixed sample)
d10 = pd.read_csv("data/taxsim_out_2010.csv")
agi10 = d10[d10.state == "CA"].set_index("taxsimid").v10_federal_agi
base["agi10"] = agi10
w, agi = base.wgt.values, base.agi10.values
th = {q: wq(agi, w, q) for q in (.2, .8, .95, .99)}
nw95, nw99 = wq(base.networth.values, w, .95), wq(base.networth.values, w, .99)
capinc = base.dividends + base.intrec + base.ltcg
capsh = np.where(base.agi10 > 0, capinc / base.agi10.clip(lower=1), 0)

groups = {
    "agi_bottom20":  agi <= th[.2],
    "agi_20_80":     (agi > th[.2]) & (agi <= th[.8]),
    "agi_80_95":     (agi > th[.8]) & (agi <= th[.95]),
    "agi_95_99":     (agi > th[.95]) & (agi <= th[.99]),
    "agi_top1":      agi > th[.99],
    "nw_top5":       base.networth.values >= nw95,
    "nw_top1":       base.networth.values >= nw99,
    "capshare_gt50_agi50k": (capsh > .5) & (agi > 50000),
    "capshare_lt10_agi50k": (capsh < .1) & (agi > 50000),
    "wagesh_gt90_top5": ((base.pwages + base.swages) / base.agi10.clip(lower=1) > .9).values & (agi > th[.95]),
    "age65plus":     base.page.values >= 65,
    "married_kids":  (base.mstat.eq("married, jointly") & (base.depx > 0)).values,
}
gmeans = {g: np.average(agi[m], weights=w[m]) for g, m in groups.items()}

# group ATR per state-year
rows = []
for f in sorted(glob.glob("data/taxsim_out_*.csv")):
    d = pd.read_csv(f)
    yr = int(d.year.iloc[0])
    d["wgt"] = d.taxsimid.map(base.wgt)
    for st, g in d.groupby("state"):
        if st in EXCLUDE:
            continue
        a, t, ww = g.v10_federal_agi.values, g.siitax.values, g.wgt.values
        row = dict(state=st, year=yr)
        for gname, mask in groups.items():
            denom = np.sum(ww[mask] * a[mask])
            row[gname] = 100 * np.sum(ww[mask] * t[mask]) / denom if denom > 0 else np.nan
        rows.append(row)
p = pd.DataFrame(rows)
p["cu"] = (p.year >= 2010).astype(int)
p["cu_co"] = p.cu * p.state.isin(CORP_ONLY)
p["cu_cw"] = p.cu * p.state.isin(CORP_UNION)

out = []
for gname in groups:
    m = smf.ols(f"{gname} ~ cu_co + cu_cw + C(state) + C(year)", data=p).fit(
        cov_type="cluster", cov_kwds={"groups": p.state}, use_t=True)
    key = "cu_cw" if "cu_cw" in m.params else "cu_cw[T.True]"
    keyc = "cu_co" if "cu_co" in m.params else "cu_co[T.True]"
    b2, se2, p2 = m.params[key], m.bse[key], m.pvalues[key]
    b1 = m.params[keyc]
    out.append(dict(group=gname, b1_corp_only=round(b1, 3), b2_corp_union=round(b2, 3),
                    se2=round(se2, 3), p2=round(p2, 3),
                    mean_agi_2010usd=round(gmeans[gname]),
                    dollar_effect_cw=round(b2 / 100 * gmeans[gname])))
res = pd.DataFrame(out)
res.to_csv("results/micro_heterogeneity.csv", index=False)
print(res.to_string(index=False))
