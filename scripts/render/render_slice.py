"""ParaView (pvpython) render: cell-centre samples beside the resampled regular grid.

Usage: pvpython render_slice.py <output png> [width height]
Reads outputs/render/{samples,grid}.vtp from compute_slice.py.
Colour: Ux with Crameri's "lajolla" (dark = slow wake), common to both halves.
"""
import json
import sys
from pathlib import Path

from paraview.simple import (ColorBy, GetActiveViewOrCreate, GetColorTransferFunction, Glyph,
                             SaveScreenshot, Show, XMLPolyDataReader)

out = Path(sys.argv[1])
width, height = (int(a) for a in (sys.argv[2:4] if len(sys.argv) > 3 else (2400, 1600)))
HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "outputs" / "render"
cmap = json.loads((HERE / "lajolla.json").read_text())

view = GetActiveViewOrCreate("RenderView")
view.ViewSize = [width, height]
view.OrientationAxesVisibility = 0
view.UseColorPaletteForBackground = 0
view.Background = [1, 1, 1]
view.EnableRayTracing = 1
view.BackEnd = "OSPRay raycaster"
view.SamplesPerPixel = 32
view.AmbientSamples = 8

lut = GetColorTransferFunction("Ux")
lut.RGBPoints = cmap["lajolla"]
lut.ColorSpace = "RGB"
lut.AutomaticRescaleRangeMode = "Never"

spheres = Glyph(Input=XMLPolyDataReader(FileName=[str(DATA / "samples.vtp")]), GlyphType="Sphere")
spheres.GlyphType.Radius = 1.0
spheres.GlyphType.ThetaResolution = 16
spheres.GlyphType.PhiResolution = 16
spheres.ScaleArray = ["POINTS", "radius"]
spheres.ScaleFactor = 1.0
spheres.GlyphMode = "All Points"
d = Show(spheres, view)
ColorBy(d, ("POINTS", "Ux"))
d.LookupTable = lut
d.SetScalarBarVisibility(view, False)
d.Specular, d.SpecularPower = 0.4, 40

d = Show(XMLPolyDataReader(FileName=[str(DATA / "grid.vtp")]), view)
ColorBy(d, ("CELLS", "Ux"))
d.LookupTable = lut
d.SetScalarBarVisibility(view, False)
d.Ambient, d.Diffuse = 0.4, 0.6
lut.RescaleTransferFunction(*cmap["range"])

view.CameraPosition = [17.0, 4.6, 6.2]
view.CameraFocalPoint = [12.0, 1.3, 10.0]
view.CameraViewUp = [0, 1, 0]
view.CameraViewAngle = 30
SaveScreenshot(str(out), view, ImageResolution=[width, height], TransparentBackground=0)
print(out)
