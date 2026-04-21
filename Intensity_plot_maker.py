import pymuninn
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Gets the muninn data
file = "results/hyp_layers_wave_pconvergence-cartoon_xz/hyp_layers_wave_pconvergence-cartoon_xz-np=21/output_1d/z/u.psi"
data = pymuninn.MuninnData(file)
grid = data.as_grid()

Z = grid.values
X = grid.xss[0]
Y = grid.ts

vmax = np.max(np.abs(Z))

norm = mcolors.SymLogNorm(
    linthresh=5e-2,   # region around 0 that's linear (tune this!)
    linscale=1,
    vmin=-vmax,
    vmax=vmax
)

plt.figure(figsize=(8, 6))

mesh = plt.pcolormesh(
    X, Y, Z,
    cmap="RdBu_r",
    norm=norm,
    shading='auto'
)

cbar = plt.colorbar(mesh)
cbar.set_label(r"$\psi$", fontsize=14)
cbar.ax.tick_params(labelsize=12)

plt.xlabel(r"$z$", fontsize=14)
plt.ylabel(r"$t$", fontsize=14)
plt.ylim(0, 35)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.grid(True, which="both", ls="--", lw=0.5)
plt.tight_layout()
plt.savefig("temp_results/hyp_layers_perturbation_z_intensity.png", dpi=300)