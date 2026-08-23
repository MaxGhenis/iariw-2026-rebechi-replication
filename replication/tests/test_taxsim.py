"""Pure and optional-R tests for the TAXSIM bridge."""

from pathlib import Path

import pandas as pd
import pytest

from cu_replication.inputs import map_scf_to_taxsim
from cu_replication.taxsim import (
    make_taxsim_inputs,
    run_single_state_year,
    taxsim_available,
)


def _base_household() -> pd.DataFrame:
    return map_scf_to_taxsim(
        pd.DataFrame(
            {
                "age": [40],
                "bussefarminc": [0.0],
                "income": [80_000.0],
                "intdivinc": [0.0],
                "kginc": [0.0],
                "kids": [1],
                "married": [1],
                "networth": [100_000.0],
                "penacctwd": [0.0],
                "ssretinc": [0.0],
                "transfothinc": [0.0],
                "wageinc": [80_000.0],
                "wgt": [1.0],
            }
        )
    )


def test_make_taxsim_inputs_scales_money_and_adds_state_year() -> None:
    """The year-specific frame should preserve IDs and apply the CPI ratio."""
    result = make_taxsim_inputs(_base_household(), 2010, "TX")
    assert result.loc[0, "taxsimid"] == 1
    assert result.loc[0, "state"] == "TX"
    assert result.loc[0, "year"] == 2010
    assert result.loc[0, "pwages"] == 48_000.0
    assert result.loc[0, "swages"] == 32_000.0


@pytest.mark.r
@pytest.mark.slow
def test_one_state_year_through_r(tmp_path: Path) -> None:
    """Run one synthetic Texas return through local TAXSIM when R is available."""
    if not taxsim_available():
        pytest.skip("Rscript or the R package usincometaxes is unavailable")
    inputs = make_taxsim_inputs(_base_household(), 2010, "TX")
    output = tmp_path / "taxsim.csv"
    result = run_single_state_year(inputs, output)
    assert result.ran
    simulated = pd.read_csv(output)
    assert len(simulated) == 1
    assert simulated.loc[0, "siitax"] == pytest.approx(0.0)
