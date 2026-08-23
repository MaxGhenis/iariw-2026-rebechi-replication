"""Collapse TAXSIM microdata into the state-year outcome panel."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd

PANEL_COLUMNS = (
    "state",
    "year",
    "atr",
    "atr_top5",
    "atr_top1",
    "atr_top5nw",
    "atr_top1nw",
    "rs",
    "beta",
)


def weighted_quantile(
    values: np.ndarray, weights: np.ndarray, quantile: float
) -> float:
    """Return the legacy interpolation-based weighted quantile."""
    values = np.asarray(values)
    weights = np.asarray(weights)
    if values.shape != weights.shape:
        raise ValueError("Values and weights must have the same shape")
    if not 0 <= quantile <= 1:
        raise ValueError("Quantile must be between zero and one")
    order = np.argsort(values)
    sorted_values = values[order]
    cumulative_weights = np.cumsum(weights[order])
    if cumulative_weights[-1] <= 0:
        raise ValueError("Weights must have a positive sum")
    return float(
        np.interp(
            quantile * cumulative_weights[-1],
            cumulative_weights,
            sorted_values,
        )
    )


def weighted_gini(values: np.ndarray, weights: np.ndarray) -> float:
    """Return a weighted Gini after clipping negative values to zero."""
    values = np.clip(np.asarray(values), 0, None)
    weights = np.asarray(weights)
    if values.shape != weights.shape:
        raise ValueError("Values and weights must have the same shape")
    order = np.argsort(values)
    sorted_values = values[order]
    weight_shares = weights[order] / weights.sum()
    income_shares = np.cumsum(weight_shares * sorted_values)
    if income_shares[-1] <= 0:
        return float("nan")
    lagged = np.concatenate([[0], income_shares[:-1]])
    numerator = np.sum(weight_shares * (lagged + income_shares))
    return float(1 - numerator / income_shares[-1])


def average_tax_rate(
    agi: np.ndarray,
    state_tax: np.ndarray,
    weights: np.ndarray,
    mask: np.ndarray | None = None,
) -> float:
    """Return the income-weighted state average tax rate in percentage points."""
    agi = np.asarray(agi)
    state_tax = np.asarray(state_tax)
    weights = np.asarray(weights)
    if mask is None:
        mask = np.ones(len(agi), dtype=bool)
    denominator = np.sum(weights[mask] * agi[mask])
    if denominator == 0:
        return float("nan")
    return float(100 * np.sum(weights[mask] * state_tax[mask]) / denominator)


def collapse_taxsim_year(
    taxsim: pd.DataFrame,
    base_households: pd.DataFrame,
    *,
    reference_state: str = "CA",
) -> pd.DataFrame:
    """Collapse one year of all-jurisdiction TAXSIM output to outcome rows."""
    required_taxsim = {"taxsimid", "state", "year", "v10_federal_agi", "siitax"}
    missing_taxsim = sorted(required_taxsim - set(taxsim.columns))
    if missing_taxsim:
        raise ValueError(f"TAXSIM columns are missing: {', '.join(missing_taxsim)}")
    required_base = {"hhid", "wgt", "networth"}
    missing_base = sorted(required_base - set(base_households.columns))
    if missing_base:
        raise ValueError(f"Base columns are missing: {', '.join(missing_base)}")
    years = taxsim["year"].unique()
    if len(years) != 1:
        raise ValueError("A state-year collapse call must contain exactly one year")

    weight_lookup = base_households.set_index("hhid")["wgt"]
    networth_lookup = base_households.set_index("hhid")["networth"]
    data = taxsim.copy()
    data["wgt"] = data["taxsimid"].map(weight_lookup)
    data["networth"] = data["taxsimid"].map(networth_lookup)
    if data[["wgt", "networth"]].isna().any(axis=None):
        raise ValueError("TAXSIM household IDs do not align with the base sample")

    agi_by_state = data.pivot_table(
        index="taxsimid", columns="state", values="v10_federal_agi"
    )
    spread = (agi_by_state.max(axis=1) - agi_by_state.min(axis=1)).abs().max()
    if spread >= 1:
        raise ValueError(f"Federal AGI varies across states by as much as {spread}")

    reference = data.loc[data["state"].eq(reference_state)]
    if reference.empty:
        raise ValueError(f"Reference state {reference_state} is absent")
    agi_reference = reference["v10_federal_agi"].to_numpy()
    weights_reference = reference["wgt"].to_numpy()
    agi_thresholds = {
        quantile: weighted_quantile(agi_reference, weights_reference, quantile)
        for quantile in (0.20, 0.80, 0.95, 0.99)
    }
    networth_values = base_households["networth"].to_numpy()
    base_weights = base_households["wgt"].to_numpy()
    networth_p95 = weighted_quantile(networth_values, base_weights, 0.95)
    networth_p99 = weighted_quantile(networth_values, base_weights, 0.99)

    rows: list[dict[str, float | int | str]] = []
    for state, group in data.groupby("state"):
        agi = group["v10_federal_agi"].to_numpy()
        state_tax = group["siitax"].to_numpy()
        weights = group["wgt"].to_numpy()
        networth = group["networth"].to_numpy()
        row = {
            "state": state,
            "year": int(years[0]),
            "atr": average_tax_rate(agi, state_tax, weights),
            "atr_top5": average_tax_rate(
                agi, state_tax, weights, agi >= agi_thresholds[0.95]
            ),
            "atr_top1": average_tax_rate(
                agi, state_tax, weights, agi >= agi_thresholds[0.99]
            ),
            "atr_top5nw": average_tax_rate(
                agi, state_tax, weights, networth >= networth_p95
            ),
            "atr_top1nw": average_tax_rate(
                agi, state_tax, weights, networth >= networth_p99
            ),
            "rs": 100
            * (
                weighted_gini(agi, weights)
                - weighted_gini(agi - state_tax, weights)
            ),
            "beta": average_tax_rate(
                agi, state_tax, weights, agi >= agi_thresholds[0.80]
            )
            - average_tax_rate(
                agi, state_tax, weights, agi <= agi_thresholds[0.20]
            ),
        }
        rows.append(row)
    return pd.DataFrame(rows, columns=PANEL_COLUMNS).sort_values(["state", "year"])


def build_outcome_panel(
    taxsim_paths: Iterable[Path], base_households: pd.DataFrame
) -> pd.DataFrame:
    """Collapse a sequence of annual TAXSIM files into a sorted panel."""
    annual = [
        collapse_taxsim_year(pd.read_csv(path), base_households)
        for path in sorted(map(Path, taxsim_paths))
    ]
    if not annual:
        raise ValueError("No TAXSIM output files were supplied")
    return pd.concat(annual, ignore_index=True).sort_values(["state", "year"])


def write_outcome_panel(panel: pd.DataFrame, path: Path) -> Path:
    """Write a state-year outcome panel to CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(path, index=False)
    return path
