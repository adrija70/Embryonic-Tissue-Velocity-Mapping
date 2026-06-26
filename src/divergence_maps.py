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

print("Loading:", mat_file.name)

data = sio.loadmat(mat_file)

u = data["u_filt_lst"]
v = data["v_filt_lst"]

x = data["xx"]
y = data["yy"]


dx = np.mean(np.diff(x[0, :]))
dy = np.mean(np.diff(y[:, 0]))

print(f"dx = {dx}")
print(f"dy = {dy}")

frames = [10, 38, 75]

fig, axes = plt.subplots(
    1,
    3,
    figsize=(18, 8),
    constrained_layout=True
)

for ax, frame in zip(axes, frames):

    u0 = u[frame]
    v0 = v[frame]

# smooth before taking spatial derivatives

    u0 = gaussian_filter(u0, sigma=1.5)
    v0 = gaussian_filter(v0, sigma=1.5)

   
    du_dx = np.gradient(
        u0,
        dx,
        axis=1
    )

    dv_dy = np.gradient(
        v0,
        dy,
        axis=0
    )
# divergence = local expansion (+) or contraction 
    divergence = du_dx + dv_dy

    print(
        f"Frame {frame}: "
        f"min={np.nanmin(divergence):.4f} "
        f"max={np.nanmax(divergence):.4f} "
        f"mean={np.nanmean(divergence):.4f}"
    )
# avoid a few extreme values dominating the color scale
    vmax = np.percentile(
        np.abs(divergence),
        99
    )

    mesh = ax.pcolormesh(
        x,
        y,
        divergence,
        shading="auto",
        cmap="RdBu_r",
        vmin=-vmax,
        vmax=vmax
    )

    ax.set_title(
        f"Frame {frame}"
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")


cbar = fig.colorbar(
    mesh,
    ax=axes,
    shrink=0.8
)

cbar.set_label("Divergence")


outfile = FIGURE_DIR / "Fig2_divergence_maps.png"

plt.savefig(
    outfile,
    dpi=600,
    bbox_inches="tight"
)

plt.close()

print("\nSaved:", outfile)
