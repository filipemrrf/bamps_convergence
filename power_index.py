import pymuninn
import matplotlib.pyplot as plt
import numpy as np

file = "temp_results/hyp_layers_cubic_wave_hconvergence-cartoon_x/hyp_layers_cubic_wave_hconvergence-cartoon_x-nh=2/output_1d/x/u.psi"
data = pymuninn.MuninnData(file)
grid = data.as_grid()

for r_fixed in [0.0, 6.0, 10.0, 20.0, 30.0]:
    # Finds the index corresponding to the fixed r
    r_index = 0
    for i, r in zip(range(len(grid.xss[0])), grid.xss[0]):
        if r == r_fixed:
            r_index = i
            break

    psi = [grid.values[i][r_index] for i in range(len(grid.ts))]

    ln_psi = np.log(np.abs(psi))
    ln_t = np.log(np.array(grid.ts))
    h = []
    power_index = []

    """
    for i in range(0, len(ln_t)-1):
        h.append(ln_t[i+1] - ln_t[i])

    for i in range(1, len(ln_psi)-1):
        power_index.append(-h[i]/(h[i-1] * (h[i] + h[i-1])) * ln_psi[i-1] + (h[i]**2 - h[i-1]**2)/(h[i]*h[i-1]*(h[i] + h[i-1])) * ln_psi[i] + h[i-1]/(h[i]*(h[i] + h[i-1])) * ln_psi[i+1])
    """

    plt.plot(ln_t[1:-1], ln_psi[1:-1], label=f"r = {r_fixed}")

    #plt.plot(grid.ts[1:-1], power_index, label=f"r = {r_fixed}")

# Plot reference slopes -2 and -3
x_ref = np.linspace(2, 6, 100)
plt.plot(x_ref, -2 * x_ref, 'k--', label="slope = -2")
plt.plot(x_ref, -1 * x_ref, 'r--', label="slope = -1")

plt.xlabel(r"$ln(t)$", fontsize=14)
plt.ylabel(r"$\psi$", fontsize=14)
plt.xlim(2, 6)
plt.ylim(-20.0, 1)

plt.grid(True, which="both", ls="--", lw=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("temp_results/power_index.png")

