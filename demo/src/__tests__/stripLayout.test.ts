import { describe, it, expect } from 'vitest';
import { computeStripAngles, STRIP_ANGLE, STRIP_COUNT, LAND_STRIP_CENTER } from '../lib/sceneGeometry';

describe('O\'Neill strip layout', () => {
  it('produces exactly 6 strips', () => {
    expect(computeStripAngles().length).toBe(STRIP_COUNT);
  });

  it('each strip spans π/3 (60°)', () => {
    const strips = computeStripAngles();
    for (const s of strips) {
      expect(s.arcAngle).toBeCloseTo(Math.PI / 3);
    }
  });

  it('6 strips cover full 2π circle', () => {
    expect(STRIP_COUNT * STRIP_ANGLE).toBeCloseTo(2 * Math.PI);
  });

  it('even indices are land, odd indices are window', () => {
    const strips = computeStripAngles();
    expect(strips[0].type).toBe('land');
    expect(strips[1].type).toBe('window');
    expect(strips[2].type).toBe('land');
    expect(strips[3].type).toBe('window');
    expect(strips[4].type).toBe('land');
    expect(strips[5].type).toBe('window');
  });

  it('start angles are contiguous (no gaps)', () => {
    const strips = computeStripAngles();
    for (let i = 1; i < strips.length; i++) {
      const prevEnd = strips[i - 1].startAngle + strips[i - 1].arcAngle;
      expect(strips[i].startAngle).toBeCloseTo(prevEnd);
    }
  });

  it('first land strip center is at π/6 (30°) = LAND_STRIP_CENTER', () => {
    const strips = computeStripAngles();
    expect(strips[0].centerAngle).toBeCloseTo(LAND_STRIP_CENTER);
    expect(LAND_STRIP_CENTER).toBeCloseTo(Math.PI / 6);
  });

  it('window strip centers at 90°, 210°, 330° with no offset', () => {
    const strips = computeStripAngles();
    const windows = strips.filter(s => s.type === 'window');
    expect(windows[0].centerAngle).toBeCloseTo(Math.PI / 2);      // 90°
    expect(windows[1].centerAngle).toBeCloseTo(7 * Math.PI / 6);  // 210°
    expect(windows[2].centerAngle).toBeCloseTo(11 * Math.PI / 6); // 330°
  });

  it('with π/3 stagger offset, window centers shift by 60°', () => {
    const strips = computeStripAngles(Math.PI / 3);
    const windows = strips.filter(s => s.type === 'window');
    expect(windows[0].centerAngle).toBeCloseTo(Math.PI / 2 + Math.PI / 3);      // 150°
    expect(windows[1].centerAngle).toBeCloseTo(7 * Math.PI / 6 + Math.PI / 3);  // 270°
    expect(windows[2].centerAngle).toBeCloseTo(11 * Math.PI / 6 + Math.PI / 3); // 390° = 30°
  });
});
