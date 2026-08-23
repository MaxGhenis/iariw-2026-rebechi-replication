"""Difference-in-differences estimation and inference."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from cu_replication.constants import (
    CORP_ONLY_STATES,
    CORP_UNION_STATES,
    EXCLUDED_STATES,
    NO_OR_LIMITED_INCOME_TAX_STATES,
    OUTCOMES_TABLE4,
)

EVENT_STUDY_OUTCOMES = ("atr_top1", "rs", "atr_top5", "atr")


def add_treatment_indicators(
    panel: pd.DataFrame, *, cu_from: int = 2010
) -> pd.DataFrame:
    """Return a copy with treatment groups and post interactions."""
    data = panel.copy()
    data["corp_only"] = data["state"].isin(CORP_ONLY_STATES).astype(int)
    data["corp_union"] = data["state"].isin(CORP_UNION_STATES).astype(int)
    data["cu"] = data["year"].ge(cu_from).astype(int)
    data["cu_co"] = data["cu"] * data["corp_only"]
    data["cu_cw"] = data["cu"] * data["corp_union"]
    return data


def analytic_sample(
    panel: pd.DataFrame,
    *,
    exclude_dc: bool = False,
    income_tax_only: bool = False,
    dropped_states: Iterable[str] = (),
) -> pd.DataFrame:
    """Return one of the paper's analytic samples."""
    exclusions = set(EXCLUDED_STATES) | set(dropped_states)
    if exclude_dc:
        exclusions.add("DC")
    if income_tax_only:
        exclusions.update(NO_OR_LIMITED_INCOME_TAX_STATES)
    return panel.loc[~panel["state"].isin(exclusions)].copy()


def fit_twfe(
    panel: pd.DataFrame, outcome: str, *, cu_from: int = 2010
):
    """Fit equation (7) with state/year fixed effects and state-clustered SEs."""
    data = add_treatment_indicators(panel, cu_from=cu_from)
    formula = f"{outcome} ~ cu_co + cu_cw + C(state) + C(year)"
    model = smf.ols(formula, data=data).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": data["state"],
            "use_correction": True,
            "df_correction": True,
        },
        use_t=True,
    )
    return model


def estimate_twfe(
    panel: pd.DataFrame, outcome: str, *, cu_from: int = 2010
) -> dict[str, float | int]:
    """Return equation (7) coefficients, clustered inference, and difference row."""
    model = fit_twfe(panel, outcome, cu_from=cu_from)
    difference = model.t_test("cu_cw = cu_co")
    return {
        "b1": float(model.params["cu_co"]),
        "se1": float(model.bse["cu_co"]),
        "p1": float(model.pvalues["cu_co"]),
        "b2": float(model.params["cu_cw"]),
        "se2": float(model.bse["cu_cw"]),
        "p2": float(model.pvalues["cu_cw"]),
        "diff": float(np.asarray(difference.effect).squeeze()),
        "sed": float(np.asarray(difference.sd).squeeze()),
        "pdiff": float(np.asarray(difference.pvalue).squeeze()),
        "n": int(model.nobs),
        "r2": float(model.rsquared),
    }


def estimate_table4(panel: pd.DataFrame) -> pd.DataFrame:
    """Reproduce all rows stored in ``results/table4_replication.csv``."""
    sample_specs = (
        ("main_846", analytic_sample(panel), 2010),
        ("noDC_828", analytic_sample(panel, exclude_dc=True), 2010),
        ("B1_702", analytic_sample(panel, income_tax_only=True), 2010),
        ("main_cu2011", analytic_sample(panel), 2011),
    )
    rows: list[dict[str, float | int | str]] = []
    for sample_name, sample, cu_from in sample_specs:
        for outcome in OUTCOMES_TABLE4:
            row = estimate_twfe(sample, outcome, cu_from=cu_from)
            row.update(
                {"outcome": outcome, "sample": sample_name, "cu_from": cu_from}
            )
            rows.append(row)
    return pd.DataFrame(rows)


def estimate_event_study(
    panel: pd.DataFrame,
    outcomes: Sequence[str] = EVENT_STUDY_OUTCOMES,
    *,
    reference_year: int = 2009,
) -> pd.DataFrame:
    """Estimate equation (8), with one omitted year and two ban groups."""
    data = analytic_sample(panel)
    data["co"] = data["state"].isin(CORP_ONLY_STATES).astype(int)
    data["cw"] = data["state"].isin(CORP_UNION_STATES).astype(int)
    years = sorted(data["year"].unique())
    terms: list[str] = []
    for year in years:
        if year == reference_year:
            continue
        data[f"co_{year}"] = data["year"].eq(year) * data["co"]
        data[f"cw_{year}"] = data["year"].eq(year) * data["cw"]
        terms.extend((f"co_{year}", f"cw_{year}"))

    rows: list[dict[str, float | int | str]] = []
    for outcome in outcomes:
        formula = f"{outcome} ~ {' + '.join(terms)} + C(state) + C(year)"
        model = smf.ols(formula, data=data).fit(
            cov_type="cluster",
            cov_kwds={
                "groups": data["state"],
                "use_correction": True,
                "df_correction": True,
            },
            use_t=True,
        )
        for year in years:
            if year == reference_year:
                rows.extend(
                    (
                        {
                            "outcome": outcome,
                            "year": year,
                            "group": "corp_union",
                            "b": 0.0,
                            "se": 0.0,
                        },
                        {
                            "outcome": outcome,
                            "year": year,
                            "group": "corp_only",
                            "b": 0.0,
                            "se": 0.0,
                        },
                    )
                )
                continue
            rows.extend(
                (
                    {
                        "outcome": outcome,
                        "year": year,
                        "group": "corp_union",
                        "b": float(model.params[f"cw_{year}"]),
                        "se": float(model.bse[f"cw_{year}"]),
                    },
                    {
                        "outcome": outcome,
                        "year": year,
                        "group": "corp_only",
                        "b": float(model.params[f"co_{year}"]),
                        "se": float(model.bse[f"co_{year}"]),
                    },
                )
            )
    return pd.DataFrame(rows)


def double_demean(matrix: np.ndarray) -> np.ndarray:
    """Remove row and column means from a balanced panel matrix."""
    matrix = np.asarray(matrix, dtype=float)
    return (
        matrix
        - matrix.mean(axis=1, keepdims=True)
        - matrix.mean(axis=0, keepdims=True)
        + matrix.mean()
    )


def twfe_coefficients(
    outcome_matrix: np.ndarray,
    post: np.ndarray,
    group_one_indices: Sequence[int],
    group_two_indices: Sequence[int],
) -> np.ndarray:
    """Fit two post-by-group coefficients by exact two-way demeaning."""
    outcome_matrix = np.asarray(outcome_matrix, dtype=float)
    post = np.asarray(post, dtype=float)
    state_count, year_count = outcome_matrix.shape
    if post.shape != (year_count,):
        raise ValueError("Post indicator length must equal the number of panel years")
    group_one = np.zeros((state_count, year_count))
    group_two = np.zeros((state_count, year_count))
    group_one[list(group_one_indices), :] = post
    group_two[list(group_two_indices), :] = post
    design = np.column_stack(
        (double_demean(group_one).ravel(), double_demean(group_two).ravel())
    )
    return np.linalg.lstsq(
        design, double_demean(outcome_matrix).ravel(), rcond=None
    )[0]


def randomization_inference(
    panel: pd.DataFrame,
    *,
    outcomes: Sequence[str] = ("atr_top1", "rs"),
    draws: int = 5_000,
    seed: int = 287,
) -> pd.DataFrame:
    """Permute fixed-size ban groups and return two-sided sharp-null p-values."""
    data = analytic_sample(panel).sort_values(["state", "year"])
    states = sorted(data["state"].unique())
    years = np.sort(data["year"].unique())
    post = years.__ge__(2010).astype(float)
    group_one = [states.index(state) for state in CORP_ONLY_STATES]
    group_two = [states.index(state) for state in CORP_UNION_STATES]
    generator = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for outcome in outcomes:
        matrix = (
            data.pivot(index="state", columns="year", values=outcome)
            .loc[states, years]
            .to_numpy()
        )
        b1, b2 = twfe_coefficients(matrix, post, group_one, group_two)
        observed_difference = b2 - b1
        permuted_b2 = np.empty(draws)
        permuted_difference = np.empty(draws)
        for draw in range(draws):
            assignment = generator.permutation(len(states))
            permuted_b1, permuted_b2_value = twfe_coefficients(
                matrix, post, assignment[:8], assignment[8:21]
            )
            permuted_b2[draw] = permuted_b2_value
            permuted_difference[draw] = permuted_b2_value - permuted_b1
        rows.append(
            {
                "outcome": outcome,
                "b1": b1,
                "b2": b2,
                "diff": observed_difference,
                "ri_p_b2": np.mean(np.abs(permuted_b2) >= abs(b2)),
                "ri_p_diff": np.mean(
                    np.abs(permuted_difference) >= abs(observed_difference)
                ),
                "draws": draws,
                "seed": seed,
            }
        )
    return pd.DataFrame(rows)


def leave_out_estimates(
    panel: pd.DataFrame,
    *,
    outcomes: Sequence[str] = ("atr_top1", "rs"),
) -> pd.DataFrame:
    """Return legacy single-state and selected joint leave-out coefficients."""
    data = analytic_sample(panel).sort_values(["state", "year"])
    drop_sets: tuple[str | tuple[str, ...], ...] = (
        *CORP_UNION_STATES,
        ("NC", "ND", "OH"),
        ("NC",),
        ("NC", "OH"),
    )
    years = np.sort(data["year"].unique())
    post = years.__ge__(2010).astype(float)
    rows: list[dict[str, float | str]] = []
    for outcome in outcomes:
        for drop in drop_sets:
            dropped = list(drop) if isinstance(drop, tuple) else [drop]
            sample = data.loc[~data["state"].isin(dropped)]
            states = sorted(sample["state"].unique())
            matrix = (
                sample.pivot(index="state", columns="year", values=outcome)
                .loc[states, years]
                .to_numpy()
            )
            group_one = [
                states.index(state) for state in CORP_ONLY_STATES if state in states
            ]
            group_two = [
                states.index(state) for state in CORP_UNION_STATES if state in states
            ]
            b1, b2 = twfe_coefficients(matrix, post, group_one, group_two)
            rows.append(
                {
                    "outcome": outcome,
                    "dropped": "+".join(dropped),
                    "b2": b2,
                    "diff": b2 - b1,
                }
            )
    return pd.DataFrame(rows)


def leave_three_out(panel: pd.DataFrame) -> pd.DataFrame:
    """Return clustered estimates after dropping NC, ND, and OH."""
    main = analytic_sample(panel)
    reduced = main.loc[~main["state"].isin(("NC", "ND", "OH"))]
    rows: list[dict[str, float | str]] = []
    for outcome in ("atr_top1", "rs"):
        baseline = estimate_twfe(main, outcome)
        leave_three = estimate_twfe(reduced, outcome)
        rows.append(
            {
                "outcome": outcome,
                "b2": baseline["b2"],
                "se2": baseline["se2"],
                "p_cluster_t": baseline["p2"],
                "b2_drop_NC_ND_OH": leave_three["b2"],
                "se2_drop": leave_three["se2"],
                "p_drop": leave_three["p2"],
            }
        )
    return pd.DataFrame(rows)


def per_state_did(
    panel: pd.DataFrame,
    *,
    outcomes: Sequence[str] = ("atr_top1", "rs"),
) -> pd.DataFrame:
    """Compute each treated state's plain pre/post DiD against never-ban controls."""
    data = analytic_sample(panel)
    treated = set(CORP_UNION_STATES) | set(CORP_ONLY_STATES)
    controls = data.loc[~data["state"].isin(treated)]
    rows: list[dict[str, float | str]] = []
    for outcome in outcomes:
        control_pre = controls.loc[controls["year"].lt(2010), outcome].mean()
        control_post = controls.loc[controls["year"].ge(2010), outcome].mean()
        control_change = control_post - control_pre
        for state in (*CORP_UNION_STATES, *CORP_ONLY_STATES):
            state_data = data.loc[data["state"].eq(state)]
            state_change = (
                state_data.loc[state_data["year"].ge(2010), outcome].mean()
                - state_data.loc[state_data["year"].lt(2010), outcome].mean()
            )
            rows.append(
                {
                    "outcome": outcome,
                    "state": state,
                    "group": (
                        "corp_union" if state in CORP_UNION_STATES else "corp_only"
                    ),
                    "did": state_change - control_change,
                }
            )
    return pd.DataFrame(rows)


def group_means_by_year(panel: pd.DataFrame) -> pd.DataFrame:
    """Return the rounded group-mean levels and treated-control gaps by year."""
    data = analytic_sample(panel)
    data["group"] = np.select(
        [
            data["state"].isin(CORP_UNION_STATES),
            data["state"].isin(CORP_ONLY_STATES),
        ],
        ["corp_union", "corp_only"],
        default="control",
    )
    series = (
        data.groupby(["group", "year"])[["atr_top1", "rs"]]
        .mean()
        .round(3)
    )
    wide = series.unstack("group")
    wide.columns = [f"{outcome}_{group}" for outcome, group in wide.columns]
    wide["gap_cw_ctrl_atr_top1"] = (
        wide["atr_top1_corp_union"] - wide["atr_top1_control"]
    ).round(3)
    wide["gap_cw_ctrl_rs"] = (
        wide["rs_corp_union"] - wide["rs_control"]
    ).round(3)
    return wide.reset_index()


def wild_bootstrap_pvalue(
    panel: pd.DataFrame,
    outcome: str,
    *,
    draws: int = 9_999,
    seed: int = 287,
) -> float | None:
    """Return a wild-cluster p-value when ``wildboottest`` is importable."""
    try:
        from wildboottest.wildboottest import wildboottest
    except ImportError:
        return None
    data = add_treatment_indicators(panel)
    clusters = pd.factorize(data["state"])[0]
    formula = f"{outcome} ~ cu_co + cu_cw + C(state) + C(year)"
    result = wildboottest(
        smf.ols(formula, data=data),
        param="cu_cw",
        cluster=clusters,
        B=draws,
        seed=seed,
    )
    return float(result["p-value"].iloc[0])
