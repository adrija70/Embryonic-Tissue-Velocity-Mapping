from pathlib import Path
import scipy.io as sio
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    PROJECT_DIR
    / "data"
    / "piv_data"
    / "[INTERNAL] PIVlab_results"
)

mat_file = DATA_DIR / "WT_202001101100_PIVlab.mat"

data = sio.loadmat(mat_file)

x = data["xx"]
y = data["yy"]

plt.figure(figsize=(8,8))

plt.scatter(
    x,
    y,
    s=2
)

plt.title("PIV Grid Coordinates")
plt.xlabel("X")
plt.ylabel("Y")

plt.tight_layout()

plt.savefig(
    PROJECT_DIR / "analysis" / "grid_check.png",
    dpi=300
)

plt.show()
