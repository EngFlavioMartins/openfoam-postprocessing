"""ParaView (pvpython) render in the OpenONDA style: OpenFOAM cell-centre samples
beside the same plane resampled onto a regular grid.

Usage: pvpython render_slice.py <output png> <samples|grid> [width height]
Reads outputs/render/{samples,grid}.vtp from compute_slice.py.

Black background. Both halves show the velocity deficit 1 - u_x/U_inf with
thesis_blue on one common range: the slow wake glows, the free stream is the
darkest teal of the map (kept visible so the sample spacing shows).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import onda_style as style  # noqa: E402
from paraview.simple import Calculator, Glyph, Show, XMLPolyDataReader  # noqa: E402

out, which = Path(sys.argv[1]), sys.argv[2]
width, height = (int(a) for a in (sys.argv[3:5] if len(sys.argv) > 4 else (3000, 1875)))
DATA = HERE.parents[1] / "outputs" / "render"
U_INF, DEFICIT_MAX = 4.0, 0.6

view = style.setup_view(width, height)
lut = style.lut("deficit", "thesis_blue", 0.0, DEFICIT_MAX)

samples = Calculator(Input=XMLPolyDataReader(FileName=[str(DATA / "samples.vtp")]),
                     ResultArrayName="deficit", Function=f"1 - Ux/{U_INF}")
spheres = Glyph(Input=samples, GlyphType="Sphere")
spheres.GlyphType.Radius = 1.0
spheres.GlyphType.ThetaResolution = 16
spheres.GlyphType.PhiResolution = 16
spheres.ScaleArray = ["POINTS", "radius"]
spheres.ScaleFactor = 1.0
spheres.GlyphMode = "All Points"
if which == "samples":
    style.mapped(Show(spheres, view), "deficit", lut, roughness=0.35)

grid = Calculator(Input=XMLPolyDataReader(FileName=[str(DATA / "grid.vtp")]), AttributeType="Cell Data",
                  ResultArrayName="deficit", Function=f"1 - Ux/{U_INF}")
if which == "grid":
    d = Show(grid, view)
    style.mapped(d, "deficit", lut, assoc="CELLS")
    d.Interpolation = "Flat"
    d.Ambient, d.Diffuse = 1.0, 0.0             # unlit: the field glows
lut.RescaleTransferFunction(0.0, DEFICIT_MAX)

view.CameraPosition = [18.3, 4.7, 6.3]
view.CameraFocalPoint = [12.0, 1.3, 9.45]
view.CameraViewUp = [0, 1, 0]
view.CameraViewAngle = 30
style.save(view, out, width, height)
print(out)
