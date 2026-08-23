"""Partisan-control horse-race specifications for the replication panel.

The estimators in this module are a path-independent refactor of the legacy
``horserace/horserace.py`` script.  Data-frame inputs make the statistical core easy
to test, while the default paths point to the committed panel and partisan-control
files in the replication directory.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from cu_replication.constants import (
    CORP_ONLY_STATES,
    CORP_UNION_STATES,
    EXCLUDED_STATES,
    REDMAP_STATES,
)

REPLICATION_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PANEL_PATH = REPLICATION_ROOT / "results" / "panel_state_year.csv"
DEFAULT_PARTISAN_PATH = REPLICATION_ROOT / "horserace" / "partisan_control.csv"
DEFAULT_OUTPUT_DIR = REPLICATION_ROOT / "horserace"

DataSource = pd.DataFrame | str | Path

OUTCOMES = ("atr_top1", "rs", "atr_top5", "beta")
BASE_TERMS = ("cu_x_corp_only", "cu_x_corp_union")
TERM_LABELS = {
    "cu_x_corp_only": "CU x CorpOnly",
    "cu_x_corp_union": "CU x CorpUnion",
    "cu_x_rep_trifecta_acq": "CU x R-trifecta acquirer",
    "rep_trifecta": "R trifecta (t)",
    "rep_trifecta_lag": "R trifecta (t-1)",
    "cu_x_redmap": "CU x REDMAP",
}

PARTY_COLUMNS = (
    "governor_party",
    "lower_chamber_majority_party",
    "upper_chamber_majority_party",
)
PARTISAN_COLUMNS = (
    "state",
    "year",
    *PARTY_COLUMNS,
    "rep_trifecta",
)


def read_frame(source: DataSource) -> pd.DataFrame:
    """Return a defensive copy of a data frame or load a CSV path."""
    if isinstance(source, pd.DataFrame):
        return source.copy()
    return pd.read_csv(Path(source))


def identify_trifecta_acquirers(partisan: pd.DataFrame) -> set[str]:
    """Identify states acquiring an R trifecta during the 2011--13 wave.

    Acquisition follows the legacy definition exactly: a state must have no
    Republican trifecta in both 2009 and 2010 and at least one in 2011--13.
    """
    required_years = [2009, 2010, 2011, 2012, 2013]
    wide = partisan.pivot(index="state", columns="year", values="rep_trifecta")
    missing_years = sorted(set(required_years) - set(wide.columns))
    if missing_years:
        years = ", ".join(map(str, missing_years))
        raise ValueError(f"Partisan-control data are missing required years: {years}")
    acquired = wide[[2009, 2010]].eq(0).all(axis=1)
    acquired &= wide[[2011, 2012, 2013]].eq(1).any(axis=1)
    return set(wide.index[acquired])


def validate_partisan_control(partisan: pd.DataFrame) -> None:
    """Validate the fields and internal trifecta coding of the partisan panel."""
    missing = sorted(set(PARTISAN_COLUMNS) - set(partisan.columns))
    if missing:
        raise ValueError(
            "Partisan-control columns are missing: " + ", ".join(missing)
        )
    if partisan.duplicated(["state", "year"]).any():
        raise ValueError("Partisan-control data contain duplicate state-year rows")

    if not set(partisan["governor_party"].dropna()) <= {
        "Republican",
        "Democratic",
        "Independent",
    }:
        raise ValueError("Partisan-control data contain an unknown governor party")
    chamber_values = {"Republican", "Democratic", "Split"}
    for chamber in PARTY_COLUMNS[1:]:
        if not set(partisan[chamber].dropna()) <= chamber_values:
            raise ValueError(f"Partisan-control data contain an unknown {chamber}")

    computed = partisan.loc[:, PARTY_COLUMNS].eq("Republican").all(axis=1).astype(int)
    comparable = partisan["state"].ne("NE")
    if not partisan.loc[comparable, "rep_trifecta"].eq(
        computed.loc[comparable]
    ).all():
        raise ValueError("rep_trifecta disagrees with its three party components")


def prepare_analysis_panel(
    panel: pd.DataFrame,
    partisan: pd.DataFrame,
) -> tuple[pd.DataFrame, set[str]]:
    """Merge tax outcomes with partisan controls and construct model regressors."""
    panel_required = {"state", "year", *OUTCOMES}
    missing = sorted(panel_required - set(panel.columns))
    if missing:
        raise ValueError("Tax-panel columns are missing: " + ", ".join(missing))
    if panel.duplicated(["state", "year"]).any():
        raise ValueError("Tax panel contains duplicate state-year rows")

    validate_partisan_control(partisan)
    acquired = identify_trifecta_acquirers(partisan)
    analysis = panel.loc[~panel["state"].isin(EXCLUDED_STATES)].copy()
    analysis = analysis.merge(
        partisan.loc[:, PARTISAN_COLUMNS],
        on=["state", "year"],
        how="left",
        validate="one_to_one",
    )
    if analysis["rep_trifecta"].isna().any():
        missing_states = sorted(
            analysis.loc[analysis["rep_trifecta"].isna(), "state"].unique()
        )
        raise ValueError(
            "Partisan controls are missing for analysis states: "
            + ", ".join(missing_states)
        )

    analysis["cu"] = analysis["year"].ge(2010).astype(int)
    analysis["corp_only"] = analysis["state"].isin(CORP_ONLY_STATES).astype(int)
    analysis["corp_union"] = analysis["state"].isin(CORP_UNION_STATES).astype(int)
    analysis["rep_trifecta_acq"] = analysis["state"].isin(acquired).astype(int)
    analysis["redmap"] = analysis["state"].isin(REDMAP_STATES).astype(int)
    for name in ("corp_only", "corp_union", "rep_trifecta_acq", "redmap"):
        analysis[f"cu_x_{name}"] = analysis["cu"] * analysis[name]

    analysis = analysis.sort_values(["state", "year"]).reset_index(drop=True)
    analysis["rep_trifecta_lag"] = analysis.groupby("state")[
        "rep_trifecta"
    ].shift(1)
    return analysis, acquired


def load_analysis_panel(
    panel: DataSource | None = None,
    partisan_control: DataSource | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, set[str]]:
    """Load or copy inputs and return the merged horse-race analysis panel.

    With no arguments, the function reads ``results/panel_state_year.csv`` and
    ``horserace/partisan_control.csv`` beneath the replication root.
    """
    panel_frame = read_frame(DEFAULT_PANEL_PATH if panel is None else panel)
    partisan_frame = read_frame(
        DEFAULT_PARTISAN_PATH if partisan_control is None else partisan_control
    )
    analysis, acquired = prepare_analysis_panel(panel_frame, partisan_frame)
    return analysis, partisan_frame, acquired


def fit_twfe(
    frame: pd.DataFrame,
    outcome: str,
    terms: Sequence[str],
):
    """Fit TWFE OLS with CR1 state-clustered covariance and cluster-t tests."""
    selected_terms = list(terms)
    model_frame = frame.dropna(subset=[outcome, *selected_terms]).copy()
    formula = f"{outcome} ~ {' + '.join(selected_terms)} + C(state) + C(year)"
    model = smf.ols(formula, data=model_frame).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": model_frame["state"],
            "use_correction": True,
            "df_correction": True,
        },
        use_t=True,
    )
    return model, model_frame


def specifications() -> list[dict[str, object]]:
    """Return the legacy trifecta, REDMAP, no-ban, and restricted model grid."""
    base = list(BASE_TERMS)
    return [
        {
            "spec": "a_baseline",
            "label": "(a) Baseline",
            "terms": base,
            "added": [],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "b_acquirer",
            "label": "(b) + CU x R-trifecta acquirer",
            "terms": base + ["cu_x_rep_trifecta_acq"],
            "added": ["cu_x_rep_trifecta_acq"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "c_contemporaneous",
            "label": "(c) + R trifecta (t)",
            "terms": base + ["rep_trifecta"],
            "added": ["rep_trifecta"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "c_lagged",
            "label": "(c-lag) + R trifecta (t-1)",
            "terms": base + ["rep_trifecta_lag"],
            "added": ["rep_trifecta_lag"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "d_redmap",
            "label": "(d) + CU x REDMAP",
            "terms": base + ["cu_x_redmap"],
            "added": ["cu_x_redmap"],
            "sample": "full",
            "key": True,
        },
        {
            "spec": "e_acquirer_redmap",
            "label": "(e) + acquirer and REDMAP",
            "terms": base + ["cu_x_rep_trifecta_acq", "cu_x_redmap"],
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


def _term_value(model, terms: Sequence[str], position: int, attribute: str):
    """Return a named model statistic for one optional added term."""
    if len(terms) <= position:
        return np.nan
    term = terms[position]
    return getattr(model, attribute).get(term, np.nan)


def run_models(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit every specification and return tidy and one-row-per-model outputs."""
    tidy_rows: list[dict[str, object]] = []
    model_rows: list[dict[str, object]] = []
    model_store: dict[tuple[str, str], object] = {}

    for outcome in OUTCOMES:
        for order, spec in enumerate(specifications()):
            sample = str(spec["sample"])
            model_input = (
                frame.loc[frame["corp_only"].eq(0)].copy()
                if sample == "restricted"
                else frame.copy()
            )
            terms = list(spec["terms"])
            added = list(spec["added"])
            spec_name = str(spec["spec"])
            model, used = fit_twfe(model_input, outcome, terms)
            model_store[(outcome, spec_name)] = model

            displayed = [
                term
                for term in [*BASE_TERMS, *added]
                if term in terms
            ]
            for term in displayed:
                tidy_rows.append(
                    {
                        "outcome": outcome,
                        "spec_order": order,
                        "spec": spec_name,
                        "spec_label": spec["label"],
                        "sample": sample,
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

            model_rows.append(
                {
                    "outcome": outcome,
                    "spec_order": order,
                    "spec": spec_name,
                    "spec_label": spec["label"],
                    "sample": sample,
                    "key_table": spec["key"],
                    "corp_union_coef": model.params.get(
                        "cu_x_corp_union", np.nan
                    ),
                    "corp_union_se": model.bse.get("cu_x_corp_union", np.nan),
                    "corp_union_p": model.pvalues.get("cu_x_corp_union", np.nan),
                    "corp_only_coef": model.params.get("cu_x_corp_only", np.nan),
                    "corp_only_se": model.bse.get("cu_x_corp_only", np.nan),
                    "corp_only_p": model.pvalues.get("cu_x_corp_only", np.nan),
                    "added_terms": "; ".join(TERM_LABELS[term] for term in added),
                    "added_1_term": TERM_LABELS[added[0]] if added else "",
                    "added_1_coef": _term_value(model, added, 0, "params"),
                    "added_1_se": _term_value(model, added, 0, "bse"),
                    "added_1_p": _term_value(model, added, 0, "pvalues"),
                    "added_2_term": TERM_LABELS[added[1]] if len(added) > 1 else "",
                    "added_2_coef": _term_value(model, added, 1, "params"),
                    "added_2_se": _term_value(model, added, 1, "bse"),
                    "added_2_p": _term_value(model, added, 1, "pvalues"),
                    "nobs": int(model.nobs),
                    "clusters": int(used["state"].nunique()),
                    "formula": model.model.formula,
                }
            )

    models = pd.DataFrame(model_rows)
    models["attenuation_vs_matched_sample_pct"] = np.nan
    for outcome in OUTCOMES:
        baseline = model_store[(outcome, "a_baseline")].params[
            "cu_x_corp_union"
        ]
        restricted_baseline = model_store[
            (outcome, "g0_restricted_baseline")
        ].params["cu_x_corp_union"]
        outcome_rows = models["outcome"].eq(outcome)
        coefficients = models.loc[outcome_rows, "corp_union_coef"]
        models.loc[outcome_rows, "attenuation_vs_a_pct"] = (
            100 * (abs(baseline) - coefficients.abs()) / abs(baseline)
        )
        models.loc[
            outcome_rows, "attenuation_vs_restricted_baseline_pct"
        ] = (
            100
            * (abs(restricted_baseline) - coefficients.abs())
            / abs(restricted_baseline)
        )

        lag_baseline, _ = fit_twfe(
            frame.loc[frame["year"].ge(2005)].copy(), outcome, BASE_TERMS
        )
        restricted_lag_baseline, _ = fit_twfe(
            frame.loc[frame["year"].ge(2005) & frame["corp_only"].eq(0)].copy(),
            outcome,
            ["cu_x_corp_union"],
        )
        lag_rows = outcome_rows & models["spec"].eq("c_lagged")
        restricted_lag_rows = outcome_rows & models["spec"].eq(
            "g_restricted_lagged"
        )
        lag_coefficient = lag_baseline.params["cu_x_corp_union"]
        restricted_lag_coefficient = restricted_lag_baseline.params[
            "cu_x_corp_union"
        ]
        models.loc[lag_rows, "attenuation_vs_matched_sample_pct"] = models.loc[
            lag_rows, "corp_union_coef"
        ].abs().rsub(abs(lag_coefficient)).mul(100).div(abs(lag_coefficient))
        models.loc[
            restricted_lag_rows, "attenuation_vs_matched_sample_pct"
        ] = (
            models.loc[restricted_lag_rows, "corp_union_coef"]
            .abs()
            .rsub(abs(restricted_lag_coefficient))
            .mul(100)
            .div(abs(restricted_lag_coefficient))
        )

    return pd.DataFrame(tidy_rows), models


def acquisition_counts(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the 2-by-3 acquisition-wave overlap table for analysis states."""
    state_frame = frame.sort_values("year").groupby("state", as_index=False).first()
    state_frame["ban_group"] = np.select(
        [state_frame["corp_union"].eq(1), state_frame["corp_only"].eq(1)],
        ["CorpUnion", "CorpOnly"],
        default="Controls",
    )
    counts = (
        state_frame.groupby(["rep_trifecta_acq", "ban_group"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=[1, 0], columns=["CorpUnion", "CorpOnly", "Controls"])
        .reset_index()
    )
    counts.columns.name = None
    return counts


def run_horserace(
    panel: DataSource | None = None,
    partisan_control: DataSource | None = None,
) -> dict[str, pd.DataFrame]:
    """Estimate the horse race and return its core publication-ready outputs."""
    analysis, _, _ = load_analysis_panel(panel, partisan_control)
    tidy, models = run_models(analysis)
    key_models = models.loc[models["key_table"]].copy()
    no_ban_models = models.loc[models["spec"].str.startswith("f_")].copy()
    baseline = tidy.loc[
        tidy["spec"].eq("a_baseline")
        & tidy["term"].isin(BASE_TERMS)
    ].copy()
    return {
        "horserace_tidy": tidy,
        "horserace_models": models,
        "key_models": key_models,
        "no_ban_models": no_ban_models,
        "baseline": baseline,
        "acquisition_counts": acquisition_counts(analysis),
    }


def write_horserace_outputs(
    outputs: dict[str, pd.DataFrame],
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> tuple[Path, ...]:
    """Write returned horse-race frames directly beneath *output_dir*."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, frame in outputs.items():
        path = destination / f"{name}.csv"
        frame.to_csv(path, index=False)
        paths.append(path)
    return tuple(paths)
