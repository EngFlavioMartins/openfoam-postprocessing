# OpenFOAM post-processing

<p align="center">
  <a href="https://github.com/EngFlavioMartins/openfoam-postprocessing/actions/workflows/example.yml"><img src="https://github.com/EngFlavioMartins/openfoam-postprocessing/actions/workflows/example.yml/badge.svg" alt="Example smoke test"></a>
  <a href="https://doi.org/10.5194/wes-10-41-2025"><img src="https://img.shields.io/badge/paper-10.5194%2Fwes--10--41--2025-1F6FEB" alt="paper: 10.5194/wes-10-41-2025"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white" alt="python: 3.10+"></a>
  <a href="https://github.com/EngFlavioMartins/openfoam-postprocessing/blob/HEAD/LICENSE"><img src="https://img.shields.io/badge/license-MIT-2E7D32" alt="license: MIT"></a>
  <a href="https://engflaviomartins.github.io/#openfoam-postprocessing"><img src="https://img.shields.io/badge/website-research%20page-15212B" alt="website: research page"></a>
</p>

**From OpenFOAM cell data to regular NumPy grids.**

<p align="center"><img src="docs/assets/render.webp" width="560" alt="One wake plane: OpenFOAM cell centres on the left and the same velocity deficit on a regular grid on the right"></p>

Read OpenFOAM fields with [fluidfoam](https://fluidfoam.readthedocs.io/) and resample them onto regular arrays with local radial-basis interpolation, ready for profiles and planar sections. A rotor-wake snapshot is included; no OpenFOAM installation is needed to read it.

## Get started

```bash
git clone https://github.com/EngFlavioMartins/openfoam-postprocessing.git
cd openfoam-postprocessing
pip install -r requirements.txt
python examples/plot_sample.py
```

This plots one plane of the bundled snapshot to `outputs/sample.svg`. The notebooks [Creating_Backups.ipynb](Creating_Backups.ipynb) and [Examples.ipynb](Examples.ipynb) show the full workflow.

## Make the figure above

```bash
sh scripts/render/make_figure.sh
```

You need [ParaView](https://www.paraview.org/download/) (for `pvpython`), a LaTeX installation, and `pip install pyvista pillow`.

## Cite

The bundled data comes from the work below. If you use the data or this workflow, please cite:

```bibtex
@article{martins2025multirotor,
  author  = {Martins, Flavio A. C. and van Zuijlen, A. and Ferreira, C. S.},
  title   = {Proof of Concept for Multirotor Systems with Vortex-Generating Modes for Regenerative Wind Energy: A Study Based on Numerical Simulations and Experimental Data},
  journal = {Wind Energy Science},
  volume  = {10},
  pages   = {41--58},
  year    = {2025},
  doi     = {10.5194/wes-10-41-2025}
}
```

GitHub's **Cite this repository** button (from [CITATION.cff](CITATION.cff)) gives the same reference in other formats.

## Licence

MIT; see [LICENSE](LICENSE).
