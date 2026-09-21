"""Read the bundled raw OpenFOAM snapshot and plot cell-centred velocity samples."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from fluidfoam import readmesh, readvector


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=root / "OFBackups/OFData")
    parser.add_argument("--time", default="429")
    parser.add_argument("--output", type=Path, default=Path("outputs/sample.svg"))
    args = parser.parse_args()
    x, y, z = readmesh(str(args.case))
    velocity = readvector(str(args.case), args.time, "U")
    # Select the available cell-centre layer closest to the centre of the z extent.
    centre = (z.min()+z.max())/2
    zplane = z[np.argmin(np.abs(z-centre))]
    mask = np.isclose(z, zplane, rtol=0, atol=max(np.ptp(z)*1e-7, 1e-9))
    if np.count_nonzero(mask) < 3:
        parser.error("the selected case has no sufficiently populated z layer")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)
    field = ax.scatter(x[mask], y[mask], c=velocity[0, mask], s=7, cmap="viridis", linewidths=0)
    ax.set(xlabel="x [case units]", ylabel="y [case units]", aspect="equal",
           title=f"Cell-centred Ux · z = {zplane:g} · time {args.time}")
    fig.colorbar(field, ax=ax, label="Ux [case velocity units]")
    fig.savefig(args.output, dpi=170)
    plt.close(fig)
    print(f"Plotted {np.count_nonzero(mask)} cell samples to {args.output.resolve()}")


if __name__ == "__main__":
    main()
