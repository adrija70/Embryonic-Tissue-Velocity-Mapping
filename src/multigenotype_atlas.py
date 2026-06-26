import os
import scipy.io
import numpy as np
import pandas as pd

from scipy.ndimage import gaussian_filter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "piv_data",
    "[INTERNAL] PIVlab_results"
)

OUTPUT_CSV = os.path.join(
    PROJECT_ROOT,
    "analysis",
    "all_genotype_features.csv"
)

OUTPUT_FIG = os.path.join(
    PROJECT_ROOT,
    "figure",
    "Fig8_multigenotype_atlas.png"
)

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_FIG), exist_ok=True)


def compute_features(mat_file):

    mat = scipy.io.loadmat(mat_file)

    u = mat["u_filt_lst"]
    v = mat["v_filt_lst"]

    x = mat["xx"]
    y = mat["yy"]

    dx = float(np.mean(np.diff(x[0, :])))
    dy = float(np.mean(np.diff(y[:, 0])))

    rows = []

    n_frames = u.shape[0]

    for t in range(n_frames):

        u0 = gaussian_filter(u[t], sigma=1.5)
        v0 = gaussian_filter(v[t], sigma=1.5)

        speed = np.sqrt(u0**2 + v0**2)

        du_dx = np.gradient(u0, dx, axis=1)
        dv_dy = np.gradient(v0, dy, axis=0)

        divergence = du_dx + dv_dy

        dv_dx = np.gradient(v0, dx, axis=1)
        du_dy = np.gradient(u0, dy, axis=0)

        vorticity = dv_dx - du_dy

        rows.append([
            np.mean(speed),
            np.std(speed),
            np.percentile(speed, 95),

            np.mean(divergence),
            np.std(divergence),

            np.mean(vorticity),
            np.std(vorticity)
        ])

    rows = np.array(rows)

    return rows.mean(axis=0)


records = []

for fname in sorted(os.listdir(DATA_DIR)):

    if not fname.endswith(".mat"):
        continue

    path = os.path.join(DATA_DIR, fname)

    try:

        features = compute_features(path)

        genotype = "Unknown"

        name_lower = fname.lower()

        if "wt" in name_lower:
            genotype = "WT"

        elif "halo_snail" in name_lower:
            genotype = "Halo-Snail"

        elif "halo_twist" in name_lower:
            genotype = "Halo-Twist"

        elif "spaetzle" in name_lower:
            genotype = "Spaetzle"

        elif "toll" in name_lower:
            genotype = "Toll"

        records.append({
            "embryo": fname,
            "genotype": genotype,

            "mean_speed": features[0],
            "std_speed": features[1],
            "p95_speed": features[2],

            "mean_divergence": features[3],
            "std_divergence": features[4],

            "mean_vorticity": features[5],
            "std_vorticity": features[6]
        })

        print("Processed:", fname)

    except Exception as e:

        print("FAILED:", fname)
        print(e)


df = pd.DataFrame(records)

df.to_csv(OUTPUT_CSV, index=False)

print()
print("Saved:")
print(OUTPUT_CSV)

print()
print("Rows:", len(df))
print(df.groupby("genotype").size())


feature_cols = [
    "mean_speed",
    "std_speed",
    "p95_speed",
    "mean_divergence",
    "std_divergence",
    "mean_vorticity",
    "std_vorticity"
]

X = df[feature_cols].values

X = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)

coords = pca.fit_transform(X)

df["PC1"] = coords[:, 0]
df["PC2"] = coords[:, 1]

print()
print("Explained variance:")
print(pca.explained_variance_ratio_)

plt.figure(figsize=(9,7))

for genotype in sorted(df["genotype"].unique()):

    subset = df[df["genotype"] == genotype]

    plt.scatter(
        subset["PC1"],
        subset["PC2"],
        s=120,
        label=genotype
    )

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Multi-Genotype Morphodynamic Atlas")

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_FIG,
    dpi=300,
    bbox_inches="tight"
)

print()
print("Saved:")
print(OUTPUT_FIG)

print("\nDone.")
