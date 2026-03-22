import { describe, it, expect } from 'vitest';
import {
  computeMirrorVertices,
  computeMirrorCenterAngle,
  computeMirrorHingePosition,
  computeMirrorGroupRotation,
  MIRROR_TANGENT_FRACTION,
  HINGE_OFFSET,
} from '../lib/sceneGeometry';

describe('mirror geometry', () => {
  const radius = 2;
  const length = 6;

  describe('mirror vertices (45° diagonal)', () => {
    it('outer vertices encode exact 45° angle via (d, d, ±t)', () => {
      const verts = computeMirrorVertices(6, 1.7);
      // Vector from hinge to outer: (d, d, 0). Angle = atan2(d, d) = PI/4
      const dx = verts.v2[0] - verts.v0[0]; // d - 0 = d
      const dy = verts.v2[1] - verts.v0[1]; // d - 0 = d
      const angle = Math.atan2(dy, dx);
      expect(angle).toBeCloseTo(Math.PI / 4); // 45°
    });

    it('hinge vertices are at local origin (0, 0, ±t)', () => {
      const verts = computeMirrorVertices(6, 1.7);
      expect(verts.v0[0]).toBe(0);
      expect(verts.v0[1]).toBe(0);
      expect(verts.v1[0]).toBe(0);
      expect(verts.v1[1]).toBe(0);
    });

    it('tangent half-width matches ±t', () => {
      const tangent = 1.7;
      const t = tangent / 2;
      const verts = computeMirrorVertices(6, tangent);
      expect(verts.v0[2]).toBeCloseTo(-t);
      expect(verts.v1[2]).toBeCloseTo(t);
      expect(verts.v2[2]).toBeCloseTo(-t);
      expect(verts.v3[2]).toBeCloseTo(t);
    });

    it('mirror tangent = radius × 0.85', () => {
      const tangent = radius * MIRROR_TANGENT_FRACTION;
      expect(tangent).toBeCloseTo(1.7);
    });

    it('mirror axial extent equals cylinder length', () => {
      const verts = computeMirrorVertices(length, 1.7);
      expect(verts.v2[0]).toBe(length); // d = axialExtent = length
      expect(verts.v2[1]).toBe(length); // d = axialExtent = length
    });

    it('all vertices have finite coordinates', () => {
      const verts = computeMirrorVertices(6, 1.7);
      for (const v of [verts.v0, verts.v1, verts.v2, verts.v3]) {
        for (const c of v) {
          expect(Number.isFinite(c)).toBe(true);
        }
      }
    });
  });

  describe('mirror center angles', () => {
    it('default (no offset): 90°, 210°, 330°', () => {
      expect(computeMirrorCenterAngle(0)).toBeCloseTo(Math.PI / 2);       // 90°
      expect(computeMirrorCenterAngle(1)).toBeCloseTo(7 * Math.PI / 6);   // 210°
      expect(computeMirrorCenterAngle(2)).toBeCloseTo(11 * Math.PI / 6);  // 330°
    });

    it('with 60° stagger: 150°, 270°, 30°', () => {
      const offset = Math.PI / 3;
      expect(computeMirrorCenterAngle(0, offset)).toBeCloseTo(5 * Math.PI / 6);  // 150°
      expect(computeMirrorCenterAngle(1, offset)).toBeCloseTo(3 * Math.PI / 2);  // 270°
      expect(computeMirrorCenterAngle(2, offset)).toBeCloseTo(13 * Math.PI / 6); // 390° = 30°
    });
  });

  describe('mirror hinge position', () => {
    it('hinge is at anti-sun end (Y = -length/2)', () => {
      const pos = computeMirrorHingePosition(Math.PI / 2, radius, length);
      expect(pos[1]).toBeCloseTo(-length / 2);
    });

    it('hinge is just outside cylinder surface (radius + offset)', () => {
      const angle = Math.PI / 2;
      const pos = computeMirrorHingePosition(angle, radius, length);
      const radialDist = Math.sqrt(pos[0] ** 2 + pos[2] ** 2);
      expect(radialDist).toBeCloseTo(radius + HINGE_OFFSET);
    });
  });

  describe('mirror group rotation', () => {
    it('rotation Y component is NEGATIVE of center angle (critical sign)', () => {
      const angle = Math.PI / 2;
      const rot = computeMirrorGroupRotation(angle);
      expect(rot[0]).toBe(0);
      expect(rot[1]).toBeCloseTo(-angle); // NEGATIVE — R_Y(+θ) sends mirror inward!
      expect(rot[2]).toBe(0);
    });
  });
});
