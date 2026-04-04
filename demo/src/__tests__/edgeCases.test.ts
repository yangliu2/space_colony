import { describe, it, expect } from 'vitest';
import {
  sceneScale,
  getCameraPresets,
  computeInterCylinderSpacing,
  computeMirrorVertices,
} from '../lib/sceneGeometry';

describe('edge cases — extreme parameters', () => {
  it('small radius (r=50m) produces valid output', () => {
    const { r, l, s } = sceneScale(50, 200);
    expect(r).toBe(2);
    expect(l).toBeCloseTo(8);
    expect(s).toBeCloseTo(0.04);
    expect(Number.isFinite(r)).toBe(true);
    expect(Number.isFinite(l)).toBe(true);

    // Camera presets should also be valid
    const presets = getCameraPresets(r, l);
    for (const p of presets) {
      for (const c of [...p.position, ...p.target]) {
        expect(Number.isFinite(c)).toBe(true);
      }
    }
  });

  it('large radius (r=5000m) caps length correctly', () => {
    const { r, l } = sceneScale(5000, 40000);
    expect(r).toBe(2);
    // rawL = 40000 * (2/5000) = 16 > 12, should be capped
    expect(l).toBe(12);
  });

  it('length exactly at cap boundary (rawL = 12)', () => {
    const { l } = sceneScale(1000, 6000);
    // rawL = 6000 * 0.002 = 12, exactly at cap
    expect(l).toBeCloseTo(12);
  });

  it('zero omega does not cause errors in spacing calculations', () => {
    // computeInterCylinderSpacing doesn't depend on omega
    const spacing = computeInterCylinderSpacing(2, 6);
    expect(Number.isFinite(spacing.sideOffset)).toBe(true);
    expect(spacing.gap).toBeGreaterThan(0);
  });

  it('equal radius and length', () => {
    const { r, l } = sceneScale(1000, 1000);
    expect(r).toBe(2);
    expect(l).toBeCloseTo(2);
    expect(l).toBeLessThan(12); // well under cap
  });

  it('very large length-to-radius ratio caps length', () => {
    const { l } = sceneScale(100, 10000);
    // rawL = 10000 * (2/100) = 200, way over cap
    expect(l).toBe(12);
  });

  it('mirror geometry valid for extreme dimensions', () => {
    // Very small
    const v1 = computeMirrorVertices(0.1, 0.05);
    expect(v1.v2[0]).toBeCloseTo(0.1);
    expect(v1.v2[1]).toBeCloseTo(0.1);

    // Very large
    const v2 = computeMirrorVertices(100, 50);
    expect(v2.v2[0]).toBeCloseTo(100);
    expect(v2.v2[1]).toBeCloseTo(100);

    // Both should have finite values
    for (const v of [v1, v2]) {
      for (const vert of [v.v0, v.v1, v.v2, v.v3]) {
        for (const c of vert) {
          expect(Number.isFinite(c)).toBe(true);
        }
      }
    }
  });
});
