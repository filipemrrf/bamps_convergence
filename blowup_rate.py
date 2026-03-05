import pymuninn
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

file = "temp_results/hyp_layers_cubic_wave_pconvergence-cartoon_x/hyp_layers_cubic_wave_pconvergence-cartoon_x-np=29/output_1d/x/u.psi"   # your input files
data = pymuninn.MuninnData(file)
grid = data.as_grid()

t = grid.ts
psi = [grid.values[i][0] for i in range(len(grid.ts))]

T_blowup, pcov = curve_fit(lambda tm, tb: (np.sqrt(2)/(tb-tm)), t[1:-1], psi[1:-1], nan_policy='raise')
print(f"T_Blowup: {T_blowup} \t cov: {pcov}")
tbar = []

for ti in t:
    tbar.append(1.0 / (T_blowup - ti))

plt.figure(figsize=(8, 6))
plt.plot(tbar, psi, label="$numerics$")
plt.plot(tbar, np.sqrt(2) * np.array(tbar), '--', label="theory")

plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"$1 / (t_{blowup} - t)$", fontsize=14)
plt.ylabel(r"$\psi$", fontsize=14)
plt.ylim(top=1e6)

plt.grid(True, which="both", ls="--", lw=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("temp_results/blowup_rate.png")

