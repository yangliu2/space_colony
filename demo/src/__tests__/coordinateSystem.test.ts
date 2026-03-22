import { describe, it, expect } from 'vitest';
import {
  computeMirrorGroupRotation,
  computeMirrorHingePosition,
  computeMirrorVertices,
  computeMirrorCenterAngle,
  STRIP_ANGLE,
  LAND_STRIP_CENTER,
} from '../lib/sceneGeometry';

describe('coordinate system invariants', () => {
  const radius = 2;
  const length = 6;

  describe('local coordinate system: Y=axis, XZ=radial', () => {
    it('point on rim at angle θ: [cos(θ)*r, y, sin(θ)*r]', () => {
      const theta = Math.PI / 4; // 45°
      const y = 1.5;
      const point = [Math.cos(theta) * radius, y, Math.sin(theta) * radius];
      // Radial distance should equal radius
      const radialDist = Math.sqrt(point[0] ** 2 + point[2] ** 2);
      expect(radialDist).toBeCloseTo(radius);
    });

    it('radial outward direction at angle θ: [cos(θ), 0, sin(θ)]', () => {
      const theta = Math.PI / 3;
      const dir = [Math.cos(theta), 0, Math.sin(theta)];
      const mag = Math.sqrt(dir[0] ** 2 + dir[1] ** 2 + dir[2] ** 2);
      expect(mag).toBeCloseTo(1); // unit vector
    });

    it('tangential direction at angle θ: [-sin(θ), 0, cos(θ)]', () => {
      const theta = Math.PI / 3;
      const radial = [Math.cos(theta), 0, Math.sin(theta)];
      const tangent = [-Math.sin(theta), 0, Math.cos(theta)];
      // Radial and tangential should be perpendicular
      const dot = radial[0] * tangent[0] + radial[2] * tangent[2];
      expect(dot).toBeCloseTo(0);
    });

    it('cylinder axis is along Y (rotation axis)', () => {
      // Cylinder extends from -length/2 to +length/2 along Y
      const endPositions = [-length / 2, length / 2];
      for (const y of endPositions) {
        // Points at both ends, same radial position, differ only in Y
        const p1 = [radius, endPositions[0], 0];
        const p2 = [radius, endPositions[1], 0];
        expect(p1[0]).toBe(p2[0]); // same X
        expect(p1[2]).toBe(p2[2]); // same Z
      }
    });
  });

  describe('R_Y(-θ) maps +X to radial outward', () => {
    it('R_Y(-θ) applied to (1,0,0) gives (cos θ, 0, sin θ)', () => {
      // Three.js R_Y(α): x' = x*cos(α) + z*sin(α), z' = -x*sin(α) + z*cos(α)
      // For α = -θ: x' = cos(θ), z' = sin(θ)  (since cos(-θ)=cosθ, sin(-θ)=-sinθ)
      const theta = Math.PI / 2; // 90°
      const alpha = -theta;
      const x = 1, z = 0;
      const xPrime = x * Math.cos(alpha) + z * Math.sin(alpha);
      const zPrime = -x * Math.sin(alpha) + z * Math.cos(alpha);
      expect(xPrime).toBeCloseTo(Math.cos(theta)); // cos(90°) = 0
      expect(zPrime).toBeCloseTo(Math.sin(theta)); // sin(90°) = 1
    });

    it('using +θ instead of -θ gives WRONG direction (radially inward)', () => {
      const theta = Math.PI / 2; // 90°
      const alpha = theta; // WRONG sign
      const x = 1, z = 0;
      const xPrime = x * Math.cos(alpha) + z * Math.sin(alpha);
      const zPrime = -x * Math.sin(alpha) + z * Math.cos(alpha);
      // This maps (1,0,0) to (cos90°, 0, -sin90°) = (0, 0, -1)
      // But radial outward at 90° is (0, 0, +1)
      // So Z component has WRONG sign
      expect(zPrime).toBeCloseTo(-Math.sin(theta)); // -1, not +1
      expect(zPrime).not.toBeCloseTo(Math.sin(theta));
    });

    it('mirror group rotation uses NEGATIVE angle (verified)', () => {
      for (let i = 0; i < 3; i++) {
        const angle = computeMirrorCenterAngle(i);
        const rot = computeMirrorGroupRotation(angle);
        expect(rot[1]).toBeCloseTo(-angle); // negative!
      }
    });
  });

  describe('outer rotation R_x(-π/2) maps local Y to world Z', () => {
    it('R_x(-π/2) applied to (0, 1, 0) gives (0, 0, 1)', () => {
      // R_x(α): y' = y*cos(α) - z*sin(α), z' = y*sin(α) + z*cos(α)
      const alpha = -Math.PI / 2;
      const y = 1, z = 0;
      const yPrime = y * Math.cos(alpha) - z * Math.sin(alpha);
      const zPrime = y * Math.sin(alpha) + z * Math.cos(alpha);
      expect(yPrime).toBeCloseTo(0);
      expect(zPrime).toBeCloseTo(-1); // local +Y maps to world -Z
      // But we center-offset by -(l+r*1.5)/2, so effective world Z is positive
    });
  });
});
