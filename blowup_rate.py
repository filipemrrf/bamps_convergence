import pymuninn
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

file = "temp_results/hyp_layers_cubic_wave_pconvergence-cartoon_x/hyp_layers_cubic_wave_pconvergence-cartoon_x-np=29/output_1d/x/u.psi"   # your input files
data = pymuninn.MuninnData(file)
grid = data.as_grid()

t = np.array(grid.ts)
psi = np.array([grid.values[i][0] for i in range(len(grid.ts))])
logpsim1 = np.log(1/psi)

start = int(0.7 * len(t))

Tb_local = t[start:] + np.sqrt(2)/psi[start:]

# Fit quadratic trend in tail
x = t[start:]
y = Tb_local

coeff = np.polyfit(x, y, 2)

# Extrapolate to t = max(t)
T_blowup = np.polyval(coeff, np.max(t))
print(T_blowup)

tbar = 1.0 / (T_blowup - t)

plt.figure(figsize=(8, 6))
plt.plot(tbar, psi, 'o', label="$numerics$")
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

