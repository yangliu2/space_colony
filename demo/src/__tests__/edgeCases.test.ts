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

  it('large radius (r=5000m) within bending limit is not capped', () => {
    const { r, l } = sceneScale(5000, 40000);
    expect(r).toBe(2);
    // r=5000m: bending limit = 75.22 * 5000^0.75 * 1.2 ≈ 95,218m
    // 40000m < 95218m → not capped; rawL = 40000 * (2/5000) = 16
    expect(l).toBeCloseTo(16, 1);
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
    expect(l).toBeLessThan(10); // well under bending cap
  });

  it('very large length-to-radius ratio caps at bending resonance limit', () => {
    // r=100m: bending limit = 75.22 * 100^0.75 * 1.2 ≈ 2853m
    // l=10000m >> 2853m → capped; cap in scene units = 2853 * (2/100) ≈ 57.1
    const { l } = sceneScale(100, 10000);
    expect(l).toBeCloseTo(57.1, 0);
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
