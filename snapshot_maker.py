import pymuninn
import matplotlib.pyplot as plt
import numpy as np

# Gets the muninn data
file = "results/hyp_layers_wave_pconvergence-cartoon_xz/hyp_layers_wave_pconvergence-cartoon_xz-np=21/output_1d/z/u.psi"
data = pymuninn.MuninnData(file)
grid = data.as_grid()

#file2 = "temp_results/_exact_sol_cache/exact.u.psi.n=23"
#data2 = pymuninn.MuninnData(file2)
#grid2 = data2.as_grid()

# Gets the index of the time slice to plot
time_slice = [0, 5, 15, 30]

for t in time_slice:
    for i, time in zip(range(len(grid.ts)), grid.ts):
        if time < t:
            continue
        else:
            plt.figure(figsize=(8, 6))
            plt.plot(grid.xss[i], grid.values[i])
            #plt.plot(grid2.xss[i], grid2.values[i], linestyle=(0, (5, 7)), label="Analytical solution")
            plt.xlabel(r"$z$", fontsize=14)
            plt.ylabel(r"$\psi$", fontsize=14)
            plt.xlim(0, 30)
            #plt.ylim(-0.2, 2.2)
            plt.grid(True, which="both", ls="--", lw=0.5)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            #plt.legend(fontsize=12)
            plt.tight_layout()
            plt.savefig(f"temp_results/hyp_layers_perturbation_z_snapshots_t={t}.png")
            break
            