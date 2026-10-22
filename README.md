# COMSOL Learning

Personal practice models and helper scripts from learning COMSOL Multiphysics.

## Layout

```
schottky/                Schottky contact (Semiconductor Module tutorial)
  models/                schottky_contact_practice.mph   (not tracked)
  tutorials/             models.semicond.schottky_contact.pdf (not tracked)
sic/                     SiC power-module thermal model (die-size sweep)
  models/                sic_module_validation.mph       (not tracked)
  scripts/
    sweep_with_mph.py    run the L_die sweep from Python via MPh
    plot_spreading.py    compare COMSOL Tmax with a 1D thermal-resistance estimate
  results/
    comsol_tmax.txt      exported Tmax vs. die size
    tmax_vs_die_size.png comparison plot
```

## Projects

### Schottky contact
Follows the COMSOL Application Gallery tutorial *Schottky Contact*
(Semiconductor Module). The tutorial PDF is available from the COMSOL
Application Gallery and is not redistributed here.

### SiC module thermal model
3D steady-state heat transfer through a SiC die / SAC305 solder / DBC
(Cu–Al2O3–Cu) stack, 100 W dissipation, convective cooling
h = 1e4 W/(m²·K) at 25 °C. The die side length `L_die` is swept from
3 to 10 mm and the maximum temperature is compared against a 1D estimate
that ignores heat spreading.

```bash
pip install -r requirements.txt
cd sic/results
python ../scripts/sweep_with_mph.py ../models/sic_module_validation.mph   # needs COMSOL
python ../scripts/plot_spreading.py comsol_tmax.txt                      # plot only
```

Before running the sweep from Python, disable the Parametric Sweep in
Study 1 and save the model, otherwise it overrides the value set from Python.

## Model files (`.mph`)

`.mph` files are not tracked in git: they are large binaries (tens of MB
with solutions and meshes) that git cannot diff. To share a model, either
- save a slim copy (*File > Compact History*, then *Study > Clear All Solutions*
  and *Clear All Meshes* before saving), or
- track them with [Git LFS](https://git-lfs.com/).
