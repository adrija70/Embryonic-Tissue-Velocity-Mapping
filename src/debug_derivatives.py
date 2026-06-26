from pathlib import Path
import scipy.io as sio
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    PROJECT_DIR
    / "data"
    / "piv_data"
    / "[INTERNAL] PIVlab_results"
)

mat_file = DATA_DIR / "WT_202001101100_PIVlab.mat"

data = sio.loadmat(mat_file)

x = data["xx"]
y = data["yy"]

print("x[:,0] diff mean =", np.mean(np.diff(x[:,0])))
print("x[0,:] diff mean =", np.mean(np.diff(x[0,:])))

print("y[:,0] diff mean =", np.mean(np.diff(y[:,0])))
print("y[0,:] diff mean =", np.mean(np.diff(y[0,:])))