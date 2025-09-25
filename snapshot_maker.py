import pymuninn
import matplotlib.pyplot as plt
import numpy as np

# Gets the muninn data
file = "results/hyp_wave_pconvergence-cartoon_x/hyp_wave_pconvergence-cartoon_x-np=23/output_1d/x/u.psi"
data = pymuninn.MuninnData(file)
grid = data.as_grid()

#file2 = "results/hyp_wave_pconvergence-cartoon_x/hyp_wave_pconvergence-cartoon_x-np=23/output_1d/x/ana.cmx"
#data2 = pymuninn.MuninnData(file2)
#grid2 = data2.as_grid()

# Gets the index of the time slice to plot
time_slice = [0, 5, 10, 20, 30]

for t in time_slice:
    for i, time in zip(range(len(grid.ts)), grid.ts):
        if time < t:
            continue
        else:
            plt.figure(figsize=(8, 6))
            plt.plot(grid.xss[i], grid.values[i])

            plt.xlabel(r"$r$", fontsize=14)
            plt.ylabel(r"$\psi$", fontsize=14)
            plt.xlim(0, 30)
            plt.ylim(-0.2, 2.2)
            plt.grid(True, which="both", ls="--", lw=0.5)
            plt.tight_layout()
            plt.savefig(f"temp_results/hyp_wave_t={t}.png")
            break