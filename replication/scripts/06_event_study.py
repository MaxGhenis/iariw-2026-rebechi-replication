"""06: Event study (paper eq. 8): year-dummies x ban-group, 2009 omitted,
controls = never-ban states. Main sample (47 units incl. DC). Cluster by state.
Saves results/event_study.csv and results/event_study.png.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CORP_UNION = ["AK","AZ","MI","NH","NC","ND","OH","OK","PA","RI","TX","WI","WY"]
CORP_ONLY  = ["CT","IA","KY","MA","MN","MT","TN","WV"]
EXCLUDE    = ["CO","SD","NE","LA"]

panel = pd.read_csv("results/panel_state_year.csv")
d = panel[~panel.state.isin(EXCLUDE)].copy()
d["co"] = d.state.isin(CORP_ONLY).astype(int)
d["cw"] = d.state.isin(CORP_UNION).astype(int)

years = sorted(d.year.unique())
terms = []
for y in years:
    if y == 2009:
        continue
    d[f"co_{y}"] = (d.year == y) * d.co
    d[f"cw_{y}"] = (d.year == y) * d.cw
    terms += [f"co_{y}", f"cw_{y}"]

rows = []
for outcome in ["atr_top1", "rs", "atr_top5", "atr"]:
    m = smf.ols(f"{outcome} ~ {' + '.join(terms)} + C(state) + C(year)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d.state}, use_t=True)
    for y in years:
        if y == 2009:
            rows.append(dict(outcome=outcome, year=y, group="corp_union", b=0, se=0))
            rows.append(dict(outcome=outcome, year=y, group="corp_only", b=0, se=0))
        else:
            rows.append(dict(outcome=outcome, year=y, group="corp_union",
                             b=m.params[f"cw_{y}"], se=m.bse[f"cw_{y}"]))
            rows.append(dict(outcome=outcome, year=y, group="corp_only",
                             b=m.params[f"co_{y}"], se=m.bse[f"co_{y}"]))
es = pd.DataFrame(rows)
es.to_csv("results/event_study.csv", index=False)

fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharex=True)
for ax, outcome, ttl in zip(axes.flat,
                            ["atr_top1", "rs", "atr_top5", "atr"],
                            ["ATR top 1% (pp)", "Reynolds-Smolensky (x100)",
                             "ATR top 5% (pp)", "ATR overall (pp)"]):
    for grp, color, off, lab in [("corp_union", "#b13636", -0.12, "corp & union ban"),
                                 ("corp_only", "#3465a4", 0.12, "corp-only ban")]:
        g = es[(es.outcome == outcome) & (es.group == grp)].sort_values("year")
        ax.errorbar(g.year + off, g.b, yerr=1.96 * g.se, fmt="o-", ms=3, lw=1,
                    capsize=2, color=color, label=lab)
    ax.axvline(2009.5, color="gray", ls="--", lw=0.8)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_title(ttl, fontsize=10)
axes[0, 0].legend(fontsize=8)
fig.suptitle("Event study vs 2009: replication (46 states + DC, state taxes only)", fontsize=11)
fig.tight_layout()
fig.savefig("results/event_study.png", dpi=130)
print("wrote results/event_study.csv and .png")
print(es[(es.outcome=="atr_top1") & (es.group=="corp_union")][["year","b","se"]].round(3).to_string(index=False))
