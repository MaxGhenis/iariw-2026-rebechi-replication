#!/usr/bin/env python3
"""Reproduce and extend the Citizens United / partisan-control horse race.

Run with:
    uv run --with pandas,numpy,statsmodels,requests,lxml,bs4 python horserace.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"

EXCLUDED = {"CO", "SD", "NE", "LA"}
CORP_ONLY = {"CT", "IA", "KY", "MA", "MN", "MT", "TN", "WV"}
CORP_UNION = {
    "AK",
    "AZ",
    "MI",
    "NH",
    "NC",
    "ND",
    "OH",
    "OK",
    "PA",
    "RI",
    "TX",
    "WI",
    "WY",
}
OUTCOMES = ("atr_top1", "rs", "atr_top5", "beta")
REDMAP = {"MI", "OH", "PA", "TX", "NC", "WI"}
PLACEBO_SEED = 20260823
PLACEBO_DRAWS = 10_000

BASE_TERMS = ["cu_x_corp_only", "cu_x_corp_union"]
TERM_LABELS = {
    "cu_x_corp_only": "CU x CorpOnly",
    "cu_x_corp_union": "CU x CorpUnion",
    "cu_x_rep_trifecta_acq": "CU x R-trifecta acquirer",
    "rep_trifecta": "R trifecta (t)",
    "rep_trifecta_lag": "R trifecta (t-1)",
    "cu_x_redmap": "CU x REDMAP",
}


def load_analysis_panel() -> tuple[pd.DataFrame, pd.DataFrame, set[str]]:
    """Load, validate, and merge the tax and partisan-control panels."""
    df = pd.read_csv(ROOT / "panel_state_year.csv")
    df = df.loc[~df["state"].isin(EXCLUDED)].copy()
    partisan = pd.read_csv(ROOT / "partisan_control.csv")

    assert len(partisan) == 51 * 18
    assert not partisan.duplicated(["state", "year"]).any()
    assert partisan["source"].notna().all()
    assert partisan["source_url"].notna().all()
    assert set(partisan["governor_party"].dropna()) <= {
        "Republican",
        "Democratic",
        "Independent",
    }
    for chamber in (
        "lower_chamber_majority_party",
        "upper_chamber_majority_party",
    ):
        assert set(partisan[chamber].dropna()) <= {
            "Republican",
            "Democratic",
            "Split",
        }

    computed_rep = (
        partisan[
            [
                "governor_party",
                "lower_chamber_majority_party",
                "upper_chamber_majority_party",
            ]
        ]
        .eq("Republican")
        .all(axis=1)
        .astype(int)
    )
    comparable = partisan["state"].ne("NE")
    assert partisan.loc[comparable, "rep_trifecta"].eq(
        computed_rep.loc[comparable]
    ).all()

    wide = partisan.pivot(index="state", columns="year", values="rep_trifecta")
    acquired = set(
        wide.index[
            wide[[2009, 2010]].eq(0).all(axis=1)
            & wide[[2011, 2012, 2013]].eq(1).any(axis=1)
        ]
    )

    df = df.merge(
        partisan[
            [
                "state",
                "year",
                "governor_party",
                "lower_chamber_majority_party",
                "upper_chamber_majority_party",
                "rep_trifecta",
            ]
        ],
        on=["state", "year"],
        how="left",
        validate="one_to_one",
    )
    assert df["rep_trifecta"].notna().all()

    df["cu"] = (df["year"] >= 2010).astype(int)
    df["corp_only"] = df["state"].isin(CORP_ONLY).astype(int)
    df["corp_union"] = df["state"].isin(CORP_UNION).astype(int)
    df["rep_trifecta_acq"] = df["state"].isin(acquired).astype(int)
    df["redmap"] = df["state"].isin(REDMAP).astype(int)
    df["cu_x_corp_only"] = df["cu"] * df["corp_only"]
    df["cu_x_corp_union"] = df["cu"] * df["corp_union"]
    df["cu_x_rep_trifecta_acq"] = df["cu"] * df["rep_trifecta_acq"]
    df["cu_x_redmap"] = df["cu"] * df["redmap"]
    df = df.sort_values(["state", "year"]).reset_index(drop=True)
    df["rep_trifecta_lag"] = df.groupby("state")["rep_trifecta"].shift(1)
    return df, partisan, acquired


def fit_twfe(df: pd.DataFrame, outcome: str, terms: list[str]):
    """Fit TWFE OLS with CR1 state-clustered covariance and cluster-t tests."""
    model_df = df.dropna(subset=[outcome, *terms]).copy()
    formula = f"{outcome} ~ {' + '.join(terms)} + C(state) + C(year)"
    model = smf.ols(formula, data=model_df).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": model_df["state"],
            "use_correction": True,
            "df_correction": True,
        },
        use_t=True,
    )
    return model, model_df


def specifications() -> list[dict]:
    """Requested model grid plus transparent no-ban and restricted variants."""
    return [
        {
            "spec": "a_baseline",
            "label": "(a) Baseline",
            "terms": BASE_TERMS,
            "added": [],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "b_acquirer",
            "label": "(b) + CU x R-trifecta acquirer",
            "terms": BASE_TERMS + ["cu_x_rep_trifecta_acq"],
            "added": ["cu_x_rep_trifecta_acq"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "c_contemporaneous",
            "label": "(c) + R trifecta (t)",
            "terms": BASE_TERMS + ["rep_trifecta"],
            "added": ["rep_trifecta"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "c_lagged",
            "label": "(c-lag) + R trifecta (t-1)",
            "terms": BASE_TERMS + ["rep_trifecta_lag"],
            "added": ["rep_trifecta_lag"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "d_redmap",
            "label": "(d) + CU x REDMAP",
            "terms": BASE_TERMS + ["cu_x_redmap"],
            "added": ["cu_x_redmap"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "e_acquirer_redmap",
            "label": "(e) + acquirer and REDMAP",
            "terms": BASE_TERMS
            + ["cu_x_rep_trifecta_acq", "cu_x_redmap"],
            "added": ["cu_x_rep_trifecta_acq", "cu_x_redmap"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "f_acquirer_no_bans",
            "label": "(f-acq) Acquirer only; no ban terms",
            "terms": ["cu_x_rep_trifecta_acq"],
            "added": ["cu_x_rep_trifecta_acq"],
            "sample": "full",
            "key": False,
        },
        {
            "spec": "f_contemporaneous_no_bans",
            "label": "(f-t) R trifecta (t) only; no ban terms",
            "terms": ["rep_trifecta"],
            "added": ["rep_trifecta"],
            "sample": "full",
            "key": False,
        },
        {
            "spec": "f_lagged_no_bans",
            "label": "(f-lag) R trifecta (t-1) only; no ban terms",
            "terms": ["rep_trifecta_lag"],
            "added": ["rep_trifecta_lag"],
            "sample": "full",
            "key": False,
        },
        {
            "spec": "f_redmap_no_bans",
            "label": "(f-map) REDMAP only; no ban terms",
            "terms": ["cu_x_redmap"],
            "added": ["cu_x_redmap"],
            "sample": "full",
            "key": False,
        },
        {
            "spec": "f_both_no_bans",
            "label": "(f) Acquirer + REDMAP; no ban terms",
            "terms": ["cu_x_rep_trifecta_acq", "cu_x_redmap"],
            "added": ["cu_x_rep_trifecta_acq", "cu_x_redmap"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "g0_restricted_baseline",
            "label": "Restricted baseline (13 CorpUnion + 26 controls)",
            "terms": ["cu_x_corp_union"],
            "added": [],
            "sample": "restricted",
            "key": False,
        },
        {
            "spec": "g_restricted_contemporaneous",
            "label": "(g) Restricted + R trifecta (t)",
            "terms": ["cu_x_corp_union", "rep_trifecta"],
            "added": ["rep_trifecta"],
            "sample": "restricted",
            "key": True,
        },
        {
            "spec": "g_restricted_lagged",
            "label": "(g-lag) Restricted + R trifecta (t-1)",
            "terms": ["cu_x_corp_union", "rep_trifecta_lag"],
            "added": ["rep_trifecta_lag"],
            "sample": "restricted",
            "key": True,
        },
    ]


def run_models(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit every specification and return tidy and one-row-per-model outputs."""
    tidy_rows: list[dict] = []
    model_rows: list[dict] = []
    model_store: dict[tuple[str, str], object] = {}

    for outcome in OUTCOMES:
        for order, spec in enumerate(specifications()):
            model_input = (
                df.loc[df["corp_only"].eq(0)].copy()
                if spec["sample"] == "restricted"
                else df.copy()
            )
            model, used = fit_twfe(model_input, outcome, spec["terms"])
            model_store[(outcome, spec["spec"])] = model

            displayed = [
                term
                for term in [*BASE_TERMS, *spec["added"]]
                if term in spec["terms"]
            ]
            for term in displayed:
                tidy_rows.append(
                    {
                        "outcome": outcome,
                        "spec_order": order,
                        "spec": spec["spec"],
                        "spec_label": spec["label"],
                        "sample": spec["sample"],
                        "term": term,
                        "term_label": TERM_LABELS[term],
                        "coef": model.params[term],
                        "se": model.bse[term],
                        "pvalue_cluster_t": model.pvalues[term],
                        "nobs": int(model.nobs),
                        "clusters": int(used["state"].nunique()),
                        "formula": model.model.formula,
                    }
                )

            row = {
                "outcome": outcome,
                "spec_order": order,
                "spec": spec["spec"],
                "spec_label": spec["label"],
                "sample": spec["sample"],
                "key_table": spec["key"],
                "corp_union_coef": model.params.get("cu_x_corp_union", np.nan),
                "corp_union_se": model.bse.get("cu_x_corp_union", np.nan),
                "corp_union_p": model.pvalues.get("cu_x_corp_union", np.nan),
                "corp_only_coef": model.params.get("cu_x_corp_only", np.nan),
                "corp_only_se": model.bse.get("cu_x_corp_only", np.nan),
                "corp_only_p": model.pvalues.get("cu_x_corp_only", np.nan),
                "added_terms": "; ".join(TERM_LABELS[t] for t in spec["added"]),
                "added_1_term": TERM_LABELS[spec["added"][0]]
                if spec["added"]
                else "",
                "added_1_coef": model.params.get(spec["added"][0], np.nan)
                if spec["added"]
                else np.nan,
                "added_1_se": model.bse.get(spec["added"][0], np.nan)
                if spec["added"]
                else np.nan,
                "added_1_p": model.pvalues.get(spec["added"][0], np.nan)
                if spec["added"]
                else np.nan,
                "added_2_term": TERM_LABELS[spec["added"][1]]
                if len(spec["added"]) > 1
                else "",
                "added_2_coef": model.params.get(spec["added"][1], np.nan)
                if len(spec["added"]) > 1
                else np.nan,
                "added_2_se": model.bse.get(spec["added"][1], np.nan)
                if len(spec["added"]) > 1
                else np.nan,
                "added_2_p": model.pvalues.get(spec["added"][1], np.nan)
                if len(spec["added"]) > 1
                else np.nan,
                "nobs": int(model.nobs),
                "clusters": int(used["state"].nunique()),
                "formula": model.model.formula,
            }
            model_rows.append(row)

    models = pd.DataFrame(model_rows)
    models["attenuation_vs_matched_sample_pct"] = np.nan
    for outcome in OUTCOMES:
        base = model_store[(outcome, "a_baseline")].params["cu_x_corp_union"]
        restricted_base = model_store[
            (outcome, "g0_restricted_baseline")
        ].params["cu_x_corp_union"]
        idx = models["outcome"].eq(outcome)
        models.loc[idx, "attenuation_vs_a_pct"] = models.loc[idx, "corp_union_coef"].map(
            lambda b: 100 * (abs(base) - abs(b)) / abs(base) if pd.notna(b) else np.nan
        )
        models.loc[idx, "attenuation_vs_restricted_baseline_pct"] = models.loc[
            idx, "corp_union_coef"
        ].map(
            lambda b: 100 * (abs(restricted_base) - abs(b)) / abs(restricted_base)
            if pd.notna(b)
            else np.nan
        )

        # The requested lagged models omit 2004. Retain movement relative to
        # full (a) above, and also expose an apples-to-apples 2005-21 sensitivity.
        lag_base, _ = fit_twfe(
            df.loc[df["year"].ge(2005)].copy(), outcome, BASE_TERMS
        )
        lag_restricted_base, _ = fit_twfe(
            df.loc[df["year"].ge(2005) & df["corp_only"].eq(0)].copy(),
            outcome,
            ["cu_x_corp_union"],
        )
        lag_idx = idx & models["spec"].eq("c_lagged")
        restricted_lag_idx = idx & models["spec"].eq("g_restricted_lagged")
        models.loc[lag_idx, "attenuation_vs_matched_sample_pct"] = models.loc[
            lag_idx, "corp_union_coef"
        ].map(
            lambda b: 100
            * (abs(lag_base.params["cu_x_corp_union"]) - abs(b))
            / abs(lag_base.params["cu_x_corp_union"])
        )
        models.loc[
            restricted_lag_idx, "attenuation_vs_matched_sample_pct"
        ] = models.loc[restricted_lag_idx, "corp_union_coef"].map(
            lambda b: 100
            * (abs(lag_restricted_base.params["cu_x_corp_union"]) - abs(b))
            / abs(lag_restricted_base.params["cu_x_corp_union"])
        )

    return pd.DataFrame(tidy_rows), models


def diagnostic_outputs(
    df: pd.DataFrame, partisan: pd.DataFrame, acquired: set[str]
) -> None:
    """Write source coverage, acquisition counts/list, and requested sanity checks."""
    state_df = df.sort_values("year").groupby("state", as_index=False).first()
    state_df["ban_group"] = np.select(
        [state_df["corp_union"].eq(1), state_df["corp_only"].eq(1)],
        ["CorpUnion", "CorpOnly"],
        default="Controls",
    )
    counts = (
        state_df.groupby(["rep_trifecta_acq", "ban_group"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=[1, 0], columns=["CorpUnion", "CorpOnly", "Controls"])
        .reset_index()
    )
    counts.to_csv(RESULTS / "acquisition_counts.csv", index=False)

    wide = partisan.pivot(index="state", columns="year", values="rep_trifecta")
    first_acq = {
        state: next(
            (year for year in (2011, 2012, 2013) if wide.loc[state, year] == 1),
            np.nan,
        )
        for state in acquired
    }
    all_states = pd.DataFrame({"state": sorted(partisan["state"].unique())})
    all_states["rep_trifecta_acq"] = all_states["state"].isin(acquired).astype(int)
    all_states["first_acquisition_year"] = all_states["state"].map(first_acq)
    all_states["rep_trifecta_2009"] = all_states["state"].map(wide[2009])
    all_states["rep_trifecta_2010"] = all_states["state"].map(wide[2010])
    all_states["in_analysis_sample"] = (~all_states["state"].isin(EXCLUDED)).astype(int)
    all_states["ban_group"] = np.select(
        [
            all_states["state"].isin(CORP_UNION),
            all_states["state"].isin(CORP_ONLY),
        ],
        ["CorpUnion", "CorpOnly"],
        default="Controls",
    )
    all_states.to_csv(RESULTS / "acquirer_list.csv", index=False)

    source_coverage = (
        partisan.groupby(["year", "source", "source_url"], as_index=False)
        .agg(jurisdictions=("state", "nunique"), rows=("state", "size"))
        .sort_values(["year", "source"])
    )
    source_coverage.to_csv(RESULTS / "source_coverage.csv", index=False)

    def all_components(state: str, years: list[int], party: str) -> bool:
        x = partisan.loc[
            partisan["state"].eq(state) & partisan["year"].isin(years)
        ]
        return bool(
            x[
                [
                    "governor_party",
                    "lower_chamber_majority_party",
                    "upper_chamber_majority_party",
                ]
            ]
            .eq(party)
            .all(axis=None)
        )

    checks = [
        {
            "check": "MI OH OK PA WI are 0 in 2009-10 and 1 in 2011",
            "passed": all(
                wide.loc[s, [2009, 2010, 2011]].tolist() == [0, 0, 1]
                for s in ["MI", "OH", "OK", "PA", "WI"]
            ),
        },
        {
            "check": "NC is 0 in 2009-10 and 1 in 2013",
            "passed": wide.loc["NC", [2009, 2010, 2013]].tolist() == [0, 0, 1],
        },
        {
            "check": "KS R trifecta throughout 2011-17",
            "passed": bool(wide.loc["KS", 2011:2017].eq(1).all()),
        },
        {
            "check": "MN Democratic trifecta 2013-14",
            "passed": all_components("MN", [2013, 2014], "Democratic"),
        },
        {
            "check": "CT Democratic trifecta 2011-21",
            "passed": all_components("CT", list(range(2011, 2022)), "Democratic"),
        },
        {
            "check": "TX UT ID ND R trifecta throughout 2004-21",
            "passed": all(
                bool(wide.loc[s, 2004:2021].eq(1).all())
                for s in ["TX", "UT", "ID", "ND"]
            ),
        },
        {
            "check": "NE rep_trifecta missing throughout",
            "passed": bool(wide.loc["NE", 2004:2021].isna().all()),
        },
        {
            "check": "DC rep_trifecta zero throughout",
            "passed": bool(wide.loc["DC", 2004:2021].eq(0).all()),
        },
    ]
    pd.DataFrame(checks).to_csv(RESULTS / "sanity_checks.csv", index=False)


def double_demean(matrix: np.ndarray) -> np.ndarray:
    """Remove state and year means from a balanced state-by-year matrix."""
    return (
        matrix
        - matrix.mean(axis=1, keepdims=True)
        - matrix.mean(axis=0, keepdims=True)
        + matrix.mean()
    )


def priority2_outputs(
    df: pd.DataFrame, partisan: pd.DataFrame, acquired: set[str]
) -> None:
    """Run seeded assignment placebos and the requested change descriptives."""
    states = np.array(sorted(df["state"].unique()))
    years = np.array(sorted(df["year"].unique()))
    n_states = len(states)
    n_years = len(years)
    nobs = len(df)
    assert n_states == 47 and n_years == 18 and nobs == n_states * n_years

    # In a balanced panel, FE-residualizing G_s * CU_t yields
    # (G_s - mean(G)) * (CU_t - mean(CU)), which permits fast exact draws.
    cu_centered = (years >= 2010).astype(float)
    cu_centered -= cu_centered.mean()
    cu_ss = float(cu_centered @ cu_centered)

    actual_union = np.isin(states, sorted(CORP_UNION)).astype(float)
    actual_only = np.isin(states, sorted(CORP_ONLY)).astype(float)
    actual_acq = np.isin(states, sorted(acquired)).astype(float)
    assert actual_union.sum() == 13
    assert actual_only.sum() == 8
    assert actual_acq.sum() == 15
    union_centered = actual_union - actual_union.mean()
    only_centered = actual_only - actual_only.mean()
    acq_centered = actual_acq - actual_acq.mean()

    rng = np.random.default_rng(PLACEBO_SEED)
    order = np.argsort(rng.random((PLACEBO_DRAWS, n_states)), axis=1)
    fake_union = np.zeros((PLACEBO_DRAWS, n_states), dtype=float)
    fake_only = np.zeros((PLACEBO_DRAWS, n_states), dtype=float)
    draw_rows = np.arange(PLACEBO_DRAWS)[:, None]
    fake_union[draw_rows, order[:, :13]] = 1.0
    fake_only[draw_rows, order[:, 13:21]] = 1.0
    fake_union -= 13 / n_states
    fake_only -= 8 / n_states
    assert np.allclose(fake_union.sum(axis=1), 0)
    assert np.allclose(fake_only.sum(axis=1), 0)

    # Because fake groups are disjoint and their sizes fixed, this 2x2
    # cross-product matrix is identical in every draw.
    random_xx = cu_ss * np.array(
        [
            [fake_union[0] @ fake_union[0], fake_union[0] @ fake_only[0]],
            [fake_only[0] @ fake_union[0], fake_only[0] @ fake_only[0]],
        ]
    )
    random_xx_inv = np.linalg.inv(random_xx)
    acq_xx = cu_ss * float(acq_centered @ acq_centered)
    df_fe = nobs - (n_states + n_years - 1)
    assert df_fe == 782

    summary_rows: list[dict] = []
    draw_frames: list[pd.DataFrame] = []
    for outcome in OUTCOMES:
        outcome_matrix = (
            df.pivot(index="state", columns="year", values=outcome)
            .loc[states, years]
            .to_numpy(dtype=float)
        )
        y_within = double_demean(outcome_matrix)
        y_ss = float(np.square(y_within).sum())
        # q_s = sum_t [(CU_t - mean(CU)) * y_within_st].
        q = y_within @ cu_centered

        random_xy = np.column_stack((fake_union @ q, fake_only @ q))
        random_beta = random_xy @ random_xx_inv.T
        random_sse = y_ss - np.einsum("ij,ij->i", random_beta, random_xy)
        random_r2 = 1 - random_sse / y_ss
        random_adj_r2 = 1 - (random_sse / (df_fe - 2)) / (y_ss / df_fe)

        acq_xy = float(acq_centered @ q)
        trifecta_sse = y_ss - acq_xy**2 / acq_xx
        trifecta_r2 = 1 - trifecta_sse / y_ss
        trifecta_adj_r2 = 1 - (trifecta_sse / (df_fe - 1)) / (
            y_ss / df_fe
        )

        actual_x = np.column_stack((union_centered, only_centered))
        actual_xx = cu_ss * (actual_x.T @ actual_x)
        actual_xy = actual_x.T @ q
        actual_beta = np.linalg.solve(actual_xx, actual_xy)
        actual_sse = y_ss - float(actual_beta @ actual_xy)
        actual_r2 = 1 - actual_sse / y_ss
        actual_adj_r2 = 1 - (actual_sse / (df_fe - 2)) / (y_ss / df_fe)

        random_xx_acq = np.zeros((PLACEBO_DRAWS, 3, 3))
        random_xx_acq[:, :2, :2] = random_xx
        random_xx_acq[:, 0, 2] = random_xx_acq[:, 2, 0] = (
            cu_ss * (fake_union @ acq_centered)
        )
        random_xx_acq[:, 1, 2] = random_xx_acq[:, 2, 1] = (
            cu_ss * (fake_only @ acq_centered)
        )
        random_xx_acq[:, 2, 2] = acq_xx
        random_xy_acq = np.column_stack(
            (random_xy, np.full(PLACEBO_DRAWS, acq_xy))
        )
        random_beta_acq = np.linalg.solve(
            random_xx_acq, random_xy_acq[:, :, None]
        )[:, :, 0]

        actual_xx_acq = np.zeros((3, 3))
        actual_xx_acq[:2, :2] = actual_xx
        actual_xx_acq[:2, 2] = actual_xx_acq[2, :2] = (
            cu_ss * (actual_x.T @ acq_centered)
        )
        actual_xx_acq[2, 2] = acq_xx
        actual_xy_acq = np.append(actual_xy, acq_xy)
        actual_beta_acq = np.linalg.solve(actual_xx_acq, actual_xy_acq)

        # FWL calculations should reproduce the corresponding formula models.
        baseline_model, _ = fit_twfe(df, outcome, BASE_TERMS)
        acq_model, _ = fit_twfe(
            df, outcome, BASE_TERMS + ["cu_x_rep_trifecta_acq"]
        )
        assert np.allclose(
            actual_beta,
            baseline_model.params[["cu_x_corp_union", "cu_x_corp_only"]],
        )
        assert np.allclose(
            actual_beta_acq,
            acq_model.params[
                [
                    "cu_x_corp_union",
                    "cu_x_corp_only",
                    "cu_x_rep_trifecta_acq",
                ]
            ],
        )

        observed_shrinkage = abs(actual_beta[0]) - abs(actual_beta_acq[0])
        random_shrinkage = np.abs(random_beta[:, 0]) - np.abs(
            random_beta_acq[:, 0]
        )
        r2_quantiles = np.quantile(random_r2, [0.05, 0.50, 0.95])
        adj_r2_quantiles = np.quantile(random_adj_r2, [0.05, 0.50, 0.95])
        shrinkage_quantiles = np.quantile(
            random_shrinkage, [0.05, 0.50, 0.95]
        )
        summary_rows.append(
            {
                "outcome": outcome,
                "seed": PLACEBO_SEED,
                "draws": PLACEBO_DRAWS,
                "states": n_states,
                "fake_corp_union_states": 13,
                "fake_corp_only_states": 8,
                "acquirer_states": int(actual_acq.sum()),
                "trifecta_only_partial_within_r2": trifecta_r2,
                "trifecta_only_adjusted_within_r2": trifecta_adj_r2,
                "actual_ban_partial_within_r2": actual_r2,
                "actual_ban_adjusted_within_r2": actual_adj_r2,
                "random_ban_r2_mean": random_r2.mean(),
                "random_ban_r2_p05": r2_quantiles[0],
                "random_ban_r2_p50": r2_quantiles[1],
                "random_ban_r2_p95": r2_quantiles[2],
                "random_ban_adjusted_r2_p05": adj_r2_quantiles[0],
                "random_ban_adjusted_r2_p50": adj_r2_quantiles[1],
                "random_ban_adjusted_r2_p95": adj_r2_quantiles[2],
                "share_random_ban_r2_le_trifecta_r2": np.mean(
                    random_r2 <= trifecta_r2
                ),
                "share_random_ban_adjusted_r2_le_trifecta_adjusted_r2": np.mean(
                    random_adj_r2 <= trifecta_adj_r2
                ),
                "share_random_ban_r2_ge_actual_ban_r2": np.mean(
                    random_r2 >= actual_r2
                ),
                "observed_union_coef_baseline": actual_beta[0],
                "observed_union_coef_plus_acquirer": actual_beta_acq[0],
                "observed_abs_union_shrinkage": observed_shrinkage,
                "random_abs_shrinkage_p05": shrinkage_quantiles[0],
                "random_abs_shrinkage_p50": shrinkage_quantiles[1],
                "random_abs_shrinkage_p95": shrinkage_quantiles[2],
                "share_random_abs_shrinkage_ge_observed": np.mean(
                    random_shrinkage >= observed_shrinkage
                ),
            }
        )
        draw_frames.append(
            pd.DataFrame(
                {
                    "outcome": outcome,
                    "draw": np.arange(1, PLACEBO_DRAWS + 1),
                    "random_ban_partial_within_r2": random_r2,
                    "random_ban_adjusted_within_r2": random_adj_r2,
                    "fake_union_coef_baseline": random_beta[:, 0],
                    "fake_union_coef_plus_acquirer": random_beta_acq[:, 0],
                    "fake_union_abs_shrinkage": random_shrinkage,
                }
            )
        )

    pd.DataFrame(summary_rows).to_csv(RESULTS / "placebo_summary.csv", index=False)
    pd.concat(draw_frames, ignore_index=True).to_csv(
        RESULTS / "placebo_draws.csv", index=False
    )

    # State-level 2009-to-2021 changes and mutually exclusive 2011-13
    # partisan-wave categories. The acquisition group gets first priority.
    change = (
        df.pivot(index="state", columns="year", values="atr_top1")[2021]
        - df.pivot(index="state", columns="year", values="atr_top1")[2009]
    ).rename("atr_top1_change_2009_2021")
    d_window = partisan.loc[partisan["year"].between(2011, 2013)].copy()
    d_window["d_trifecta"] = d_window[
        [
            "governor_party",
            "lower_chamber_majority_party",
            "upper_chamber_majority_party",
        ]
    ].eq("Democratic").all(axis=1)
    ever_d = d_window.groupby("state")["d_trifecta"].any()
    state_changes = change.reset_index()
    state_changes["rep_trifecta_acq"] = state_changes["state"].isin(acquired)
    state_changes["d_trifecta_2011_2013"] = state_changes["state"].map(ever_d)
    state_changes["partisan_group"] = np.select(
        [
            state_changes["rep_trifecta_acq"],
            state_changes["d_trifecta_2011_2013"],
        ],
        ["R-trifecta acquirers", "D trifectas in 2011-13"],
        default="Others",
    )
    state_changes["ban_group"] = np.select(
        [
            state_changes["state"].isin(CORP_UNION),
            state_changes["state"].isin(CORP_ONLY),
        ],
        ["CorpUnion", "CorpOnly"],
        default="Controls",
    )
    state_changes.to_csv(RESULTS / "state_changes.csv", index=False)

    descriptive_rows: list[dict] = []
    partisan_groups = [
        "R-trifecta acquirers",
        "D trifectas in 2011-13",
        "Others",
    ]
    for ban_group in ["All", "CorpUnion", "CorpOnly", "Controls"]:
        subset = (
            state_changes
            if ban_group == "All"
            else state_changes.loc[state_changes["ban_group"].eq(ban_group)]
        )
        for partisan_group in partisan_groups:
            cell = subset.loc[subset["partisan_group"].eq(partisan_group)]
            descriptive_rows.append(
                {
                    "ban_group": ban_group,
                    "partisan_group": partisan_group,
                    "states": len(cell),
                    "mean_atr_top1_change_2009_2021": cell[
                        "atr_top1_change_2009_2021"
                    ].mean(),
                }
            )
    pd.DataFrame(descriptive_rows).to_csv(
        RESULTS / "descriptive_changes.csv", index=False
    )


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    df, partisan, acquired = load_analysis_panel()
    assert len(df) == 846
    assert df["state"].nunique() == 47
    assert int(df["corp_union"].groupby(df["state"]).max().sum()) == 13
    assert int(df["corp_only"].groupby(df["state"]).max().sum()) == 8
    assert acquired == {
        "AK",
        "AL",
        "IN",
        "KS",
        "LA",
        "ME",
        "MI",
        "MS",
        "NC",
        "OH",
        "OK",
        "PA",
        "TN",
        "VA",
        "WI",
        "WY",
    }

    tidy, models = run_models(df)
    tidy.to_csv(RESULTS / "horserace_tidy.csv", index=False)
    models.to_csv(RESULTS / "horserace_models.csv", index=False)
    models.loc[models["key_table"]].to_csv(RESULTS / "key_models.csv", index=False)
    models.loc[models["spec"].str.startswith("f_")].to_csv(
        RESULTS / "no_ban_models.csv", index=False
    )
    tidy.loc[
        tidy["spec"].eq("a_baseline")
        & tidy["term"].isin(["cu_x_corp_only", "cu_x_corp_union"])
    ].to_csv(RESULTS / "baseline.csv", index=False)
    diagnostic_outputs(df, partisan, acquired)
    priority2_outputs(df, partisan, acquired)


if __name__ == "__main__":
    main()
