"""Household-incidence and union-density heterogeneity analyses."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from cu_replication.constants import (
    CORP_ONLY_STATES,
    CORP_UNION_STATES,
    EXCLUDED_STATES,
)
from cu_replication.did import analytic_sample, estimate_twfe
from cu_replication.outcomes import weighted_quantile


def define_household_groups(
    base_households: pd.DataFrame,
    taxsim_2010: pd.DataFrame,
    *,
    reference_state: str = "CA",
) -> tuple[pd.DataFrame, dict[str, pd.Series], dict[str, float]]:
    """Define fixed micro-incidence groups from 2010 AGI and SCF characteristics."""
    base = base_households.set_index("hhid").copy()
    reference = taxsim_2010.loc[taxsim_2010["state"].eq(reference_state)]
    agi = reference.set_index("taxsimid")["v10_federal_agi"].reindex(base.index)
    if agi.isna().any():
        raise ValueError("The 2010 TAXSIM IDs do not align with base households")
    base["agi10"] = agi
    weights = base["wgt"].to_numpy()
    agi_values = base["agi10"].to_numpy()
    thresholds = {
        quantile: weighted_quantile(agi_values, weights, quantile)
        for quantile in (0.20, 0.80, 0.95, 0.99)
    }
    networth_p95 = weighted_quantile(base["networth"].to_numpy(), weights, 0.95)
    networth_p99 = weighted_quantile(base["networth"].to_numpy(), weights, 0.99)
    capital_income = base["dividends"] + base["intrec"] + base["ltcg"]
    capital_share = np.where(
        base["agi10"].gt(0), capital_income / base["agi10"].clip(lower=1), 0
    )
    wage_share = (base["pwages"] + base["swages"]) / base["agi10"].clip(lower=1)

    groups = {
        "agi_bottom20": base["agi10"].le(thresholds[0.20]),
        "agi_20_80": base["agi10"].gt(thresholds[0.20])
        & base["agi10"].le(thresholds[0.80]),
        "agi_80_95": base["agi10"].gt(thresholds[0.80])
        & base["agi10"].le(thresholds[0.95]),
        "agi_95_99": base["agi10"].gt(thresholds[0.95])
        & base["agi10"].le(thresholds[0.99]),
        "agi_top1": base["agi10"].gt(thresholds[0.99]),
        "nw_top5": base["networth"].ge(networth_p95),
        "nw_top1": base["networth"].ge(networth_p99),
        "capshare_gt50_agi50k": pd.Series(
            (capital_share > 0.5) & (agi_values > 50_000), index=base.index
        ),
        "capshare_lt10_agi50k": pd.Series(
            (capital_share < 0.1) & (agi_values > 50_000), index=base.index
        ),
        "wagesh_gt90_top5": wage_share.gt(0.9)
        & base["agi10"].gt(thresholds[0.95]),
        "age65plus": base["page"].ge(65),
        "married_kids": base["mstat"].eq("married, jointly")
        & base["depx"].gt(0),
    }
    mean_agi = {
        name: float(np.average(agi_values[mask], weights=weights[mask]))
        for name, mask in groups.items()
    }
    return base, groups, mean_agi


def collapse_group_atr_year(
    taxsim: pd.DataFrame,
    base_households: pd.DataFrame,
    groups: Mapping[str, pd.Series],
) -> pd.DataFrame:
    """Collapse one annual TAXSIM frame to group ATRs by state and year."""
    base = base_households.set_index("hhid")
    weights = base["wgt"]
    rows: list[dict[str, float | int | str]] = []
    year_values = taxsim["year"].unique()
    if len(year_values) != 1:
        raise ValueError("Group collapse input must contain exactly one year")
    for state, state_data in taxsim.groupby("state"):
        if state in EXCLUDED_STATES:
            continue
        ids = state_data["taxsimid"]
        agi = state_data["v10_federal_agi"].to_numpy()
        state_tax = state_data["siitax"].to_numpy()
        row_weights = ids.map(weights).to_numpy()
        row: dict[str, float | int | str] = {
            "state": state,
            "year": int(year_values[0]),
        }
        for group_name, household_mask in groups.items():
            mask = ids.map(household_mask).fillna(False).to_numpy(dtype=bool)
            denominator = np.sum(row_weights[mask] * agi[mask])
            row[group_name] = (
                100 * np.sum(row_weights[mask] * state_tax[mask]) / denominator
                if denominator > 0
                else np.nan
            )
        rows.append(row)
    return pd.DataFrame(rows)


def estimate_micro_incidence(
    group_panel: pd.DataFrame,
    mean_agi: Mapping[str, float],
) -> pd.DataFrame:
    """Estimate equation (7) within every fixed household group."""
    data = group_panel.copy()
    data["cu"] = data["year"].ge(2010).astype(int)
    data["cu_co"] = data["cu"] * data["state"].isin(CORP_ONLY_STATES)
    data["cu_cw"] = data["cu"] * data["state"].isin(CORP_UNION_STATES)
    rows: list[dict[str, float | int | str]] = []
    for group_name, group_mean_agi in mean_agi.items():
        formula = f"{group_name} ~ cu_co + cu_cw + C(state) + C(year)"
        model = smf.ols(formula, data=data).fit(
            cov_type="cluster",
            cov_kwds={"groups": data["state"]},
            use_t=True,
        )
        rows.append(
            {
                "group": group_name,
                "b1_corp_only": round(model.params["cu_co"], 3),
                "b2_corp_union": round(model.params["cu_cw"], 3),
                "se2": round(model.bse["cu_cw"], 3),
                "p2": round(model.pvalues["cu_cw"], 3),
                "mean_agi_2010usd": round(group_mean_agi),
                "dollar_effect_cw": round(
                    model.params["cu_cw"] / 100 * group_mean_agi
                ),
            }
        )
    return pd.DataFrame(rows)


def preperiod_union_density(union_panel: pd.DataFrame) -> pd.Series:
    """Return each state's mean total-sector union density over 2004--09."""
    required = {"sector", "year", "state2", "pctmem"}
    missing = sorted(required - set(union_panel.columns))
    if missing:
        raise ValueError(f"Union-density columns are missing: {', '.join(missing)}")
    selected = union_panel.loc[
        union_panel["sector"].eq("Total")
        & union_panel["year"].between(2004, 2009)
    ]
    return selected.groupby("state2")["pctmem"].mean() * 100


def estimate_union_density_moderator(
    panel: pd.DataFrame,
    union_panel: pd.DataFrame,
    *,
    outcomes: Sequence[str] = ("atr_top1", "rs"),
) -> pd.DataFrame:
    """Estimate the pre-period union-density moderator specifications."""
    density = preperiod_union_density(union_panel)
    data = analytic_sample(panel)
    data["dens"] = data["state"].map(density)
    if data["dens"].isna().any():
        missing_states = sorted(data.loc[data["dens"].isna(), "state"].unique())
        raise ValueError(f"Union density is missing for: {', '.join(missing_states)}")
    state_density = data.drop_duplicates("state")["dens"]
    data["dens_dm"] = data["dens"] - state_density.mean()
    data["cu"] = data["year"].ge(2010).astype(int)
    data["cu_co"] = data["cu"] * data["state"].isin(CORP_ONLY_STATES)
    data["cu_cw"] = data["cu"] * data["state"].isin(CORP_UNION_STATES)
    data["cu_dens"] = data["cu"] * data["dens_dm"]
    data["cu_cw_dens"] = data["cu_cw"] * data["dens_dm"]
    data["cu_co_dens"] = data["cu_co"] * data["dens_dm"]

    rows: list[dict[str, float | str]] = []
    for outcome in outcomes:
        specifications = {
            "densOnly": f"{outcome} ~ cu_dens + C(state) + C(year)",
            "bans+dens": (
                f"{outcome} ~ cu_co + cu_cw + cu_dens + C(state) + C(year)"
            ),
            "bans+dens+within": (
                f"{outcome} ~ cu_co + cu_cw + cu_dens + cu_cw_dens + "
                "cu_co_dens + C(state) + C(year)"
            ),
        }
        for label, formula in specifications.items():
            model = smf.ols(formula, data=data).fit(
                cov_type="cluster",
                cov_kwds={"groups": data["state"]},
                use_t=True,
            )
            row: dict[str, float | str] = {"outcome": outcome, "spec": label}
            for term in ("cu_co", "cu_cw", "cu_dens", "cu_cw_dens", "cu_co_dens"):
                if term in model.params:
                    row[term] = round(model.params[term], 3)
                    row[f"{term}_p"] = round(model.pvalues[term], 3)
            rows.append(row)
    return pd.DataFrame(rows)


def estimate_beta_incidence(panel: pd.DataFrame) -> pd.DataFrame:
    """Return the main-sample equation (7) result for the β incidence outcome."""
    result = estimate_twfe(analytic_sample(panel), "beta")
    return pd.DataFrame([{"outcome": "beta", **result}])
