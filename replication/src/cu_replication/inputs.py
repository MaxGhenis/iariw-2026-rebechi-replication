"""Map the SCF summary extract into the fixed TAXSIM household sample."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from cu_replication.constants import SCF_EXPECTED_IMPLICATE_ROWS
from cu_replication.data import rescale_scf_dollars

REQUIRED_SCF_COLUMNS = {
    "age",
    "bussefarminc",
    "income",
    "intdivinc",
    "kginc",
    "kids",
    "married",
    "networth",
    "penacctwd",
    "ssretinc",
    "transfothinc",
    "wageinc",
    "wgt",
}


def select_implicate(frame: pd.DataFrame, implicate: int = 1) -> pd.DataFrame:
    """Select one SCF implicate using the final digit of ``y1``."""
    if "y1" not in frame:
        return frame.copy().reset_index(drop=True)
    selected = frame.loc[frame["y1"].mod(10).eq(implicate)]
    return selected.copy().reset_index(drop=True)


def map_scf_to_taxsim(frame_2010usd: pd.DataFrame) -> pd.DataFrame:
    """Map an SCF frame already expressed in 2010 dollars to TAXSIM inputs.

    The public summary extract combines several fields available separately in LWS.
    This function exactly retains the legacy replication's documented compromises:
    joint filing for married/cohabiting households, a 60/40 wage split, equal splits
    of interest and dividends, and negative transfers routed to ``otherprop``.
    """
    missing = sorted(REQUIRED_SCF_COLUMNS - set(frame_2010usd.columns))
    if missing:
        raise ValueError(f"SCF mapping columns are missing: {', '.join(missing)}")

    source = frame_2010usd.reset_index(drop=True)
    married = source["married"].eq(1)
    kids = source["kids"].astype(int)
    age = source["age"].astype(int)
    transfers = source["transfothinc"]
    return pd.DataFrame(
        {
            "hhid": np.arange(1, len(source) + 1),
            "wgt": source["wgt"].to_numpy(),
            "mstat": np.where(married, "married, jointly", "single"),
            "page": age,
            "sage": np.where(married, age, 0).astype(int),
            "depx": kids,
            "age1": np.where(kids.ge(1), 10, 0),
            "age2": np.where(kids.ge(2), 10, 0),
            "age3": np.where(kids.ge(3), 10, 0),
            "pwages": np.where(married, 0.6 * source["wageinc"], source["wageinc"]),
            "swages": np.where(married, 0.4 * source["wageinc"], 0.0),
            "psemp": source["bussefarminc"],
            "dividends": 0.5 * source["intdivinc"],
            "intrec": 0.5 * source["intdivinc"],
            "ltcg": source["kginc"],
            "pensions": source["ssretinc"] + source["penacctwd"],
            "transfers": transfers.clip(lower=0),
            "otherprop": transfers.clip(upper=0),
            "scf_income": source["income"],
            "networth": source["networth"],
        }
    )


def build_base_households(
    scf: pd.DataFrame,
    *,
    implicate: int = 1,
    validate_row_count: bool = True,
) -> pd.DataFrame:
    """Select, rescale, and map the fixed SCF household sample."""
    selected = select_implicate(scf, implicate)
    if validate_row_count and len(selected) != SCF_EXPECTED_IMPLICATE_ROWS:
        raise ValueError(
            f"SCF implicate {implicate} has {len(selected):,} rows; "
            f"expected {SCF_EXPECTED_IMPLICATE_ROWS:,}"
        )
    return map_scf_to_taxsim(rescale_scf_dollars(selected))


def write_base_households(frame: pd.DataFrame, path: Path) -> Path:
    """Write mapped households to the CSV consumed by the TAXSIM stage."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path
