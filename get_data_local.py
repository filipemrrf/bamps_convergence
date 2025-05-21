"""
 " @file get_data_local.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief Script to run the hyperboloidal wave equation project in bamps with several resolutions on my own computer
 " @version 1.0
 " @date 2025-05-20
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import os
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process the arguments to get the data')

# Add arguments to the parser
parser.add_argument('--runs', type=int, required=True, help='Number of resolutions to run')
parser.add_argument('--base_nxyz', type=int, required=True, help='Number of points in each dimension for the base resolution')
parser.add_argument('--cartoon', type=str, help='Cartoon axis (default: none)')
parser.add_argument('--reflect', type=str, help='Reflect axis (default: none)')
parser.add_argument('--tmax', type=float, required=True, help='Maximum time for the simulation')
parser.add_argument('--out_every', type=int, default=10, help='Output frequency (default: 10)')
parser.add_argument('--np', type=int, default=1, help='Number of processors to use (default: 1)')

# Parse the arguments
args = parser.parse_args()
runs = args.runs  # Number of resolutions to run
base_nxyz = args.base_nxyz  # Number of points in each dimension for the base resolution
cartoon = args.cartoon  # Cartoon axis
reflect = args.reflect  # Reflect axis
tmax = args.tmax  # Maximum time for the simulation
out_every = args.out_every  # Output frequency
np = args.np  # Number of processors to use

# Create the results directory if it doesn't exist
if os.path.exists("results/hyp_wave_convergence/"):
    if os.path.exists("results/hyp_wave_convergence_previous/"):
        os.system("rm -rf results/hyp_wave_convergence_previous/")
    # Move the previous results to a backup directory
    os.system("mv results/hyp_wave_convergence/ results/hyp_wave_convergence_previous/")

os.makedirs("results/hyp_wave_convergence/")

for i in range(runs):
    # Calculate the number of points in each dimension for the current resolution
    nxyz = base_nxyz + (2 * i)
    
    # Create the command to run the par_file_writer.py script
    cmd = f"python3 par_file_writer.py --nxyz {nxyz} --tmax {tmax} --out_every {out_every}"
    if args.cartoon:
        cmd += f" --cartoon {cartoon}"
    if args.reflect:
        cmd += f" --reflect {reflect}"
    
    # Run the command
    os.system(cmd)

    # Moves the par_file to the bamps executable directory
    os.system(f"mv hyp_wave_convergence_nxyz{nxyz}.par ../bamps/exe/")

    # Change directory to the bamps executable directory
    os.chdir("../bamps/exe/")

    # Run the bamps executable with the generated par_file
    os.system(f"mpirun -np {np} --use-hwthread-cpus ./bamps hyp_wave_convergence_nxyz{nxyz}.par")

    # Delete the par_file created from bamps executable directory
    os.system("rm hyp_wave_convergence_nxyz*.par")

    # Move the results to the results directory
    os.system(f"mv hyp_wave_convergence_nxyz{nxyz} ../../bamps_convergence/results/hyp_wave_convergence/")

    # Change back to the original directory
    os.chdir("../../bamps_convergence/")