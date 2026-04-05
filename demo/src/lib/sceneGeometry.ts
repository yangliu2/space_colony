/**
 * Pure geometry/math functions for the O'Neill cylinder 3D scene.
 *
 * These are extracted from CylinderScene.tsx so they can be unit-tested
 * without React or Three.js dependencies. Every formula here corresponds
 * to a physics constraint or engineering spec in plans/*.md.
 */

// ── Constants ──────────────────────────────────────────────────────

/** Angular width of each O'Neill strip (land or window): 60° = π/3. */
export const STRIP_ANGLE = Math.PI / 3;

/** Number of alternating strips (3 land + 3 window). */
export const STRIP_COUNT = 6;

/** Rotational offset between the two counter-rotating cylinders. */
export const STAGGER_ANGLE = Math.PI / 3; // 60°

/** Center angle of the first land strip (strip 0: 0°–60°, center 30°). */
export const LAND_STRIP_CENTER = Math.PI / 6;

/** Mirror tangent width as fraction of radius. */
export const MIRROR_TANGENT_FRACTION = 0.85;

/** Hinge offset from cylinder surface (scene units). */
export const HINGE_OFFSET = 0.03;

/** Tension cable offset from cylinder surface (scene units). */
export const CABLE_OFFSET = 0.06;

/** Agriculture pod length as fraction of radius. */
export const POD_LENGTH_FRACTION = 0.4;

/** Agriculture pod deployment: how far beyond end cap (fraction of podLen). */
export const POD_BEYOND_END_FRACTION = 0.6;

/** End cap hemisphere depth as fraction of radius. */
export const ENDCAP_DEPTH_FRACTION = 0.3;

// ── Scene Scale ────────────────────────────────────────────────────

/**
 * Bending resonance coefficient — must match ParameterSliders.tsx and api/main.py.
 * L_max = C_BENDING * r^0.75 (see plans/constraint_cylinder_length.md).
 */
const C_BENDING_SCENE = 75.22;

/**
 * Normalize real-world meters to scene units.
 * Radius maps to ~2 scene units; length capped at 1.2× the bending resonance
 * limit so the full feasible range is always visible in the 3D model.
 */
export function sceneScale(radius_m: number, length_m: number) {
  const targetR = 2;
  const s = targetR / radius_m;
  const r = targetR;
  const rawL = length_m * s;
  // Cap at 20% above the physics limit so the slider's full range renders correctly
  const maxPhysicalLength = C_BENDING_SCENE * Math.pow(radius_m, 0.75) * 1.2;
  const l = Math.min(rawL, maxPhysicalLength * s);
  return { r, l, s };
}

// ── Strip Layout ───────────────────────────────────────────────────

export interface StripInfo {
  index: number;
  type: "land" | "window";
  startAngle: number;
  arcAngle: number;
  centerAngle: number;
}

/**
 * Compute the 6 O'Neill strip definitions (3 land, 3 window, alternating).
 * Even indices = land; odd indices = window.
 */
export function computeStripAngles(angleOffset = 0): StripInfo[] {
  const strips: StripInfo[] = [];
  for (let i = 0; i < STRIP_COUNT; i++) {
    const startAngle = i * STRIP_ANGLE + angleOffset;
    strips.push({
      index: i,
      type: i % 2 === 0 ? "land" : "window",
      startAngle,
      arcAngle: STRIP_ANGLE,
      centerAngle: startAngle + STRIP_ANGLE / 2,
    });
  }
  return strips;
}

// ── Mirror Geometry ────────────────────────────────────────────────

/**
 * Compute center angle for mirror i (0, 1, 2) — centered on window strip.
 * Window strips are at odd indices (1, 3, 5).
 * Default (angleOffset=0): 90°, 210°, 330°.
 */
export function computeMirrorCenterAngle(
  i: number,
  angleOffset = 0,
): number {
  return STRIP_ANGLE * (2 * i + 1) + STRIP_ANGLE / 2 + angleOffset;
}

export interface MirrorVertices {
  /** Hinge vertex, tangential - */
  v0: [number, number, number];
  /** Hinge vertex, tangential + */
  v1: [number, number, number];
  /** Outer vertex (diagonal), tangential - */
  v2: [number, number, number];
  /** Outer vertex (diagonal), tangential + */
  v3: [number, number, number];
}

/**
 * Compute the 4 vertices of the mirror quad in group-local coordinates.
 * The 45° diagonal is baked into the vertex positions: outer edge at (d, d, ±t).
 */
export function computeMirrorVertices(
  axialExtent: number,
  tangentWidth: number,
): MirrorVertices {
  const t = tangentWidth / 2;
  const d = axialExtent;
  return {
    v0: [0, 0, -t],
    v1: [0, 0, t],
    v2: [d, d, -t],
    v3: [d, d, t],
  };
}

/**
 * Compute the hinge position for a mirror at a given center angle.
 * Returns [x, y, z] in the cylinder's local coordinate system.
 */
export function computeMirrorHingePosition(
  centerAngle: number,
  radius: number,
  length: number,
): [number, number, number] {
  const hingeR = radius + HINGE_OFFSET;
  return [
    Math.cos(centerAngle) * hingeR,
    -length / 2, // anti-sun end
    Math.sin(centerAngle) * hingeR,
  ];
}

/**
 * Compute the group rotation for a mirror at a given center angle.
 * The NEGATIVE sign is critical: R_Y(-θ) maps +X → radial outward.
 */
export function computeMirrorGroupRotation(
  centerAngle: number,
): [number, number, number] {
  return [0, -centerAngle, 0];
}

// ── Inter-Cylinder Spacing ─────────────────────────────────────────

export interface CylinderSpacing {
  /** At 45° tilt, mirror radial extent = axial extent = length. */
  mirrorRadialExtent: number;
  /** Gap between cylinder rims (staggered: L + R). */
  gap: number;
  /** Center-to-center distance: 2R + gap = 3R + L. */
  sideOffset: number;
  /** Stagger angle for second cylinder's strips/mirrors. */
  staggerAngle: number;
}

export function computeInterCylinderSpacing(
  radius: number,
  length: number,
): CylinderSpacing {
  const mirrorRadialExtent = length;
  const gap = mirrorRadialExtent + radius;
  const sideOffset = radius * 2 + gap;
  return { mirrorRadialExtent, gap, sideOffset, staggerAngle: STAGGER_ANGLE };
}

// ── Camera Presets ─────────────────────────────────────────────────

export interface CameraPreset {
  name: string;
  position: [number, number, number];
  target: [number, number, number];
}

/**
 * Dynamic camera presets based on scene dimensions.
 * All coordinates are in world space (after the R_x(-π/2) rotation).
 *
 * Primary cylinder center in world = [0, 0, cz] where cz = (l + r*1.5) / 2.
 * The centering group offsets local Y by -(l + r*1.5)/2.
 * R_x(-π/2) maps local (0, y, 0) → world (0, 0, -y).
 * So world Z = +(l + r*1.5)/2. (POSITIVE — this was a critical bug when negative.)
 */
export function getCameraPresets(r: number, l: number): CameraPreset[] {
  const cz = (l + r * 1.5) / 2;
  const sideOffset = r * 2 + l + r;
  const fullExtentX = sideOffset + r + l;
  const anchor: [number, number, number] = [0, 0, cz];

  return [
    {
      name: "Default",
      position: [r * 2.5, r * 1.5, cz + l * 0.8],
      target: anchor,
    },
    {
      name: "Side view",
      position: [-(fullExtentX * 0.5), fullExtentX * 0.35, cz],
      target: [sideOffset * 0.4, 0, cz],
    },
    {
      name: "End view",
      position: [r * 0.3, r * 0.3, cz + l * 0.5 + r * 4],
      target: anchor,
    },
    {
      name: "Top-down",
      position: [0, l + r * 3, cz],
      target: anchor,
    },
    {
      name: "Close-up rim",
      position: [r * 1.0, r * 0.6, cz + r * 0.25],
      target: [r * 0.866, r * 0.5, cz],
    },
    {
      name: "Full colony",
      position: [sideOffset / 2, fullExtentX * 1.0, cz + fullExtentX * 0.3],
      target: [sideOffset / 2, 0, cz],
    },
  ];
}

// ── Structural Connectivity ────────────────────────────────────────

/**
 * Compute agriculture pod Y position (should be OUTSIDE the cylinder).
 */
export function computeAgriculturePodY(
  radius: number,
  length: number,
): { yBase: number; podLen: number; ringY: number } {
  const podLen = radius * POD_LENGTH_FRACTION;
  const yBase = -length / 2 - podLen * POD_BEYOND_END_FRACTION;
  const ringY = -length / 2 - 0.1;
  return { yBase, podLen, ringY };
}

/**
 * Compute tension cable radius (should be OUTSIDE the hull).
 */
export function computeCableRadius(radius: number): number {
  return radius + CABLE_OFFSET;
}

/**
 * Compute cable hoop Y positions along the cylinder.
 */
export function computeCableHoopPositions(
  length: number,
): { numRings: number; positions: number[] } {
  const numRings = Math.max(6, Math.round(length / 0.8));
  const spacing = length / (numRings + 1);
  const positions: number[] = [];
  for (let i = 1; i <= numRings; i++) {
    positions.push(-length / 2 + spacing * i);
  }
  return { numRings, positions };
}

// ── Light Path Physics ─────────────────────────────────────────────

/** Compute reflection direction: r = d - 2(d·n)n */
export function reflectVector(
  d: [number, number, number],
  n: [number, number, number],
): [number, number, number] {
  const dot = d[0] * n[0] + d[1] * n[1] + d[2] * n[2];
  return [
    d[0] - 2 * dot * n[0],
    d[1] - 2 * dot * n[1],
    d[2] - 2 * dot * n[2],
  ];
}

// ── Physics Validation (cross-reference with plans/ documents) ────

/** Cross-coupling angular acceleration: α_cc = ω_hab × ω_head (rad/s²) */
export function computeCrossCoupling(
  omegaHab: number,
  omegaHead: number,
): number {
  return omegaHab * omegaHead;
}

/** Minimum radius from cross-coupling constraint: r = g × ω_head² / α_max² */
export function computeMinRadiusCrossCoupling(
  g: number,
  omegaHead: number,
  alphaMax: number,
): number {
  return (g * omegaHead * omegaHead) / (alphaMax * alphaMax);
}

/** Maximum radius from rim speed constraint: r = v_max² / g */
export function computeMaxRadiusRimSpeed(
  vMax: number,
  g: number,
): number {
  return (vMax * vMax) / g;
}

/** Rim speed: v_rim = sqrt(g * r) */
export function computeRimSpeed(g: number, r: number): number {
  return Math.sqrt(g * r);
}

/** Coriolis ratio: a_cor/g = 2 * v_rel / v_rim */
export function computeCoriolisRatio(vRel: number, vRim: number): number {
  return (2 * vRel) / vRim;
}

/** Gravity gradient: Δg/g = h / r */
export function computeGravityGradient(h: number, r: number): number {
  return h / r;
}

/** Angular velocity for 1g at given radius: ω = sqrt(g/r) */
export function computeOmegaFor1g(r: number, g = 9.807): number {
  return Math.sqrt(g / r);
}

/** RPM from angular velocity: RPM = ω × 30/π */
export function omegaToRPM(omega: number): number {
  return omega * 30 / Math.PI;
}

/** Check if a point (in local cylinder coords) is inside the cylinder */
export function isInsideCylinder(
  point: [number, number, number],
  radius: number,
  length: number,
): boolean {
  const [x, y, z] = point;
  const radialDist = Math.sqrt(x * x + z * z);
  return radialDist < radius && Math.abs(y) < length / 2;
}

/**
 * Transform mirror outer vertex to world position (in cylinder local frame).
 * Given: group at (hx, -L/2, hz) with rotation [0, -centerAngle, 0],
 * vertex at (d, d, ±t) in group-local space.
 * After R_Y(-θ): x' = d*cos(-θ) - (±t)*sin(-θ), z' = d*sin(-θ) + (±t)*cos(-θ)  -- wait, wrong
 * R_Y(-θ) applied to (d, d, ±t):
 *   x' = d*cos(θ) + (±t)*sin(θ)   [because R_Y(-θ) has cos(-θ)=cosθ, sin(-θ)=-sinθ]
 *   y' = d
 *   z' = -d*sin(θ) + (±t)*cos(θ)  -- wait, incorrect
 *
 * Actually Three.js R_Y(α):
 *   x' = x*cos(α) + z*sin(α)
 *   y' = y
 *   z' = -x*sin(α) + z*cos(α)
 *
 * For α = -centerAngle:
 *   x' = x*cos(centerAngle) - z*sin(centerAngle)  [cos(-θ)=cosθ, sin(-θ)=-sinθ]
 *   y' = y
 *   z' = x*sin(centerAngle) + z*cos(centerAngle)
 *
 * Then add hinge position offset.
 */
export function computeMirrorTipWorldPosition(
  centerAngle: number,
  radius: number,
  length: number,
): [number, number, number] {
  const d = length; // axialExtent
  const hingeR = radius + HINGE_OFFSET;
  const hx = Math.cos(centerAngle) * hingeR;
  const hz = Math.sin(centerAngle) * hingeR;

  // Outer vertex in group-local: (d, d, 0) — taking center of outer edge
  // Apply R_Y(-centerAngle) to (d, d, 0):
  // x' = d*cos(centerAngle) - 0*sin(centerAngle) = d*cos(centerAngle)
  // y' = d
  // z' = d*sin(centerAngle) + 0*cos(centerAngle) = d*sin(centerAngle)
  const tipLocalX = d * Math.cos(centerAngle);
  const tipLocalY = d;
  const tipLocalZ = d * Math.sin(centerAngle);

  // Add hinge position
  return [
    hx + tipLocalX,
    -length / 2 + tipLocalY, // hinge Y is -length/2
    hz + tipLocalZ,
  ];
}
