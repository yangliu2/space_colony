import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Text } from "@react-three/drei";
import { useRef, useMemo } from "react";
import * as THREE from "three";
import type { EvaluateResponse } from "../types/api";
import type { SceneToggles } from "../hooks/useSceneToggles";

/**
 * Normalize real-world meters to scene units.
 * Radius maps to ~2 scene units; length capped for readability.
 */
function sceneScale(radius_m: number, length_m: number) {
  const targetR = 2;
  const s = targetR / radius_m;
  const r = targetR;
  const rawL = length_m * s;
  const l = Math.min(rawL, r * 6);
  return { r, l, s };
}

/**
 * Curved strip on the inner cylinder wall.
 * Three.js cylinderGeometry vertices: (cos*r, y, sin*r)
 * So our strips must use the same convention: X=cos*r, Y=height, Z=sin*r
 */
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
        color="#2d6a2e"
        side={THREE.DoubleSide}
        transparent
        opacity={0.55}
      />
    </mesh>
  );
}

/** Window strip — transparent/glass panel. */
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
        color="#87ceeb"
        side={THREE.DoubleSide}
        transparent
        opacity={0.12}
      />
    </mesh>
  );
}

/** O'Neill 3-land + 3-window pattern. */
function ONeillStrips({ radius, length }: { radius: number; length: number }) {
  const stripAngle = Math.PI / 3;
  const strips: JSX.Element[] = [];
  for (let i = 0; i < 6; i++) {
    const start = i * stripAngle;
    if (i % 2 === 0) {
      strips.push(<LandStrip key={`l${i}`} radius={radius} length={length} startAngle={start} arcAngle={stripAngle} />);
    } else {
      strips.push(<WindowStrip key={`w${i}`} radius={radius} length={length} startAngle={start} arcAngle={stripAngle} />);
    }
  }
  return <>{strips}</>;
}

/** The rotating cylinder. */
function CylinderShell({
  radius,
  length,
  omegaRadS,
  feasible,
  showStrips,
}: {
  radius: number;
  length: number;
  omegaRadS: number;
  feasible: boolean;
  showStrips: boolean;
}) {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((_, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += omegaRadS * delta * 10;
    }
  });

  const color = feasible ? "#22c55e" : "#ef4444";

  return (
    <group ref={groupRef}>
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
    </group>
  );
}

/** End cap discs — positioned along local Y (the cylinder's long axis). */
function EndCaps({ radius, length }: { radius: number; length: number }) {
  return (
    <>
      {[length / 2, -length / 2].map((y, i) => (
        <group key={i} position={[0, y, 0]} rotation={[Math.PI / 2, 0, 0]}>
          <mesh>
            <circleGeometry args={[radius, 48]} />
            <meshStandardMaterial color="#334155" transparent opacity={0.3} side={THREE.DoubleSide} />
          </mesh>
          <mesh>
            <ringGeometry args={[0, radius, 48]} />
            <meshBasicMaterial color="#475569" wireframe transparent opacity={0.3} />
          </mesh>
        </group>
      ))}
    </>
  );
}

/** Stick figure on the inner rim. */
function HumanFigure({ radius, coriolisRatio }: { radius: number; coriolisRatio: number }) {
  const ref = useRef<THREE.Group>(null);
  const h = Math.max(radius * 0.15, 0.2);
  // Lean proportional to Coriolis ratio — subtle, not swinging
  const lean = Math.min(coriolisRatio * 0.5, 0.08);

  useFrame(() => {
    if (ref.current) {
      // Steady lean, not oscillation — represents constant lateral force while walking
      ref.current.rotation.z = lean;
    }
  });

  const y = -(radius - h * 0.55);

  return (
    <group ref={ref} position={[0, y, 0]}>
      <mesh>
        <capsuleGeometry args={[h * 0.08, h * 0.45, 4, 8]} />
        <meshStandardMaterial color="#e2e8f0" />
      </mesh>
      <mesh position={[0, h * 0.38, 0]}>
        <sphereGeometry args={[h * 0.12, 12, 12]} />
        <meshStandardMaterial color="#fbbf24" />
      </mesh>
      <Text position={[0, h * 0.6, 0]} fontSize={h * 0.18} color="#94a3b8" anchorX="center" anchorY="bottom">
        1.8 m
      </Text>
    </group>
  );
}

/** Coriolis force arrow. */
function CoriolisArrow({ radius, ratio }: { radius: number; ratio: number }) {
  if (ratio < 0.01) return null;
  const arrowLen = Math.min(ratio * radius * 4, radius * 0.6);

  return (
    <group position={[0, -(radius - 0.15), 0]}>
      <arrowHelper args={[new THREE.Vector3(0, 0, 1), new THREE.Vector3(0, 0, 0), arrowLen, 0xf97316, arrowLen * 0.25, arrowLen * 0.12]} />
      <Text position={[0, 0.15, arrowLen + 0.1]} fontSize={0.15} color="#f97316" anchorX="center">
        Coriolis
      </Text>
    </group>
  );
}

/** Gravity gradient rings — cross-section showing decreasing g toward center. */
function GravityRings({ radius }: { radius: number }) {
  const rings = useMemo(() => {
    const arr: JSX.Element[] = [];
    const steps = 4;
    for (let i = 1; i <= steps; i++) {
      const r = radius * (i / steps);
      const opacity = 0.04 + (i / steps) * 0.08;
      arr.push(
        <mesh key={i}>
          <ringGeometry args={[r - 0.02, r + 0.02, 48]} />
          <meshBasicMaterial color="#818cf8" side={THREE.DoubleSide} transparent opacity={opacity} />
        </mesh>,
      );
    }
    return arr;
  }, [radius]);

  return <>{rings}</>;
}

/** Rotation axis line along Z. */
function Axis({ length }: { length: number }) {
  const halfL = length * 0.6;
  return (
    <group>
      <arrowHelper args={[new THREE.Vector3(0, 0, 1), new THREE.Vector3(0, 0, -halfL), halfL * 2, 0x475569, 0.15, 0.08]} />
      <Text position={[0, 0.2, halfL + 0.2]} fontSize={0.15} color="#64748b" anchorX="center">
        rotation axis
      </Text>
    </group>
  );
}

/** Gravity label at the rim. */
function GravityLabel({ radius, gravity }: { radius: number; gravity: number }) {
  return (
    <Text position={[0, -(radius + 0.3), 0]} fontSize={0.18} color="#22c55e" anchorX="center">
      {gravity.toFixed(2)}g
    </Text>
  );
}

interface Props {
  radiusM: number;
  lengthM: number;
  omegaRadS: number;
  result: EvaluateResponse | null;
  toggles: SceneToggles;
  fullPage?: boolean;
}

export default function CylinderScene({
  radiusM,
  lengthM,
  omegaRadS,
  result,
  toggles,
  fullPage,
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
        camera={{ position: [4, 3, 6], fov: 45 }}
        style={{ height: fullPage ? "100%" : 400 }}
      >
        <color attach="background" args={["#0f0f1a"]} />
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={0.8} />
        <directionalLight position={[-3, -2, -3]} intensity={0.3} />

        <group rotation={[-Math.PI / 2, 0, 0]}>
          <CylinderShell
            radius={r}
            length={l}
            omegaRadS={omegaRadS}
            feasible={feasible}
            showStrips={toggles.showStrips}
          />
          {toggles.showEndCaps && <EndCaps radius={r} length={l} />}
        </group>

        {toggles.showHuman && <HumanFigure radius={r} coriolisRatio={coriolisRatio} />}
        {toggles.showCoriolis && <CoriolisArrow radius={r} ratio={coriolisRatio} />}
        {toggles.showGravityRings && <GravityRings radius={r} />}
        {toggles.showAxis && <Axis length={l} />}
        {toggles.showGravityLabel && <GravityLabel radius={r} gravity={gravity} />}

        <OrbitControls enableDamping dampingFactor={0.1} minDistance={3} maxDistance={15} />
      </Canvas>
    </div>
  );
}
