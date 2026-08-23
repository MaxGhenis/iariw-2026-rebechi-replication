"""Command-line interface for the replication package."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

from cu_replication.data import download_public_inputs, read_scf_extract
from cu_replication.did import estimate_table4
from cu_replication.inputs import build_base_households, write_base_households
from cu_replication.outcomes import build_outcome_panel, write_outcome_panel
from cu_replication.taxsim import run_taxsim


def resolve_project_root(explicit: str | Path | None = None) -> Path:
    """Resolve the replication root from an option, cwd, or source tree."""
    if explicit is not None:
        return Path(explicit).resolve()
    current = Path.cwd()
    if (current / "results" / "panel_state_year.csv").exists():
        return current
    if (current / "replication" / "results" / "panel_state_year.csv").exists():
        return current / "replication"
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    """Build the package command-line parser."""
    parser = argparse.ArgumentParser(prog="cu-replication")
    parser.add_argument("--root", help="Path to the replication directory")
    subcommands = parser.add_subparsers(dest="command", required=True)

    download = subcommands.add_parser("download", help="Download public Fed inputs")
    download.add_argument("--force", action="store_true", help="Replace existing files")

    subcommands.add_parser(
        "build-inputs", help="Build the fixed TAXSIM household sample"
    )

    taxsim = subcommands.add_parser("taxsim", help="Run TAXSIM through optional R")
    taxsim.add_argument("--year-from", type=int, default=2004)
    taxsim.add_argument("--year-to", type=int, default=2021)

    subcommands.add_parser("outcomes", help="Collapse TAXSIM outputs to a panel")
    subcommands.add_parser(
        "estimate", help="Reproduce Table 4 from the committed panel"
    )
    subcommands.add_parser("figures", help="Regenerate the three slide figures")
    subcommands.add_parser("report", help="Render the Quarto report")

    all_parser = subcommands.add_parser("all", help="Run the full replication pipeline")
    all_parser.add_argument("--year-from", type=int, default=2004)
    all_parser.add_argument("--year-to", type=int, default=2021)
    all_parser.add_argument("--force", action="store_true")
    return parser


def command_download(root: Path, *, force: bool = False) -> None:
    """Download the SCF and Fed macro inputs."""
    outputs = download_public_inputs(root / "data", force=force)
    print("Downloaded public inputs:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")


def command_build_inputs(root: Path) -> None:
    """Build and write the fixed base-household sample."""
    scf = read_scf_extract(root / "data" / "rscfp2010.dta")
    households = build_base_households(scf)
    path = write_base_households(households, root / "data" / "base_households.csv")
    print(f"Wrote {path} ({len(households):,} households)")


def command_taxsim(root: Path, *, year_from: int, year_to: int) -> bool:
    """Run the optional R/TAXSIM stage and report whether it ran."""
    result = run_taxsim(root, year_from=year_from, year_to=year_to)
    print(result.message)
    return result.ran


def command_outcomes(root: Path) -> None:
    """Collapse all annual TAXSIM output files to the state-year panel."""
    households = pd.read_csv(root / "data" / "base_households.csv")
    paths = sorted((root / "data").glob("taxsim_out_*.csv"))
    panel = build_outcome_panel(paths, households)
    destination = write_outcome_panel(
        panel, root / "results" / "panel_state_year.csv"
    )
    print(f"Wrote {destination} ({len(panel):,} rows)")


def command_estimate(root: Path) -> None:
    """Reproduce and write Table 4 from the committed state-year panel."""
    panel = pd.read_csv(root / "results" / "panel_state_year.csv")
    table = estimate_table4(panel)
    destination = root / "results" / "table4_replication.csv"
    verified_existing = False
    if destination.exists():
        existing = pd.read_csv(destination)
        try:
            pd.testing.assert_frame_equal(
                table, existing, check_exact=False, rtol=0, atol=1e-12
            )
        except AssertionError:
            pass
        else:
            verified_existing = True
    if not verified_existing:
        destination.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(destination, index=False)
    main = table.loc[table["sample"].eq("main_846")]
    display_columns = ["outcome", "b1", "se1", "b2", "se2", "diff", "sed"]
    print(main[display_columns].to_string(index=False))
    action = "Verified" if verified_existing else "Wrote"
    print(f"{action} {destination}")


def command_figures(root: Path) -> None:
    """Regenerate the slide figures from committed result CSVs."""
    from cu_replication.figures import generate_slide_figures

    output_dir = root.parent / "public" / "figures"
    for path in generate_slide_figures(root / "results", output_dir):
        print(f"Wrote {path}")


def command_report(root: Path) -> None:
    """Render the executable Quarto report without rerunning TAXSIM."""
    environment = os.environ.copy()
    environment["QUARTO_PYTHON"] = sys.executable
    environment["JUPYTER_PREFER_ENV_PATH"] = "1"
    subprocess.run(
        ["quarto", "render", "report"], cwd=root, env=environment, check=True
    )


def main(argv: list[str] | None = None) -> int:
    """Run one CLI subcommand and return its process status."""
    arguments = build_parser().parse_args(argv)
    root = resolve_project_root(arguments.root)
    if arguments.command == "download":
        command_download(root, force=arguments.force)
    elif arguments.command == "build-inputs":
        command_build_inputs(root)
    elif arguments.command == "taxsim":
        command_taxsim(root, year_from=arguments.year_from, year_to=arguments.year_to)
    elif arguments.command == "outcomes":
        command_outcomes(root)
    elif arguments.command == "estimate":
        command_estimate(root)
    elif arguments.command == "figures":
        command_figures(root)
    elif arguments.command == "report":
        command_report(root)
    elif arguments.command == "all":
        command_download(root, force=arguments.force)
        command_build_inputs(root)
        ran_taxsim = command_taxsim(
            root, year_from=arguments.year_from, year_to=arguments.year_to
        )
        if ran_taxsim:
            command_outcomes(root)
        elif not (root / "results" / "panel_state_year.csv").exists():
            return 0
        command_estimate(root)
        command_figures(root)
        command_report(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
