"""Animation for the README: a resampled cross-flow plane travelling down the bundled rotor wake.

Reads the bundled snapshot (OFBackups/OFData, time 429) with fluidfoam and resamples the
streamwise velocity onto a regular 3D grid around the wake (x = 9-38, y = 0-2.5, z = 8-12) with
the settings of Libs/Subroutines.interpolateToStructuredMesh (scipy RBFInterpolator, five
neighbours, linear kernel). ParaView (render_animation.py) then draws a faint isosurface of the
wake and the grid plane x = const, coloured by the velocity deficit 1 - u_x/U_inf, moving
downstream. Writes docs/assets/animation.webp.
Run:  python scripts/render/make_animation.py   (needs ParaView; set PVPYTHON if it is not found)
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pyvista as pv
from fluidfoam import readmesh, readvector
from PIL import Image
from scipy.interpolate import RBFInterpolator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from gif import crop_union, pvpython, save_gif  # noqa: E402

CASE, TIME = ROOT / "OFBackups" / "OFData", "429"
U_INF = 4.0
X_RANGE, Y_RANGE, Z_RANGE = (9.0, 38.0), (0.0, 2.5), (8.0, 12.0)
DX, DYZ, FRAMES = 0.1, 0.04, 120

x, y, z = readmesh(str(CASE))
ux = readvector(str(CASE), TIME, "U")[0]
box = ((x > X_RANGE[0] - 1) & (y < Y_RANGE[1] + 0.3) & (z > Z_RANGE[0] - 0.3) & (z < Z_RANGE[1] + 0.3))
rbf = RBFInterpolator(np.column_stack([x[box], y[box], z[box]]), ux[box], neighbors=5, kernel="linear", epsilon=20)

dims = [int(round((r[1] - r[0]) / d)) + 1 for r, d in zip((X_RANGE, Y_RANGE, Z_RANGE), (DX, DYZ, DYZ))]
grid = pv.ImageData(dimensions=dims, spacing=(DX, DYZ, DYZ), origin=(X_RANGE[0], Y_RANGE[0], Z_RANGE[0]))
grid["deficit"] = 1 - rbf(grid.points) / U_INF
print(f"resampled {grid.n_points} grid points")

with tempfile.TemporaryDirectory() as tmp:
    grid.save(Path(tmp) / "wake.vti")
    subprocess.run([pvpython(), str(HERE / "render_animation.py"), str(Path(tmp) / "wake.vti"), tmp, str(FRAMES)],
                   check=True)
    frames = crop_union([Image.open(p) for p in sorted(Path(tmp).glob("frame_*.png"))])
save_gif(frames, ROOT / "docs" / "assets" / "animation.webp", fps=20, width=840, hold=1.0)
