import pymuninn
import matplotlib.pyplot as plt
import numpy as np

# Gets the muninn data
file = "results/hyp_wave_pconvergence-cartoon_x/hyp_wave_pconvergence-cartoon_x-np=23/output_1d/x/u.psi"
data = pymuninn.MuninnData(file)
grid = data.as_grid()

# Plots the data
plt.figure(figsize=(8, 6))
plt.pcolormesh(grid.xss[0], grid.ts, grid.values)

plt.xlabel(r"$r$", fontsize=14)
plt.ylabel(r"$t$", fontsize=14)
plt.ylim(0, 35)
plt.grid(True, which="both", ls="--", lw=0.5)
plt.tight_layout()
plt.savefig("temp_results/hyp_wave_intensity.png")