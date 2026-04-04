import { describe, it, expect } from 'vitest';
import {
  computeStripAngles,
  computeMirrorVertices,
  computeMirrorCenterAngle,
  computeMirrorHingePosition,
  computeMirrorTipWorldPosition,
  computeInterCylinderSpacing,
  computeAgriculturePodY,
  computeCrossCoupling,
  computeMinRadiusCrossCoupling,
  computeMaxRadiusRimSpeed,
  computeRimSpeed,
  computeCoriolisRatio,
  computeGravityGradient,
  computeOmegaFor1g,
  omegaToRPM,
  isInsideCylinder,
  reflectVector,
  HINGE_OFFSET,
} from '../lib/sceneGeometry';

const G = 9.807; // m/s²

describe('plans/ document cross-validation', () => {

  describe('constraint_cross_coupling.md — binding constraint', () => {
    it('cross-coupling at O\'Neill (3200m): α = ω_hab × ω_head ≈ 3.3 deg/s²', () => {
      const r = 3200;
      const omega = computeOmegaFor1g(r);
      const omegaHead = 1.047; // 60°/s normal head turn (rad/s)
      const alpha = computeCrossCoupling(omega, omegaHead);
      const alphaDeg = alpha * (180 / Math.PI);
      expect(alphaDeg).toBeCloseTo(3.3, 0); // ~3.3 deg/s²
    });

    it('minimum radius at 1g for adapted threshold (6 deg/s²) = 982m', () => {
      const omegaHead = 1.047; // rad/s
      const alphaMax = 6.0 * (Math.PI / 180); // 6 deg/s² → rad/s²
      const rMin = computeMinRadiusCrossCoupling(G, omegaHead, alphaMax);
      expect(rMin).toBeCloseTo(982, -1); // within ~10m
    });

    it('cross-coupling is MORE restrictive than vestibular (RPM=2 → r=224m)', () => {
      const rVestibular = G / ((2 * Math.PI / 30) ** 2); // r = g/ω², ω = 2rpm in rad/s
      const omegaHead = 1.047;
      const alphaMax = 6.0 * (Math.PI / 180);
      const rCrossCoupling = computeMinRadiusCrossCoupling(G, omegaHead, alphaMax);
      expect(rCrossCoupling).toBeGreaterThan(rVestibular * 4); // ~4.4x more restrictive
    });
  });

  describe('constraint_rim_speed.md — upper bound', () => {
    it('max radius at v_max=300 m/s = 9177m', () => {
      const rMax = computeMaxRadiusRimSpeed(300, G);
      expect(rMax).toBeCloseTo(9177, -1);
    });

    it('O\'Neill at 3200m has rim speed ≈ 177 m/s', () => {
      const v = computeRimSpeed(G, 3200);
      expect(v).toBeCloseTo(177, 0);
    });

    it('rim speed within structural limit (300 m/s) for all feasible radii', () => {
      for (const r of [982, 2000, 3200, 5000, 9177]) {
        const v = computeRimSpeed(G, r);
        expect(v).toBeLessThanOrEqual(300.1); // small tolerance
      }
    });
  });

  describe('constraint_coriolis.md', () => {
    it('walking at 1.4 m/s in 982m habitat: Coriolis ≈ 2.9% of g', () => {
      const vRim = computeRimSpeed(G, 982);
      const ratio = computeCoriolisRatio(1.4, vRim);
      expect(ratio * 100).toBeCloseTo(2.9, 0);
    });

    it('running at 3.0 m/s in 982m habitat: Coriolis ≈ 6.1% of g', () => {
      const vRim = computeRimSpeed(G, 982);
      const ratio = computeCoriolisRatio(3.0, vRim);
      expect(ratio * 100).toBeCloseTo(6.1, 0);
    });
  });

  describe('constraint_gravity_gradient.md', () => {
    it('at r=180m, h=1.8m: gradient = 1%', () => {
      const grad = computeGravityGradient(1.8, 180);
      expect(grad).toBeCloseTo(0.01);
    });

    it('at O\'Neill r=3200m, h=1.8m: gradient = 0.056%', () => {
      const grad = computeGravityGradient(1.8, 3200);
      expect(grad * 100).toBeCloseTo(0.056, 2);
    });
  });

  describe('constraint_vestibular.md — RPM limits', () => {
    it('2 RPM limit → min radius 224m at 1g', () => {
      const omegaMax = 2.0 * Math.PI / 30; // 2 RPM → rad/s
      const rMin = G / (omegaMax * omegaMax);
      expect(rMin).toBeCloseTo(224, 0);
    });

    it('O\'Neill 3200m → ~0.55 RPM (well under 2 RPM)', () => {
      const omega = computeOmegaFor1g(3200);
      const rpm = omegaToRPM(omega);
      expect(rpm).toBeCloseTo(0.53, 1);
      expect(rpm).toBeLessThan(2.0);
    });
  });

  describe('feasible design band at 1g: [982m, 9177m]', () => {
    it('lower bound (cross-coupling) ≈ 982m', () => {
      const omegaHead = 1.047;
      const alphaMax = 6.0 * Math.PI / 180;
      const rMin = computeMinRadiusCrossCoupling(G, omegaHead, alphaMax);
      expect(rMin).toBeCloseTo(982, -1);
    });

    it('upper bound (rim speed) ≈ 9177m', () => {
      const rMax = computeMaxRadiusRimSpeed(300, G);
      expect(rMax).toBeCloseTo(9177, -1);
    });

    it('O\'Neill 3200m is within feasible band', () => {
      const omegaHead = 1.047;
      const alphaMax = 6.0 * Math.PI / 180;
      const rMin = computeMinRadiusCrossCoupling(G, omegaHead, alphaMax);
      const rMax = computeMaxRadiusRimSpeed(300, G);
      expect(3200).toBeGreaterThan(rMin);
      expect(3200).toBeLessThan(rMax);
    });
  });

  describe('mirror_geometry.md — physical correctness', () => {
    it('mirror reflects axial sunlight (0,-1,0) to radial inward (-1,0,0)', () => {
      const d: [number, number, number] = [0, -1, 0];
      const n: [number, number, number] = [-1 / Math.sqrt(2), 1 / Math.sqrt(2), 0];
      const r = reflectVector(d, n);
      expect(r[0]).toBeCloseTo(-1);
      expect(r[1]).toBeCloseTo(0);
      expect(r[2]).toBeCloseTo(0);
    });

    it('mirror at 45° has equal radial and axial extent', () => {
      const length = 6;
      const tangent = 1.7;
      const verts = computeMirrorVertices(length, tangent);
      // Outer vertex (d, d, ±t): radial component = d, axial component = d
      expect(verts.v2[0]).toBe(verts.v2[1]); // x = y = d
    });

    it('mirrors align with window strip centers, not land strips', () => {
      const strips = computeStripAngles();
      const windowCenters = strips.filter(s => s.type === 'window').map(s => s.centerAngle);
      for (let i = 0; i < 3; i++) {
        const mirrorAngle = computeMirrorCenterAngle(i);
        const match = windowCenters.some(wc => Math.abs(mirrorAngle - wc) < 0.001);
        expect(match).toBe(true);
      }
    });

    it('mirror tip is OUTSIDE the cylinder (not penetrating)', () => {
      const radius = 2;
      const length = 6;
      for (let i = 0; i < 3; i++) {
        const angle = computeMirrorCenterAngle(i);
        const tip = computeMirrorTipWorldPosition(angle, radius, length);
        // Tip should NOT be inside the cylinder
        expect(isInsideCylinder(tip, radius, length)).toBe(false);
      }
    });

    it('mirror hinge is attached to cylinder surface (not floating)', () => {
      const radius = 2;
      const length = 6;
      for (let i = 0; i < 3; i++) {
        const angle = computeMirrorCenterAngle(i);
        const pos = computeMirrorHingePosition(angle, radius, length);
        const radialDist = Math.sqrt(pos[0] ** 2 + pos[2] ** 2);
        // Should be just barely outside cylinder surface
        expect(radialDist).toBeCloseTo(radius + HINGE_OFFSET);
        expect(radialDist - radius).toBeLessThan(0.1); // very close
      }
    });
  });

  describe('inter-cylinder spacing — no mirror collision', () => {
    it('with 60° stagger, gap is sufficient for non-overlapping mirrors', () => {
      const radius = 2;
      const length = 6;
      const { gap, mirrorRadialExtent } = computeInterCylinderSpacing(radius, length);
      // With stagger, the projections don't overlap fully
      // gap should be > mirrorRadialExtent (conservative)
      expect(gap).toBeGreaterThan(mirrorRadialExtent);
    });

    it('mirror tips from cylinder 1 don\'t reach cylinder 2', () => {
      const radius = 2;
      const length = 6;
      const { sideOffset } = computeInterCylinderSpacing(radius, length);

      for (let i = 0; i < 3; i++) {
        const angle = computeMirrorCenterAngle(i);
        const tip = computeMirrorTipWorldPosition(angle, radius, length);
        // Tip X should be less than sideOffset - radius (second cylinder rim)
        expect(tip[0]).toBeLessThan(sideOffset - radius);
      }
    });
  });

  describe('structural_engineering.md — land strip coverage', () => {
    it('3 land strips cover exactly 180° (half the circumference)', () => {
      const strips = computeStripAngles();
      const landStrips = strips.filter(s => s.type === 'land');
      const totalArc = landStrips.reduce((sum, s) => sum + s.arcAngle, 0);
      expect(totalArc).toBeCloseTo(Math.PI); // 180°
    });

    it('3 window strips cover exactly 180° (other half)', () => {
      const strips = computeStripAngles();
      const windowStrips = strips.filter(s => s.type === 'window');
      const totalArc = windowStrips.reduce((sum, s) => sum + s.arcAngle, 0);
      expect(totalArc).toBeCloseTo(Math.PI); // 180°
    });

    it('no gaps between strips (full 360° coverage)', () => {
      const strips = computeStripAngles();
      let totalArc = 0;
      for (const s of strips) {
        totalArc += s.arcAngle;
      }
      expect(totalArc).toBeCloseTo(2 * Math.PI);
    });
  });

  describe('agriculture pods — exterior placement', () => {
    it('pods are physically outside the cylinder at anti-bearing end', () => {
      const radius = 2;
      const length = 6;
      const { yBase } = computeAgriculturePodY(radius, length);
      expect(yBase).toBeLessThan(-length / 2);
    });

    it('pods do not extend into cylinder interior', () => {
      const radius = 2;
      const length = 6;
      const { yBase, podLen } = computeAgriculturePodY(radius, length);
      // Pod is centered at yBase; capsule extends podLen/2 above center
      const podTop = yBase + podLen / 2;
      // Even the top of the pod should be at or below cylinder end
      expect(podTop).toBeLessThanOrEqual(-length / 2 + 0.01);
    });
  });
});
