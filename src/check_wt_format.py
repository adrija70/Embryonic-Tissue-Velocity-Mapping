# src/10d_check_wt_format.py

import os
import glob
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

wt_files = sorted(glob.glob(os.path.join(DATA_DIR, "WT*.mat")))

for path in wt_files:

    print("\n" + "="*80)

    fname = os.path.basename(path)

    print(fname)

    mat = scipy.io.loadmat(path)

    keys = [
        k for k in mat.keys()
        if not k.startswith("__")
    ]

    print(keys)
