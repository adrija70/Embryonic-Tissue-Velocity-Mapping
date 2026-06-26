import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from scipy.spatial.distance import cdist

import matplotlib.pyplot as plt
import seaborn as sns

WT_FILE = "analysis/morphodynamic_features.csv"
GENOTYPE_FILE = "analysis/all_genotype_features.csv"


feature_cols = [
    "mean_speed",
    "std_speed",
    "p95_speed",
    "mean_divergence",
    "std_divergence",
    "mean_vorticity",
    "std_vorticity"
]

# FIGURE 9
# WT TRAJECTORY
print("\nGenerating Fig9...")

wt = pd.read_csv(WT_FILE)

X_wt = StandardScaler().fit_transform(
    wt[feature_cols]
)

pca_wt = PCA(n_components=2)

coords_wt = pca_wt.fit_transform(X_wt)

wt["PC1"] = coords_wt[:, 0]
wt["PC2"] = coords_wt[:, 1]

plt.figure(figsize=(8, 6))

plt.plot(
    wt["PC1"],
    wt["PC2"],
    "-o",
    linewidth=2,
    markersize=4
)

for i in range(0, len(wt), 10):
    plt.text(
        wt["PC1"].iloc[i],
        wt["PC2"].iloc[i],
        str(int(wt["frame"].iloc[i]))
    )

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("WT Developmental Trajectory")

plt.tight_layout()

out = "figure/Fig9_WT_trajectory.png"
plt.savefig(out, dpi=300)
plt.close()

print("Saved:", out)
print("WT variance:", pca_wt.explained_variance_ratio_)

print("\nLoading genotype dataset...")

df = pd.read_csv(GENOTYPE_FILE)

print("Rows:", len(df))

X = StandardScaler().fit_transform(
    df[feature_cols]
)

pca = PCA(n_components=2)

coords = pca.fit_transform(X)

df["PC1"] = coords[:, 0]
df["PC2"] = coords[:, 1]

print("Atlas variance:", pca.explained_variance_ratio_)


# FIGURE 10
# GENOTYPE CENTROIDS
print("\nGenerating Fig10...")

centroids = (
    df.groupby("genotype")[["PC1", "PC2"]]
      .mean()
      .reset_index()
)

plt.figure(figsize=(8, 6))

plt.scatter(
    centroids["PC1"],
    centroids["PC2"],
    s=250
)

for _, row in centroids.iterrows():
    plt.text(
        row["PC1"],
        row["PC2"],
        row["genotype"]
    )

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Genotype Morphodynamic Centroids")

plt.tight_layout()

out = "figure/Fig10_genotype_centroids.png"
plt.savefig(out, dpi=300)
plt.close()

print("Saved:", out)


# FIGURE 11
# DISTANCE MATRIX
print("\nGenerating Fig11...")

feature_centroids = (
    df.groupby("genotype")[feature_cols]
      .mean()
)

scaled_centroids = StandardScaler().fit_transform(
    feature_centroids
)

dist = cdist(
    scaled_centroids,
    scaled_centroids
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    dist,
    annot=True,
    fmt=".2f",
    xticklabels=feature_centroids.index,
    yticklabels=feature_centroids.index
)

plt.title("Morphodynamic Distance Matrix")

plt.tight_layout()

out = "figure/Fig11_distance_matrix.png"
plt.savefig(out, dpi=300)
plt.close()

print("Saved:", out)


# FIGURE 12
# HIERARCHICAL CLUSTERING
print("\nGenerating Fig12...")

cluster_df = pd.DataFrame(
    scaled_centroids,
    index=feature_centroids.index,
    columns=feature_cols
)

g = sns.clustermap(
    cluster_df,
    cmap="coolwarm",
    figsize=(8, 8)
)

out = "figure/Fig12_genotype_clustering.png"

g.savefig(out, dpi=300)

plt.close("all")

print("Saved:", out)

# FIGURE 13
# FEATURE HEATMAP
print("\nGenerating Fig13...")

feature_means = (
    df.groupby("genotype")[feature_cols]
      .mean()
)

feature_scaled = pd.DataFrame(
    StandardScaler().fit_transform(feature_means),
    index=feature_means.index,
    columns=feature_cols
)

plt.figure(figsize=(10, 6))

sns.heatmap(
    feature_scaled,
    cmap="coolwarm",
    center=0,
    annot=True,
    fmt=".2f"
)

plt.title("Genotype Feature Heatmap")

plt.tight_layout()

out = "figure/Fig13_feature_heatmap.png"

plt.savefig(out, dpi=300)
plt.close()

print("Saved:", out)

loadings = pd.DataFrame(
    pca.components_.T,
    columns=["PC1", "PC2"],
    index=feature_cols
)

loadings.to_csv(
    "analysis/final_PCA_loadings.csv"
)

print("\nSaved:")
print("analysis/final_PCA_loadings.csv")

print("\nALL FIGURES COMPLETE")
