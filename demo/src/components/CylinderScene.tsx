import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls, Text, Html } from "@react-three/drei";
import { useRef, useMemo, useState, useCallback, useImperativeHandle, forwardRef, useEffect } from "react";
import * as THREE from "three";
import type { EvaluateResponse } from "../types/api";
import type { SceneToggles } from "../hooks/useSceneToggles";
import {
  sceneScale,
  getCameraPresets,
  computeInterCylinderSpacing,
  STRIP_ANGLE,
  STAGGER_ANGLE,
  LAND_STRIP_CENTER,
  MIRROR_TANGENT_FRACTION,
  HINGE_OFFSET,
  type CameraPreset,
} from "../lib/sceneGeometry";

// sceneScale and getCameraPresets imported from lib/sceneGeometry.ts
// Re-export for consumers that import from this file
export { sceneScale, getCameraPresets, type CameraPreset };

/* ── O'Neill strips ───────────────────────────────────────────────── */

function LandStrip({
  radius,
  length,
  startAngle,
  arcAngle,
}: {
  radius: number;
  length: number;
  startAngle: number;
  arcAngle: number;
}) {
  const geo = useMemo(() => {
    const r = radius - 0.01;
    const segsArc = 24;
    const segsLen = 1;
    const vertices: number[] = [];
    const indices: number[] = [];
    const uvs: number[] = [];

    for (let j = 0; j <= segsLen; j++) {
      const y = -length / 2 + (length * j) / segsLen;
      for (let i = 0; i <= segsArc; i++) {
        const a = startAngle + (arcAngle * i) / segsArc;
        vertices.push(Math.cos(a) * r, y, Math.sin(a) * r);
        uvs.push(i / segsArc, j / segsLen);
      }
    }

    for (let j = 0; j < segsLen; j++) {
      for (let i = 0; i < segsArc; i++) {
        const a = j * (segsArc + 1) + i;
        const b = a + 1;
        const c = a + segsArc + 1;
        const d = c + 1;
        indices.push(a, b, d, a, d, c);
      }
    }

    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
    g.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
    g.setIndex(indices);
    g.computeVertexNormals();
    return g;
  }, [radius, length, startAngle, arcAngle]);

  return (
    <mesh geometry={geo}>
      <meshStandardMaterial
        color="#4ade80"
        side={THREE.DoubleSide}
        transparent
        opacity={0.7}
        emissive="#1a5c2a"
        emissiveIntensity={0.3}
      />
    </mesh>
  );
}

function WindowStrip({
  radius,
  length,
  startAngle,
  arcAngle,
}: {
  radius: number;
  length: number;
  startAngle: number;
  arcAngle: number;
}) {
  const geo = useMemo(() => {
    const r = radius - 0.005;
    const segsArc = 24;
    const segsLen = 1;
    const vertices: number[] = [];
    const indices: number[] = [];

    for (let j = 0; j <= segsLen; j++) {
      const y = -length / 2 + (length * j) / segsLen;
      for (let i = 0; i <= segsArc; i++) {
        const a = startAngle + (arcAngle * i) / segsArc;
        vertices.push(Math.cos(a) * r, y, Math.sin(a) * r);
      }
    }

    for (let j = 0; j < segsLen; j++) {
      for (let i = 0; i < segsArc; i++) {
        const a = j * (segsArc + 1) + i;
        const b = a + 1;
        const c = a + segsArc + 1;
        const d = c + 1;
        indices.push(a, b, d, a, d, c);
      }
    }

    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
    g.setIndex(indices);
    g.computeVertexNormals();
    return g;
  }, [radius, length, startAngle, arcAngle]);

  return (
    <mesh geometry={geo}>
      <meshStandardMaterial
        color="#7dd3fc"
        side={THREE.DoubleSide}
        transparent
        opacity={0.3}
        emissive="#0ea5e9"
        emissiveIntensity={0.2}
      />
    </mesh>
  );
}

function ONeillStrips({ radius, length, angleOffset = 0 }: { radius: number; length: number; angleOffset?: number }) {
  const stripAngle = STRIP_ANGLE;
  const strips: JSX.Element[] = [];
  for (let i = 0; i < 6; i++) {
    const start = i * stripAngle + angleOffset;
    if (i % 2 === 0) {
      strips.push(<LandStrip key={`l${i}`} radius={radius} length={length} startAngle={start} arcAngle={stripAngle} />);
    } else {
      strips.push(<WindowStrip key={`w${i}`} radius={radius} length={length} startAngle={start} arcAngle={stripAngle} />);
    }
  }
  return <>{strips}</>;
}

/* ── Tension cables ───────────────────────────────────────────────── */

/** Circumferential tension cables on the exterior — the primary hoop stress carriers. */
function TensionCables({ radius, length }: { radius: number; length: number }) {
  const cables = useMemo(() => {
    const elements: JSX.Element[] = [];
    const cableR = radius + 0.06;
    const numRings = Math.max(6, Math.round(length / 0.8));
    const spacing = length / (numRings + 1);

    // Circumferential cables (hoop direction)
    for (let i = 1; i <= numRings; i++) {
      const y = -length / 2 + spacing * i;
      elements.push(
        <mesh key={`hoop-${i}`} position={[0, y, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[cableR, 0.008, 4, 64]} />
          <meshStandardMaterial color="#f59e0b" transparent opacity={0.6} />
        </mesh>,
      );
    }

    // Longitudinal stringers (6 axial cables connecting hoops)
    for (let i = 0; i < 6; i++) {
      const angle = (i * Math.PI * 2) / 6;
      const x = Math.cos(angle) * cableR;
      const z = Math.sin(angle) * cableR;
      const pts = [new THREE.Vector3(x, -length / 2, z), new THREE.Vector3(x, length / 2, z)];
      const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
      elements.push(
        <lineSegments key={`long-${i}`} geometry={lineGeo}>
          <lineBasicMaterial color="#f59e0b" transparent opacity={0.5} />
        </lineSegments>,
      );
    }

    return elements;
  }, [radius, length]);

  return <>{cables}</>;
}

/* ── External mirrors ─────────────────────────────────────────────── */

/**
 * Three diagonal mirror panels at the anti-sun end — one per window strip.
 *
 * PHYSICS: The cylinder axis points at the sun, so sunlight arrives along
 * -Y (axial). Mirrors MUST be diagonal (45° to axis) to redirect axial
 * light radially inward through the windows.
 *
 * Each mirror is hinged at the anti-sun end (Y = -length/2), centered on
 * a window strip. The panel extends OUTWARD (radially away from axis) and
 * TOWARD THE SUN (+Y) at 45°. Mirror length matches the cylinder length.
 *
 * Group rotation [0, -centerAngle, 0] gives:
 *   +X = (cos θ, 0, sin θ) = radial outward ✓
 *   +Y = (0, 1, 0) = along axis (toward sun)
 *   +Z = (sin θ, 0, -cos θ) = tangential
 *
 *   THREE.JS ROTATION MATH:
 *   R_Y(α) maps +X to (cos α, 0, -sin α).
 *   For +X = radial outward (cos θ, 0, sin θ):
 *     cos α = cos θ  →  α = -θ
 *     -sin α = sin θ →  α = -θ  ✓
 *   So α = -centerAngle. Using +centerAngle flips the Z and sends
 *   the mirror INWARD — that was the bug.
 *
 * Mesh rotation [-PI/2, 0, PI/4] on planeGeometry gives:
 *   Width  → local (0.707, 0.707, 0) = diagonal (radial out + toward sun)
 *   Height → local (0, 0, -1)        = tangential
 *   Normal → local (-0.707, 0.707, 0)
 *
 * Reflection: d=(0,-1,0), n=(-0.707,0.707,0), r=(-1,0,0) → radial inward ✓
 *
 * See plans/mirror_geometry.md for full derivation and diagrams.
 */
function ExternalMirrors({ radius, length, angleOffset = 0 }: { radius: number; length: number; angleOffset?: number }) {
  const stripAngle = STRIP_ANGLE; // 60° per strip

  // Mirror axial extent = full cylinder length. At 45°, radial extent = same.
  const mirrorAxialExtent = length;
  // Tangential width: window strip chord ≈ R. Use 85% to avoid land overlap.
  const mirrorTangent = radius * 0.85;

  // Custom quad geometry — NO Euler rotation, explicit vertex positions.
  // In group-local coords: +X = radial outward, +Y = toward sun, +Z = tangential
  const mirrorGeo = useMemo(() => {
    const t = mirrorTangent / 2;
    const d = mirrorAxialExtent;
    // Four corners of the mirror rectangle:
    //   Inner edge at hinge: (0, 0, ±t) — on cylinder surface, tangential span
    //   Outer edge: (d, d, ±t) — d radially outward AND d toward sun = 45°
    const vertices = new Float32Array([
      0, 0, -t,   // 0: hinge, tangential -
      0, 0,  t,   // 1: hinge, tangential +
      d, d, -t,   // 2: outer, tangential -
      d, d,  t,   // 3: outer, tangential +
    ]);
    const indices = [0, 1, 3, 0, 3, 2];
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
    g.setIndex(indices);
    g.computeVertexNormals();
    return g;
  }, [mirrorAxialExtent, mirrorTangent]);

  const mirrors = useMemo(() => {
    const elements: JSX.Element[] = [];

    for (let i = 0; i < 3; i++) {
      // Center of each window strip (strips 1, 3, 5), offset by angleOffset
      // Default: 90°, 210°, 330°. With 60° offset: 150°, 270°, 30°.
      const centerAngle = stripAngle * (2 * i + 1) + stripAngle / 2 + angleOffset;
      const hingeR = radius + 0.03;
      const hx = Math.cos(centerAngle) * hingeR;
      const hz = Math.sin(centerAngle) * hingeR;

      elements.push(
        <group
          key={`mirror-${i}`}
          position={[hx, -length / 2, hz]}
          rotation={[0, -centerAngle, 0]}
        >
          {/*
           * Group rotation [0, -θ, 0]:
           *   R_Y(-θ) maps +X → (cos θ, 0, sin θ) = radial outward ✓
           *                +Y → (0, 1, 0) = toward sun ✓
           *                +Z → tangential ✓
           *
           * Mirror geometry has vertices directly at correct positions:
           *   Inner edge: (0, 0, ±t) = at hinge, tangential span
           *   Outer edge: (d, d, ±t) = outward+sunward at 45°
           *   No mesh rotation needed — geometry IS the diagonal.
           */}
          <mesh geometry={mirrorGeo}>
            <meshStandardMaterial
              color="#ffffff"
              emissive="#cccccc"
              emissiveIntensity={0.5}
              metalness={0.95}
              roughness={0.05}
              side={THREE.DoubleSide}
              transparent
              opacity={0.75}
            />
          </mesh>
          {/* Hinge rod — tangential, same span as mirror inner edge */}
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <cylinderGeometry args={[0.025, 0.025, mirrorTangent, 6]} />
            <meshStandardMaterial color="#ff6600" metalness={0.6} roughness={0.3} />
          </mesh>
        </group>,
      );
    }
    return elements;
  }, [radius, length, stripAngle, mirrorGeo, mirrorTangent]);

  return <>{mirrors}</>;
}

/* ── Counter-rotating pair ────────────────────────────────────────── */

/**
 * Second cylinder + bearing connection — cancels angular momentum.
 *
 * O'Neill's design: two cylinders sit SIDE BY SIDE (parallel), offset in the
 * radial direction (X axis in local coords). They rotate in opposite directions
 * and are connected by bearing frameworks at both ends.
 */
function CounterRotatingPair({
  radius,
  length,
  omegaRadS,
  feasible,
  toggles,
}: {
  radius: number;
  length: number;
  omegaRadS: number;
  feasible: boolean;
  toggles: SceneToggles;
}) {
  // Side-by-side: offset in X (radial direction), NOT along Y (axis)
  // With 60° stagger, mirror fans interleave — gap reduced to ~R + L (not 2L).
  // At 45° tilt, each mirror extends L radially. With staggering, the worst-case
  // overlap direction is sin(30°) × L = L/2 per side, so gap > L + R suffices.
  const mirrorRadialExtent = length; // at 45°, radial extent = axial extent
  const staggerAngle = STAGGER_ANGLE; // 60° rotational offset between cylinders
  const gap = mirrorRadialExtent + radius; // staggered: roughly halved from 2L+R
  const sideOffset = radius * 2 + gap; // center-to-center distance in X

  const color = feasible ? "#22c55e" : "#ef4444";

  return (
    <>
      {/* Bearing connection frameworks at both ends — non-rotating */}
      {toggles.showBearing && (
        <>
          {[-1, 1].map((endSign) => {
            const endY = endSign * length / 2;
            return (
              <group key={`bearing-${endSign}`} position={[0, endY, 0]}>
                {/* Cross-struts connecting the two cylinders */}
                {[0, 1, 2].map((i) => {
                  const frac = (i + 1) / 4;
                  const strutX = sideOffset * frac;
                  const strutZ = 0;
                  return (
                    <mesh
                      key={`strut-${i}`}
                      position={[strutX, 0, strutZ]}
                      rotation={[0, 0, Math.PI / 2]}
                    >
                      <cylinderGeometry args={[0.025, 0.025, sideOffset * 0.25, 6]} />
                      <meshStandardMaterial
                        color="#b0bec5"
                        metalness={0.8}
                        roughness={0.3}
                        opacity={0.9}
                        transparent
                      />
                    </mesh>
                  );
                })}
                {/* Bearing ring between cylinders */}
                <mesh
                  position={[sideOffset / 2, 0, 0]}
                  rotation={[0, 0, Math.PI / 2]}
                >
                  <torusGeometry args={[radius * 0.2, 0.02, 8, 24]} />
                  <meshStandardMaterial
                    color="#cfd8dc"
                    metalness={0.85}
                    roughness={0.2}
                  />
                </mesh>
              </group>
            );
          })}
        </>
      )}
      {/* Second cylinder — offset in X (side by side) */}
      <group position={[sideOffset, 0, 0]}>
        {/* Everything on the second cylinder counter-rotates together */}
        <RotatingGroup omegaRadS={omegaRadS} direction={-1}>
          <mesh>
            <cylinderGeometry args={[radius, radius, length, 48, 4, true]} />
            <meshBasicMaterial color={color} wireframe transparent opacity={toggles.showStrips ? 0.12 : 0.3} />
          </mesh>
          {!toggles.showStrips && (
            <mesh>
              <cylinderGeometry args={[radius, radius, length, 48, 1, true]} />
              <meshStandardMaterial color={color} side={THREE.DoubleSide} transparent opacity={0.15} />
            </mesh>
          )}
          {toggles.showStrips && <ONeillStrips radius={radius} length={length} angleOffset={staggerAngle} />}
          {toggles.showMirrors && <ExternalMirrors radius={radius} length={length} angleOffset={staggerAngle} />}
          {toggles.showEndCaps && <EndCaps radius={radius} length={length} />}
          {toggles.showCables && <TensionCables radius={radius} length={length} />}
          {toggles.showAgriculture && (
            <AgriculturePods radius={radius} length={length} />
          )}
          {toggles.showInteriorZones && <InteriorZones radius={radius} length={length} />}
        </RotatingGroup>
      </group>
    </>
  );
}

/* ── Agriculture pods ─────────────────────────────────────────────── */

/**
 * External agriculture modules near the OUTER end cap only.
 * The inner end cap faces the counter-rotating pair bearing — no room for pods.
 */
function AgriculturePods({ radius, length }: { radius: number; length: number }) {
  const pods = useMemo(() => {
    const elements: JSX.Element[] = [];
    const numPods = 6;
    const podR = radius * 0.15;
    const podLen = radius * 0.4;
    const ringR = radius * 0.7;

    // Only the outer end (negative Y = away from bearing)
    const yBase = -length / 2 - podLen * 0.6;
    for (let i = 0; i < numPods; i++) {
      const angle = (i * Math.PI * 2) / numPods;
      const x = Math.cos(angle) * ringR;
      const z = Math.sin(angle) * ringR;
      elements.push(
        <group key={`pod-${i}`} position={[x, yBase, z]}>
          <mesh>
            <capsuleGeometry args={[podR, podLen * 0.5, 8, 12]} />
            <meshStandardMaterial
              color="#16a34a"
              transparent
              opacity={0.35}
              emissive="#15803d"
              emissiveIntensity={0.15}
            />
          </mesh>
          <mesh position={[0, podLen * 0.35, 0]}>
            <sphereGeometry args={[podR * 0.8, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2]} />
            <meshStandardMaterial
              color="#86efac"
              transparent
              opacity={0.2}
              side={THREE.DoubleSide}
            />
          </mesh>
        </group>,
      );
    }

    // Connecting ring at outer end
    elements.push(
      <mesh key="ring" position={[0, -length / 2 - 0.1, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[ringR, 0.02, 4, 48]} />
        <meshStandardMaterial color="#22c55e" transparent opacity={0.4} />
      </mesh>,
    );

    return elements;
  }, [radius, length]);

  return <>{pods}</>;
}

/* ── Mid-zone / axial infrastructure ──────────────────────────────── */

/** Interior zones: mid-zone industry ring, axial spine, radial elevators, docking ports. */
function InteriorZones({ radius, length }: { radius: number; length: number }) {
  const elements = useMemo(() => {
    const items: JSX.Element[] = [];

    // Axial spine — structural tube along rotation axis
    items.push(
      <mesh key="spine">
        <cylinderGeometry args={[0.04, 0.04, length * 1.1, 8]} />
        <meshStandardMaterial color="#818cf8" transparent opacity={0.5} />
      </mesh>,
    );

    // Docking ports at each end
    for (let end = 0; end < 2; end++) {
      const yPort = end === 0 ? -length / 2 - 0.15 : length / 2 + 0.15;
      items.push(
        <group key={`dock-${end}`} position={[0, yPort, 0]}>
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <torusGeometry args={[0.12, 0.02, 6, 16]} />
            <meshStandardMaterial color="#c084fc" transparent opacity={0.6} />
          </mesh>
          <Text
            position={[0.25, 0, 0]}
            fontSize={0.1}
            color="#c084fc"
            anchorX="left"
          >
            Dock
          </Text>
        </group>,
      );
    }

    // Radial elevator shafts — 6 lines from axis to rim
    for (let i = 0; i < 6; i++) {
      const angle = (i * Math.PI * 2) / 6;
      const xR = Math.cos(angle) * radius * 0.95;
      const zR = Math.sin(angle) * radius * 0.95;
      const pts = [new THREE.Vector3(0, 0, 0), new THREE.Vector3(xR, 0, zR)];
      const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
      items.push(
        <lineSegments key={`elev-${i}`} geometry={lineGeo}>
          <lineBasicMaterial color="#a78bfa" transparent opacity={0.3} />
        </lineSegments>,
      );
    }

    // Mid-zone industry ring at 0.5r
    const midR = radius * 0.5;
    items.push(
      <mesh key="mid-ring" rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[midR, 0.03, 6, 48]} />
        <meshStandardMaterial color="#fbbf24" transparent opacity={0.4} />
      </mesh>,
    );
    items.push(
      <Text key="mid-label" position={[midR + 0.2, 0, 0]} fontSize={0.1} color="#fbbf24" anchorX="left">
        Mid-zone (0.5g)
      </Text>,
    );

    // Zero-g recreation zone indicator near axis
    items.push(
      <mesh key="zero-g" rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[radius * 0.1, 0.02, 6, 24]} />
        <meshStandardMaterial color="#38bdf8" transparent opacity={0.4} />
      </mesh>,
    );
    items.push(
      <Text key="zero-g-label" position={[radius * 0.1 + 0.15, 0.1, 0]} fontSize={0.08} color="#38bdf8" anchorX="left">
        Zero-g zone
      </Text>,
    );

    return items;
  }, [radius, length]);

  return <>{elements}</>;
}

/* ── Existing components (updated) ────────────────────────────────── */

/** Rotating group wrapper — applies rotation animation to all children. */
function RotatingGroup({
  omegaRadS,
  direction = 1,
  children,
}: {
  omegaRadS: number;
  direction?: number;
  children: React.ReactNode;
}) {
  const ref = useRef<THREE.Group>(null);
  useFrame((_, delta) => {
    if (ref.current) {
      ref.current.rotation.y += direction * omegaRadS * delta * 10;
    }
  });
  return <group ref={ref}>{children}</group>;
}

function CylinderShell({
  radius,
  length,
  feasible,
  showStrips,
  showMirrors,
}: {
  radius: number;
  length: number;
  feasible: boolean;
  showStrips: boolean;
  showMirrors: boolean;
}) {
  const color = feasible ? "#22c55e" : "#ef4444";

  return (
    <>
      <mesh>
        <cylinderGeometry args={[radius, radius, length, 48, 4, true]} />
        <meshBasicMaterial color={color} wireframe transparent opacity={showStrips ? 0.12 : 0.3} />
      </mesh>
      {!showStrips && (
        <mesh>
          <cylinderGeometry args={[radius, radius, length, 48, 1, true]} />
          <meshStandardMaterial color={color} side={THREE.DoubleSide} transparent opacity={0.15} />
        </mesh>
      )}
      {showStrips && <ONeillStrips radius={radius} length={length} />}
      {/* Mirrors co-rotate with the hull — they're physically attached */}
      {showMirrors && <ExternalMirrors radius={radius} length={length} />}
    </>
  );
}

function EndCaps({ radius, length }: { radius: number; length: number }) {
  const hemiDepth = radius * 0.3; // how far the hemisphere bulges outward
  return (
    <>
      {[1, -1].map((sign, i) => (
        <group key={i} position={[0, sign * length / 2, 0]}>
          {/* Hemisphere — sphereGeometry with phiStart/phiLength for half sphere */}
          <mesh
            scale={[1, hemiDepth / radius, 1]}
            rotation={[sign > 0 ? 0 : Math.PI, 0, 0]}
          >
            <sphereGeometry args={[radius, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2]} />
            <meshStandardMaterial
              color="#334155"
              transparent
              opacity={0.3}
              side={THREE.DoubleSide}
            />
          </mesh>
          {/* Wireframe overlay */}
          <mesh
            scale={[1, hemiDepth / radius, 1]}
            rotation={[sign > 0 ? 0 : Math.PI, 0, 0]}
          >
            <sphereGeometry args={[radius * 1.001, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2]} />
            <meshBasicMaterial color="#475569" wireframe transparent opacity={0.3} />
          </mesh>
        </group>
      ))}
    </>
  );
}

/*
 * ── COORDINATE SYSTEM (inside the rotation group) ──────────────
 *
 *   Y = cylinder long axis (rotation axis)
 *   XZ = radial cross-section plane
 *   Rim point at angle 0:  [radius, 0, 0]
 *   "Up" from that rim point (toward center):  -X direction
 *
 *   cylinderGeometry: height along Y, circles in XZ  ✓
 *   capsuleGeometry: tall along Y
 *   ringGeometry / planeGeometry: in XY plane
 * ────────────────────────────────────────────────────────────────
 */

/** Human standing on inner rim at [radius, 0, 0]. Head points toward -X (center). */
// LAND_STRIP_CENTER imported from lib/sceneGeometry.ts

function HumanFigure({ radius, coriolisRatio }: { radius: number; coriolisRatio: number }) {
  const ref = useRef<THREE.Group>(null);
  const h = Math.max(radius * 0.15, 0.2);
  const lean = Math.min(coriolisRatio * 0.5, 0.08);

  useFrame(() => {
    if (ref.current) {
      ref.current.rotation.y = lean;
    }
  });

  // Place on the center of a land strip. First rotate the whole assembly to
  // the land strip angle, then position at [radius, 0, 0] (angle-0 in the
  // rotated frame), with capsule standing radially inward.
  return (
    <group rotation={[0, -LAND_STRIP_CENTER, 0]}>
      <group ref={ref} position={[radius, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
        <mesh position={[0, h * 0.3, 0]}>
          <capsuleGeometry args={[h * 0.08, h * 0.45, 4, 8]} />
          <meshStandardMaterial color="#e2e8f0" />
        </mesh>
        <mesh position={[0, h * 0.68, 0]}>
          <sphereGeometry args={[h * 0.12, 12, 12]} />
          <meshStandardMaterial color="#fbbf24" />
        </mesh>
        <Text position={[0, h * 0.9, 0]} fontSize={h * 0.18} color="#94a3b8" anchorX="center" anchorY="bottom">
          1.8 m
        </Text>
      </group>
    </group>
  );
}

/** Coriolis arrow at rim surface, pointing along +Y (prograde / long axis).
 *  Placed on the same land strip as the human figure. */
function CoriolisArrow({ radius, ratio }: { radius: number; ratio: number }) {
  if (ratio < 0.01) return null;
  const arrowLen = Math.min(ratio * radius * 4, radius * 0.6);

  return (
    <group rotation={[0, -LAND_STRIP_CENTER, 0]}>
      <group position={[radius - 0.15, 0, 0]}>
        <arrowHelper args={[new THREE.Vector3(0, 1, 0), new THREE.Vector3(0, 0, 0), arrowLen, 0xf97316, arrowLen * 0.25, arrowLen * 0.12]} />
        <Text position={[0, arrowLen + 0.15, 0]} fontSize={0.15} color="#f97316" anchorX="center">
          Coriolis
        </Text>
      </group>
    </group>
  );
}

/** Gravity gradient rings in XZ plane (perpendicular to long axis). */
function GravityRings({ radius }: { radius: number }) {
  const rings = useMemo(() => {
    const arr: JSX.Element[] = [];
    const steps = 4;
    for (let i = 1; i <= steps; i++) {
      const r = radius * (i / steps);
      const opacity = 0.04 + (i / steps) * 0.08;
      // ringGeometry is in XY by default; rotate PI/2 around X to put in XZ
      arr.push(
        <mesh key={i} rotation={[Math.PI / 2, 0, 0]}>
          <ringGeometry args={[r - 0.02, r + 0.02, 48]} />
          <meshBasicMaterial color="#818cf8" side={THREE.DoubleSide} transparent opacity={opacity} />
        </mesh>,
      );
    }
    return arr;
  }, [radius]);

  return <>{rings}</>;
}

/** Rotation axis arrow along Y (cylinder long axis). */
function Axis({ length }: { length: number }) {
  const halfL = length * 0.6;
  return (
    <group>
      <arrowHelper args={[new THREE.Vector3(0, 1, 0), new THREE.Vector3(0, -halfL, 0), halfL * 2, 0x475569, 0.15, 0.08]} />
      <Text position={[0.2, halfL + 0.2, 0]} fontSize={0.15} color="#64748b" anchorX="center">
        rotation axis
      </Text>
    </group>
  );
}

/** Gravity label just outside the rim at [radius+offset, 0, 0]. */
function GravityLabel({ radius, gravity }: { radius: number; gravity: number }) {
  return (
    <Text position={[radius + 0.3, 0, 0]} fontSize={0.18} color="#22c55e" anchorX="center">
      {gravity.toFixed(2)}g
    </Text>
  );
}

/* ── Camera controller for preset views ───────────────────────────── */
// CameraPreset and getCameraPresets imported from lib/sceneGeometry.ts

export interface CameraControlHandle {
  goToPreset: (preset: CameraPreset) => void;
}

const CAMERA_STORAGE_KEY = "habitat-camera-state";

interface CameraState {
  position: [number, number, number];
  target: [number, number, number];
}

function saveCameraState(state: CameraState) {
  localStorage.setItem(CAMERA_STORAGE_KEY, JSON.stringify(state));
}

function loadCameraState(): CameraState | null {
  try {
    const raw = localStorage.getItem(CAMERA_STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    // ignore
  }
  return null;
}

const CameraController = forwardRef<CameraControlHandle>(function CameraController(_, ref) {
  const { camera } = useThree();
  const controlsRef = useRef<any>(null);
  const skipNextSave = useRef(false);

  // Restore saved camera state on mount
  useEffect(() => {
    const saved = loadCameraState();
    if (saved) {
      camera.position.set(...saved.position);
      if (controlsRef.current) {
        controlsRef.current.target.set(...saved.target);
        controlsRef.current.update();
      }
    }
  }, [camera]);

  // Listen for camera changes from other tabs
  useEffect(() => {
    const handler = (e: StorageEvent) => {
      if (e.key === CAMERA_STORAGE_KEY && e.newValue) {
        const state: CameraState = JSON.parse(e.newValue);
        skipNextSave.current = true;
        camera.position.set(...state.position);
        if (controlsRef.current) {
          controlsRef.current.target.set(...state.target);
          controlsRef.current.update();
        }
      }
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, [camera]);

  // Persist camera state on each frame (throttled)
  const lastSave = useRef(0);
  useFrame(() => {
    if (skipNextSave.current) {
      skipNextSave.current = false;
      return;
    }
    const now = performance.now();
    if (now - lastSave.current < 300) return;
    lastSave.current = now;
    const target = controlsRef.current?.target;
    if (!target) return;
    saveCameraState({
      position: [camera.position.x, camera.position.y, camera.position.z],
      target: [target.x, target.y, target.z],
    });
  });

  const goToPreset = useCallback(
    (preset: CameraPreset) => {
      camera.position.set(...preset.position);
      if (controlsRef.current) {
        controlsRef.current.target.set(...preset.target);
        controlsRef.current.update();
      }
      saveCameraState({ position: preset.position, target: preset.target });
    },
    [camera],
  );

  useImperativeHandle(ref, () => ({ goToPreset }), [goToPreset]);

  return <OrbitControls ref={controlsRef} enableDamping dampingFactor={0.1} minDistance={0.5} maxDistance={200} />;
});

/* ── Viewpoint hotspots (Google Maps-style) ───────────────────────── */

interface HotspotDef {
  id: string;
  /** Position in the local (pre-flip) coordinate system: Y = cylinder long axis */
  localPos: [number, number, number];
  label: string;
  description: string;
  icon: string;
  promptFile: string;
  /** Optional path to AI-generated viewpoint image in /viewpoints/ */
  image?: string;
}

function getHotspots(r: number, l: number): HotspotDef[] {
  return [
    {
      id: "rim-surface",
      localPos: [r * 0.7, 0, r * 0.7],
      label: "Standing on the rim",
      description:
        "Looking along the inner surface at 1g. Land strips curve upward on both sides. Through the window strips, you see reflected sunlight (day) or stars (night).",
      icon: "👤",
      promptFile: "01_rim_surface.md",
      image: "/viewpoints/rim_surface.png",
    },
    {
      id: "window-view",
      localPos: [0, l * 0.3, r * 0.95],
      label: "Window strip view",
      description:
        "Looking outward through a transparent window panel. External mirrors reflect sunlight inward. Cable mesh is nearly invisible at this distance.",
      icon: "🪟",
      promptFile: "02_window_view.md",
      image: "/viewpoints/window_view_2.png",
    },
    {
      id: "axis-zerog",
      localPos: [0, 0, 0],
      label: "Zero-g axis",
      description:
        "Floating at the rotation axis. Weightless zone for recreation (human-powered flight!) and zero-g manufacturing. Docking ports at each end.",
      icon: "🚀",
      promptFile: "03_zero_g_axis.md",
      image: "/viewpoints/zero_g_axis.png",
    },
    {
      id: "mid-zone",
      localPos: [r * 0.5, 0, 0],
      label: "Mid-zone (0.5g)",
      description:
        "Industry and services zone at half gravity. Easier material handling, medical rehabilitation facilities, water reservoirs.",
      icon: "🏭",
      promptFile: "04_mid_zone.md",
      image: "/viewpoints/mid_zone.png",
    },
    {
      id: "endcap",
      localPos: [0, l * 0.48, 0],
      label: "End cap & docking",
      description:
        "Hemispherical end cap with docking port. Spacecraft arrive along the rotation axis where relative velocity is minimal. Agriculture pods visible nearby.",
      icon: "🛸",
      promptFile: "05_end_cap.md",
      image: "/viewpoints/end_cap.png",
    },
    {
      id: "looking-up",
      localPos: [0, -l * 0.2, -(r * 0.85)],
      label: "Looking up from surface",
      description:
        "The iconic O'Neill view: looking 'up' you see the opposite land strip curving overhead ~2 km away. Between land strips, window strips show sky/space.",
      icon: "👀",
      promptFile: "06_looking_up.md",
      image: "/viewpoints/looking_up.png",
    },
    {
      id: "mirror-daylight",
      localPos: [r * 0.5, l * 0.3, r * 0.75],
      label: "Mirror daylight",
      description:
        "Simulated sunrise: an external mirror pivots open, reflecting sunlight through the window strip. Golden light floods the land strip as the 2 km-long mirror gradually tilts to full 45°.",
      icon: "☀️",
      promptFile: "08_mirror_daylight.md",
      image: "/viewpoints/mirror_daylight.png",
    },
  ];
}

/** A clickable hotspot marker that expands to show a description overlay. */
function Hotspot({ def }: { def: HotspotDef }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <group position={def.localPos}>
      {/* Pulsing sphere marker */}
      <mesh onClick={() => setExpanded(!expanded)}>
        <sphereGeometry args={[0.08, 12, 12]} />
        <meshBasicMaterial color="#fbbf24" transparent opacity={0.8} />
      </mesh>
      {/* Outer ring */}
      <mesh onClick={() => setExpanded(!expanded)}>
        <ringGeometry args={[0.1, 0.13, 16]} />
        <meshBasicMaterial color="#fbbf24" transparent opacity={0.5} side={THREE.DoubleSide} />
      </mesh>
      {/* Always-visible icon label */}
      <Html center distanceFactor={8} style={{ pointerEvents: "none" }}>
        <div
          style={{
            fontSize: "18px",
            cursor: "pointer",
            userSelect: "none",
            textShadow: "0 0 6px rgba(0,0,0,0.8)",
          }}
        >
          {def.icon}
        </div>
      </Html>
      {/* Expanded info card */}
      {expanded && (
        <Html center distanceFactor={6}>
          <div className="hotspot-card">
            <div className="hotspot-title">{def.icon} {def.label}</div>
            {def.image && (
              <div className="hotspot-image-wrap">
                <img
                  src={def.image}
                  alt={def.label}
                  className="hotspot-image"
                  onClick={(e) => {
                    e.stopPropagation();
                    window.open(def.image, "_blank");
                  }}
                />
              </div>
            )}
            <div className="hotspot-desc">{def.description}</div>
            <div className="hotspot-actions">
              {def.image && (
                <span
                  className="hotspot-prompt-link"
                  onClick={(e) => {
                    e.stopPropagation();
                    window.open(def.image, "_blank");
                  }}
                >
                  🖼 View full image
                </span>
              )}
              {!def.image && (
                <span className="hotspot-prompt-link" style={{ opacity: 0.5 }}>
                  📷 No image yet
                </span>
              )}
              <span
                className="hotspot-close"
                onClick={(e) => { e.stopPropagation(); setExpanded(false); }}
              >
                ✕
              </span>
            </div>
          </div>
        </Html>
      )}
    </group>
  );
}

/** All viewpoint hotspots. */
function ViewpointHotspots({ radius, length }: { radius: number; length: number }) {
  const hotspots = useMemo(() => getHotspots(radius, length), [radius, length]);
  return (
    <>
      {hotspots.map((h) => (
        <Hotspot key={h.id} def={h} />
      ))}
    </>
  );
}

/* ── Interior lighting ────────────────────────────────────────────── */

/** Warm interior point lights simulating reflected sunlight through windows. */
function InteriorLighting({ radius, length }: { radius: number; length: number }) {
  return (
    <>
      {/* Central warm light simulating reflected sunlight */}
      <pointLight position={[0, 0, 0]} intensity={0.6} color="#fff5e6" distance={radius * 3} />
      {/* Three lights near each window strip to simulate mirror-reflected sunlight */}
      {[0, 1, 2].map((i) => {
        const angle = (Math.PI / 3) * (2 * i + 1) + Math.PI / 6;
        const x = Math.cos(angle) * radius * 0.4;
        const z = Math.sin(angle) * radius * 0.4;
        return (
          <pointLight
            key={`win-light-${i}`}
            position={[x, 0, z]}
            intensity={0.3}
            color="#ffe4b5"
            distance={radius * 2}
          />
        );
      })}
      {/* Soft fill lights at each end */}
      <pointLight position={[0, length * 0.4, 0]} intensity={0.2} color="#e0e7ff" distance={radius * 2} />
      <pointLight position={[0, -length * 0.4, 0]} intensity={0.2} color="#e0e7ff" distance={radius * 2} />
    </>
  );
}

/* ── Main scene ───────────────────────────────────────────────────── */

interface Props {
  radiusM: number;
  lengthM: number;
  omegaRadS: number;
  result: EvaluateResponse | null;
  toggles: SceneToggles;
  fullPage?: boolean;
  cameraRef?: React.RefObject<CameraControlHandle | null>;
}

export default function CylinderScene({
  radiusM,
  lengthM,
  omegaRadS,
  result,
  toggles,
  fullPage,
  cameraRef,
}: Props) {
  const { r, l } = sceneScale(radiusM, lengthM);
  const feasible = result?.all_feasible ?? true;
  const gravity = result?.gravity_g ?? 1.0;

  const coriolisRatio =
    result?.constraints.find((c) => c.name === "coriolis")?.details
      .coriolis_to_gravity_running ?? 0;

  const wrapperClass = fullPage ? "scene-fullpage" : "panel scene-panel";

  return (
    <div className={wrapperClass}>
      <div className="scene-header">
        <h2>3D Habitat</h2>
        {!fullPage && (
          <a href="/3d" className="fullpage-link" target="_blank" rel="noopener">
            Full view &rarr;
          </a>
        )}
      </div>
      <Canvas
        camera={{ position: [4, 3, 6], fov: 45, near: 0.05, far: 500 }}
        style={{ height: fullPage ? "100%" : 400 }}
      >
        <color attach="background" args={["#0f0f1a"]} />
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={0.8} />
        <directionalLight position={[-3, -2, -3]} intensity={0.3} />

        {/* Scene: group flips from Y-axis to Z-axis, centered on bearing link */}
        <group rotation={[-Math.PI / 2, 0, 0]}>
        <group position={[0, -(l + r * 1.5) / 2, 0]}>

          {/* Primary cylinder — everything physically attached rotates together */}
          <RotatingGroup omegaRadS={omegaRadS}>
            <CylinderShell
              radius={r}
              length={l}
              feasible={feasible}
              showStrips={toggles.showStrips}
              showMirrors={toggles.showMirrors}
            />
            {toggles.showEndCaps && <EndCaps radius={r} length={l} />}
            {toggles.showCables && <TensionCables radius={r} length={l} />}
            {toggles.showAgriculture && <AgriculturePods radius={r} length={l} />}
            {toggles.showInteriorZones && <InteriorZones radius={r} length={l} />}
            {/* Human + Coriolis co-rotate on a land strip */}
            {toggles.showHuman && <HumanFigure radius={r} coriolisRatio={coriolisRatio} />}
            {toggles.showCoriolis && <CoriolisArrow radius={r} ratio={coriolisRatio} />}
          </RotatingGroup>

          {/* Counter-rotating pair (second cylinder + bearing framework) */}
          <CounterRotatingPair
            radius={r}
            length={l}
            omegaRadS={omegaRadS}
            feasible={feasible}
            toggles={toggles}
          />

          {/* Static physics overlays — reference frames that don't rotate */}
          {toggles.showGravityRings && <GravityRings radius={r} />}
          {toggles.showAxis && <Axis length={l} />}
          {toggles.showGravityLabel && <GravityLabel radius={r} gravity={gravity} />}
          {toggles.showHotspots && <ViewpointHotspots radius={r} length={l} />}
          {toggles.showInteriorLighting && <InteriorLighting radius={r} length={l} />}

        </group>
        </group>

        <CameraController ref={cameraRef} />
      </Canvas>
    </div>
  );
}
