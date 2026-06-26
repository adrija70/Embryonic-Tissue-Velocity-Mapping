# src/10g_test_feature_extraction.py

import scipy.io
import numpy as np
from scipy.ndimage import gaussian_filter

mat_file = (
    "data/piv_data/[INTERNAL] PIVlab_results/"
    "WT_202001101100_PIVlab.mat"
)

mat = scipy.io.loadmat(mat_file)

u = mat["u_filt_lst"]
v = mat["v_filt_lst"]

print("u shape:", u.shape)
print("v shape:", v.shape)

u0 = gaussian_filter(u[0], sigma=1.5)
v0 = gaussian_filter(v[0], sigma=1.5)

speed = np.sqrt(u0**2 + v0**2)

print()
print("mean_speed =", np.mean(speed))
print("std_speed  =", np.std(speed))
print("p95_speed  =", np.percentile(speed,95))
