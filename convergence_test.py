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
os.system("python3 get_data_local.py --runs 5 --base_nxyz 15 --tmax 30.0 --out_every 100 --np 15 --gamma2 2.0 --cartoon x")
print("Data acquired.")

print("Running the convergence test...")
os.system("python3 norm_convergence.py results/hyp_wave_convergence/")
print("Convergence test finished.")