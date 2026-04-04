import { describe, it, expect } from 'vitest';
import {
  computeInterCylinderSpacing,
  STAGGER_ANGLE,
} from '../lib/sceneGeometry';

describe('inter-cylinder spacing', () => {
  const radius = 2;
  const length = 6;

  it('gap = length + radius (staggered mirrors)', () => {
    const { gap } = computeInterCylinderSpacing(radius, length);
    expect(gap).toBeCloseTo(length + radius);
  });

  it('sideOffset = 3R + L (center-to-center)', () => {
    const { sideOffset } = computeInterCylinderSpacing(radius, length);
    expect(sideOffset).toBeCloseTo(3 * radius + length);
  });

  it('stagger angle is π/3 (60°)', () => {
    const { staggerAngle } = computeInterCylinderSpacing(radius, length);
    expect(staggerAngle).toBeCloseTo(Math.PI / 3);
    expect(STAGGER_ANGLE).toBeCloseTo(Math.PI / 3);
  });

  it('gap > length for any positive radius (no mirror collision)', () => {
    // This is the collision safety condition with staggering
    for (const r of [0.5, 1, 2, 5, 10]) {
      for (const l of [1, 3, 6, 12]) {
        const { gap } = computeInterCylinderSpacing(r, l);
        expect(gap).toBeGreaterThan(l);
      }
    }
  });

  it('sideOffset matches getCameraPresets formula', () => {
    const { sideOffset } = computeInterCylinderSpacing(radius, length);
    // getCameraPresets computes: sideOffset = r * 2 + l + r = 3r + l
    const presetSideOffset = radius * 2 + length + radius;
    expect(sideOffset).toBeCloseTo(presetSideOffset);
  });
});
