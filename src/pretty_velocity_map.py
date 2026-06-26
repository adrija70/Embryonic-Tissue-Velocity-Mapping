from pathlib import Path
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    PROJECT_DIR
    / "data"
    / "piv_data"
    / "[INTERNAL] PIVlab_results"
)

FIGURE_DIR = PROJECT_DIR / "figure"
FIGURE_DIR.mkdir(exist_ok=True)


mat_file = DATA_DIR / "WT_202001101100_PIVlab.mat"

data = sio.loadmat(mat_file)

u = data["u_filt_lst"]
v = data["v_filt_lst"]

x = data["xx"]
y = data["yy"]

frame = 38

u0 = u[frame]
v0 = v[frame]

speed = np.sqrt(u0**2 + v0**2)

speed_smooth = gaussian_filter(
    speed,
    sigma=2
)

# FIGURE A
fig, ax = plt.subplots(figsize=(8,10))

mesh = ax.pcolormesh(
    x,
    y,
    speed_smooth,
    shading="auto"
)

fig.colorbar(
    mesh,
    ax=ax,
    label="Velocity magnitude"
)

ax.set_title(
    f"Embryonic Tissue Flow (Frame {frame})"
)

ax.set_xlabel("X")
ax.set_ylabel("Y")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "Fig1A_velocity_map.png",
    dpi=600
)

plt.close()

# FIGURE B
fig, ax = plt.subplots(figsize=(8,10))

mesh = ax.pcolormesh(
    x,
    y,
    speed_smooth,
    shading="auto"
)

fig.colorbar(
    mesh,
    ax=ax,
    label="Velocity magnitude"
)

step = 6

ax.quiver(
    x[::step, ::step],
    y[::step, ::step],
    u0[::step, ::step],
    v0[::step, ::step],
    color="white",
    alpha=0.85,
    scale=200
)

ax.set_title(
    f"Embryonic Tissue Flow (Frame {frame})"
)

ax.set_xlabel("X")
ax.set_ylabel("Y")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "Fig1B_velocity_map_vectors.png",
    dpi=600
)

plt.close()

print("Saved:")
print("Fig1A_velocity_map.png")
print("Fig1B_velocity_map_vectors.png")
