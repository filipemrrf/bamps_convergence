import pymuninn
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def Omega(r):
    if r <= Ri:
        return 1.0
    elif r >= Rt:
        return 1.0 - ((r - Ri)/(S - Ri))**2
    else:
        return 1.0 + ((r - Ri)**5 * (6.0 * r**2 + 3.0 * r * Ri + Ri**2 - 5.0 * (3.0 * r + Ri) * Rt + 10.0 * Rt**2))/((Ri - Rt)**5 * (Ri - S)**2)

def tau(t, r):
    if r == 0:
        return t - 1.0
    elif r == S:
        return t - S
    else:
        R  = (r - Ri) / Omega(r) + Ri
        return t + (2.0 * R**2 + S**2 - np.sqrt(4.0 * R**2 * S**2 + S**4))/(2.0 * R) - np.sqrt(1 + R**2)
    
def rho(r):
    if r == 0:
        return 0.0
    else:
        return (-Omega(r) + np.sqrt(r**2 + 2.0 * r * Ri * (-1.0 + Omega(r)) + Ri**2 * (-1.0 + Omega(r))**2 + Omega(r)**2)) / (r + Ri * (-1.0 + Omega(r)))

def attractor(tau, rho, a, b):
    return 2.0 * np.sqrt(2.0) / ((tau + a + 1) * (b * (tau + a + 1) + 1) - rho**2 * (tau + a - 1) * (b * (tau + a - 1) + 1))

Ri = 10.0
Rt = 20.0
S = 30.0

file = "temp_results/hyp_layers_cubic_wave_hconvergence-cartoon_x/hyp_layers_cubic_wave_hconvergence-cartoon_x-nh=8/output_1d/x/u.psi"
data = pymuninn.MuninnData(file)

time_a_list = []
time_b_list = []
space_a_list = []
space_b_list = []

# Performs the fit in time
for i in range(int(len(data.points)/len(data.times))):
    time = []
    r_fixed = data.points[i][1]
    psi = []

    for j in range(len(data.points)):
        if data.points[j][0] < 100.0:
            continue
        if data.points[j][1] == r_fixed:
            time.append(data.points[j][0])
            psi.append(data.values[j])
    
    if len(time) < len(data.times):
        continue

    anil_tau = [tau(t, r_fixed) for t in time]
    anil_rho_fixed = rho(r_fixed)

    #try:
    params, _ = curve_fit(lambda t, a, b: attractor(t, anil_rho_fixed, a, b), anil_tau, psi)
    #except RuntimeError:
    #    continue 

    time_a_list.append(params[0])
    time_b_list.append(params[1])

time_a = np.mean(time_a_list)
time_b = np.mean(time_b_list)

print(f"Fitted parameters in time: a = {time_a}, b = {time_b}, std(a) = {np.std(time_a_list)}, std(b) = {np.std(time_b_list)}")
#Fitted parameters in time: a = -68.05005362613613, b = 4202.82185933907, std(a) = 2.1004940664810934, std(b) = 1527.7899821095182

# Calculates the L2 norm of the difference between the numerical and the attractor solution
FIT_FILE = open(f"temp_results/psi({time_a},{time_b}).data", 'w')
INTERP_FILE = open("temp_results/psi_interp.data", 'w')

errornorm = []
phinorm = []

for i in range(len(data.times)):
    t_fixed = data.times[i]
    r = []
    psi = []

    for j in range(len(data.points)):
        if data.points[j][0] == t_fixed:
            r.append(data.points[j][1])
            psi.append(data.values[j])

    r_grid = np.arange(0, 30.25, 0.25)
    psi_interp = np.interp(r_grid, r, psi)
    fit_psi = [attractor(tau(t_fixed, r_val), rho(r_val), time_a, time_b) for r_val in r_grid]

    FIT_FILE.write(f"\"Time = {t_fixed}\n")
    INTERP_FILE.write(f"\"Time = {t_fixed}\n")
    for r_val, psi_val in zip(r_grid, psi_interp):
        FIT_FILE.write(f"{r_val} {psi_val}\n")
        INTERP_FILE.write(f"{r_val} {attractor(tau(t_fixed, r_val), rho(r_val), time_a, time_b)}\n")
    FIT_FILE.write(f"\n")
    INTERP_FILE.write(f"\n")

    error = np.array(psi_interp) - np.array(fit_psi)
    errornorm.append(np.sqrt(4.0 * np.pi * 0.25 * np.sum([x * x * err * err for x, err in zip(r_grid, error)])))
    phinorm.append(np.sqrt(4.0 * np.pi * 0.25 * np.sum([x * x * psi_interp[x] * psi_interp[x] for x in range(len(psi_interp))])))

plt.plot(data.times, errornorm)

plt.xlabel(r"$t$", fontsize=14)
plt.ylabel(r"$||\psi - \psi_{(a,b)}||_{L^2}$", fontsize=14)
plt.yscale('log')
    
plt.grid(True, which="both", ls="--", lw=0.5)
#plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("temp_results/attractor_convergence.png")

# Plot normalized error in a separate figure
normalized_error = np.array(errornorm) / np.array(phinorm)
plt.figure(figsize=(8, 6))
plt.plot(data.times, normalized_error)
plt.xlabel(r"$t$", fontsize=14)
plt.ylabel(r"$||\psi - \psi_{(a,b)}||_{L^2} / ||\psi||_{L^2}$", fontsize=14)
plt.yscale('log')
plt.grid(True, which="both", ls="--", lw=0.5)
plt.tight_layout()
plt.savefig("temp_results/attractor_convergence_normalized.png")

FIT_FILE.close()
INTERP_FILE.close()