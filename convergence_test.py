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
os.system("python3 get_convergence_data.py --runs 4 --convergence_type h --base_nxyz 13 --tmax 30 --out_every 100 --np 10 --nh 2 --amp 1.0 --sigma 1.0 --gamma2 4 --cartoon x --debug True")
print("Data acquired.")

print("Running the convergence test...")
#os.system("python3 pointwise_convergence.py temp_results/hyp_wave_pconvergence-cartoon_x --exact 1")
os.system("python3 norm_convergence.py temp_results/hyp_wave_hconvergence-cartoon_x")
print("Convergence test finished.") 