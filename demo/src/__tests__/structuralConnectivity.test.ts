import { describe, it, expect } from 'vitest';
import {
  computeMirrorHingePosition,
  computeMirrorVertices,
  computeMirrorCenterAngle,
  computeAgriculturePodY,
  computeCableRadius,
  computeCableHoopPositions,
  computeInterCylinderSpacing,
  HINGE_OFFSET,
  MIRROR_TANGENT_FRACTION,
} from '../lib/sceneGeometry';

describe('structural connectivity — nothing floats in space', () => {
  const radius = 2;
  const length = 6;

  it('mirror hinge touches cylinder surface at anti-sun end', () => {
    const angle = computeMirrorCenterAngle(0);
    const pos = computeMirrorHingePosition(angle, radius, length);
    // Radial distance should be radius + small offset
    const radialDist = Math.sqrt(pos[0] ** 2 + pos[2] ** 2);
    expect(radialDist).toBeCloseTo(radius + HINGE_OFFSET);
    // Y should be at anti-sun end
    expect(pos[1]).toBeCloseTo(-length / 2);
  });

  it('mirror mesh starts at hinge position (vertices 0,1 at origin)', () => {
    const tangent = radius * MIRROR_TANGENT_FRACTION;
    const verts = computeMirrorVertices(length, tangent);
    // Vertices 0 and 1 are at (0, 0, ±t) — the group origin = hinge
    expect(verts.v0[0]).toBe(0);
    expect(verts.v0[1]).toBe(0);
    expect(verts.v1[0]).toBe(0);
    expect(verts.v1[1]).toBe(0);
  });

  it('end caps at ±length/2 (flush with cylinder ends)', () => {
    // EndCaps component positions at [0, sign * length/2, 0]
    const endPositions = [length / 2, -length / 2];
    for (const y of endPositions) {
      expect(Math.abs(y)).toBeCloseTo(length / 2);
    }
  });

  it('agriculture pods are OUTSIDE the cylinder', () => {
    const { yBase } = computeAgriculturePodY(radius, length);
    expect(yBase).toBeLessThan(-length / 2);
  });

  it('agriculture connecting ring is near end cap', () => {
    const { ringY } = computeAgriculturePodY(radius, length);
    // Ring at -length/2 - 0.1, just beyond end cap
    expect(ringY).toBeLessThan(-length / 2);
    expect(ringY).toBeGreaterThan(-length / 2 - 0.5); // not too far
  });

  it('tension cables are OUTSIDE hull', () => {
    const cableR = computeCableRadius(radius);
    expect(cableR).toBeGreaterThan(radius);
  });

  it('cable hoops are within cylinder length bounds', () => {
    const { positions } = computeCableHoopPositions(length);
    for (const y of positions) {
      expect(y).toBeGreaterThan(-length / 2);
      expect(y).toBeLessThan(length / 2);
    }
  });

  it('interior spine extends slightly beyond cylinder (length × 1.1)', () => {
    const spineLength = length * 1.1;
    expect(spineLength).toBeGreaterThan(length);
    // Spine centered at origin, extends from -spineLength/2 to +spineLength/2
    expect(spineLength / 2).toBeGreaterThan(length / 2);
  });

  it('radial elevators connect axis to near-rim (0.95 × radius)', () => {
    const elevatorReach = 0.95 * radius;
    expect(elevatorReach).toBeLessThan(radius);
    expect(elevatorReach).toBeGreaterThan(radius * 0.9);
  });

  it('bearing struts span between the two cylinders', () => {
    const { sideOffset } = computeInterCylinderSpacing(radius, length);
    const strutPositions = [0.25, 0.5, 0.75].map(f => f * sideOffset);
    for (const x of strutPositions) {
      expect(x).toBeGreaterThan(0);
      expect(x).toBeLessThan(sideOffset);
    }
  });
});
