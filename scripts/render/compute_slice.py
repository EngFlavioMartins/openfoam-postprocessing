"""Geometry for the website render: from OpenFOAM cell centres to a regular grid.

Reads the bundled snapshot (OFBackups/OFData, time 429) with fluidfoam and
takes the cross-flow plane x = X0 over the README's example region
(y = 0.2-2.5, z = 8-12). Writes for ParaView:
  samples.vtp  cell centres within half a fine cell of the plane, z >= Z_SPLIT,
               with Ux and a display radius from the local sample spacing
  grid.vtp     Ux resampled onto a regular grid (spacing DX) for z < Z_SPLIT,
               one quad per grid cell, shrunk slightly so the grid reads
The resampler uses the settings of Libs/Subroutines.interpolateToStructuredMesh:
scipy RBFInterpolator, five neighbours, linear kernel.
"""
from pathlib import Path

import numpy as np
import pyvista as pv
from fluidfoam import readmesh, readvector
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "render"
CASE, TIME = ROOT / "OFBackups" / "OFData", "429"
X0, Y_RANGE, Z_RANGE, Z_SPLIT, DX, LAYER = 12.0, (0.2, 2.5), (8.0, 12.0), 10.0, 0.06, 0.03

x, y, z = readmesh(str(CASE))
U = readvector(str(CASE), TIME, "U")

# raw samples: the cell centres closest to the plane
near = (np.abs(x - X0) < LAYER) & (y > Y_RANGE[0]) & (y < Y_RANGE[1]) & (z >= Z_SPLIT) & (z < Z_RANGE[1])
yz = np.column_stack([y[near], z[near]])
spacing = cKDTree(yz).query(yz, k=2)[0][:, 1]
samples = pv.PolyData(np.column_stack([np.full(near.sum(), X0), yz]))
samples["Ux"] = U[0, near]
samples["radius"] = 0.32 * spacing
print(f"{near.sum()} cell-centre samples")

# resampled grid, using the cell centres of a slab around the plane
slab = np.abs(x - X0) < 0.5
rbf = RBFInterpolator(np.column_stack([x[slab], y[slab], z[slab]]), U[0, slab], neighbors=5, kernel="linear", epsilon=20)
yg = np.arange(Y_RANGE[0], Y_RANGE[1] + 1e-9, DX)
zg = np.arange(Z_RANGE[0], Z_SPLIT + 1e-9, DX)
Yc, Zc = np.meshgrid(0.5 * (yg[1:] + yg[:-1]), 0.5 * (zg[1:] + zg[:-1]), indexing="ij")
ux = rbf(np.column_stack([np.full(Yc.size, X0), Yc.ravel(), Zc.ravel()]))
h = 0.46 * DX                                   # half-size of each drawn quad (gap of 0.08 DX)
pts, faces = [], []
for i, (yc, zc) in enumerate(zip(Yc.ravel(), Zc.ravel())):
    pts.extend([[X0, yc - h, zc - h], [X0, yc - h, zc + h], [X0, yc + h, zc + h], [X0, yc + h, zc - h]])
    faces.append([4, 4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3])
grid = pv.PolyData(np.array(pts), faces=np.hstack(faces))
grid.cell_data["Ux"] = ux
print(f"{Yc.size} grid cells at spacing {DX}")

OUT.mkdir(parents=True, exist_ok=True)
samples.save(OUT / "samples.vtp")
grid.save(OUT / "grid.vtp")
print("wrote", OUT)
