import pymuninn
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def Omega(r):
    r = np.asarray(r)
    out = np.empty_like(r, dtype=float)
    out[r <= Ri] = 1.0
    out[r >= Rt] = 1.0 - ((r[r >= Rt] - Ri)/(S - Ri))**2
    mask = (r > Ri) & (r < Rt)
    out[mask] = 1.0 + ((r[mask] - Ri)**5 * (6.0 * r[mask]**2 + 3.0 * r[mask] * Ri + Ri**2 - 5.0 * (3.0 * r[mask] + Ri) * Rt + 10.0 * Rt**2))/((Ri - Rt)**5 * (Ri - S)**2)
    return out

def tau(t, r):
    r = np.asarray(r)
    t = np.asarray(t)
    out = np.empty_like(r, dtype=float)
    out[r == 0] = t - 1.0
    out[r == S] = t - S
    mask = (r != 0) & (r != S)
    R = (r[mask] - Ri) / Omega(r[mask]) + Ri
    out[mask] = t + (2.0 * R**2 + S**2 - np.sqrt(4.0 * R**2 * S**2 + S**4))/(2.0 * R) - np.sqrt(1 + R**2)
    return out

def rho(r):
    r = np.asarray(r)
    out = np.empty_like(r, dtype=float)
    out[r == 0] = 0.0
    mask = (r != 0)
    out[mask] = (-Omega(r[mask]) + np.sqrt(r[mask]**2 + 2.0 * r[mask] * Ri * (-1.0 + Omega(r[mask])) + Ri**2 * (-1.0 + Omega(r[mask]))**2 + Omega(r[mask])**2)) / (r[mask] + Ri * (-1.0 + Omega(r[mask])))
    return out

def attractor(tau, rho, a, b):
    return 2.0 * np.sqrt(2.0) / ((tau + a + 1) * (b * (tau + a + 1) + 1) - rho**2 * (tau + a - 1) * (b * (tau + a - 1) + 1))

Ri = 10.0
Rt = 20.0
S = 30.0

file = "temp_results/hyp_layers_cubic_wave_hconvergence-cartoon_x/hyp_layers_cubic_wave_hconvergence-cartoon_x-nh=8/output_1d/x/u.psi"
data = pymuninn.MuninnData(file)
grid = data.as_grid()

a_list = []
b_list = []

# Fits the solution to the attractor for each fixed r
FIT_RESULTS = open(f"temp_results/fit_results.data", 'w')
FIT_RESULTS.write(f"#t\ta\tb\n")

"""
time = []
psi = []

for i, r in zip(range(len(grid.xss[0])), grid.xss[0]):
    time.clear()
    psi.clear()

    for j, t in zip(range(len(grid.ts)), grid.ts):
        if t < 300.0:
            continue
        
        time.append(t)
        psi.append(grid.values[j][i])

    anil_tau = [tau(t, r) for t in time]

    params, _ = curve_fit(lambda t, a, b: attractor(t, rho(r), a, b), anil_tau, psi)

    a_list.append(params[0])
    b_list.append(params[1])
    FIT_RESULTS.write(f"{r}\t{params[0]}\t{params[1]}\n")
"""

for i, t in zip(range(len(grid.ts)), grid.ts):
    if t < 300.0:
        continue

    try:
        params, _ = curve_fit(lambda r, a, b: attractor(tau(t, r), rho(r), a, b), grid.xss[i], grid.values[i])
    except RuntimeError:
        continue

    a_list.append(params[0])
    b_list.append(params[1])
    FIT_RESULTS.write(f"{t}\t{params[0]}\t{params[1]}\n")

a = np.mean(a_list)
b = np.mean(b_list)

FIT_RESULTS.write(f"\n#Mean values:\n# a = {a}\n# b = {b}\n")
FIT_RESULTS.write(f"#std(a) = {np.std(a_list)}\n#std(b) = {np.std(b_list)}")
FIT_RESULTS.close()

a_list.clear()
b_list.clear()

FIT_FILE = open(f"temp_results/psi_ab.data", 'w')

for i, t in zip(range(len(grid.ts)), grid.ts):
    FIT_FILE.write(f"\"Time = {t}\n")

    for r in grid.xss[i]:
        FIT_FILE.write(f"{r}\t{attractor(tau(t, r), rho(r), a, b)}\n")

    FIT_FILE.write(f"\n")

FIT_FILE.close()
