"""Add the LaTeX overlay (half labels and the deficit colour bar) to the slice render.

Usage: python compose_slice.py <samples png> <grid png> <output stem>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from overlay import compose  # noqa: E402

samples, grid, stem = (Path(a) for a in sys.argv[1:4])
compose([(samples, "Cell centres"), (grid, "Regular grid")], stem, layout="row",
        bar=dict(name="thesis_blue", vmin=0, vmax=0.6, title=r"$1-u_x/U_\infty$", ticks=[(0.0, "0"), (1.0, "0.6")]))
