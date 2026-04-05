import { describe, it, expect } from 'vitest';
import { sceneScale } from '../lib/sceneGeometry';

describe('sceneScale', () => {
  it('always normalizes radius to 2 scene units', () => {
    expect(sceneScale(1000, 5000).r).toBe(2);
    expect(sceneScale(50, 200).r).toBe(2);
    expect(sceneScale(5000, 10000).r).toBe(2);
  });

  it('computes correct scale factor', () => {
    expect(sceneScale(1000, 5000).s).toBeCloseTo(0.002);
    expect(sceneScale(500, 1000).s).toBeCloseTo(0.004);
  });

  it('caps length at bending resonance limit when length exceeds physics bound', () => {
    // r=1000m, bending limit = 75.22 * 1000^0.75 * 1.2 ≈ 16,052m
    // l=20000m exceeds limit → capped at 16052 * (2/1000) ≈ 32.1 scene units
    const { l } = sceneScale(1000, 20000);
    expect(l).toBeCloseTo(32.1, 0);
  });

  it('does not cap length when scaled length is within limit', () => {
    // 1000m radius, 2000m length: rawL = 2000 * 0.002 = 4 < 12
    const { l } = sceneScale(1000, 2000);
    expect(l).toBeCloseTo(4);
  });

  it('produces all positive, finite values', () => {
    const cases = [[50, 200], [982, 10680], [3200, 32000], [5000, 40000]];
    for (const [r, len] of cases) {
      const result = sceneScale(r, len);
      expect(result.r).toBeGreaterThan(0);
      expect(result.l).toBeGreaterThan(0);
      expect(result.s).toBeGreaterThan(0);
      expect(Number.isFinite(result.r)).toBe(true);
      expect(Number.isFinite(result.l)).toBe(true);
      expect(Number.isFinite(result.s)).toBe(true);
    }
  });
});
