"""
 " @file find_blowup.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief macro to find the threshold of blowup using the amplitude solutions for the hyperboloidal wave equation project
 " @version 1.0
 " @date 2025-06-
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import os
import glob

def check_blowup(A: float) -> bool:
    # Checks if the program exited with an error
    if glob.glob(f"temp_results/hyp_cubic_wave_blowup/hyp_cubic_wave_A{A}/ERROREXIT.*"):
        return True
    
    for field in ["psi", "pi", "phix", "phiy", "phiz"]:
        # Opens the output file for the field 
        OUT_FILE = open(f"temp_results/hyp_cubic_wave_blowup/hyp_cubic_wave_A{A}/output_0d/{blowup_criteria}/u.{field}", 'r')
    

        # Reads the last non empty line of the files and gets the value of the fields
        lines = OUT_FILE.readlines()
        last_line = ""
        for line in reversed(lines):
            if line.strip():
                last_line = line.strip()
                break

        field_max = float((last_line.split())[1])

        # Closes the output file
        OUT_FILE.close()

        if abs(field_max) > blowup_threshold or field_max != field_max:
            return True
    
    return False


def run_bamps_simulation(base_nxyz: int, tmax: float, gamma1: float, gamma2: float, A: float) -> None:
    # Creates the parameter file
    os.system(f"python3 par_file_writer.py --nxyz {nxyz} --tmax {tmax} --output blowup --out_1d_every {out_1d_every} --gamma1 {gamma1} --gamma2 {gamma2} --amp {A} --cartoon x --amr True --source cubic > /dev/null 2>&1")

    # Renames the par file and moves it to the exe directory
    os.system(f"mv parameters.par hyp_cubic_wave_A{A}.par")
    os.system(f"mv hyp_cubic_wave_A{A}.par ../bamps/exe/")

    # Move to the bamps directory and run the simulation
    os.chdir("../bamps/exe/")
    os.system(f"mpirun -np 10 ./bamps hyp_cubic_wave_A{A}.par > A{A}.log 2>&1")

    # Delete the par_file created from bamps executable directory
    os.system(f"rm hyp_cubic_wave_A{A}.par")

    # Move the results to the results directory
    os.system(f"mv A{A}.log hyp_cubic_wave_A{A}")
    os.system(f"mv hyp_cubic_wave_A{A} ../../bamps_convergence/temp_results/hyp_cubic_wave_blowup/")

    # Change back to the original directory
    os.chdir("../../bamps_convergence/")


# Define the parameters for the equation
nxyz = 19
tmax = 150
gamma1 = -1.0
gamma2 = 2.0

# Define parameters for the output
out_1d_every = 500 

# Define the initial range for the test and the tolerance
stable_A = 2.75
unstable_A = 2.8
tol = 1e-15

# Blowup criteria
blowup_criteria = "max"
blowup_threshold = 1e3

# Create a folder to store the results
if os.path.exists("temp_results/hyp_cubic_wave_blowup/"):
    if os.path.exists(f"temp_results/hyp_cubic_wave_blowup_previous/"):
        os.system(f"rm -rf temp_results/hyp_cubic_wave_blowup_previous/")
    os.system(f"mv temp_results/hyp_cubic_wave_blowup/ temp_results/hyp_cubic_wave_blowup_previous/")
os.makedirs("temp_results/hyp_cubic_wave_blowup", exist_ok=True)

# WE ARE USING THE BISECTION METHOD TO FIND THE THRESHOLD OF BLOWUP
while unstable_A - stable_A > tol:
    print(f"Current range: [{stable_A}, {unstable_A}] with tolerance {tol}\n")

    # Calculate the midpoint of the current range
    A = (stable_A + unstable_A) / 2.0
    
    # Run the convergence test with the current amplitude
    run_bamps_simulation(nxyz, tmax, gamma1, gamma2, A)
    
    # Check if the solution blows up
    if check_blowup(A):
        unstable_A = A
        print(f"Unstable amplitude found: {unstable_A}")
    else:
        stable_A = A
        print(f"Stable amplitude found: {stable_A}")

# Create a file with the result
with open("temp_results/hyp_cubic_wave_blowup/threshold.txt", "w") as f:
    f.write(f"Threshold of blowup found at A = {stable_A} with tolerance {tol}\n")
    f.write(f"Final range: [{stable_A}, {unstable_A}]")

# Print the final result
print(f"Threshold of blowup found at A = {stable_A} with tolerance {tol}")