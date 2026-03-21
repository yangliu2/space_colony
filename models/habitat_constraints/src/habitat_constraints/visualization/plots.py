"""Matplotlib visualizations for habitat constraint analysis."""

from __future__ import annotations

from pathlib import Path

import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np

from habitat_constraints.analysis.monte_carlo import MonteCarloReport
from habitat_constraints.analysis.sensitivity import (
    SensitivityReport,
)
from habitat_constraints.core.solver import (
    FeasibleRegionSolver,
    SweepPoint,
)
from habitat_constraints.core.parameters import HabitatParameters

Figure = matplotlib.figure.Figure


def plot_feasible_region(
    solver: FeasibleRegionSolver,
    gravity_levels: list[float] | None = None,
    r_range: tuple[float, float] = (50.0, 15000.0),
    n_points: int = 300,
    output_path: Path | str | None = None,
) -> Figure:
    """Plot feasible region as radius vs. gravity with constraint shading.

    Each constraint that fails at a given (radius, gravity) point is
    shown as a colored region. The white area is the feasible zone.
    """
    if gravity_levels is None:
        gravity_levels = [round(0.2 + i * 0.05, 2) for i in range(17)]  # 0.2 to 1.0

    radii = np.linspace(r_range[0], r_range[1], n_points)

    # Collect constraint names from first evaluation
    test_params = HabitatParameters.from_radius_and_gravity(1000.0)
    test_results = solver.evaluate_point(test_params)
    constraint_names = [cr.constraint_name for cr in test_results]
    n_constraints = len(constraint_names)

    # Build feasibility matrix: (n_gravity, n_radii, n_constraints)
    fail_matrix = np.zeros((len(gravity_levels), len(radii), n_constraints), dtype=bool)

    for gi, g in enumerate(gravity_levels):
        for ri, r in enumerate(radii):
            params = HabitatParameters.from_radius_and_gravity(r, g)
            results = solver.evaluate_point(params)
            for ci, cr in enumerate(results):
                fail_matrix[gi, ri, ci] = not cr.feasible

    # Plot
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = plt.cm.tab10(np.linspace(0, 1, n_constraints))  # type: ignore[attr-defined]

    # For each constraint, shade the infeasible region
    for ci, cname in enumerate(constraint_names):
        for gi, g in enumerate(gravity_levels):
            failing_radii = radii[fail_matrix[gi, :, ci]]
            if len(failing_radii) > 0:
                ax.scatter(
                    failing_radii,
                    [g] * len(failing_radii),
                    c=[colors[ci]],
                    s=2,
                    alpha=0.4,
                    label=cname if gi == 0 else "",
                )

    # Mark feasible region
    for gi, g in enumerate(gravity_levels):
        all_feasible = ~np.any(fail_matrix[gi, :, :], axis=1)
        feasible_radii = radii[all_feasible]
        if len(feasible_radii) > 0:
            ax.scatter(
                feasible_radii,
                [g] * len(feasible_radii),
                c="white",
                edgecolors="green",
                s=3,
                alpha=0.6,
                label="feasible" if gi == 0 else "",
            )

    ax.set_xlabel("Radius (m)", fontsize=12)
    ax.set_ylabel("Target Gravity (g)", fontsize=12)
    ax.set_title("Habitat Feasible Region — Constraint Map", fontsize=14)

    # De-duplicate legend
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(
        unique.values(),
        unique.keys(),
        loc="upper right",
        fontsize=9,
    )
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_path:
        fig.savefig(str(output_path), dpi=150, bbox_inches="tight")
    return fig


def plot_tornado(
    report: SensitivityReport,
    output_path: Path | str | None = None,
    top_n: int = 10,
) -> Figure:
    """Horizontal bar tornado chart of sensitivity analysis results.

    Shows which parameters most affect the minimum feasible radius.
    """
    entries = report.tornado[:top_n]
    entries = list(reversed(entries))  # largest at top

    fig, ax = plt.subplots(figsize=(12, max(4, len(entries) * 0.6 + 1)))

    baseline_r = report.baseline_min_radius or 0.0
    y_pos = np.arange(len(entries))

    for i, entry in enumerate(entries):
        r_low = entry.radius_at_low
        r_high = entry.radius_at_high

        if r_low is None or r_high is None:
            # Can't plot if no feasible region found
            ax.barh(
                i,
                0,
                color="gray",
                alpha=0.3,
            )
            continue

        # Bar from r_low to r_high, centered on baseline
        left = min(r_low, r_high)
        width = abs(r_high - r_low)

        color = "steelblue" if width > 50 else "lightsteelblue"
        ax.barh(i, width, left=left, height=0.6, color=color)

        # Annotate values
        ax.text(
            left - 20,
            i,
            f"{left:.0f}m",
            va="center",
            ha="right",
            fontsize=8,
        )
        ax.text(
            left + width + 20,
            i,
            f"{left + width:.0f}m",
            va="center",
            ha="left",
            fontsize=8,
        )

    ax.axvline(
        baseline_r,
        color="red",
        linestyle="--",
        linewidth=1.5,
        label=f"Baseline: {baseline_r:.0f}m",
    )

    labels = [
        f"{e.parameter_name}\n[{e.low_value:.2f}, {e.high_value:.2f}]" for e in entries
    ]
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Minimum Feasible Radius (m)", fontsize=12)
    ax.set_title(
        f"Sensitivity Tornado — ±{report.perturbation_pct:.0f}% " f"Perturbation",
        fontsize=14,
    )
    ax.legend(fontsize=10)
    ax.grid(True, axis="x", alpha=0.3)

    plt.tight_layout()
    if output_path:
        fig.savefig(str(output_path), dpi=150, bbox_inches="tight")
    return fig


def plot_radius_sweep(
    sweep_points: list[SweepPoint],
    output_path: Path | str | None = None,
) -> Figure:
    """Plot constraint pass/fail across a radius sweep."""
    if not sweep_points:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No data", transform=ax.transAxes)
        return fig

    radii = [sp.radius_m for sp in sweep_points]

    # Get constraint names
    constraint_names = [cr.constraint_name for cr in sweep_points[0].constraint_results]
    n_constraints = len(constraint_names)

    fig, axes = plt.subplots(
        n_constraints + 1,
        1,
        figsize=(14, 2.5 * (n_constraints + 1)),
        sharex=True,
    )

    # Top subplot: overall feasibility
    feasible = [1 if sp.all_feasible else 0 for sp in sweep_points]
    axes[0].fill_between(
        radii,
        feasible,
        alpha=0.3,
        color="green",
        step="mid",
    )
    axes[0].set_ylabel("All Pass", fontsize=10)
    axes[0].set_ylim(-0.1, 1.1)
    axes[0].set_yticks([0, 1])
    axes[0].set_yticklabels(["Fail", "Pass"])

    # Per-constraint subplots
    colors = plt.cm.tab10(np.linspace(0, 1, n_constraints))  # type: ignore[attr-defined]
    for ci, cname in enumerate(constraint_names):
        ax = axes[ci + 1]
        passes = []
        for sp in sweep_points:
            cr = sp.constraint_results[ci]
            passes.append(1 if cr.feasible else 0)

        ax.fill_between(radii, passes, alpha=0.3, color=colors[ci], step="mid")
        ax.set_ylabel(cname, fontsize=9, rotation=0, labelpad=80)
        ax.set_ylim(-0.1, 1.1)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["Fail", "Pass"])

    axes[-1].set_xlabel("Radius (m)", fontsize=12)
    fig.suptitle(
        "Constraint Pass/Fail across Radius Sweep",
        fontsize=14,
        y=1.01,
    )

    plt.tight_layout()
    if output_path:
        fig.savefig(str(output_path), dpi=150, bbox_inches="tight")
    return fig


def plot_monte_carlo_histogram(
    report: MonteCarloReport,
    output_path: Path | str | None = None,
) -> Figure:
    """Histogram of minimum feasible radius from Monte Carlo trials."""
    min_radii = report.min_radii

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: minimum radius distribution
    if min_radii:
        arr = np.array(min_radii)
        axes[0].hist(
            arr,
            bins=50,
            color="steelblue",
            edgecolor="white",
            alpha=0.8,
        )

        # Percentile lines
        for pct, style in [
            (5, ":"),
            (50, "--"),
            (95, ":"),
        ]:
            val = np.percentile(arr, pct)
            axes[0].axvline(
                val,
                color="red",
                linestyle=style,
                linewidth=1.5,
                label=f"P{pct}: {val:.0f}m",
            )

        axes[0].set_xlabel("Minimum Feasible Radius (m)", fontsize=12)
        axes[0].set_ylabel("Count", fontsize=12)
        axes[0].set_title(
            f"Min Radius Distribution (n={len(min_radii)})",
            fontsize=12,
        )
        axes[0].legend(fontsize=9)
    else:
        axes[0].text(
            0.5,
            0.5,
            "No feasible trials",
            transform=axes[0].transAxes,
            ha="center",
        )

    # Right: feasible band width
    band_widths = [
        r.feasible_band_width
        for r in report.results
        if r.feasible_band_width is not None
    ]
    if band_widths:
        barr = np.array(band_widths)
        axes[1].hist(
            barr,
            bins=50,
            color="forestgreen",
            edgecolor="white",
            alpha=0.8,
        )

        med = float(np.median(barr))
        axes[1].axvline(
            med,
            color="red",
            linestyle="--",
            linewidth=1.5,
            label=f"Median: {med:.0f}m",
        )

        axes[1].set_xlabel("Feasible Band Width (m)", fontsize=12)
        axes[1].set_ylabel("Count", fontsize=12)
        axes[1].set_title(
            f"Band Width Distribution (n={len(band_widths)})",
            fontsize=12,
        )
        axes[1].legend(fontsize=9)
    else:
        axes[1].text(
            0.5,
            0.5,
            "No feasible trials",
            transform=axes[1].transAxes,
            ha="center",
        )

    fig.suptitle(
        f"Monte Carlo Feasibility Analysis — "
        f"{report.n_trials} trials at "
        f"{report.target_gravity_g}g",
        fontsize=14,
    )

    plt.tight_layout()
    if output_path:
        fig.savefig(str(output_path), dpi=150, bbox_inches="tight")
    return fig


def plot_mass_budget(
    radius_m: float,
    length_m: float,
    shielding_kg_m2: float = 4500.0,
    pressure_kpa: float = 101.3,
    output_path: Path | str | None = None,
) -> Figure:
    """Stacked bar chart of habitat mass budget components."""
    import math

    barrel_area = 2.0 * math.pi * radius_m * length_m
    endcap_area = 2.0 * math.pi * radius_m**2
    total_area = barrel_area + endcap_area
    volume = math.pi * radius_m**2 * length_m

    # Structural shell (high-strength steel, SF=3)
    sigma_y = 1.4e9  # Pa (maraging steel)
    t_shell = 3.0 * pressure_kpa * 1000 * radius_m / sigma_y
    rho_steel = 8000.0  # kg/m³
    shell_mass_mt = rho_steel * t_shell * total_area / 1e9

    # Radiation shielding
    shield_mass_mt = shielding_kg_m2 * total_area / 1e9

    # Atmosphere
    rho_air = pressure_kpa * 28.97 / (8.314 * 293.0)
    atmo_mass_mt = rho_air * volume / 1e9

    # Soil (50% area, 0.75m depth, 1400 kg/m³)
    soil_area = barrel_area * 0.5
    soil_mass_mt = 0.75 * 1400.0 * soil_area / 1e9

    # Water (4.2 t/person, estimate population)
    pop_est = max(1, int(barrel_area * 0.5 / 67.0))  # 67 m²/person
    water_mass_mt = pop_est * 4200.0 / 1e9

    components = {
        "Structural Shell": shell_mass_mt,
        "Radiation Shielding": shield_mass_mt,
        "Atmosphere": atmo_mass_mt,
        "Soil": soil_mass_mt,
        "Water": water_mass_mt,
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: stacked bar
    labels = list(components.keys())
    values = list(components.values())
    colors_list = [
        "steelblue",
        "coral",
        "lightskyblue",
        "sandybrown",
        "mediumaquamarine",
    ]
    bottom = 0.0
    for label, val, color in zip(labels, values, colors_list):
        axes[0].bar(
            "Mass Budget",
            val,
            bottom=bottom,
            color=color,
            label=f"{label}: {val:.1f} Mt",
            edgecolor="white",
        )
        bottom += val

    axes[0].set_ylabel("Mass (Mt — megatonnes)", fontsize=12)
    axes[0].set_title(
        f"r={radius_m:.0f}m, L={length_m:.0f}m\n" f"Total: {sum(values):.1f} Mt",
        fontsize=12,
    )
    axes[0].legend(loc="upper left", fontsize=9)

    # Right: pie chart
    axes[1].pie(
        values,
        labels=labels,
        colors=colors_list,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 9},
    )
    axes[1].set_title("Mass Fraction", fontsize=12)

    fig.suptitle(
        f"Habitat Mass Budget — "
        f"Shielding: {shielding_kg_m2:.0f} kg/m², "
        f"P: {pressure_kpa:.0f} kPa",
        fontsize=14,
    )

    plt.tight_layout()
    if output_path:
        fig.savefig(str(output_path), dpi=150, bbox_inches="tight")
    return fig
