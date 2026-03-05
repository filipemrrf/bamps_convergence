"""
 " @file convergence_test.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief macro to run the convergence test for the hyperboloidal wave equation project
 " @version 1.1
 " @date 2025-06-17
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import os

print("Running the convergence test for the hyperboloidal wave equation project...")

print("Acquiring the data...")
os.system("python3 get_convergence_data.py --runs 1 --base_nxyz 29 --tmax 300 --out_every 1 --np 10 --cartoon x --amp 1.5 --sigma 1.0 --gamma2 4 --layers True --source cubic --amr True")
print("Data acquired.")

print("Running the convergence test...")
#os.system("python3 pointwise_convergence.py temp_results/hyp_wave_pconvergence-cartoon_x --exact 1")
#os.system("python3 norm_convergence.py temp_results/hyp_layers_cubic_wave_pconvergence-cartoon_x")
print("Convergence test finished.")