"""Add the LaTeX overlay (half labels and the deficit colour bar) to the slice render.

Usage: python compose_slice.py <raw png> <output stem>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from overlay import compose  # noqa: E402

raw, stem = Path(sys.argv[1]), Path(sys.argv[2])
compose(raw, stem,
        bar=dict(name="thesis_blue", vmin=0, vmax=0.6, x=70, y=10, height=24, title=r"$1-u_x/U_\infty$",
                 ticks=[(0.0, "0"), (1.0, "0.6")]),
        labels=[(4, 52.5, "Cell centres", "north west"), (38, 52.5, "Regular grid", "north west")])
