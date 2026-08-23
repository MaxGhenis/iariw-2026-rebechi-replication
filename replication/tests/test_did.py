"""Numerical regression tests for the DiD estimators."""

from pathlib import Path

import pandas as pd
import pytest

from cu_replication.did import (
    analytic_sample,
    estimate_event_study,
    estimate_table4,
    estimate_twfe,
    leave_out_estimates,
    leave_three_out,
    per_state_did,
    randomization_inference,
)


def test_table4_matches_committed_results(
    panel: pd.DataFrame, replication_root: Path
) -> None:
    """All six outcomes and committed sample/dating combinations should match."""
    expected = pd.read_csv(replication_root / "results" / "table4_replication.csv")
    actual = estimate_table4(panel)
    assert list(actual.columns) == list(expected.columns)
    pd.testing.assert_frame_equal(
        actual, expected, check_exact=False, rtol=0, atol=1e-6
    )


def test_event_study_leads_match_committed_results(
    panel: pd.DataFrame, replication_root: Path
) -> None:
    """Every pre-treatment coefficient and reference row should match the fixture."""
    expected = pd.read_csv(replication_root / "results" / "event_study.csv")
    expected = expected.loc[expected["year"].le(2009)].reset_index(drop=True)
    actual = estimate_event_study(panel)
    actual = actual.loc[actual["year"].le(2009)].reset_index(drop=True)
    pd.testing.assert_frame_equal(
        actual, expected, check_exact=False, rtol=0, atol=1e-6
    )


def test_leave_out_coefficients_match_committed_results(
    panel: pd.DataFrame, replication_root: Path
) -> None:
    """Legacy single and joint leave-out coefficients should remain unchanged."""
    expected = pd.read_csv(replication_root / "results" / "leave_out.csv")
    actual = leave_out_estimates(panel)
    pd.testing.assert_frame_equal(
        actual, expected, check_exact=False, rtol=0, atol=1e-6
    )


def test_leave_three_out_matches_inference_summary(
    panel: pd.DataFrame, replication_root: Path
) -> None:
    """The clustered leave-three estimates should match the rounded fixture."""
    expected = pd.read_csv(replication_root / "results" / "inference_summary.csv")
    actual = leave_three_out(panel)
    for column, digits in {
        "b2": 3,
        "se2": 3,
        "p_cluster_t": 4,
        "b2_drop_NC_ND_OH": 3,
        "se2_drop": 3,
        "p_drop": 4,
    }.items():
        assert actual[column].round(digits).tolist() == expected[column].tolist()


def test_per_state_mean_equals_corp_union_twfe(panel: pd.DataFrame) -> None:
    """The 13 equally weighted state DiDs should average to the TWFE coefficient."""
    estimates = per_state_did(panel)
    main = analytic_sample(panel)
    for outcome in ("atr_top1", "rs"):
        state_mean = estimates.loc[
            estimates["outcome"].eq(outcome)
            & estimates["group"].eq("corp_union"),
            "did",
        ].mean()
        assert state_mean == pytest.approx(
            estimate_twfe(main, outcome)["b2"], abs=1e-12
        )


def test_beta_baseline_is_stable(panel: pd.DataFrame) -> None:
    """The incidence-gradient outcome should retain its headline coefficient and SE."""
    result = estimate_twfe(analytic_sample(panel), "beta")
    assert result["b2"] == pytest.approx(-0.679, abs=0.0005)
    assert result["se2"] == pytest.approx(0.219, abs=0.0005)


def test_randomization_inference_rejects_with_fixed_seed(panel: pd.DataFrame) -> None:
    """A deterministic short test should keep the top-1% p-value below five percent."""
    result = randomization_inference(
        panel, outcomes=("atr_top1",), draws=500, seed=287
    ).iloc[0]
    assert result["ri_p_b2"] < 0.05
    assert result["ri_p_diff"] < 0.05


def test_pretrend_tests_match_committed_results(
    panel: pd.DataFrame, replication_root: Path
) -> None:
    """Differential linear pre-trend slopes should match the committed fixture."""
    from cu_replication.did import pretrend_tests

    expected = pd.read_csv(replication_root / "results" / "pretrend_tests.csv")
    observed = pretrend_tests(panel)
    merged = expected.merge(
        observed, on=["sample", "outcome"], suffixes=("_e", "_o")
    )
    assert len(merged) == len(expected) == 8
    for col in ("corp_union_slope", "corp_union_se", "corp_union_p", "corp_only_slope"):
        assert (merged[f"{col}_e"] - merged[f"{col}_o"]).abs().max() < 1e-6
    main_top1 = observed.query("sample == 'main' and outcome == 'atr_top1'").iloc[0]
    assert main_top1["corp_union_slope"] < -0.08
    assert main_top1["corp_union_p"] < 0.10
