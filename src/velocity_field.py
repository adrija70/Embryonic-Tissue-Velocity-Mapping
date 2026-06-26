from pathlib import Path
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt


PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data" / "piv_data" / "[INTERNAL] PIVlab_results"
ANALYSIS_DIR = PROJECT_DIR / "analysis"

ANALYSIS_DIR.mkdir(exist_ok=True)


mat_file = DATA_DIR / "WT_202001101100_PIVlab.mat"

print(f"Loading: {mat_file.name}")

data = sio.loadmat(mat_file)

u = data["u_filt_lst"]
v = data["v_filt_lst"]

x = data["xx"]
y = data["yy"]

print("u shape:", u.shape)
print("v shape:", v.shape)
print("x shape:", x.shape)
print("y shape:", y.shape)


frame = 0

u0 = u[frame]
v0 = v[frame]

speed = np.sqrt(u0**2 + v0**2)

plt.figure(figsize=(10, 7))

plt.quiver(
    x,
    y,
    u0,
    v0,
    speed,
    angles="xy",
    scale_units="xy",
    scale=None
)

plt.colorbar(label="Velocity magnitude")

plt.title("Frame 0 Tissue Velocity Field")
plt.xlabel("X")
plt.ylabel("Y")

plt.tight_layout()

outfile = ANALYSIS_DIR / "frame0_velocity_field.png"

plt.savefig(outfile, dpi=300)
plt.close()

print(f"Saved: {outfile}")
