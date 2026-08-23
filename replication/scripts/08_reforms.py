"""08: Put a face on the number — changes in simulated top-1% ATR and RS around
well-known state reforms, plus the treated-minus-control mean series by year.
"""
import pandas as pd

CORP_UNION = ["AK","AZ","MI","NH","NC","ND","OH","OK","PA","RI","TX","WI","WY"]
CORP_ONLY  = ["CT","IA","KY","MA","MN","MT","TN","WV"]
EXCLUDE    = ["CO","SD","NE","LA"]

panel = pd.read_csv("results/panel_state_year.csv").set_index(["state","year"])
REFORMS = [
    ("NC", 2012, 2015, "2013 flat-tax reform: 7.75% top -> 5.75%"),
    ("OH", 2004, 2011, "2005-2011 21% across-the-board phase-down"),
    ("OH", 2012, 2015, "2013-2015 rate cuts"),
    ("ND", 2008, 2015, "2009/2011/2013/2015 rate cuts"),
    ("WI", 2012, 2014, "2013 rate cuts"),
    ("OK", 2004, 2016, "top rate 6.65% -> 5.0%"),
    ("CT", 2008, 2012, "2009/2011 top-bracket INCREASES (6.5%, 6.7%)"),
    ("MN", 2012, 2014, "2013 new 9.85% top bracket"),
]
rows = []
for st, y0, y1, note in REFORMS:
    a0, a1 = panel.loc[(st, y0), "atr_top1"], panel.loc[(st, y1), "atr_top1"]
    r0, r1 = panel.loc[(st, y0), "rs"], panel.loc[(st, y1), "rs"]
    rows.append(dict(state=st, from_y=y0, to_y=y1, note=note,
                     atr_top1_from=round(a0,2), atr_top1_to=round(a1,2),
                     d_atr_top1=round(a1-a0,2), rs_from=round(r0,3),
                     rs_to=round(r1,3), d_rs=round(r1-r0,3),
                     share_of_group_mean_if_alone=round((a1-a0)/13,3)))
ref = pd.DataFrame(rows)
ref.to_csv("results/illustrative_reforms.csv", index=False)
print(ref.to_string(index=False))

# treated-minus-control mean series
p = panel.reset_index()
p = p[~p.state.isin(EXCLUDE)]
grp = p.assign(group=lambda x: x.state.map(
    lambda s: "corp_union" if s in CORP_UNION else "corp_only" if s in CORP_ONLY else "control"))
series = grp.groupby(["group","year"])[["atr_top1","rs"]].mean().round(3)
wide = series.unstack("group")
wide.columns = [f"{a}_{b}" for a,b in wide.columns]
wide["gap_cw_ctrl_atr_top1"] = (wide.atr_top1_corp_union - wide.atr_top1_control).round(3)
wide["gap_cw_ctrl_rs"] = (wide.rs_corp_union - wide.rs_control).round(3)
wide.to_csv("results/group_means_by_year.csv")
print("\nGroup means by year (atr_top1):")
print(wide[["atr_top1_control","atr_top1_corp_only","atr_top1_corp_union",
            "gap_cw_ctrl_atr_top1","gap_cw_ctrl_rs"]].to_string())
