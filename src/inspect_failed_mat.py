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

TARGET = "toll[RM9]_202101111920_PIVlab.mat"

path = os.path.join(DATA_DIR, TARGET)

print("Loading:")
print(path)

mat = scipy.io.loadmat(path)

print("\nVARIABLES FOUND:\n")

for key in mat.keys():

    if key.startswith("__"):
        continue

    obj = mat[key]

    try:
        print(key, obj.shape)
    except Exception:
        print(key, type(obj))
