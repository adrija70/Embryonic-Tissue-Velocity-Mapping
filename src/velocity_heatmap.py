from pathlib import Path
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

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
# use the first frame as a representative example
u0 = u[0]
v0 = v[0]

speed = np.sqrt(u0**2 + v0**2)


fig, ax = plt.subplots(figsize=(8,10))

mesh = ax.pcolormesh(
    x,
    y,
    speed,
    shading="auto"
)

fig.colorbar(
    mesh,
    ax=ax,
    label="Velocity magnitude"
)

ax.set_title("Velocity Magnitude")
ax.set_xlabel("X")
ax.set_ylabel("Y")

plt.tight_layout()

outfile = FIGURE_DIR / "velocity_heatmap_only.png"

plt.savefig(
    outfile,
    dpi=300
)

print("Saved:", outfile)
