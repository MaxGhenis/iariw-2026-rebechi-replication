"""11: Persist the remaining inference numbers: wild cluster bootstrap p-values
(Rademacher, B=9,999) and the NC+ND+OH-dropped estimates with clustered SEs.
Writes results/inference_summary.csv.
"""
import pandas as pd
import statsmodels.formula.api as smf

CORP_UNION = ["AK","AZ","MI","NH","NC","ND","OH","OK","PA","RI","TX","WI","WY"]
CORP_ONLY  = ["CT","IA","KY","MA","MN","MT","TN","WV"]
EXCLUDE    = ["CO","SD","NE","LA"]

d = pd.read_csv("results/panel_state_year.csv")
d = d[~d.state.isin(EXCLUDE)].copy()
d["cu"] = (d.year >= 2010).astype(int)
d["cu_co"] = (d.cu * d.state.isin(CORP_ONLY)).astype(float)
d["cu_cw"] = (d.cu * d.state.isin(CORP_UNION)).astype(float)
d["cl"] = pd.factorize(d.state)[0]

rows = []
from wildboottest.wildboottest import wildboottest
for outc in ["atr_top1", "rs"]:
    m = smf.ols(f"{outc} ~ cu_co + cu_cw + C(state) + C(year)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d.state}, use_t=True)
    wb = wildboottest(smf.ols(f"{outc} ~ cu_co + cu_cw + C(state) + C(year)", data=d),
                      param="cu_cw", cluster=d.cl.values, B=9999, seed=287)
    sub = d[~d.state.isin(["NC", "ND", "OH"])]
    m3 = smf.ols(f"{outc} ~ cu_co + cu_cw + C(state) + C(year)", data=sub).fit(
        cov_type="cluster", cov_kwds={"groups": sub.state}, use_t=True)
    rows.append(dict(
        outcome=outc,
        b2=round(m.params["cu_cw"], 3), se2=round(m.bse["cu_cw"], 3),
        p_cluster_t=round(m.pvalues["cu_cw"], 4),
        p_wildboot=round(float(wb["p-value"].iloc[0]), 4),
        b2_drop_NC_ND_OH=round(m3.params["cu_cw"], 3),
        se2_drop=round(m3.bse["cu_cw"], 3),
        p_drop=round(m3.pvalues["cu_cw"], 4)))
res = pd.DataFrame(rows)
res.to_csv("results/inference_summary.csv", index=False)
print(res.to_string(index=False))
