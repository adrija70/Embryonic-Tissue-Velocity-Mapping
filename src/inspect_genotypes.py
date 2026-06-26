# src/10b_inspect_genotypes.py

import os
import scipy.io

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "piv_data",
    "[INTERNAL] PIVlab_results"
)

targets = [
    "spaetzle[A]_201712191340_PIVlab.mat",
    "halo_snail[IIG05]_202101281300_PIVlab.mat",
    "halo_twist[ey53]_202007171100_PIVlab.mat"
]

for fname in targets:

    print("\n" + "=" * 60)
    print(fname)

    path = os.path.join(DATA_DIR, fname)

    mat = scipy.io.loadmat(path)

    for key in mat.keys():

        if key.startswith("__"):
            continue

        obj = mat[key]

        try:
            print(key, obj.shape)
        except:
            print(key)
