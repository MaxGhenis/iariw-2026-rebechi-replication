"""10: Mechanism moderator — does the CU effect scale with pre-2010 union density?
Union density: Hirsch-Macpherson-Even unionstats.com state panel (CPS), sector=Total,
pctmem, pre-period mean 2004-2009, demeaned over the 47 analysis units.
"""
import pandas as pd
import pyreadstat
import statsmodels.formula.api as smf

CORP_UNION = ["AK","AZ","MI","NH","NC","ND","OH","OK","PA","RI","TX","WI","WY"]
CORP_ONLY  = ["CT","IA","KY","MA","MN","MT","TN","WV"]
EXCLUDE    = ["CO","SD","NE","LA"]

u, _ = pyreadstat.read_dta("data/unionstats_state.dta")
u = u[(u.sector == "Total") & u.year.between(2004, 2009)]
dens = u.groupby("state2").pctmem.mean() * 100  # percent

d = pd.read_csv("results/panel_state_year.csv")
d = d[~d.state.isin(EXCLUDE)].copy()
d["dens"] = d.state.map(dens)
assert d.dens.notna().all(), d[d.dens.isna()].state.unique()
d["dens_dm"] = d.dens - d.drop_duplicates("state").dens.mean()
d["cu"] = (d.year >= 2010).astype(int)
d["cu_co"] = (d.cu * d.state.isin(CORP_ONLY)).astype(float)
d["cu_cw"] = (d.cu * d.state.isin(CORP_UNION)).astype(float)
d["cu_dens"] = d.cu * d.dens_dm
d["cu_cw_dens"] = d.cu_cw * d.dens_dm
d["cu_co_dens"] = d.cu_co * d.dens_dm

print("pre-2010 mean union density (%): overall {:.1f}; corp&union {:.1f}; corp-only {:.1f}; controls {:.1f}".format(
    d.drop_duplicates('state').dens.mean(),
    d[d.state.isin(CORP_UNION)].drop_duplicates('state').dens.mean(),
    d[d.state.isin(CORP_ONLY)].drop_duplicates('state').dens.mean(),
    d[~d.state.isin(CORP_UNION+CORP_ONLY)].drop_duplicates('state').dens.mean()))

rows = []
for outc in ["atr_top1", "rs"]:
    specs = {
        "densOnly": f"{outc} ~ cu_dens + C(state) + C(year)",
        "bans+dens": f"{outc} ~ cu_co + cu_cw + cu_dens + C(state) + C(year)",
        "bans+dens+within": f"{outc} ~ cu_co + cu_cw + cu_dens + cu_cw_dens + cu_co_dens + C(state) + C(year)",
    }
    for lab, f in specs.items():
        m = smf.ols(f, data=d).fit(cov_type="cluster", cov_kwds={"groups": d.state}, use_t=True)
        r = dict(outcome=outc, spec=lab)
        for t in ["cu_co", "cu_cw", "cu_dens", "cu_cw_dens", "cu_co_dens"]:
            if t in m.params:
                r[t] = round(m.params[t], 3)
                r[t + "_p"] = round(m.pvalues[t], 3)
        rows.append(r)
res = pd.DataFrame(rows)
res.to_csv("results/union_density_moderator.csv", index=False)
print(res.to_string(index=False))
