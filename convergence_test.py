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
os.system("python3 get_convergence_data_local.py --runs 1 --base_nxyz 19 --tmax 20.0 --out_every 10 --np 10 --gamma2 2.0 --cartoon xz --amr True --source cubic --amp 3.0")
print("Data acquired.")

print("Running the convergence test...")
os.system("python3 norm_convergence.py temp_results/hyp_cubic_wave_convergence/")
print("Convergence test finished.")