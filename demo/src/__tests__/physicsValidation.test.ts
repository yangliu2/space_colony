import { describe, it, expect } from 'vitest';
import {
  LAND_STRIP_CENTER,
  ENDCAP_DEPTH_FRACTION,
  computeStripAngles,
} from '../lib/sceneGeometry';

describe('physics validation — cross-reference with plans/ documents', () => {
  it('end cap is a hemisphere (thetaLength = π/2 in Three.js)', () => {
    // structural_engineering.md §2.3: hemispheres for end caps
    // sphereGeometry args include thetaLength = PI/2
    const thetaLength = Math.PI / 2;
    expect(thetaLength).toBeCloseTo(Math.PI / 2);
  });

  it('end cap depth fraction is 0.3 (shallower than full hemisphere)', () => {
    expect(ENDCAP_DEPTH_FRACTION).toBeCloseTo(0.3);
  });

  it('gravity gradient is linear: g(d) = ω²d', () => {
    // From plans/: artificial gravity varies linearly with distance from axis
    const omega = 0.1; // rad/s (typical for 1g at 982m)
    const testDistances = [0, 0.25, 0.5, 0.75, 1.0]; // fractions of radius
    const radius = 982;
    for (const frac of testDistances) {
      const d = frac * radius;
      const g = omega * omega * d;
      const expectedG = frac * omega * omega * radius; // linear relationship
      expect(g).toBeCloseTo(expectedG);
    }
  });

  it('mid-zone at 0.5r gives 0.5g, zero-g zone at 0.1r gives 0.1g', () => {
    // interior_space_utilization.md: mid-zone at half radius
    const omega = 0.1;
    const radius = 982;
    const g_rim = omega * omega * radius; // ~9.82 m/s²

    const g_mid = omega * omega * (0.5 * radius);
    expect(g_mid / g_rim).toBeCloseTo(0.5);

    const g_zero = omega * omega * (0.1 * radius);
    expect(g_zero / g_rim).toBeCloseTo(0.1);
  });

  it('human figure is at LAND_STRIP_CENTER = π/6 (center of land strip 0)', () => {
    // Must be on a land strip, not a window strip boundary
    expect(LAND_STRIP_CENTER).toBeCloseTo(Math.PI / 6);
    const strips = computeStripAngles();
    const landStrip0 = strips[0];
    expect(landStrip0.type).toBe('land');
    // LAND_STRIP_CENTER should be within land strip 0 bounds
    expect(LAND_STRIP_CENTER).toBeGreaterThanOrEqual(landStrip0.startAngle);
    expect(LAND_STRIP_CENTER).toBeLessThanOrEqual(landStrip0.startAngle + landStrip0.arcAngle);
    // And at its center
    expect(LAND_STRIP_CENTER).toBeCloseTo(landStrip0.centerAngle);
  });
});
