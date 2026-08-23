# Citizens United tax replication

This directory is an importable Python package for the public-data reconstruction of
Rebechi et al., *What Can Money Buy? Inequality and Fiscal Policy Implications of
Citizens United v. Federal Election Commission*.

## Quick start

From this directory, sync the locked Python environment and reproduce Table 4 from the
committed state-year panel:

```bash
uv sync
uv run cu-replication estimate
```

The estimate step takes seconds and does not require the household microdata, network
access, R, or TAXSIM. Run the tests and linter with:

```bash
uv run pytest -q
uv run ruff check .
```

## Full pipeline

The full SCF-to-panel pipeline additionally requires R, the R package
`usincometaxes`, and network access for the public Federal Reserve inputs:

```bash
uv run cu-replication download
uv run cu-replication build-inputs
uv run cu-replication taxsim --year-from 2004 --year-to 2021
uv run cu-replication outcomes
uv run cu-replication estimate
uv run cu-replication figures
```

If R or `usincometaxes` is absent, the TAXSIM command reports a clean skip. CI only uses
the committed `results/panel_state_year.csv` and never needs R.

The numbered Python and shell drivers are superseded by the package CLI; the checked-in
`scripts/03_run_taxsim.R` remains the implementation behind the optional `taxsim`
subcommand.

## Report

Render the executable Quarto report without rerunning TAXSIM:

```bash
uv run quarto render report
```

The report reads the committed CSVs in `results/` and `horserace/` and writes its HTML
output under `report/_output/`.
