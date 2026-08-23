"""04: Collapse simulated microdata to the state-year outcome panel.

Outcomes per paper Section 3.1, strategy 1 (state taxes only, main text):
  X = TAXSIM federal AGI (v10), T = state income tax liability (siitax).
  ATR            = 100 * sum(w*T)/sum(w*X)
  ATR top5/top1  = same within top-5%/1% of the WEIGHTED national AGI distribution
                   (thresholds computed per year over the fixed sample; identical
                   households are "top" in every state by construction)
  ATR top5/1 nw  = same but groups defined by SCF net worth (fixed over years)
  RS             = 100 * [Gini(X) - Gini(X - T)]; negatives clipped to 0 for Gini
  beta (eq. 5)   = ATR(top 20% by AGI) - ATR(bottom 20% by AGI)
"""
import numpy as np
import pandas as pd
import glob

def wquantile(x, w, q):
    o = np.argsort(x)
    x, w = x[o], w[o]
    c = np.cumsum(w)
    return np.interp(q * c[-1], c, x)

def wgini(x, w):
    x = np.clip(x, 0, None)
    o = np.argsort(x)
    x, w = x[o], w[o]
    f = w / w.sum()
    s = np.cumsum(f * x)
    if s[-1] <= 0:
        return np.nan
    return 1 - np.sum(f * (np.concatenate([[0], s[:-1]]) + s)) / s[-1]

base = pd.read_csv("data/base_households.csv")
nw = base.set_index("hhid")["networth"]
w_all = base.set_index("hhid")["wgt"]

# net-worth thresholds are year-invariant
nw_p95 = wquantile(nw.values, w_all.values, 0.95)
nw_p99 = wquantile(nw.values, w_all.values, 0.99)
print(f"net worth p95={nw_p95:,.0f} p99={nw_p99:,.0f} (2010$)")

rows = []
for f in sorted(glob.glob("data/taxsim_out_*.csv")):
    d = pd.read_csv(f)
    yr = int(d.year.iloc[0])
    d["wgt"] = d.taxsimid.map(w_all)
    d["networth"] = d.taxsimid.map(nw)
    # AGI must be state-invariant within year: check on first state pair
    agi_by_state = d.pivot_table(index="taxsimid", columns="state", values="v10_federal_agi")
    spread = (agi_by_state.max(axis=1) - agi_by_state.min(axis=1)).abs().max()
    assert spread < 1.0, f"AGI varies across states in {yr}: {spread}"
    # thresholds from any one state's AGI vector (national fixed sample)
    one = d[d.state == "CA"]
    agi_v, w_v = one.v10_federal_agi.values, one.wgt.values
    th = {q: wquantile(agi_v, w_v, q) for q in (0.20, 0.80, 0.95, 0.99)}
    for st, g in d.groupby("state"):
        agi, tax, w = g.v10_federal_agi.values, g.siitax.values, g.wgt.values
        def atr(mask):
            denom = np.sum(w[mask] * agi[mask])
            return 100 * np.sum(w[mask] * tax[mask]) / denom if denom != 0 else np.nan
        allm = np.ones(len(g), bool)
        rows.append(dict(
            state=st, year=yr,
            atr=atr(allm),
            atr_top5=atr(agi >= th[0.95]),
            atr_top1=atr(agi >= th[0.99]),
            atr_top5nw=atr(g.networth.values >= nw_p95),
            atr_top1nw=atr(g.networth.values >= nw_p99),
            rs=100 * (wgini(agi, w) - wgini(agi - tax, w)),
            beta=atr(agi >= th[0.80]) - atr(agi <= th[0.20]),
        ))
    print(f"{yr} done")

panel = pd.DataFrame(rows).sort_values(["state", "year"])
panel.to_csv("results/panel_state_year.csv", index=False)
print("wrote results/panel_state_year.csv", panel.shape)

# ---- sanity checks ----
p = panel.set_index(["state", "year"])
print("\nZero-tax states, mean ATR 2004-21 (should be ~0):")
print(panel[panel.state.isin(["TX","FL","WA","NV","AK","WY","SD"])].groupby("state").atr.mean().round(3).to_string())
print("\nTN/NH mean ATR (I&D taxes only, small):")
print(panel[panel.state.isin(["TN","NH"])].groupby("state").atr.mean().round(3).to_string())
print("\nNC top-1% ATR 2012->2015 (2013 flat-tax reform should cut it):")
print(p.loc[("NC", [2012,2013,2014,2015]), "atr_top1"].round(2).to_string())
print("\nKS overall ATR 2011->2017 (Brownback dip):")
print(p.loc[("KS", [2011,2012,2013,2016,2017,2018]), "atr"].round(2).to_string())
print("\nOH top-1% ATR 2004->2011 phase-down:")
print(p.loc[("OH", [2004,2006,2008,2010,2011]), "atr_top1"].round(2).to_string())
print("\nHigh-tax states 2010 (CA NY OR MN NJ HI):")
print(p.loc[(["CA","NY","OR","MN","NJ","HI"], 2010), "atr"].round(2).to_string())
