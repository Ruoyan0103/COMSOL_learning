"""Run the die-size sweep from Python with MPh (pip install mph).

Before running: in COMSOL, right-click Study 1 > Parametric Sweep > Disable, then save.
(Otherwise the sweep inside the model overrides the value set from Python.)

Usage:
    cd sic/results && python ../scripts/sweep_with_mph.py ../models/sic_module_validation.mph
"""
import sys
import numpy as np
import mph

client = mph.start(cores=4)
model = client.load(sys.argv[1])

rows = []
for L_die in np.arange(3, 10.01, 0.5):            # mm
    model.parameter("L_die", f"{L_die}[mm]")
    model.build()                                  # rebuild geometry
    model.mesh()                                   # remesh
    model.solve("Study 1")
    T = model.evaluate("T", "degC")                # temperature at mesh nodes
    rows.append((L_die, float(np.max(T))))
    print(f"L_die = {L_die:4.1f} mm  ->  Tmax = {rows[-1][1]:.2f} degC")

np.savetxt("comsol_tmax.txt", rows, header="L_die_mm  Tmax_degC", comments="% ")
print("Saved comsol_tmax.txt  ->  now run: python ../scripts/plot_spreading.py comsol_tmax.txt")
