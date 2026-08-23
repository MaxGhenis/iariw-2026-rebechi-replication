"""Smoke tests for the package command-line interface."""

from pathlib import Path

import pandas as pd

from cu_replication.cli import build_parser, main, resolve_project_root


def test_cli_exposes_every_pipeline_subcommand() -> None:
    """The parser should accept every documented pipeline stage."""
    parser = build_parser()
    for command in (
        "download",
        "build-inputs",
        "taxsim",
        "outcomes",
        "estimate",
        "figures",
        "report",
        "all",
    ):
        assert parser.parse_args([command]).command == command


def test_explicit_project_root_is_resolved(tmp_path: Path) -> None:
    """An explicit project root should not depend on the current working directory."""
    assert resolve_project_root(tmp_path) == tmp_path.resolve()


def test_estimate_command_reproduces_table4(
    tmp_path: Path, replication_root: Path, capsys
) -> None:
    """The fast CLI path should reproduce Table 4 from only the committed panel."""
    results = tmp_path / "results"
    results.mkdir()
    panel = pd.read_csv(replication_root / "results" / "panel_state_year.csv")
    panel.to_csv(results / "panel_state_year.csv", index=False)

    assert main(["--root", str(tmp_path), "estimate"]) == 0
    expected = pd.read_csv(replication_root / "results" / "table4_replication.csv")
    actual = pd.read_csv(results / "table4_replication.csv")
    pd.testing.assert_frame_equal(
        actual, expected, check_exact=False, rtol=0, atol=1e-6
    )
    assert "Wrote" in capsys.readouterr().out
