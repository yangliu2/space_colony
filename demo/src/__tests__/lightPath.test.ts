import { describe, it, expect } from 'vitest';
import { reflectVector, computeMirrorCenterAngle, computeStripAngles } from '../lib/sceneGeometry';

describe('light path physics', () => {
  it('mirror reflects axial sunlight radially inward', () => {
    // From mirror_geometry.md:
    // Incident light d = (0, -1, 0) — axial, from sun
    // Mirror normal n = (-1/√2, 1/√2, 0)
    // Expected reflected r = (-1, 0, 0) — radially inward
    const d: [number, number, number] = [0, -1, 0];
    const n: [number, number, number] = [-1 / Math.sqrt(2), 1 / Math.sqrt(2), 0];
    const r = reflectVector(d, n);
    expect(r[0]).toBeCloseTo(-1);
    expect(r[1]).toBeCloseTo(0);
    expect(r[2]).toBeCloseTo(0);
  });

  it('incident dot normal gives correct value', () => {
    const d: [number, number, number] = [0, -1, 0];
    const n: [number, number, number] = [-1 / Math.sqrt(2), 1 / Math.sqrt(2), 0];
    const dot = d[0] * n[0] + d[1] * n[1] + d[2] * n[2];
    expect(dot).toBeCloseTo(-1 / Math.sqrt(2));
  });

  it('mirror center angles align with window strips, not land strips', () => {
    const strips = computeStripAngles();
    const windowCenters = strips.filter(s => s.type === 'window').map(s => s.centerAngle);
    for (let i = 0; i < 3; i++) {
      const mirrorAngle = computeMirrorCenterAngle(i);
      // Mirror should be at a window center
      const matchesWindow = windowCenters.some(
        wc => Math.abs(mirrorAngle - wc) < 0.001
      );
      expect(matchesWindow).toBe(true);
    }
  });

  it('no mirror center angle aligns with a land strip center', () => {
    const strips = computeStripAngles();
    const landCenters = strips.filter(s => s.type === 'land').map(s => s.centerAngle);
    for (let i = 0; i < 3; i++) {
      const mirrorAngle = computeMirrorCenterAngle(i);
      for (const lc of landCenters) {
        expect(Math.abs(mirrorAngle - lc)).toBeGreaterThan(0.1);
      }
    }
  });
});
