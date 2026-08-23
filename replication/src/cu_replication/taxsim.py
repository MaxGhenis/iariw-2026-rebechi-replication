"""Optional R bridge for local TAXSIM-35 simulations.

The full simulation requires ``Rscript`` and the R package ``usincometaxes``. Neither
is needed for estimation from the committed state-year panel or for continuous
integration. Missing R requirements are reported as a clean skip rather than an error.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from cu_replication.constants import CPI_U

TAXSIM_MONEY_COLUMNS = (
    "pwages",
    "swages",
    "psemp",
    "dividends",
    "intrec",
    "ltcg",
    "pensions",
    "transfers",
    "otherprop",
)
TAXSIM_ID_COLUMNS = (
    "hhid",
    "mstat",
    "page",
    "sage",
    "depx",
    "age1",
    "age2",
    "age3",
)


@dataclass(frozen=True)
class TaxsimRunResult:
    """Outcome of an optional TAXSIM subprocess."""

    ran: bool
    message: str
    output_paths: tuple[Path, ...] = ()


def taxsim_available() -> bool:
    """Return whether Rscript can load the optional ``usincometaxes`` package."""
    rscript = shutil.which("Rscript")
    if rscript is None:
        return False
    probe = (
        '.libPaths(c("~/Rlibs", .libPaths())); '
        'quit(status=ifelse(requireNamespace("usincometaxes", quietly=TRUE), 0, 1))'
    )
    result = subprocess.run(
        [rscript, "-e", probe], capture_output=True, check=False, text=True
    )
    return result.returncode == 0


def make_taxsim_inputs(
    base_households: pd.DataFrame, year: int, state: str
) -> pd.DataFrame:
    """Create one state-year TAXSIM input frame with CPI-scaled money fields."""
    if year not in CPI_U:
        raise ValueError(f"No CPI-U value is configured for {year}")
    required = set(TAXSIM_ID_COLUMNS) | set(TAXSIM_MONEY_COLUMNS)
    missing = sorted(required - set(base_households.columns))
    if missing:
        raise ValueError(f"Base household columns are missing: {', '.join(missing)}")
    factor = CPI_U[year] / CPI_U[2010]
    inputs = base_households.loc[:, TAXSIM_ID_COLUMNS].copy()
    inputs = inputs.rename(columns={"hhid": "taxsimid"})
    inputs["year"] = year
    inputs["state"] = state
    inputs[list(TAXSIM_MONEY_COLUMNS)] = (
        base_households.loc[:, TAXSIM_MONEY_COLUMNS].to_numpy() * factor
    )
    ordered = (
        "taxsimid",
        "year",
        "state",
        "mstat",
        "page",
        "sage",
        "depx",
        "age1",
        "age2",
        "age3",
        *TAXSIM_MONEY_COLUMNS,
    )
    return inputs.loc[:, ordered]


def write_taxsim_inputs(frame: pd.DataFrame, path: Path) -> Path:
    """Write a state-year TAXSIM input frame."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path


def run_taxsim(
    project_root: Path,
    year_from: int = 2004,
    year_to: int = 2021,
) -> TaxsimRunResult:
    """Invoke the checked-in R driver, or return a graceful dependency skip."""
    project_root = Path(project_root)
    if not taxsim_available():
        return TaxsimRunResult(
            ran=False,
            message=(
                "Skipped TAXSIM: Rscript or the R package usincometaxes is "
                "unavailable."
            ),
        )
    script = project_root / "scripts" / "03_run_taxsim.R"
    subprocess.run(
        ["Rscript", str(script), str(year_from), str(year_to)],
        cwd=project_root,
        check=True,
    )
    outputs = tuple(
        project_root / "data" / f"taxsim_out_{year}.csv"
        for year in range(year_from, year_to + 1)
    )
    return TaxsimRunResult(True, "TAXSIM completed.", outputs)


def run_single_state_year(inputs: pd.DataFrame, output_path: Path) -> TaxsimRunResult:
    """Run a small already-mapped input frame through R for integration testing."""
    if not taxsim_available():
        return TaxsimRunResult(
            ran=False,
            message=(
                "Skipped TAXSIM: Rscript or the R package usincometaxes is "
                "unavailable."
            ),
        )
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cu-taxsim-") as temporary:
        input_path = Path(temporary) / "input.csv"
        inputs.to_csv(input_path, index=False)
        expression = (
            '.libPaths(c("~/Rlibs", .libPaths())); '
            'suppressMessages(library(usincometaxes)); '
            f'x <- read.csv("{input_path}", check.names=FALSE); '
            'y <- as.data.frame(taxsim_calculate_taxes('
            'x, return_all_information=TRUE)); '
            f'write.csv(y, "{output_path}", row.names=FALSE)'
        )
        subprocess.run(["Rscript", "-e", expression], check=True)
    return TaxsimRunResult(
        True, "TAXSIM state-year smoke test completed.", (output_path,)
    )
