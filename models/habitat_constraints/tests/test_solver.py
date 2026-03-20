"""Tests for FeasibleRegionSolver."""

import pytest

from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.core.solver import FeasibleRegionSolver
from habitat_constraints.constraints.vestibular import VestibularConstraint
from habitat_constraints.constraints.gravity_level import (
    GravityLevelConstraint,
)
from habitat_constraints.constraints.gravity_gradient import (
    GravityGradientConstraint,
)


@pytest.fixture
def solver() -> FeasibleRegionSolver:
    return FeasibleRegionSolver(
        constraints=[
            VestibularConstraint(),
            GravityLevelConstraint(),
            GravityGradientConstraint(),
        ],
    )


class TestFeasibleRegionSolver:
    def test_oneill_is_feasible(
        self,
        solver: FeasibleRegionSolver,
        oneill_params: HabitatParameters,
    ) -> None:
        assert solver.is_feasible(oneill_params) is True

    def test_small_habitat_infeasible(
        self,
        solver: FeasibleRegionSolver,
        small_habitat_params: HabitatParameters,
    ) -> None:
        assert solver.is_feasible(small_habitat_params) is False

    def test_evaluate_point_returns_all_constraints(
        self,
        solver: FeasibleRegionSolver,
        oneill_params: HabitatParameters,
    ) -> None:
        results = solver.evaluate_point(oneill_params)
        assert len(results) == 3
        names = {r.constraint_name for r in results}
        assert names == {
            "vestibular",
            "gravity_level",
            "gravity_gradient",
        }

    def test_compute_all_bounds(self, solver: FeasibleRegionSolver) -> None:
        bounds = solver.compute_all_bounds()
        assert "radius_m" in bounds
        assert "angular_velocity_rad_s" in bounds

    def test_feasible_range_radius(self, solver: FeasibleRegionSolver) -> None:
        lower, upper = solver.feasible_range("radius_m")
        # Vestibular gives r_min ~224m, gradient gives r_min ~180m
        # Intersection: r_min should be ~224m (the tighter bound)
        assert lower is not None
        assert lower == pytest.approx(224.0, rel=0.02)
        # No upper bound on radius from these constraints
        assert upper is None

    def test_feasible_range_nonexistent_param(
        self, solver: FeasibleRegionSolver
    ) -> None:
        lower, upper = solver.feasible_range("nonexistent")
        assert lower is None
        assert upper is None

    def test_add_and_remove_constraint(self) -> None:
        solver = FeasibleRegionSolver(constraints=[])
        assert len(solver.constraints) == 0

        solver.add_constraint(VestibularConstraint())
        assert len(solver.constraints) == 1

        solver.remove_constraint("vestibular")
        assert len(solver.constraints) == 0

    def test_sweep_radius(self, solver: FeasibleRegionSolver) -> None:
        results = solver.sweep_radius(r_min=50, r_max=5000, n_points=50)
        assert len(results) == 50
        assert results[0].radius_m == pytest.approx(50.0)

        # Small radius should be infeasible
        assert results[0].all_feasible is False

        # Large radius (near 5000m) should be feasible
        assert results[-1].all_feasible is True

    def test_sweep_radius_transition(self, solver: FeasibleRegionSolver) -> None:
        """There should be a transition from infeasible to feasible."""
        results = solver.sweep_radius(r_min=100, r_max=500, n_points=100)
        feasibility = [r.all_feasible for r in results]
        # Should start infeasible and become feasible
        assert feasibility[0] is False
        assert feasibility[-1] is True
        # Should transition exactly once (monotonic)
        transitions = sum(
            1 for i in range(1, len(feasibility)) if feasibility[i] != feasibility[i - 1]
        )
        assert transitions == 1

    def test_custom_assumptions(self) -> None:
        """Solver respects custom assumptions."""
        relaxed = HumanAssumptions(max_comfortable_rpm=4.0)
        solver = FeasibleRegionSolver(
            constraints=[VestibularConstraint()],
            assumptions=relaxed,
        )
        # r=100m at 1g is ~3 RPM, feasible with 4 RPM limit
        params = HabitatParameters.from_radius_and_gravity(100.0)
        assert solver.is_feasible(params) is True
