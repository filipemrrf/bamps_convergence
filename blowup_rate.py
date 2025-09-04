import pymuninn
import matplotlib.pyplot as plt
import numpy as np

file = "temp_results/hyp_layers_cubic_wave_pconvergence-cartoon_x/hyp_layers_cubic_wave_pconvergence-cartoon_x_pconvergence_np20/output_1d/x/u.psi"   # your input files
data = pymuninn.MuninnData(file)


tbar = []
T_blowup = 0.3312021081679338
psi = []


for i in range(len(data.points)):
    if data.points[i][1] == 0.0:
        tbar.append(1.0 / (T_blowup - data.points[i][0]))
        psi.append(data.values[i])

plt.figure(figsize=(8, 6))
plt.plot(tbar[0:-1], psi[0:-1], label="$numerics$")
plt.plot(tbar[0:-1], np.sqrt(2) * np.array(tbar[0:-1]), '--', label="theory")

plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"$1 / (T_{blowup} - t)$", fontsize=14)
plt.ylabel(r"$\psi$", fontsize=14)

plt.grid(True, which="both", ls="--", lw=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("blowup_rate.png")

