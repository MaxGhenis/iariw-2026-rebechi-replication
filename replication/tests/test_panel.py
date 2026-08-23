"""Regression checks for the committed state-law outcome panel."""

import pandas as pd

from cu_replication.did import analytic_sample
from cu_replication.outcomes import PANEL_COLUMNS


def test_committed_panel_shape_and_columns(panel: pd.DataFrame) -> None:
    """The panel should contain 51 jurisdictions over 18 balanced years."""
    assert panel.shape == (51 * 18, len(PANEL_COLUMNS))
    assert tuple(panel.columns) == PANEL_COLUMNS
    assert panel["state"].nunique() == 51
    assert panel["year"].nunique() == 18
    assert not panel.duplicated(["state", "year"]).any()


def test_analytic_sample_includes_dc(panel: pd.DataFrame) -> None:
    """The main sample should have 47 units, 846 rows, and include DC."""
    sample = analytic_sample(panel)
    assert sample["state"].nunique() == 47
    assert len(sample) == 846
    assert "DC" in set(sample["state"])


def test_known_state_law_paths(panel: pd.DataFrame) -> None:
    """Known reforms and no-tax paths should remain visible in the panel."""
    outcomes = [column for column in PANEL_COLUMNS if column not in {"state", "year"}]
    zero_states = panel.loc[panel["state"].isin(("TX", "FL", "WA", "NV", "WY", "AK"))]
    assert zero_states[outcomes].eq(0).all(axis=None)

    indexed = panel.set_index(["state", "year"])
    assert (
        indexed.loc[("NC", 2013), "atr_top1"]
        - indexed.loc[("NC", 2014), "atr_top1"]
        > 1
    )
    assert indexed.loc[("KS", 2013), "atr"] < indexed.loc[("KS", 2012), "atr"]
    assert indexed.loc[("KS", 2016), "atr"] < indexed.loc[("KS", 2012), "atr"]
    assert indexed.loc[("KS", 2017), "atr"] > indexed.loc[("KS", 2016), "atr"]
    assert indexed.loc[("MN", 2013), "atr_top1"] > indexed.loc[("MN", 2012), "atr_top1"]
    assert indexed.loc[("TN", 2021), outcomes].eq(0).all()
