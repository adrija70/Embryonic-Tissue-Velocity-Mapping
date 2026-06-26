# src/10e_find_wt_files.py

import os
import glob

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "piv_data",
    "[INTERNAL] PIVlab_results"
)

print("DATA_DIR:")
print(DATA_DIR)
print()

files = glob.glob(os.path.join(DATA_DIR, "*.mat"))

print("TOTAL MAT FILES:", len(files))
print()

for f in sorted(files):
    print(os.path.basename(f))
