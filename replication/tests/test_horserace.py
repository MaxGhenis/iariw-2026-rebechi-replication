"""Regression tests for the partisan-control horse race."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from pandas.api.types import is_bool_dtype, is_numeric_dtype

from cu_replication.horserace import (
    DEFAULT_PANEL_PATH,
    DEFAULT_PARTISAN_PATH,
    load_analysis_panel,
    run_horserace,
)

REPLICATION_ROOT = Path(__file__).resolve().parents[1]
HORSERACE_DIR = REPLICATION_ROOT / "horserace"


@pytest.fixture(scope="module")
def outputs() -> dict[str, pd.DataFrame]:
    """Run the full model grid once for all horse-race regression tests."""
    return run_horserace()


def test_frame_inputs_and_default_paths_use_committed_layout() -> None:
    """Defaults and in-memory inputs should resolve the committed project data."""
    assert DEFAULT_PANEL_PATH == REPLICATION_ROOT / "results/panel_state_year.csv"
    assert DEFAULT_PARTISAN_PATH == HORSERACE_DIR / "partisan_control.csv"

    panel = pd.read_csv(DEFAULT_PANEL_PATH)
    partisan = pd.read_csv(DEFAULT_PARTISAN_PATH)
    original_panel_columns = panel.columns.tolist()
    analysis, returned_partisan, acquired = load_analysis_panel(panel, partisan)

    assert panel.columns.tolist() == original_panel_columns
    assert len(analysis) == 846
    assert analysis["state"].nunique() == 47
    assert len(returned_partisan) == 918
    assert len(acquired) == 16


def test_key_models_match_committed_results(
    outputs: dict[str, pd.DataFrame],
) -> None:
    """All key coefficients and inference fields should match within 1e-6."""
    actual = outputs["key_models"].reset_index(drop=True)
    expected = pd.read_csv(HORSERACE_DIR / "key_models.csv")

    assert actual.shape == expected.shape == (36, 27)
    structural = [
        "outcome",
        "spec_order",
        "spec",
        "spec_label",
        "sample",
        "key_table",
        "nobs",
        "clusters",
        "formula",
    ]
    pd.testing.assert_frame_equal(
        actual.loc[:, structural],
        expected.loc[:, structural],
        check_dtype=False,
    )

    numeric = [
        column
        for column in expected.columns
        if is_numeric_dtype(expected[column]) or is_bool_dtype(expected[column])
    ]
    np.testing.assert_allclose(
        actual.loc[:, numeric].to_numpy(dtype=float),
        expected.loc[:, numeric].to_numpy(dtype=float),
        atol=1e-6,
        rtol=0,
        equal_nan=True,
    )


def test_acquisition_counts_match_committed_results(
    outputs: dict[str, pd.DataFrame],
) -> None:
    """The strict acquisition rule should reproduce the committed 2-by-3 table."""
    actual = outputs["acquisition_counts"].reset_index(drop=True)
    expected = pd.read_csv(HORSERACE_DIR / "acquisition_counts.csv")
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False)
