"""Download and normalize the public Federal Reserve inputs."""

from __future__ import annotations

import shutil
import urllib.request
import zipfile
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from cu_replication.constants import (
    SCF_2022_TO_2010_DOLLAR_FACTOR,
    SCF_MONEY_COLUMNS,
)

SCF_URL = "https://www.federalreserve.gov/econres/files/scfp2010s.zip"
FED_MACRO_URL = "https://www.federalreserve.gov/econres/files/bulletin.macro.txt"
DOWNLOAD_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def download_file(url: str, destination: Path, *, force: bool = False) -> Path:
    """Download *url* to *destination* with the user agent required by the Fed."""
    destination = Path(destination)
    if destination.exists() and not force:
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": DOWNLOAD_USER_AGENT})
    with urllib.request.urlopen(request) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)
    return destination


def download_public_inputs(data_dir: Path, *, force: bool = False) -> dict[str, Path]:
    """Download and extract the SCF 2010 summary file and Fed macro generator."""
    data_dir = Path(data_dir)
    archive = download_file(SCF_URL, data_dir / "scfp2010s.zip", force=force)
    scf_path = data_dir / "rscfp2010.dta"
    if force or not scf_path.exists():
        with zipfile.ZipFile(archive) as bundle:
            member = next(
                name for name in bundle.namelist() if name.endswith("rscfp2010.dta")
            )
            with bundle.open(member) as source, scf_path.open("wb") as output:
                shutil.copyfileobj(source, output)
    macro_path = download_file(
        FED_MACRO_URL, data_dir / "bulletin.macro.txt", force=force
    )
    return {"scf": scf_path, "macro": macro_path, "archive": archive}


def read_scf_extract(path: Path) -> pd.DataFrame:
    """Read the public SCF summary extract from a Stata file."""
    return pd.read_stata(path)


def rescale_scf_dollars(
    frame: pd.DataFrame,
    columns: Iterable[str] = SCF_MONEY_COLUMNS,
) -> pd.DataFrame:
    """Return a copy with the Fed's published 2022-dollar fields in 2010 dollars."""
    result = frame.copy()
    selected = list(columns)
    missing = sorted(set(selected) - set(result.columns))
    if missing:
        raise ValueError(f"SCF dollar columns are missing: {', '.join(missing)}")
    result[selected] = result[selected] * SCF_2022_TO_2010_DOLLAR_FACTOR
    return result
