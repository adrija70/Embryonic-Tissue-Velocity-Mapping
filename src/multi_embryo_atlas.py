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

wt_files = sorted(
    DATA_DIR.glob("WT*_PIVlab.mat")
)

print(f"\nFound {len(wt_files)} WT embryos\n")

if len(wt_files) < 2:
    raise ValueError(
        "Need multiple WT embryos for atlas analysis."
    )

all_features = []

for mat_file in wt_files:

    print(f"Processing: {mat_file.name}")

    data = sio.loadmat(mat_file)

    u_all = data["u_filt_lst"]
    v_all = data["v_filt_lst"]

    x = data["xx"]
    y = data["yy"]

    dx = np.mean(np.diff(x[0, :]))
    dy = np.mean(np.diff(y[:, 0]))

    embryo_features = []

    n_frames = u_all.shape[0]

    for frame in range(n_frames):

        u = gaussian_filter(
            u_all[frame],
            sigma=1.5
        )

        v = gaussian_filter(
            v_all[frame],
            sigma=1.5
        )


        speed = np.sqrt(u**2 + v**2)

        mean_speed = np.mean(speed)
        std_speed = np.std(speed)
        p95_speed = np.percentile(
            speed,
            95
        )


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

        embryo_features.append(
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

    embryo_features = np.array(
        embryo_features
    )

    mean_profile = embryo_features.mean(
        axis=0
    )

    all_features.append(
        [
            mat_file.stem,
            *mean_profile
        ]
    )

columns = [
    "embryo",
    "mean_speed",
    "std_speed",
    "p95_speed",
    "mean_divergence",
    "std_divergence",
    "mean_vorticity",
    "std_vorticity",
]

df = pd.DataFrame(
    all_features,
    columns=columns
)

csv_file = (
    ANALYSIS_DIR
    / "WT_embryo_features.csv"
)

df.to_csv(
    csv_file,
    index=False
)

print("\nSaved:")
print(csv_file)


feature_cols = columns[1:]

X = df[feature_cols]

X_scaled = StandardScaler().fit_transform(
    X
)

pca = PCA(
    n_components=2
)

pcs = pca.fit_transform(
    X_scaled
)

df["PC1"] = pcs[:, 0]
df["PC2"] = pcs[:, 1]

print("\nExplained variance:")

print(
    pca.explained_variance_ratio_
)

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    df["PC1"],
    df["PC2"],
    s=120
)

for _, row in df.iterrows():

    plt.text(
        row["PC1"],
        row["PC2"],
        row["embryo"][:12],
        fontsize=8
    )

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.title(
    "WT Morphodynamic Atlas"
)

outfile = (
    FIGURE_DIR
    / "Fig7_WT_morphodynamic_atlas.png"
)

plt.savefig(
    outfile,
    dpi=600,
    bbox_inches="tight"
)

plt.close()

print("\nSaved:")
print(outfile)


loadings = pd.DataFrame(
    pca.components_.T,
    index=feature_cols,
    columns=["PC1", "PC2"]
)

loadings_file = (
    ANALYSIS_DIR
    / "WT_PCA_loadings.csv"
)

loadings.to_csv(
    loadings_file
)

print(loadings.round(3))

print("\nDone.")
