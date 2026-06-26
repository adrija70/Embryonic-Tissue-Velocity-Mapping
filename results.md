# Results

## Summary

The analysis pipeline transforms PIV-derived velocity fields into quantitative morphodynamic descriptors capable of characterizing embryonic development across multiple spatial and temporal scales. By integrating velocity, divergence, and vorticity measurements with dimensionality reduction and atlas construction approaches, the workflow provides a framework for developmental-state modeling, comparative embryology, and genotype-level phenotypic analysis. This document summarizes the quantitative analysis of embryonic tissue dynamics using Particle Image Velocimetry (PIV)-derived velocity fields.

---

## Velocity Field Reconstruction Reveals Coordinated Tissue Motion

Particle Image Velocimetry was used to reconstruct tissue-scale velocity fields from embryonic imaging data. Spatial velocity maps reveal coordinated directional movements across the embryo and capture large-scale tissue rearrangements occurring during development.

### Velocity Magnitude Map

![Velocity Magnitude Map](figure/Fig1A_velocity_map.png)

### Velocity Vector Field

Velocity vector fields illustrate the magnitude and direction of tissue motion, highlighting regions of coordinated flow and spatially heterogeneous dynamics.

![Velocity Vector Field](figure/Fig1B_velocity_map_vectors.png)

---

## Temporal Changes in Tissue Speed During Development

Mean tissue speed was quantified across the imaging sequence to characterize developmental dynamics. Temporal analysis reveals periods of elevated coordinated motion interspersed with relatively stable developmental intervals.

### Mean Tissue Speed

![Mean Tissue Speed](figure/mean_speed_vs_time.png)

### Developmental Trajectory

Developmental trajectories reconstructed in morphodynamic space reveal transitions between developmental states over time.

![Developmental Trajectory](figure/Fig5_developmental_trajectory.png)

---

## Divergence Analysis Identifies Regions of Tissue Expansion and Contraction

Spatial derivatives of the velocity field were used to estimate tissue divergence. Positive divergence values correspond to local tissue expansion, whereas negative values indicate tissue convergence.

![Divergence Maps](figure/Fig2_divergence_maps.png)

---

## Vorticity Mapping Reveals Rotational Tissue Dynamics

Vorticity analysis quantifies rotational components of tissue motion. Elevated vorticity regions identify localized rotational flows and complex tissue rearrangements.

![Vorticity Maps](figure/Fig3_vorticity_maps.png)

---

## Morphodynamic Feature Extraction Captures Developmental State

Quantitative descriptors derived from velocity, divergence, and vorticity fields were integrated into a morphodynamic feature space and analyzed using Principal Component Analysis (PCA).

### Morphodynamic PCA

![Morphodynamic PCA](figure/Fig4_morphodynamic_PCA.png)

### PCA Explained Variance

The first principal components capture the majority of morphodynamic variation across developmental stages.

![PCA Variance](figure/Fig6_PCA_variance.png)

---

## Construction of a Wild-Type Morphodynamic Atlas

Feature extraction across wild-type embryos enabled the generation of a reference morphodynamic atlas describing normal developmental progression.

### Wild-Type Morphodynamic Atlas

![WT Atlas](figure/Fig7_WT_morphodynamic_atlas.png)

### Wild-Type Developmental Trajectory

Wild-type embryos follow reproducible developmental trajectories through morphodynamic feature space.

![WT Trajectory](figure/Fig9_WT_trajectory.png)

---

## Multi-Embryo Integration Reveals Shared Developmental Trajectories

Integration of multiple embryos within a common morphodynamic framework revealed conserved developmental programs despite biological variability.

---

## Multi-Genotype Atlas Reveals Distinct Dynamic Phenotypes

Extension of the atlas to multiple genotypes revealed genotype-specific developmental trajectories and dynamic phenotypes.

### Multi-Genotype Morphodynamic Atlas

![Multi-Genotype Atlas](figure/Fig8_multigenotype_atlas.png)

### Genotype Morphodynamic Centroids

Distinct genotype centroids indicate that tissue dynamics can serve as quantitative developmental phenotypes.

![Genotype Centroids](figure/Fig10_genotype_centroids.png)

---

## Feature Similarity Analysis Identifies Relationships Between Genotypes

Pairwise comparison of morphodynamic features generated similarity and distance matrices that revealed relationships among developmental conditions.

### Morphodynamic Distance Matrix

![Distance Matrix](figure/Fig11_distance_matrix.png)

### Hierarchical Genotype Clustering

Clustering analyses identified groups of genotypes sharing related tissue dynamic signatures while separating phenotypically distinct populations.

![Genotype Clustering](figure/Fig12_genotype_clustering.png)

### Genotype Feature Heatmap

![Feature Heatmap](figure/Fig13_feature_heatmap.png)


