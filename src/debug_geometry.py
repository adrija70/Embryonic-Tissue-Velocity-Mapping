from pathlib import Path
import scipy.io as sio
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    PROJECT_DIR
    / "data"
    / "piv_data"
    / "[INTERNAL] PIVlab_results"
)

mat_file = DATA_DIR / "WT_202001101100_PIVlab.mat"

data = sio.loadmat(mat_file)

u = data["u_filt_lst"]
v = data["v_filt_lst"]

x = data["xx"]
y = data["yy"]

u0 = u[0]
v0 = v[0]

print("\n=== SHAPES ===")
print("u:", u.shape)
print("v:", v.shape)
print("x:", x.shape)
print("y:", y.shape)
print("u0:", u0.shape)
print("v0:", v0.shape)

print("\n=== RANGES ===")
print("x min/max:", x.min(), x.max())
print("y min/max:", y.min(), y.max())

print("\n=== CORNERS ===")

print("x[0,0] =", x[0,0])
print("x[-1,-1] =", x[-1,-1])

print("y[0,0] =", y[0,0])
print("y[-1,-1] =", y[-1,-1])

print("\n=== SPEED ===")

speed = np.sqrt(u0**2 + v0**2)

print("speed shape:", speed.shape)
print("speed min:", speed.min())
print("speed max:", speed.max())
print("speed mean:", speed.mean())