"""Generate the three replication figures used by the discussant slides."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

TEAL = "#0d9488"
VIOLET = "#7c3aed"
ORANGE = "#c2410c"
GRAY = "#94a3b8"


def plot_per_state_did(
    estimates: pd.DataFrame, output_path: Path | None = None
):
    """Plot corp-and-union state contributions to the top-1% DiD."""
    data = estimates.loc[
        estimates["outcome"].eq("atr_top1")
        & estimates["group"].eq("corp_union")
    ].sort_values("did")
    mechanical = {"AK", "NH", "PA", "TX", "WY"}
    colors = [GRAY if state in mechanical else TEAL for state in data["state"]]
    figure, axis = plt.subplots(figsize=(9, 4.8))
    axis.bar(data["state"], data["did"], color=colors)
    axis.axhline(data["did"].mean(), color=ORANGE, linestyle="--", linewidth=1.5)
    axis.axhline(0, color="#334155", linewidth=0.8)
    axis.set_ylabel("Top-1% ATR DiD (percentage points)")
    axis.set_xlabel("State")
    axis.set_title("The group effect is concentrated in a few reforms")
    figure.tight_layout()
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=160, bbox_inches="tight")
    return figure


def plot_group_means(series: pd.DataFrame, output_path: Path | None = None):
    """Plot annual top-1% ATR means for control and two ban groups."""
    figure, axis = plt.subplots(figsize=(9, 4.8))
    for column, label, color in (
        ("atr_top1_control", "Control", VIOLET),
        ("atr_top1_corp_only", "Corporate-only ban", ORANGE),
        ("atr_top1_corp_union", "Corporate-and-union ban", TEAL),
    ):
        axis.plot(series["year"], series[column], label=label, color=color, linewidth=2)
    axis.axvline(2009.5, color="#64748b", linestyle="--", linewidth=1)
    axis.set_ylabel("Mean top-1% ATR (%)")
    axis.set_xlabel("Year")
    axis.set_title("Top-income tax burdens diverged before and after the ruling")
    axis.legend(frameon=False, ncol=3, fontsize=8)
    figure.tight_layout()
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=160, bbox_inches="tight")
    return figure


def plot_incidence(incidence: pd.DataFrame, output_path: Path | None = None):
    """Plot the AGI-group incidence gradient with 95% confidence intervals."""
    order = ["agi_bottom20", "agi_20_80", "agi_80_95", "agi_95_99", "agi_top1"]
    labels = ["Bottom 20%", "20–80%", "80–95%", "95–99%", "Top 1%"]
    data = incidence.set_index("group").loc[order]
    positions = np.arange(len(data))
    colors = [TEAL if p < 0.05 else GRAY for p in data["p2"]]
    figure, axis = plt.subplots(figsize=(8, 4.8))
    axis.errorbar(
        positions,
        data["b2_corp_union"],
        yerr=1.96 * data["se2"],
        fmt="none",
        ecolor="#475569",
        capsize=4,
        linewidth=1.2,
    )
    axis.scatter(positions, data["b2_corp_union"], c=colors, s=55, zorder=3)
    axis.axhline(0, color="#334155", linewidth=0.8)
    axis.set_xticks(positions, labels)
    axis.set_ylabel("Corp-and-union coefficient (percentage points)")
    axis.set_title("Estimated tax cuts grow toward the top of the AGI distribution")
    figure.tight_layout()
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=160, bbox_inches="tight")
    return figure


def generate_slide_figures(
    results_dir: Path,
    output_dir: Path,
) -> tuple[Path, Path, Path]:
    """Regenerate all three slide figures from committed CSV results."""
    results_dir = Path(results_dir)
    output_dir = Path(output_dir)
    paths = (
        output_dir / "repl-per-state.png",
        output_dir / "repl-group-means.png",
        output_dir / "repl-incidence.png",
    )
    figures = (
        plot_per_state_did(pd.read_csv(results_dir / "per_state_did.csv"), paths[0]),
        plot_group_means(
            pd.read_csv(results_dir / "group_means_by_year.csv"), paths[1]
        ),
        plot_incidence(
            pd.read_csv(results_dir / "micro_heterogeneity.csv"), paths[2]
        ),
    )
    for figure in figures:
        plt.close(figure)
    return paths
