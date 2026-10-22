"""1D finite volume solver for steady heat conduction through the SiC module stack.

Each cell is a small slab. Between two neighbouring cells there is a thermal
resistance, exactly like the hand calculation, just with many thin slabs
instead of five thick ones. Heat balance in each cell gives one linear equation.
"""
import numpy as np

# ---------------- problem definition ----------------
A = (10e-3) ** 2                    # cross-section area, m^2
P = 100.0                           # die power, W
h, T_cool = 1e4, 25.0               # bottom convection, W/(m^2 K), degC

# layers from bottom (z = 0) to top: (name, thickness m, k W/(m K), heated?)
layers = [
    ("Cu bottom", 0.3e-3,  390, False),
    ("Al2O3",     0.38e-3,  24, False),
    ("Cu top",    0.3e-3,  390, False),
    ("SAC305",    0.1e-3,   58, False),
    ("SiC die",   0.2e-3,  370, True),
]
n_per_layer = 20                    # cells per layer (try 2, 5, 20, 100)

# ---------------- 1. mesh: list of cells ----------------
dz, k, q = [], [], []               # cell thickness, conductivity, heat generated in cell (W)
for name, t, kk, heated in layers:
    for _ in range(n_per_layer):
        dz.append(t / n_per_layer)
        k.append(kk)
        q.append(P / n_per_layer if heated else 0.0)
dz, k, q = map(np.array, (dz, k, q))
N = len(dz)

# ---------------- 2. resistance between neighbouring cell centres ----------------
# from centre of cell i to centre of cell i+1: half of cell i + half of cell i+1 in series
R_face = (dz[:-1] / 2) / (k[:-1] * A) + (dz[1:] / 2) / (k[1:] * A)
G_face = 1 / R_face                 # conductance, W/K

# bottom: from centre of cell 0 to the coolant, half cell + convection in series
G_bottom = 1 / ((dz[0] / 2) / (k[0] * A) + 1 / (h * A))

# ---------------- 3. assemble  M @ T = b  (heat balance in every cell) ----------------
# heat out of cell i to each neighbour j = G (T_i - T_j); sum of heat out = heat generated
M = np.zeros((N, N))
b = q.copy()
for i in range(N - 1):              # each interior face couples cell i and i+1
    g = G_face[i]
    M[i, i] += g;  M[i, i + 1] -= g
    M[i + 1, i + 1] += g;  M[i + 1, i] -= g
M[0, 0] += G_bottom                 # bottom face: heat lost to coolant
b[0] += G_bottom * T_cool
# top face is insulated: nothing to add

# ---------------- 4. solve ----------------
T = np.linalg.solve(M, b)

# temperature on the insulated top surface (extrapolate half a cell; no flux through it)
print(f"cells: {N}")
print(f"T at top cell centre : {T[-1]:.3f} degC")
print(f"T bottom cell centre : {T[0]:.3f} degC")
print("hand calculation     : Tmax = 144.37 degC, bottom surface = 125.00 degC")
