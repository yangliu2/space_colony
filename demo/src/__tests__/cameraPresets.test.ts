import { describe, it, expect } from 'vitest';
import { getCameraPresets } from '../lib/sceneGeometry';

describe('camera presets', () => {
  const r = 2;
  const l = 6;
  const presets = getCameraPresets(r, l);

  it('returns exactly 6 presets with correct names', () => {
    expect(presets.length).toBe(6);
    const names = presets.map(p => p.name);
    expect(names).toEqual([
      'Default', 'Side view', 'End view', 'Top-down', 'Close-up rim', 'Full colony',
    ]);
  });

  it('cz = (l + r * 1.5) / 2 is POSITIVE (critical sign bug fix)', () => {
    const cz = (l + r * 1.5) / 2;
    expect(cz).toBeGreaterThan(0);
    // Verify anchor Z is positive in the presets
    const defaultPreset = presets.find(p => p.name === 'Default')!;
    expect(defaultPreset.target[2]).toBeCloseTo(cz);
    expect(defaultPreset.target[2]).toBeGreaterThan(0);
  });

  it('all positions and targets are finite (no NaN/Infinity)', () => {
    for (const p of presets) {
      for (const coord of [...p.position, ...p.target]) {
        expect(Number.isFinite(coord)).toBe(true);
      }
    }
  });

  it('camera position differs from target for every preset', () => {
    for (const p of presets) {
      const dx = p.position[0] - p.target[0];
      const dy = p.position[1] - p.target[1];
      const dz = p.position[2] - p.target[2];
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      expect(dist).toBeGreaterThan(0.1);
    }
  });

  it('Default, End, Top-down target primary cylinder anchor [0, 0, cz]', () => {
    const cz = (l + r * 1.5) / 2;
    for (const name of ['Default', 'End view', 'Top-down']) {
      const preset = presets.find(p => p.name === name)!;
      expect(preset.target[0]).toBeCloseTo(0);
      expect(preset.target[1]).toBeCloseTo(0);
      expect(preset.target[2]).toBeCloseTo(cz);
    }
  });

  it('Full colony targets midpoint between cylinders', () => {
    const sideOffset = r * 2 + l + r;
    const cz = (l + r * 1.5) / 2;
    const fullColony = presets.find(p => p.name === 'Full colony')!;
    expect(fullColony.target[0]).toBeCloseTo(sideOffset / 2);
    expect(fullColony.target[1]).toBeCloseTo(0);
    expect(fullColony.target[2]).toBeCloseTo(cz);
  });
});
