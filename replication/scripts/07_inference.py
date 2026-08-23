"""07: Inference beyond clustered SEs, for atr_top1 and rs (main sample, N=846).

(a) Randomization inference: permute which 8 units are "corp-only" and which 13 are
    "corp&union" among the 47 units (sharp null, group sizes fixed), 5,000 draws.
    Balanced panel => TWFE via exact two-way demeaning (FWL), so each draw is cheap.
(b) Leave-one-out / leave-{NC,ND,OH}-out for the corp&union coefficient.
(c) Per-treated-state DiD vs never-ban controls (pre/post 2010 means).
"""
import numpy as np
import pandas as pd

CORP_UNION = ["AK","AZ","MI","NH","NC","ND","OH","OK","PA","RI","TX","WI","WY"]
CORP_ONLY  = ["CT","IA","KY","MA","MN","MT","TN","WV"]
EXCLUDE    = ["CO","SD","NE","LA"]
rng = np.random.default_rng(287)

panel = pd.read_csv("results/panel_state_year.csv")
d = panel[~panel.state.isin(EXCLUDE)].copy().sort_values(["state","year"])
states = sorted(d.state.unique()); S = len(states); T = d.year.nunique()
years = np.sort(d.year.unique())
cu = (years >= 2010).astype(float)                      # length T

def twfe(ymat, g1_idx, g2_idx):
    """ymat: S x T outcome. Returns (b1, b2) for CU x g1, CU x g2 via 2-way demeaning."""
    ns, nt = ymat.shape
    def dd(M):
        return M - M.mean(1, keepdims=True) - M.mean(0, keepdims=True) + M.mean()
    T1 = np.zeros((ns, nt)); T1[g1_idx, :] = cu
    T2 = np.zeros((ns, nt)); T2[g2_idx, :] = cu
    X = np.column_stack([dd(T1).ravel(), dd(T2).ravel()])
    b = np.linalg.lstsq(X, dd(ymat).ravel(), rcond=None)[0]
    return b

results = {}
for outcome in ["atr_top1", "rs"]:
    ymat = d.pivot(index="state", columns="year", values=outcome).loc[states].values
    i_co = [states.index(s) for s in CORP_ONLY]
    i_cw = [states.index(s) for s in CORP_UNION]
    b1_obs, b2_obs = twfe(ymat, i_co, i_cw)
    diff_obs = b2_obs - b1_obs

    NPERM = 5000
    b2_perm = np.empty(NPERM); diff_perm = np.empty(NPERM)
    for k in range(NPERM):
        perm = rng.permutation(S)
        p_co, p_cw = perm[:8], perm[8:8+13]
        p1, p2 = twfe(ymat, p_co, p_cw)
        b2_perm[k], diff_perm[k] = p2, p2 - p1
    ri_p_b2 = np.mean(np.abs(b2_perm) >= abs(b2_obs))
    ri_p_diff = np.mean(np.abs(diff_perm) >= abs(diff_obs))
    results[outcome] = dict(b1=b1_obs, b2=b2_obs, diff=diff_obs,
                            ri_p_b2=ri_p_b2, ri_p_diff=ri_p_diff)
    print(f"{outcome}: b1={b1_obs:.3f} b2={b2_obs:.3f} diff={diff_obs:.3f} | "
          f"RI p(b2)={ri_p_b2:.3f} RI p(diff)={ri_p_diff:.3f}")

pd.DataFrame(results).T.to_csv("results/randomization_inference.csv")

# (b) leave-out for corp&union coefficient
loo_rows = []
for outcome in ["atr_top1", "rs"]:
    for drop in CORP_UNION + [("NC","ND","OH"), ("NC",), ("NC","OH")]:
        drops = list(drop) if isinstance(drop, tuple) else [drop]
        sub = d[~d.state.isin(drops)]
        ss = sorted(sub.state.unique())
        ymat = sub.pivot(index="state", columns="year", values=outcome).loc[ss].values
        i_co = [ss.index(s) for s in CORP_ONLY if s in ss]
        i_cw = [ss.index(s) for s in CORP_UNION if s in ss]
        b1, b2 = twfe(ymat, i_co, i_cw)
        loo_rows.append(dict(outcome=outcome, dropped="+".join(drops), b2=b2, diff=b2-b1))
loo = pd.DataFrame(loo_rows)
loo.to_csv("results/leave_out.csv", index=False)
print("\nLeave-out (corp&union b2), atr_top1:")
print(loo[loo.outcome=="atr_top1"].round(3).to_string(index=False))

# (c) per-treated-state plain DiD vs never-ban controls
ctrl = d[~d.state.isin(CORP_UNION + CORP_ONLY)]
rows = []
for outcome in ["atr_top1", "rs"]:
    c_pre = ctrl[ctrl.year < 2010][outcome].mean()
    c_post = ctrl[ctrl.year >= 2010][outcome].mean()
    for s in CORP_UNION + CORP_ONLY:
        g = d[d.state == s]
        did = (g[g.year >= 2010][outcome].mean() - g[g.year < 2010][outcome].mean()) \
              - (c_post - c_pre)
        rows.append(dict(outcome=outcome, state=s,
                         group="corp_union" if s in CORP_UNION else "corp_only", did=did))
ps = pd.DataFrame(rows)
ps.to_csv("results/per_state_did.csv", index=False)
print("\nPer-state DiD (atr_top1, pp):")
print(ps[ps.outcome=="atr_top1"].sort_values("did").round(3).to_string(index=False))
print("\ncorp&union mean of per-state DiDs (should ~= b2):")
print(ps.groupby(["outcome","group"]).did.mean().round(3).to_string())
