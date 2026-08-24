"""Generate the three replication figures used by the discussant slides."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use("Agg")

TEAL = "#0d9488"
VIOLET = "#7c3aed"
ORANGE = "#c2410c"
LIGHT = "#cbd5e1"
INK = "#1e293b"
INK2 = "#475569"
MUTED = "#94a3b8"
GRID = "#e2e8f0"

plt.rcParams["font.family"] = ["Helvetica Neue", "Arial", "DejaVu Sans"]

MECHANICAL_STATES = {"AK", "NH", "PA", "TX", "WY"}


def _style(axis) -> None:
    for side in ("top", "right"):
        axis.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        axis.spines[side].set_color(GRID)
    axis.tick_params(colors=INK2, labelsize=13, length=0)
    axis.set_axisbelow(True)


def _save(figure, output_path: Path | None):
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, facecolor="white")
    return figure


def plot_group_means(series: pd.DataFrame, output_path: Path | None = None):
    """Plot annual top-1% ATR group means with the treated-control gap called out."""
    figure, axis = plt.subplots(figsize=(9.2, 5.0), dpi=200)
    axis.plot(series["year"], series["atr_top1_control"], color=VIOLET, lw=2.2)
    axis.plot(series["year"], series["atr_top1_corp_only"], color=ORANGE, lw=2.2)
    axis.plot(series["year"], series["atr_top1_corp_union"], color=TEAL, lw=2.6)
    axis.axvline(2009.5, color=MUTED, lw=1.2, ls=(0, (4, 3)))
    axis.text(2009.65, 6.42, "Citizens United", color=INK2, fontsize=12, va="top")
    last = series.iloc[-1]
    axis.text(
        2021.25, last["atr_top1_control"] + 0.05, "No ban (26)",
        color=VIOLET, fontsize=12.5, va="center", fontweight="bold",
    )
    axis.text(
        2021.25, last["atr_top1_corp_only"] - 0.22, "Corporate-only ban (8)",
        color=ORANGE, fontsize=12.5, va="center", fontweight="bold",
    )
    axis.text(
        2021.25, last["atr_top1_corp_union"], "Corporate & union ban (13)",
        color=TEAL, fontsize=12.5, va="center", fontweight="bold",
    )
    for year in (2004, 2009, 2021):
        row = series.loc[series["year"].eq(year)].iloc[0]
        gap = row["atr_top1_corp_union"] - row["atr_top1_control"]
        axis.annotate(
            "",
            xy=(year, row["atr_top1_corp_union"]),
            xytext=(year, row["atr_top1_control"]),
            arrowprops={"arrowstyle": "<->", "color": INK2, "lw": 1.1},
        )
        axis.text(
            year + 0.18,
            (row["atr_top1_corp_union"] + row["atr_top1_control"]) / 2,
            f"gap {gap:+.2f}",
            color=INK, fontsize=12.5, va="center", fontweight="bold",
        )
    axis.set_ylim(2.8, 6.5)
    axis.set_xlim(2003.6, 2027)
    axis.set_xticks([2004, 2007, 2010, 2013, 2016, 2019, 2021])
    axis.set_ylabel(
        "Top-1% state income-tax ATR, group mean (%)", color=INK2, fontsize=12.5
    )
    _style(axis)
    axis.yaxis.grid(True, color=GRID, lw=0.8)
    figure.tight_layout()
    return _save(figure, output_path)


def plot_per_state_did(estimates: pd.DataFrame, output_path: Path | None = None):
    """Plot corp-and-union state contributions to the top-1% DiD."""
    data = estimates.loc[
        estimates["outcome"].eq("atr_top1") & estimates["group"].eq("corp_union")
    ].sort_values("did")
    colors = [LIGHT if state in MECHANICAL_STATES else TEAL for state in data["state"]]
    figure, axis = plt.subplots(figsize=(9.2, 5.0), dpi=200)
    bars = axis.barh(data["state"], data["did"], color=colors, height=0.62)
    for bar, value in zip(bars, data["did"], strict=True):
        axis.text(
            value - 0.04 if value < 0 else value + 0.04,
            bar.get_y() + bar.get_height() / 2,
            f"{value:+.2f}",
            va="center",
            ha="right" if value < 0 else "left",
            color=INK, fontsize=12,
        )
    mean = data["did"].mean()
    axis.axvline(0, color=INK2, lw=1)
    axis.axvline(mean, color=INK2, lw=1.2, ls=(0, (4, 3)))
    axis.text(
        mean - 0.05, len(data) - 0.55,
        f"13-state mean {mean:+.2f} (= the DiD coefficient)",
        color=INK, fontsize=12, ha="right", va="center", fontweight="bold",
    )
    axis.text(
        0.45, 0.6, "grey: no or flat income tax,\nmechanically ≈ 0",
        color=INK2, fontsize=11.5, ha="left", va="center",
    )
    axis.set_xlim(-2.6, 1.5)
    axis.set_xlabel(
        "Per-state DiD vs never-ban controls: "
        "top-1% state ATR, post-2010 minus pre (pp)",
        color=INK2, fontsize=12,
    )
    _style(axis)
    axis.xaxis.grid(True, color=GRID, lw=0.8)
    figure.tight_layout()
    return _save(figure, output_path)


def plot_incidence(incidence: pd.DataFrame, output_path: Path | None = None):
    """Plot the AGI-group incidence gradient, top 1% at the top."""
    order = ["agi_top1", "agi_95_99", "agi_80_95", "agi_20_80", "agi_bottom20"]
    labels = ["Top 1%", "95–99%", "80–95%", "20–80%", "Bottom 20%"]
    data = incidence.set_index("group").loc[order]
    values = data["b2_corp_union"].to_numpy()
    errors = data["se2"].to_numpy()
    dollars = data["dollar_effect_cw"].to_numpy()
    figure, axis = plt.subplots(figsize=(9.2, 5.0), dpi=200)
    positions = np.arange(len(order))[::-1]
    axis.barh(
        positions,
        values,
        color=[TEAL if value < 0 else LIGHT for value in values],
        height=0.62,
        xerr=1.96 * errors,
        error_kw={"ecolor": INK2, "lw": 1.2, "capsize": 3},
    )
    axis.set_yticks(positions, labels)
    axis.tick_params(axis="y", labelsize=13, colors=INK)
    for position, value, dollar in zip(positions, values, dollars, strict=True):
        axis.text(
            -1.62, position, f"{value:+.2f} pp",
            va="center", ha="left", color=INK, fontsize=12.5, fontweight="bold",
        )
        sign = "+" if dollar > 0 else "−"
        axis.text(
            0.62, position, f"{sign}${abs(int(dollar)):,} per household-year",
            va="center", ha="left", color=INK2, fontsize=12.5,
        )
    axis.axvline(0, color=INK2, lw=1)
    axis.set_xlim(-1.7, 1.75)
    axis.set_xlabel(
        "Effect on the group's state ATR in corporate-&-union-ban states (pp, 95% CI)",
        color=INK2, fontsize=12,
    )
    axis.set_ylabel("Households ranked by AGI", color=INK2, fontsize=12.5)
    _style(axis)
    axis.xaxis.grid(True, color=GRID, lw=0.8)
    figure.tight_layout()
    return _save(figure, output_path)


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
