"""ParaView (pvpython) animation frames: a grid plane travelling down the resampled wake.

Usage: pvpython render_animation.py <wake.vti> <frame directory> [frames]
Black background. The plane x = const of the regular grid glows with thesis_blue (velocity
deficit, on the range of the still figure) and moves from just behind the rotors to the end of
the domain; as it passes each station it leaves a copy behind, so the wake builds up as a row
of planes. A thin grey box outlines the resampled region.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
import onda_style as style  # noqa: E402
from paraview.simple import Hide, Outline, Show, Slice, XMLImageDataReader  # noqa: E402

src, out = Path(sys.argv[1]), Path(sys.argv[2])
frames = int(sys.argv[3]) if len(sys.argv) > 3 else 120
width, height = 1800, 1000
DEFICIT_MAX = 0.6
STATIONS = [10.0, 12.0, 15.0, 19.0, 24.0, 30.0, 36.0]

view = style.setup_view(width, height)
wake = XMLImageDataReader(FileName=[str(src)])
wake.UpdatePipeline()
x0, x1 = wake.GetDataInformation().GetBounds()[:2]
lut = style.lut("deficit", "thesis_blue", 0.0, DEFICIT_MAX)


def glowing_slice(x):
    s = Slice(Input=wake)
    s.SliceType = "Plane"
    s.SliceType.Origin = [x, 1.25, 10.0]
    s.SliceType.Normal = [1, 0, 0]
    d = Show(s, view)
    style.mapped(d, "deficit", lut)
    d.Interpolation = "Flat"
    d.Ambient, d.Diffuse = 1.0, 0.0             # unlit: the field glows
    return s, d


box = Show(Outline(Input=wake), view)
box.AmbientColor = box.DiffuseColor = [0.35, 0.37, 0.38]
moving, _ = glowing_slice(x0 + 0.4)
kept = [glowing_slice(x)[1] for x in STATIONS]
lut.RescaleTransferFunction(0.0, DEFICIT_MAX)

view.CameraFocalPoint = [23.5, 1.25, 10.0]
view.CameraPosition = [23.5 - 13.0, 1.25 + 9.0, 10.0 - 15.0]   # from upstream, above and to the side
view.CameraViewUp = [0, 1, 0]
view.CameraViewAngle = 30
view.ResetCamera(False)
view.GetActiveCamera().Dolly(1.25)
out.mkdir(parents=True, exist_ok=True)
s = np.linspace(0, 1, frames)
for k, f in enumerate(s * s * (3 - 2 * s)):
    x = x0 + 0.4 + (x1 - x0 - 0.8) * f
    moving.SliceType.Origin = [x, 1.25, 10.0]
    for station, d in zip(STATIONS, kept):
        (Show if station <= x else Hide)(d.Input, view)
    style.save(view, out / f"frame_{k:03d}.png", width, height)
    print(k, end=" ", flush=True)
print()
