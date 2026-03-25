# AI Image Generation Prompts

Constraint-accurate prompts for generating visualizations of the O'Neill cylinder
habitat. Each prompt encodes the actual physics and geometry from our model.

## Design Parameters (Minimum Viable Cylinder)

| Parameter | Value |
|-----------|-------|
| Radius | 982 m |
| Diameter | 1,964 m |
| Length | 2,000 m |
| Gravity | 1.0g at rim |
| RPM | ~0.96 (one rotation every ~62 seconds) |
| Population | ~8,000 |
| Land strip width | ~1,028 m (60° arc) |
| Window strip width | ~1,028 m (60° arc) |
| Strips | 3 land (green) + 3 window (transparent), alternating |
| Atmosphere | Earth-normal (101.3 kPa) |
| Interior surface | ~12.3 km² (livable area) |

## Usage

1. Copy the prompt text from any `.md` file in this folder
2. Paste into your preferred AI image generator (Midjourney, DALL-E 3, etc.)
3. For Midjourney, append `--ar 16:9 --v 6` for widescreen
4. For DALL-E 3, the prompts work as-is
5. Save generated images to `demo/public/viewpoints/` and they will be
   linked from the 3D hotspot cards

## Viewpoints

| File | Hotspot | Description |
|------|---------|-------------|
| `01_rim_surface.md` | 👤 Standing on the rim | First-person view on the inner surface |
| `02_window_view.md` | 🪟 Window strip view | Looking outward through transparent panel |
| `03_zero_g_axis.md` | 🚀 Zero-g axis | Floating weightless at the rotation center |
| `04_mid_zone.md` | 🏭 Mid-zone industry | Half-gravity industrial/services area |
| `05_end_cap.md` | 🛸 End cap & docking | Spacecraft arrival at the rotation axis |
| `06_looking_up.md` | 👀 Looking up from surface | The iconic O'Neill overhead landscape view |
| `07_exterior.md` | — | External view of the full colony in space (no hotspot — hard to get physics right with image generation) |
| `08_mirror_daylight.md` | ☀️ Mirror daylight | Mirrors reflecting sunlight through windows |
