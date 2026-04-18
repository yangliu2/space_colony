"""Tests for MicrometeoiteConstraint."""

from __future__ import annotations

import math

import pytest

from habitat_constraints.constraints.micrometeorite import MicrometeoiteConstraint
from habitat_constraints.core.parameters import HabitatParameters, HumanAssumptions


def _params(radius_m: float = 982.0, length_m: float = 1276.0) -> HabitatParameters:
    return HabitatParameters.from_radius_and_gravity(
        radius_m=radius_m,
        target_gravity_g=1.0,
        length_m=length_m,
    )


def _assumptions(**kwargs) -> HumanAssumptions:
    return HumanAssumptions(**kwargs)


@pytest.fixture
def constraint() -> MicrometeoiteConstraint:
    return MicrometeoiteConstraint()


class TestBasicProperties:
    def test_name(self, constraint: MicrometeoiteConstraint) -> None:
        assert constraint.name == "micrometeorite"

    def test_description_non_empty(self, constraint: MicrometeoiteConstraint) -> None:
        assert len(constraint.description) > 0

    def test_compute_bounds_returns_empty(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        """Bounds are geometry-dependent; compute_bounds returns empty list."""
        bounds = constraint.compute_bounds(_assumptions())
        assert bounds == []


class TestFeasibility:
    def test_passes_at_default_flux(self, constraint: MicrometeoiteConstraint) -> None:
        """Default 1e-7 flux is at the feasibility boundary for the reference design."""
        result = constraint.evaluate(_params(), _assumptions())
        # At r=982, L=1276, window=0.5: exposed ~10 million m², flux 1e-7 → ~1 hit/yr
        assert result.details["expected_annual_perforations"] == pytest.approx(
            result.details["exposed_area_m2"] * 1e-7
        )

    def test_fails_at_iss_flux(self, constraint: MicrometeoiteConstraint) -> None:
        """ISS-level flux (6e-5) produces catastrophic perforation rate."""
        result = constraint.evaluate(
            _params(),
            _assumptions(meteoroid_penetrating_flux_m2_yr=6e-5),
        )
        assert result.feasible is False
        assert result.details["expected_annual_perforations"] > 100

    def test_passes_with_low_flux(self, constraint: MicrometeoiteConstraint) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(meteoroid_penetrating_flux_m2_yr=1e-10),
        )
        assert result.feasible is True

    def test_fails_when_annual_exceeds_max(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(
                meteoroid_penetrating_flux_m2_yr=1e-5,
                max_annual_perforations=1.0,
            ),
        )
        assert result.feasible is False

    def test_passes_when_max_raised(self, constraint: MicrometeoiteConstraint) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(
                meteoroid_penetrating_flux_m2_yr=1e-5,
                max_annual_perforations=1000.0,
            ),
        )
        assert result.feasible is True


class TestExposedArea:
    def test_exposed_area_formula(self, constraint: MicrometeoiteConstraint) -> None:
        r, length = 500.0, 1000.0
        p = _params(radius_m=r, length_m=length)
        a = _assumptions(window_fraction=0.5)
        result = constraint.evaluate(p, a)
        expected = 0.5 * p.barrel_area_m2 + p.endcap_area_m2
        assert result.details["exposed_area_m2"] == pytest.approx(expected)

    def test_shielded_area_formula(self, constraint: MicrometeoiteConstraint) -> None:
        r, length = 500.0, 1000.0
        p = _params(radius_m=r, length_m=length)
        a = _assumptions(window_fraction=0.5)
        result = constraint.evaluate(p, a)
        expected = 0.5 * p.barrel_area_m2
        assert result.details["shielded_area_m2"] == pytest.approx(expected)

    def test_zero_window_fraction_minimises_exposure(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        """Zero window fraction → only end caps exposed."""
        p = _params()
        a = _assumptions(window_fraction=0.01)
        result = constraint.evaluate(p, a)
        # exposed ≈ endcap_area only (near-zero window strip)
        assert result.details["exposed_area_m2"] == pytest.approx(
            0.01 * p.barrel_area_m2 + p.endcap_area_m2
        )

    def test_larger_radius_increases_exposure(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        r1 = constraint.evaluate(_params(radius_m=500), _assumptions())
        r2 = constraint.evaluate(_params(radius_m=1000), _assumptions())
        assert r2.details["exposed_area_m2"] > r1.details["exposed_area_m2"]

    def test_zero_length_exposes_only_endcaps(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        p = _params(length_m=0)
        result = constraint.evaluate(p, _assumptions())
        assert result.details["exposed_area_m2"] == pytest.approx(p.endcap_area_m2)
        assert result.details["shielded_area_m2"] == pytest.approx(0.0)


class TestFormulas:
    def test_annual_perforations_formula(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        flux = 5e-8
        result = constraint.evaluate(
            _params(), _assumptions(meteoroid_penetrating_flux_m2_yr=flux)
        )
        expected = flux * result.details["exposed_area_m2"]
        assert result.details["expected_annual_perforations"] == pytest.approx(expected)

    def test_lifetime_perforations_formula(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(
                meteoroid_penetrating_flux_m2_yr=1e-8,
                habitat_lifespan_years=50.0,
            ),
        )
        assert result.details["expected_lifetime_perforations"] == pytest.approx(
            result.details["expected_annual_perforations"] * 50.0
        )

    def test_reliability_is_poisson_zero_probability(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        """P(zero events) = exp(-lambda)."""
        result = constraint.evaluate(
            _params(),
            _assumptions(
                meteoroid_penetrating_flux_m2_yr=1e-9,
                habitat_lifespan_years=10.0,
            ),
        )
        lam = result.details["expected_lifetime_perforations"]
        assert result.details["reliability_lifetime"] == pytest.approx(math.exp(-lam))

    def test_high_lifetime_perforations_gives_near_zero_reliability(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        """Very high perforation count → reliability approaches zero."""
        result = constraint.evaluate(
            _params(),
            _assumptions(
                meteoroid_penetrating_flux_m2_yr=1e-3,
                habitat_lifespan_years=100.0,
            ),
        )
        assert result.details["reliability_lifetime"] == pytest.approx(0.0, abs=1e-10)

    def test_max_flux_to_pass_formula(self, constraint: MicrometeoiteConstraint) -> None:
        max_n = 2.0
        result = constraint.evaluate(
            _params(),
            _assumptions(max_annual_perforations=max_n),
        )
        area = result.details["exposed_area_m2"]
        assert result.details["max_flux_to_pass_m2_yr"] == pytest.approx(max_n / area)

    def test_annual_scales_linearly_with_flux(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        r1 = constraint.evaluate(
            _params(), _assumptions(meteoroid_penetrating_flux_m2_yr=1e-8)
        )
        r2 = constraint.evaluate(
            _params(), _assumptions(meteoroid_penetrating_flux_m2_yr=2e-8)
        )
        assert r2.details["expected_annual_perforations"] == pytest.approx(
            2.0 * r1.details["expected_annual_perforations"]
        )


class TestDetails:
    def test_details_contain_required_keys(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        result = constraint.evaluate(_params(), _assumptions())
        expected_keys = {
            "exposed_area_m2",
            "shielded_area_m2",
            "expected_annual_perforations",
            "expected_lifetime_perforations",
            "reliability_lifetime",
            "penetrating_flux_m2_yr",
            "max_flux_to_pass_m2_yr",
        }
        assert set(result.details.keys()) == expected_keys

    def test_flux_reflected_in_details(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        flux = 3.7e-8
        result = constraint.evaluate(
            _params(), _assumptions(meteoroid_penetrating_flux_m2_yr=flux)
        )
        assert result.details["penetrating_flux_m2_yr"] == pytest.approx(flux)


class TestScaleInsight:
    def test_iss_flux_catastrophic_for_large_habitat(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        """ISS Whipple flux is totally inadequate at O'Neill scale."""
        oneill = _params(radius_m=3200, length_m=32000)
        result = constraint.evaluate(
            oneill,
            _assumptions(meteoroid_penetrating_flux_m2_yr=6e-5),
        )
        # Expect thousands of perforations per year
        assert result.details["expected_annual_perforations"] > 1000
        assert result.feasible is False

    def test_regolith_shielding_makes_oneill_feasible(
        self, constraint: MicrometeoiteConstraint
    ) -> None:
        """Regolith-level flux (1e-10) makes even O'Neill-scale habitat safe."""
        oneill = _params(radius_m=3200, length_m=32000)
        result = constraint.evaluate(
            oneill,
            _assumptions(meteoroid_penetrating_flux_m2_yr=1e-10),
        )
        assert result.feasible is True
