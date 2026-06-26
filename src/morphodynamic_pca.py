from pathlib import Path

import scipy.io as sio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    PROJECT_DIR
    / "data"
    / "piv_data"
    / "[INTERNAL] PIVlab_results"
)

FIGURE_DIR = PROJECT_DIR / "figure"
FIGURE_DIR.mkdir(exist_ok=True)

ANALYSIS_DIR = PROJECT_DIR / "analysis"
ANALYSIS_DIR.mkdir(exist_ok=True)

mat_file = DATA_DIR / "WT_202001101100_PIVlab.mat"

print(f"Loading: {mat_file.name}")

data = sio.loadmat(mat_file)

u_all = data["u_filt_lst"]
v_all = data["v_filt_lst"]

x = data["xx"]
y = data["yy"]

n_frames = u_all.shape[0]

print(f"Frames: {n_frames}")

dx = np.mean(np.diff(x[0, :]))
dy = np.mean(np.diff(y[:, 0]))

print(f"dx = {dx}")
print(f"dy = {dy}")


features = []

for frame in range(n_frames):

    u = u_all[frame]
    v = v_all[frame]

    u = gaussian_filter(u, sigma=1.5)
    v = gaussian_filter(v, sigma=1.5)

    speed = np.sqrt(u**2 + v**2)

    mean_speed = np.mean(speed)
    std_speed = np.std(speed)
    p95_speed = np.percentile(speed, 95)

    du_dx = np.gradient(
        u,
        dx,
        axis=1
    )

    dv_dy = np.gradient(
        v,
        dy,
        axis=0
    )

    divergence = du_dx + dv_dy

    mean_div = np.mean(divergence)
    std_div = np.std(divergence)

    dv_dx = np.gradient(
        v,
        dx,
        axis=1
    )

    du_dy = np.gradient(
        u,
        dy,
        axis=0
    )

    vorticity = dv_dx - du_dy

    mean_vort = np.mean(vorticity)
    std_vort = np.std(vorticity)

    features.append(
        [
            mean_speed,
            std_speed,
            p95_speed,
            mean_div,
            std_div,
            mean_vort,
            std_vort,
        ]
    )

feature_names = [
    "mean_speed",
    "std_speed",
    "p95_speed",
    "mean_divergence",
    "std_divergence",
    "mean_vorticity",
    "std_vorticity",
]

df = pd.DataFrame(
    features,
    columns=feature_names
)

df["frame"] = np.arange(n_frames)

csv_out = ANALYSIS_DIR / "morphodynamic_features.csv"

df.to_csv(
    csv_out,
    index=False
)

print("\nSaved:")
print(csv_out)

X = df[feature_names].values

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)

pcs = pca.fit_transform(X_scaled)

df["PC1"] = pcs[:, 0]
df["PC2"] = pcs[:, 1]


variance = pca.explained_variance_ratio_

print("\nExplained variance:")
print(f"PC1: {variance[0]:.3f}")
print(f"PC2: {variance[1]:.3f}")
print(f"Total: {(variance[0]+variance[1]):.3f}")


plt.figure(figsize=(8, 6))

scatter = plt.scatter(
    df["PC1"],
    df["PC2"],
    c=df["frame"],
    cmap="viridis",
    s=60
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.title(
    "Morphodynamic PCA"
)

cbar = plt.colorbar(scatter)
cbar.set_label("Developmental Frame")

outfile = FIGURE_DIR / "Fig4_morphodynamic_PCA.png"

plt.savefig(
    outfile,
    dpi=600,
    bbox_inches="tight"
)

plt.close()

print(outfile)


plt.figure(figsize=(8, 6))

plt.plot(
    df["PC1"],
    df["PC2"],
    "-o",
    linewidth=2,
    markersize=4
)

for idx in [0, 20, 40, 60, 86]:

    plt.text(
        df.loc[idx, "PC1"],
        df.loc[idx, "PC2"],
        str(idx)
    )

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.title(
    "Developmental Trajectory in PCA Space"
)

outfile = FIGURE_DIR / "Fig5_developmental_trajectory.png"

plt.savefig(
    outfile,
    dpi=600,
    bbox_inches="tight"
)

plt.close()

print(outfile)


pca_full = PCA()

pca_full.fit(X_scaled)

var = pca_full.explained_variance_ratio_

plt.figure(figsize=(7, 5))

plt.plot(
    np.arange(1, len(var)+1),
    np.cumsum(var),
    marker="o"
)

plt.xlabel("Number of PCs")
plt.ylabel("Cumulative Explained Variance")

plt.title(
    "PCA Explained Variance"
)

plt.ylim(0, 1.05)

outfile = FIGURE_DIR / "Fig6_PCA_variance.png"

plt.savefig(
    outfile,
    dpi=600,
    bbox_inches="tight"
)

plt.close()

print(outfile)


loadings = pd.DataFrame(
    pca.components_.T,
    index=feature_names,
    columns=["PC1", "PC2"]
)

print("\nPCA Loadings:")
print(loadings.round(3))

loadings.to_csv(
    ANALYSIS_DIR / "PCA_loadings.csv"
)

print("\nDone.")
