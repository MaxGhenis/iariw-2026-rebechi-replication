"""Smoke tests for the three CSV-driven replication figures."""

from pathlib import Path

from cu_replication.figures import generate_slide_figures


def test_generate_slide_figures(
    tmp_path: Path, replication_root: Path
) -> None:
    """All slide figures should render as nonempty PNG files."""
    paths = generate_slide_figures(replication_root / "results", tmp_path)
    assert len(paths) == 3
    assert all(path.exists() and path.stat().st_size > 10_000 for path in paths)
