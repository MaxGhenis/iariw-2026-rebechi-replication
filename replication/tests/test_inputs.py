"""Unit tests for the public SCF-to-TAXSIM mapping."""

import pandas as pd
import pytest

from cu_replication.constants import SCF_2022_TO_2010_DOLLAR_FACTOR
from cu_replication.data import rescale_scf_dollars
from cu_replication.inputs import map_scf_to_taxsim, select_implicate


@pytest.fixture
def tiny_scf() -> pd.DataFrame:
    """Return a two-household synthetic SCF frame in already-normalized dollars."""
    return pd.DataFrame(
        {
            "age": [40, 70],
            "bussefarminc": [100.0, -20.0],
            "income": [1_000.0, 500.0],
            "intdivinc": [80.0, 10.0],
            "kginc": [-30.0, 4.0],
            "kids": [2, 0],
            "married": [1, 0],
            "networth": [5_000.0, -100.0],
            "penacctwd": [7.0, 30.0],
            "ssretinc": [3.0, 200.0],
            "transfothinc": [-25.0, 12.0],
            "wageinc": [600.0, 300.0],
            "wgt": [1.5, 2.0],
        }
    )


def test_scf_mapping_preserves_legacy_compromises(tiny_scf: pd.DataFrame) -> None:
    """Marriage, income splits, dependents, and negative transfers map exactly."""
    result = map_scf_to_taxsim(tiny_scf)

    married = result.iloc[0]
    assert married["mstat"] == "married, jointly"
    assert married["page"] == married["sage"] == 40
    assert married["pwages"] == 360.0
    assert married["swages"] == 240.0
    assert married["dividends"] == married["intrec"] == 40.0
    assert married["depx"] == 2
    assert (married[["age1", "age2", "age3"]].to_numpy() == [10, 10, 0]).all()
    assert married["transfers"] == 0.0
    assert married["otherprop"] == -25.0
    assert married["ltcg"] == -30.0

    single = result.iloc[1]
    assert single["mstat"] == "single"
    assert single["sage"] == 0
    assert single["pwages"] == 300.0
    assert single["swages"] == 0.0
    assert single["transfers"] == 12.0
    assert single["otherprop"] == 0.0
    assert single["pensions"] == 230.0


def test_scf_dollar_rescale_uses_fed_ratio(tiny_scf: pd.DataFrame) -> None:
    """Published dollar values should be converted with the Fed generator ratio."""
    result = rescale_scf_dollars(tiny_scf)
    assert result.loc[0, "wageinc"] == pytest.approx(
        600.0 * SCF_2022_TO_2010_DOLLAR_FACTOR
    )
    assert result.loc[0, "wgt"] == tiny_scf.loc[0, "wgt"]


def test_implicate_selection_uses_y1_final_digit() -> None:
    """Only rows belonging to the requested implicate should remain."""
    frame = pd.DataFrame({"y1": [1001, 1002, 1011], "value": [1, 2, 3]})
    result = select_implicate(frame, 1)
    assert result["value"].tolist() == [1, 3]
