import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

# -----------------------------
# Dark mode styling
# -----------------------------
plt.style.use("dark_background")

# Custom colours for readability
bg_color = "#0d0d0d"
grid_color = "#AAAAAA"
text_color = "#ffffff"
contour_label_color = "#ffffff"

# Turn radius formula
def turn_radius_nm(V, phi_deg):
    phi = np.radians(phi_deg)
    return (1.457e-5 * (V**2) * 2) / np.tan(phi)

# Range scaling
TAS = np.linspace(25, 450, 200)
bank_angles = np.linspace(1, 60, 200)

TAS_grid, PHI_grid = np.meshgrid(TAS, bank_angles)
R_grid = turn_radius_nm(TAS_grid, PHI_grid)


def log_scale(phi):
    return np.log(phi + 1)

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# Contours of turn radius in NM

# list of display strings showing 1/4 @ 1500ft and 0.5 @ 3000ft

@dataclass
class turnRadius:
    display: str
    num: float

#    turnRadius("¼ NM", 0.25),
#    turnRadius("½ NM", 0.5),


radii = [
    turnRadius("0.25 NM", 0.25),
    turnRadius("0.5 NM", 0.5),
    turnRadius("1 NM", 1.0),
    turnRadius("2 NM", 2.0),
    turnRadius("4 NM", 4.0),
    turnRadius("6 NM", 6.0),
    turnRadius("8 NM", 8.0),
    turnRadius("10 NM",10.0),
    turnRadius("15 NM",15),
    turnRadius("20 NM",20),
    turnRadius("30 NM",30),
    turnRadius("40 NM",40),
    turnRadius("50 NM", 50),
    turnRadius("75 NM", 75),
    turnRadius("100 NM",100)
]

# Map numeric radius → display string
level_to_label = {r.num: r.display for r in radii}

def fmt(level):
    for r in radii:
        if abs(float(level) - r.num) < 1e-6:
            return r.display
    return f"{level}"

levels = [0.25, 0.5, 1, 2, 4, 6, 8, 10, 15, 20, 30, 40, 50, 75, 100]
contours = ax.contour(
    TAS,
    log_scale(bank_angles),
    R_grid,
    levels=levels,
    cmap="Set3",
    linewidths=1.3,
    fmt = fmt
)




# Calculate manual positions for labels at the midpoint of each contour
manual_positions = []
for i, level in enumerate(levels):
    segs = contours.allsegs[i]
    if segs:
        path = segs[0]  # Take the first segment for each level
        vertices = path
        mid_idx = len(vertices) // 3
        mid_point = vertices[mid_idx]
        manual_positions.append(mid_point)

# Label contours
ax.clabel(
    contours,
    levels=levels,
    manual=manual_positions,
    inline=True,
    fontsize=10,
    colors=contour_label_color,
    inline_spacing=1,
    fmt=fmt
)
# Axes
ax.set_xlabel("TAS (kt)", color=text_color)
ax.set_ylabel("Bank Angle", color=text_color)
ax.set_title("TAS(kts) + Bank Angle = Turn Radius(NM)", color=text_color)

# Y axis to ADI Labels
true_ticks = [5, 10, 15, 20, 25, 30, 45, 60]
ax.set_yticks(log_scale(np.array(true_ticks)))
ax.set_yticklabels([f"{t}°" for t in true_ticks], color=text_color)

# X-axis colours
ax.tick_params(axis='x', colors=text_color)
ax.tick_params(axis='y', colors=text_color)

# Grid
ax.grid(True, linestyle="--", alpha=0.3, color=grid_color)

plt.tight_layout()
plt.savefig('turn_radius_plot.png')
plt.show()