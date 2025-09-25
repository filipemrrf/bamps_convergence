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
os.system("python3 get_convergence_data.py --runs 5 --convergence_type p --base_nxyz 15 --tmax 100 --out_every 100 --np 10")
print("Data acquired.")

print("Running the convergence test...")
os.system("python3 norm_convergence.py temp_results/hyp_wave_pconvergence")
print("Convergence test finished.")