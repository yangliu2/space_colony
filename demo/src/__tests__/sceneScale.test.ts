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

  it('caps length at r × 6 = 12 when scaled length exceeds cap', () => {
    // 1000m radius, 8000m length: rawL = 8000 * 0.002 = 16 > 12
    const { l } = sceneScale(1000, 8000);
    expect(l).toBe(12);
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
