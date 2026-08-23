"""Shared pytest fixtures for committed replication artifacts."""

from pathlib import Path

import pandas as pd
import pytest

REPLICATION_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def replication_root() -> Path:
    """Return the replication project root."""
    return REPLICATION_ROOT


@pytest.fixture(scope="session")
def panel(replication_root: Path) -> pd.DataFrame:
    """Load the committed state-year outcome panel once per test session."""
    return pd.read_csv(replication_root / "results" / "panel_state_year.csv")
