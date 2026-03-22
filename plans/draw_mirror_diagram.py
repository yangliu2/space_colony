"""
Generate mirror geometry diagrams for O'Neill cylinder.

PHYSICS RULES — every diagram must follow these:
  1. Light comes from the sun ONLY, along the cylinder axis
  2. Light does NOT pass through mirrors, land strips, or any opaque part
  3. Light ONLY reflects on the mirror's reflective side (one-sided)
  4. Law of reflection: θᵢ = θᵣ, both rays on the SAME side of the surface
  5. Mirror is a flexible reflective surface attached to a hinge on one short side
  6. Hinge is tangent to the window strip, covering the window strip width
  7. Hinge is at the anti-sunlight end of the cylinder
  8. Mirror angle is 0–45° from the tangent plane of the cylinder
  9. The reflective face is the side facing the sun and the window
     (lower-right side in the side view), NOT the side facing away

TEXT RULE — no text may overlap with any other text or diagram element.
  Place labels in clear open space. Use leader lines when needed.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
BG_COLOR = "#1a1a2e"
LAND_COLOR = "#8B7355"
WINDOW_COLOR = "#87CEEB"
MIRROR_COLOR = "white"
SUN_COLOR = "#FFD700"
REFLECT_COLOR = "#FF4500"
NORMAL_COLOR = "#4488ff"
HINGE_COLOR = "#ff6600"
OUTER_COLOR = "#cc0000"


def reflect(d, n):
    """Reflect direction d off surface with outward normal n."""
    d = np.array(d, dtype=float)
    n = np.array(n, dtype=float)
    n = n / np.linalg.norm(n)
    return d - 2 * np.dot(d, n) * n


def draw_arrow(ax, start, end, color, lw=2.5):
    """Draw an arrow from start to end."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    ax.annotate(
        "",
        xy=(end[0], end[1]),
        xytext=(start[0], start[1]),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=14),
        zorder=10,
    )


def draw_light_ray(ax, start, direction, length, color, lw=2.5):
    """Draw a light ray arrow."""
    start = np.array(start, dtype=float)
    direction = np.array(direction, dtype=float)
    end = start + direction * length
    draw_arrow(ax, start, end, color, lw)


def setup_ax(ax):
    """Common axis setup."""
    ax.set_facecolor(BG_COLOR)
    ax.set_aspect("equal")
    ax.axis("off")


# ═══════════════════════════════════════════════════════════════
# FIGURE 1: Law of Reflection — basic physics diagram
# ═══════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(8, 6), facecolor=BG_COLOR)
setup_ax(ax1)
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-0.5, 1.8)

# Mirror surface (horizontal line)
ax1.plot([-1.0, 1.0], [0, 0], color="white", linewidth=4, solid_capstyle="round")
ax1.text(1.1, 0, "mirror\nsurface", fontsize=9, color="white", va="center")

# Hatching on back of mirror
for x in np.arange(-0.95, 1.0, 0.15):
    ax1.plot([x, x - 0.1], [0, -0.12], color="#555555", linewidth=1)
ax1.text(0, -0.28, "(back face — not reflective)", fontsize=7,
         color="#777777", ha="center")

# Normal line (perpendicular to surface = vertical)
normal = np.array([0, 1])
ax1.plot([0, 0], [0, 1.3], "--", color=NORMAL_COLOR, linewidth=1.8, zorder=5)
ax1.text(0.55, 1.25, "normal $\\hat{n}$\n(perpendicular\nto surface)",
         fontsize=8, color=NORMAL_COLOR, ha="center")

# Incoming ray — from upper RIGHT
inc_dir = np.array([-0.707, -0.707])
inc_start = np.array([0, 0]) - inc_dir * 1.1
draw_light_ray(ax1, inc_start, inc_dir, 1.1, SUN_COLOR, lw=3)
ax1.text(0.85, 0.75, "incoming\nray", fontsize=9, color=SUN_COLOR,
         fontweight="bold", ha="center")

# Reflected ray
ref_dir = reflect(inc_dir, normal)
draw_light_ray(ax1, np.array([0, 0]), ref_dir, 1.1, REFLECT_COLOR, lw=3)
ax1.text(-0.85, 0.75, "reflected\nray", fontsize=9, color=REFLECT_COLOR,
         fontweight="bold", ha="center")

# Angle arcs
a_inc = np.degrees(np.arctan2((-inc_dir)[1], (-inc_dir)[0]))
a_norm = 90
a_ref = np.degrees(np.arctan2(ref_dir[1], ref_dir[0]))

arc_r = 0.35
angles_i = np.linspace(np.radians(a_inc), np.radians(a_norm), 20)
ax1.plot(np.cos(angles_i) * arc_r, np.sin(angles_i) * arc_r,
         color=SUN_COLOR, linewidth=1.2)
ax1.text(0.22, 0.32, "$\\theta_i$", fontsize=11, color=SUN_COLOR, ha="center")

angles_r = np.linspace(np.radians(a_norm), np.radians(a_ref), 20)
ax1.plot(np.cos(angles_r) * arc_r, np.sin(angles_r) * arc_r,
         color=REFLECT_COLOR, linewidth=1.2)
ax1.text(-0.22, 0.32, "$\\theta_r$", fontsize=11, color=REFLECT_COLOR, ha="center")

# Title and caption
ax1.text(0, 1.7, "Law of Reflection:  $\\theta_i = \\theta_r$",
         fontsize=14, color="white", ha="center", fontweight="bold")
ax1.text(0, -0.45, "Both rays are on the SAME side of the mirror surface.\n"
         "Light does NOT pass through a reflective mirror.",
         fontsize=9, color="#cccccc", ha="center", fontstyle="italic")

# Impact point
ax1.plot(0, 0, "o", color=HINGE_COLOR, markersize=8, zorder=11)

fig1.tight_layout()
fig1.savefig(os.path.join(OUT_DIR, "mirror_law_of_reflection.png"),
             dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
print("Saved mirror_law_of_reflection.png")


# ═══════════════════════════════════════════════════════════════
# FIGURE 2: Side View — PRIMARY physics diagram
#
# Coordinate system:
#   X-axis = along cylinder axis (right = toward sun)
#   Y-axis = radial (up = outward from cylinder center)
#
# Mirror geometry at 45°:
#   mirror_dir = (cos45, sin45) = (1/√2, 1/√2) from hinge
#   Reflective face normal = (sin45, -cos45) = (1/√2, -1/√2)
#     → points toward the sun (right) and window (down)
#     → this is the face that catches sunlight
#   Back face is on the upper-left side (away from sun)
# ═══════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(14, 9), facecolor=BG_COLOR)
setup_ax(ax2)

CYL_LEN = 6.0
CYL_R = 1.2
MIRROR_LEN_2 = CYL_LEN * 0.65

# --- Cylinder outline ---
# Top surface = window strip (transparent)
ax2.plot([-CYL_LEN / 2, CYL_LEN / 2], [CYL_R, CYL_R],
         color=WINDOW_COLOR, linewidth=4, solid_capstyle="butt", zorder=3)

# Bottom surface
ax2.plot([-CYL_LEN / 2, CYL_LEN / 2], [-CYL_R, -CYL_R],
         color=LAND_COLOR, linewidth=4, solid_capstyle="butt", zorder=3)

# End caps (dashed)
ax2.plot([-CYL_LEN / 2, -CYL_LEN / 2], [-CYL_R, CYL_R],
         color="#666666", linewidth=2, linestyle="--", zorder=2)
ax2.plot([CYL_LEN / 2, CYL_LEN / 2], [-CYL_R, CYL_R],
         color="#666666", linewidth=2, linestyle="--", zorder=2)

# Interior label (centered, out of the way)
ax2.text(1.2, 0, "INTERIOR", fontsize=13, color="#444444",
         ha="center", fontweight="bold")

# Window strip label — along top edge, right side (clear area)
ax2.text(CYL_LEN / 2 - 0.1, CYL_R + 0.15, "window strip (transparent)",
         fontsize=8, color=WINDOW_COLOR, ha="right", va="bottom")

# End labels — well below cylinder
ax2.text(-CYL_LEN / 2, -CYL_R - 0.45, "anti-sun end",
         fontsize=10, color="#aaaaaa", ha="center")
ax2.text(CYL_LEN / 2, -CYL_R - 0.45, "sun-facing end",
         fontsize=10, color=SUN_COLOR, ha="center", fontweight="bold")

# --- Mirror ---
hinge = np.array([-CYL_LEN / 2, CYL_R])
mirror_dir = np.array([1, 1]) / np.sqrt(2)
outer = hinge + mirror_dir * MIRROR_LEN_2

# Mirror surface line
ax2.plot([hinge[0], outer[0]], [hinge[1], outer[1]],
         color=MIRROR_COLOR, linewidth=5, solid_capstyle="round", zorder=7)

# --- CORRECT face assignment ---
# Reflective face normal: rotate mirror_dir 90° CLOCKWISE = (1/√2, -1/√2)
# This points toward the sun (right) and toward the window (down)
reflective_normal = np.array([mirror_dir[1], -mirror_dir[0]])  # (1/√2, -1/√2)

# Back face direction: opposite = (-1/√2, 1/√2) = upper-left
back_normal = -reflective_normal

# Back-face hatching on the UPPER-LEFT side (away from sun)
for frac in np.arange(0.03, 1.0, 0.04):
    pt = hinge + mirror_dir * MIRROR_LEN_2 * frac
    ax2.plot([pt[0], pt[0] + back_normal[0] * 0.1],
             [pt[1], pt[1] + back_normal[1] * 0.1],
             color="#555555", linewidth=0.8, zorder=6)

# Hinge marker and label — to the left of hinge, above cylinder
ax2.plot(hinge[0], hinge[1], "o", color=HINGE_COLOR, markersize=10, zorder=11)
ax2.text(-CYL_LEN / 2 - 1.0, CYL_R + 0.7,
         "HINGE\n(at anti-sun end,\ntangent to window strip)",
         fontsize=9, color=HINGE_COLOR, fontweight="bold", ha="center")
ax2.annotate("", xy=(hinge[0], hinge[1]),
             xytext=(-CYL_LEN / 2 - 0.5, CYL_R + 0.55),
             arrowprops=dict(arrowstyle="->", color=HINGE_COLOR, lw=1.2))

# Outer edge marker and label — above outer edge
ax2.plot(outer[0], outer[1], "s", color=OUTER_COLOR, markersize=8, zorder=11)
ax2.text(outer[0], outer[1] + 0.35,
         "OUTER EDGE (free)",
         fontsize=9, color=OUTER_COLOR, fontweight="bold", ha="center")

# Reflective face label — on the LOWER-RIGHT side of mirror (correct side!)
refl_label_pos = hinge + mirror_dir * MIRROR_LEN_2 * 0.55 + reflective_normal * 0.45
ax2.text(refl_label_pos[0], refl_label_pos[1],
         "reflective face\n(faces sun & window)",
         fontsize=8, color="#dddddd", ha="center", fontstyle="italic",
         rotation=-45)

# Back face label — on the UPPER-LEFT side
back_label_pos = hinge + mirror_dir * MIRROR_LEN_2 * 0.55 + back_normal * 0.35
ax2.text(back_label_pos[0], back_label_pos[1],
         "back face",
         fontsize=7, color="#777777", ha="center", fontstyle="italic",
         rotation=-45)

# --- 45° angle indicator ---
# Reference line along tangent plane (horizontal from hinge toward sun)
ax2.plot([hinge[0], hinge[0] + 1.4], [hinge[1], hinge[1]],
         ":", color="#888888", linewidth=1, zorder=5)

# Arc from horizontal to mirror direction
arc_r2 = 0.9
arc_angles = np.linspace(0, np.pi / 4, 25)
ax2.plot(hinge[0] + np.cos(arc_angles) * arc_r2,
         hinge[1] + np.sin(arc_angles) * arc_r2,
         color="white", linewidth=1.5, zorder=5)
ax2.text(hinge[0] + arc_r2 * 1.0, hinge[1] + arc_r2 * 0.45,
         "45°", fontsize=13, color="white", fontweight="bold")

# --- Mirror normal (on reflective side) ---
# Normal = (1/√2, -1/√2), pointing toward sun & window
m_mid = hinge + mirror_dir * MIRROR_LEN_2 * 0.5
n_start = m_mid
n_end = m_mid + reflective_normal * 0.8
ax2.plot([n_start[0], n_end[0]], [n_start[1], n_end[1]],
         "--", color=NORMAL_COLOR, linewidth=1.8, zorder=9)
# n-hat label — below-right of normal arrow tip
ax2.text(n_end[0] + 0.15, n_end[1] - 0.1,
         "$\\hat{n}$", fontsize=13, color=NORMAL_COLOR, fontweight="bold")

# --- Axial sunlight rays ---
# Light travels from sun (right) toward anti-sun end (left): direction = (-1, 0)
sun_d = np.array([-1, 0])
ray_fracs = [0.3, 0.5, 0.7]

for frac in ray_fracs:
    hit = hinge + mirror_dir * MIRROR_LEN_2 * frac
    # Incoming ray from the right
    inc_start = np.array([CYL_LEN / 2 + 1.0, hit[1]])
    inc_len = inc_start[0] - hit[0]
    draw_light_ray(ax2, inc_start, sun_d, inc_len, SUN_COLOR, lw=2.5)

    # Reflected ray using CORRECT reflective normal
    ref = reflect(sun_d, reflective_normal)
    ref = ref / np.linalg.norm(ref)
    # ref should be (0, -1) = straight down through window
    ref_len = (hit[1] - CYL_R) + 0.5
    if ref_len > 0.1:
        draw_light_ray(ax2, hit, ref, ref_len, REFLECT_COLOR, lw=2.5)

# --- Angle arcs at middle ray hit point ---
hit_mid = hinge + mirror_dir * MIRROR_LEN_2 * 0.5

# θᵢ: angle between -sun_d (= +X, pointing right) and normal
# -sun_d direction angle = 0° (pointing right)
# normal direction angle = atan2(-1/√2, 1/√2) = -45° = 315°
# Arc from 315° to 360° (= 0°)
arc_r3 = 0.45
n_angle = np.arctan2(reflective_normal[1], reflective_normal[0])  # -π/4
sun_away_angle = 0  # -sun_d = (1, 0)

# Draw θᵢ arc: from normal to -sun_d (the smaller arc)
# From -45° to 0°
angles_i2 = np.linspace(n_angle, sun_away_angle, 20)
ax2.plot(hit_mid[0] + np.cos(angles_i2) * arc_r3,
         hit_mid[1] + np.sin(angles_i2) * arc_r3,
         color=SUN_COLOR, linewidth=1.3, zorder=9)
mid_a_i = (n_angle + sun_away_angle) / 2
ax2.text(hit_mid[0] + np.cos(mid_a_i) * (arc_r3 + 0.2),
         hit_mid[1] + np.sin(mid_a_i) * (arc_r3 + 0.2),
         "$\\theta_i$", fontsize=11, color=SUN_COLOR)

# θᵣ: angle between normal and reflected direction
# reflected = (0, -1), angle = -π/2 = -90°
ref_angle = -np.pi / 2
# From -90° to -45°
angles_r2 = np.linspace(ref_angle, n_angle, 20)
ax2.plot(hit_mid[0] + np.cos(angles_r2) * arc_r3,
         hit_mid[1] + np.sin(angles_r2) * arc_r3,
         color=REFLECT_COLOR, linewidth=1.3, zorder=9)
mid_a_r = (ref_angle + n_angle) / 2
ax2.text(hit_mid[0] + np.cos(mid_a_r) * (arc_r3 + 0.2),
         hit_mid[1] + np.sin(mid_a_r) * (arc_r3 + 0.2),
         "$\\theta_r$", fontsize=11, color=REFLECT_COLOR)

# --- Sun indicator (top-right corner) ---
sun_x, sun_y = CYL_LEN / 2 + 1.5, outer[1] + 0.5
ax2.text(sun_x, sun_y, "SUN", fontsize=16,
         color=SUN_COLOR, fontweight="bold", ha="center")
for dy in [-0.25, 0, 0.25]:
    draw_arrow(ax2, [sun_x + 0.3, sun_y - 0.6 + dy],
               [sun_x - 0.3, sun_y - 0.6 + dy], SUN_COLOR, lw=1.5)

# --- Key physics box (bottom, well clear of diagram) ---
ax2.text(
    -CYL_LEN / 2, -CYL_R - 1.2,
    "  Axis points toward sun  \u2192  light arrives along axis\n"
    "  Mirror at 45\u00b0 from tangent plane catches axial light\n"
    "  Reflective face faces the sun and the window\n"
    "  \u03b8\u1d62 = \u03b8\u1d63 = 45\u00b0  \u2192  light deflected 90\u00b0 radially inward",
    fontsize=8, color="#cccccc", family="monospace",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#2a2a4e", edgecolor="#444"),
    va="top",
)

ax2.set_xlim(-CYL_LEN / 2 - 2.0, CYL_LEN / 2 + 2.5)
ax2.set_ylim(-CYL_R - 2.5, outer[1] + 1.2)
ax2.set_title("Side View \u2014 Mirror Reflects Axial Sunlight Radially Inward",
              fontsize=13, color="white", pad=15)

fig2.tight_layout()
fig2.savefig(os.path.join(OUT_DIR, "mirror_side_view.png"),
             dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
print("Saved mirror_side_view.png")


# ═══════════════════════════════════════════════════════════════
# FIGURE 3: Day/Night Cycle — 3 side views at different tilts
#
# Same physics as Figure 2. Reflective face normal at tilt α:
#   n = (sin α, -cos α) — always faces sun & window
# ═══════════════════════════════════════════════════════════════
fig3, axes3 = plt.subplots(1, 3, figsize=(18, 7), facecolor=BG_COLOR)

tilt_configs = [
    (5, "Night (nearly closed)", "0%"),
    (25, "Dawn / Dusk", "~50%"),
    (45, "Noon (fully open)", "~100%"),
]

for ax_i, (tilt_deg, title, pct) in enumerate(tilt_configs):
    ax = axes3[ax_i]
    setup_ax(ax)

    cl = 4.0
    cr = 0.8
    ml = cl * 0.6

    # Cylinder outline
    ax.plot([-cl / 2, cl / 2], [cr, cr],
            color=WINDOW_COLOR, linewidth=3, solid_capstyle="butt", zorder=3)
    ax.plot([-cl / 2, cl / 2], [-cr, -cr],
            color=LAND_COLOR, linewidth=3, solid_capstyle="butt", zorder=3)
    ax.plot([-cl / 2, -cl / 2], [-cr, cr],
            color="#666666", linewidth=1.5, linestyle="--", zorder=2)
    ax.plot([cl / 2, cl / 2], [-cr, cr],
            color="#666666", linewidth=1.5, linestyle="--", zorder=2)

    # Mirror at given tilt angle from tangent plane
    tilt_rad = np.radians(tilt_deg)
    h = np.array([-cl / 2, cr])
    # mirror direction: cos(α) along axis + sin(α) radially outward
    m_dir = np.array([np.cos(tilt_rad), np.sin(tilt_rad)])
    outer_pt = h + m_dir * ml

    # Draw mirror
    ax.plot([h[0], outer_pt[0]], [h[1], outer_pt[1]],
            color=MIRROR_COLOR, linewidth=4, solid_capstyle="round", zorder=7)

    # Hinge
    ax.plot(h[0], h[1], "o", color=HINGE_COLOR, markersize=7, zorder=11)

    # Back-face hatching on UPPER-LEFT side (away from sun)
    # Back normal = (-sin α, cos α)
    back_n = np.array([-np.sin(tilt_rad), np.cos(tilt_rad)])
    for frac in np.arange(0.05, 1.0, 0.06):
        pt = h + m_dir * ml * frac
        ax.plot([pt[0], pt[0] + back_n[0] * 0.06],
                [pt[1], pt[1] + back_n[1] * 0.06],
                color="#555555", linewidth=0.7, zorder=6)

    # Angle arc from tangent plane
    if tilt_deg > 3:
        arc_r4 = 0.55
        arc_a = np.linspace(0, tilt_rad, 20)
        ax.plot(h[0] + np.cos(arc_a) * arc_r4,
                h[1] + np.sin(arc_a) * arc_r4,
                color="white", linewidth=1.2)
        mid_a = tilt_rad / 2
        ax.text(h[0] + np.cos(mid_a) * (arc_r4 + 0.18),
                h[1] + np.sin(mid_a) * (arc_r4 + 0.18),
                f"{tilt_deg}\u00b0", fontsize=9, color="white",
                ha="center", va="center")

    # Light rays (only for tilt > 5°)
    if tilt_deg > 5:
        # Reflective normal = (sin α, -cos α) — faces sun & window
        refl_n = np.array([np.sin(tilt_rad), -np.cos(tilt_rad)])
        sun_d4 = np.array([-1, 0])

        if np.dot(sun_d4, refl_n) < 0:  # d·n < 0 means light hits reflective face
            for frac in [0.35, 0.65]:
                hit4 = h + m_dir * ml * frac
                # Incoming
                draw_light_ray(ax, np.array([cl / 2 + 0.5, hit4[1]]),
                               sun_d4, cl / 2 + 0.5 - hit4[0],
                               SUN_COLOR, lw=1.8)
                # Reflected
                ref4 = reflect(sun_d4, refl_n)
                ref4 = ref4 / np.linalg.norm(ref4)
                ref_len4 = (hit4[1] - cr) + 0.35
                if ref_len4 > 0.05:
                    draw_light_ray(ax, hit4, ref4, ref_len4,
                                   REFLECT_COLOR, lw=1.8)

    # Sun label (top-right, compact)
    ax.text(cl / 2 + 0.5, outer_pt[1] + 0.6, "SUN",
            fontsize=10, color=SUN_COLOR, fontweight="bold", ha="center")
    draw_arrow(ax, [cl / 2 + 0.6, outer_pt[1] + 0.2],
               [cl / 2 + 0.2, outer_pt[1] + 0.2], SUN_COLOR, lw=1.2)

    # Light percentage
    pct_color = SUN_COLOR if tilt_deg > 5 else "#888"
    ax.text(0, -cr - 0.45, f"Light: {pct}",
            fontsize=11, color=pct_color, fontweight="bold", ha="center")

    ax.set_title(title, fontsize=11, color="white", pad=10)
    ax.set_xlim(-cl / 2 - 0.8, cl / 2 + 1.2)
    ax.set_ylim(-cr - 0.9, outer_pt[1] + 1.2)

fig3.suptitle("Day/Night Cycle \u2014 Mirror Tilt Controls Light Entry (Side View)",
              fontsize=13, color="white", y=0.98)
fig3.tight_layout(rect=[0, 0, 1, 0.95])
fig3.savefig(os.path.join(OUT_DIR, "mirror_daynight_diagram.png"),
             dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
print("Saved mirror_daynight_diagram.png")


print("\nAll diagrams generated.")
