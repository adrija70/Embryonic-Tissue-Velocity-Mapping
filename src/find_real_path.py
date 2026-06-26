# src/10f_find_real_path.py

import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

for root, dirs, files in os.walk(
    os.path.join(PROJECT_ROOT, "data")
):
    mat_files = [f for f in files if f.endswith(".mat")]

    if len(mat_files) > 0:
        print("\nDIRECTORY:")
        print(root)

        print("\nFIRST FILE:")
        print(mat_files[0])

        print("\nTOTAL FILES:")
        print(len(mat_files))

        break
