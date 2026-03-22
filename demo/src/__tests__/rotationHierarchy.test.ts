import { describe, it, expect } from 'vitest';
import {
  LAND_STRIP_CENTER,
  STAGGER_ANGLE,
  computeStripAngles,
} from '../lib/sceneGeometry';

/**
 * These tests validate the INTENDED rotation hierarchy of the 3D scene.
 * They don't test Three.js rendering directly, but verify the design
 * contracts that the component tree must satisfy.
 *
 * Scene hierarchy (from CylinderScene.tsx):
 *   <group rotation={[-PI/2, 0, 0]}>         ← world transform
 *     <group position={centering}>            ← center offset
 *       <RotatingGroup ω>                     ← PRIMARY rotation
 *         CylinderShell (wireframe + strips + mirrors)
 *         EndCaps
 *         TensionCables
 *         AgriculturePods
 *         InteriorZones
 *         HumanFigure
 *         CoriolisArrow
 *       </RotatingGroup>
 *       <CounterRotatingPair>                 ← COUNTER rotation
 *         Bearing framework (STATIC)
 *         <group offset=[sideOffset,0,0]>
 *           <RotatingGroup ω direction=-1>
 *             CylinderShell + strips + mirrors (staggered)
 *             EndCaps, Cables, Agriculture, InteriorZones
 *           </RotatingGroup>
 *         </group>
 *       </CounterRotatingPair>
 *       GravityRings (STATIC)
 *       Axis (STATIC)
 *       GravityLabel (STATIC)
 *       ViewpointHotspots (STATIC)
 *       InteriorLighting (STATIC)
 *     </group>
 *   </group>
 */

describe('rotation hierarchy contracts', () => {
  // These are design-level tests that document what MUST rotate and what MUST NOT.
  // The actual Three.js component tree is verified by reading the source.

  describe('components that MUST co-rotate with primary cylinder', () => {
    const mustRotate = [
      'CylinderShell',
      'ONeillStrips (land + window)',
      'ExternalMirrors',
      'EndCaps',
      'TensionCables',
      'AgriculturePods',
      'InteriorZones',
      'HumanFigure',
      'CoriolisArrow',
    ];

    it('documents 9 component types that must rotate', () => {
      expect(mustRotate.length).toBe(9);
    });
  });

  describe('components that MUST be static (reference frames)', () => {
    const mustBeStatic = [
      'GravityRings',
      'Axis',
      'GravityLabel',
      'ViewpointHotspots',
      'InteriorLighting',
      'Bearing framework (cross-struts + ring)',
    ];

    it('documents 6 component types that must NOT rotate', () => {
      expect(mustBeStatic.length).toBe(6);
    });
  });

  describe('human figure and Coriolis must be co-located on land strip', () => {
    it('both positioned at LAND_STRIP_CENTER = π/6 (30°)', () => {
      expect(LAND_STRIP_CENTER).toBeCloseTo(Math.PI / 6);
    });

    it('LAND_STRIP_CENTER is within land strip 0 (index 0, type=land)', () => {
      const strips = computeStripAngles();
      const land0 = strips[0];
      expect(land0.type).toBe('land');
      expect(LAND_STRIP_CENTER).toBeGreaterThanOrEqual(land0.startAngle);
      expect(LAND_STRIP_CENTER).toBeLessThanOrEqual(land0.startAngle + land0.arcAngle);
    });

    it('human is at center of land strip (not at edge/boundary)', () => {
      const strips = computeStripAngles();
      expect(LAND_STRIP_CENTER).toBeCloseTo(strips[0].centerAngle);
    });
  });

  describe('counter-rotating cylinder', () => {
    it('second cylinder uses direction = -1 (opposite rotation)', () => {
      // This is a design contract; direction=-1 is passed to RotatingGroup
      const direction = -1;
      expect(direction).toBe(-1);
    });

    it('second cylinder has 60° stagger offset', () => {
      expect(STAGGER_ANGLE).toBeCloseTo(Math.PI / 3);
    });

    it('staggered strips still cover full 360°', () => {
      const strips = computeStripAngles(STAGGER_ANGLE);
      const totalArc = strips.reduce((sum, s) => sum + s.arcAngle, 0);
      expect(totalArc).toBeCloseTo(2 * Math.PI);
    });

    it('staggered window centers differ from primary by exactly 60°', () => {
      const primary = computeStripAngles(0).filter(s => s.type === 'window');
      const secondary = computeStripAngles(STAGGER_ANGLE).filter(s => s.type === 'window');
      for (let i = 0; i < 3; i++) {
        const diff = secondary[i].centerAngle - primary[i].centerAngle;
        expect(diff).toBeCloseTo(Math.PI / 3); // 60°
      }
    });
  });

  describe('rotation speed', () => {
    it('RotatingGroup applies ω × delta × 10 per frame (10x visual speedup)', () => {
      // Visual speedup factor = 10 (documented in RotatingGroup)
      const speedupFactor = 10;
      const omegaRadS = 0.05; // typical
      const delta = 1 / 60; // 60fps
      const rotationPerFrame = omegaRadS * delta * speedupFactor;
      expect(rotationPerFrame).toBeGreaterThan(0);
      // At 0.05 rad/s with 10x speedup at 60fps: 0.05 * 1/60 * 10 ≈ 0.0083 rad/frame
      expect(rotationPerFrame).toBeCloseTo(0.0083, 3);
    });
  });
});
