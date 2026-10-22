"""Compare COMSOL 3D results with the 1D thermal-resistance estimate.

Usage:
    cd sic/results && python ../scripts/plot_spreading.py comsol_tmax.txt

comsol_tmax.txt is the table exported from COMSOL (two columns: L_die in mm, Tmax in degC).
Lines starting with % are COMSOL header lines and are skipped.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

# ---- model parameters (same as in COMSOL) ----
L = 10e-3                      # DBC side length, m
P, h, T_cool = 100.0, 1e4, 25.0
layers = [  # thickness m, k W/(m K), uniformly heated?
    (0.2e-3, 370, True),   # SiC die
    (0.1e-3,  58, False),  # SAC305 solder
    (0.3e-3, 390, False),  # Cu top
    (0.38e-3, 24, False),  # Al2O3
    (0.3e-3, 390, False),  # Cu bottom
]

def tmax_1d(L_die):
    """1D estimate: conduction through die-sized column, convection over full base."""
    A_die = L_die ** 2
    R_cond = sum(t / (k * A_die) / (2 if heated else 1) for t, k, heated in layers)
    R_conv = 1 / (h * L ** 2)
    return T_cool + P * (R_cond + R_conv)

# ---- COMSOL data ----
data = np.loadtxt(sys.argv[1], comments="%")
L_die_mm, T_comsol = data[:, 0], data[:, 1]

L_fine = np.linspace(L_die_mm.min(), L_die_mm.max(), 200)
T_1d = [tmax_1d(x * 1e-3) for x in L_fine]

# ---- print comparison table ----
print(f"{'L_die (mm)':>10} {'COMSOL':>9} {'1D':>9} {'1D overestimate of conduction dT':>34}")
for x, tc in zip(L_die_mm, T_comsol):
    t1 = tmax_1d(x * 1e-3)
    base = T_cool + P / (h * L ** 2)          # mean bottom temperature = 125 degC
    print(f"{x:10.1f} {tc:9.1f} {t1:9.1f} {(t1 - base) / (tc - base):33.2f}x")

# ---- plot ----
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(L_fine, T_1d, "--", color="gray", label="1D estimate (no spreading)")
ax.plot(L_die_mm, T_comsol, "o-", color="C0", label="COMSOL 3D")
ax.set_xlabel("Die side length (mm)")
ax.set_ylabel(r"$T_\mathrm{max}$ (°C)")
ax.set_title("Junction temperature vs. die size")
ax.legend(frameon=False)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("tmax_vs_die_size.png", dpi=200)
print("Saved tmax_vs_die_size.png")
