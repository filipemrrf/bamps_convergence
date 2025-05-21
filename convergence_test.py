"""
 " @file convergence_test.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief macro to run the convergence test for the hyperboloidal wave equation project
 " @version 1.0
 " @date 2025-05-21
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import os

print("Running the convergence test for the hyperboloidal wave equation project...")

print("Acquiring the data...")
os.system("python3 get_data_local.py --runs 5 --base_nxyz 10 --tmax 20.0 --out_every 10 --np 10 --cartoon x")
print("Data acquired.")

print("Running the convergence test...")
os.system("python3 norm_convergence.py results/hyp_wave_convergence/")
print("Convergence test finished.")