# src/10c_debug_one_embryo.py

import os
import scipy.io
import numpy as np
from scipy.ndimage import gaussian_filter

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

path = os.path.join(
    PROJECT_ROOT,
    "data",
    "piv_data",
    "[INTERNAL] PIVlab_results",
    "WT_202001101100_PIVlab.mat"
)

mat = scipy.io.loadmat(path)

print(mat.keys())

u = mat["u_original"]
v = mat["v_original"]

print("u shape:", u.shape)
print("v shape:", v.shape)

if u.shape[0] < 100:
    u = np.transpose(u, (2,0,1))
    v = np.transpose(v, (2,0,1))

print("after transpose:", u.shape)

u0 = gaussian_filter(u[0], sigma=1)
v0 = gaussian_filter(v[0], sigma=1)

print("frame shape:", u0.shape)

x = mat["x"]
y = mat["y"]

print("x shape:", x.shape)
print("y shape:", y.shape)

dx = np.mean(np.diff(x, axis=1))
dy = np.mean(np.diff(y, axis=0))

print("dx =", dx)
print("dy =", dy)

du_dx = np.gradient(u0, dx, axis=1)

print("SUCCESS")
