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

speed = np.sqrt(u**2 + v**2)

mean_speed = speed.mean(axis=(1,2))
std_speed = speed.std(axis=(1,2))

frames = np.arange(len(mean_speed))

plt.figure(figsize=(8,5))

plt.plot(
    frames,
    mean_speed,
    linewidth=2
)

plt.fill_between(
    frames,
    mean_speed - std_speed,
    mean_speed + std_speed,
    alpha=0.3
)

plt.xlabel("Frame")
plt.ylabel("Mean velocity magnitude")
plt.title("Mean Tissue Speed Across Development")

plt.tight_layout()

outfile = FIGURE_DIR / "mean_speed_vs_time.png"

plt.savefig(outfile, dpi=300)

print("Saved:", outfile)

print()
print("Frames:", len(mean_speed))
print("Minimum mean speed:", mean_speed.min())
print("Maximum mean speed:", mean_speed.max())
print("Overall mean speed:", mean_speed.mean())
