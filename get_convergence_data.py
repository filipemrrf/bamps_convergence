"""
 " @file get_data_local.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief Script to run the hyperboloidal wave equation project in bamps with several resolutions on my own computer
 " @version 1.1
 " @date 2025-06-17
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
parser.add_argument('--amr', type=bool, help='AMR (default: False)')
parser.add_argument('--cartoon', type=str, help='Cartoon axis (default: none)')
parser.add_argument('--reflect', type=str, help='Reflect axis (default: none)')
parser.add_argument('--tmax', type=float, required=True, help='Maximum time for the simulation')
parser.add_argument('--amp', type=float, default=1.0, help='Amplitude of the initial data (default: 1.0)')
parser.add_argument('--gamma1', type=float, help='Gamma1 parameter for the project (default: -1)')
parser.add_argument('--gamma2', type=float, help='Gamma2 parameter for the project (default: 0)')
parser.add_argument('--source', type=str, help='Source type (default: none)')
parser.add_argument('--out_every', type=int, default=10, help='Output frequency (default: 10)')
parser.add_argument('--np', type=int, default=1, help='Number of processors to use (default: 1)')

# Parse the arguments
args = parser.parse_args()

# Determine the results folder name
if args.source:
    results_name = f"hyp_{args.source}_wave"
else:
    results_name = f"hyp_wave"

# Create the results directory if it doesn't exist
if os.path.exists(f"temp_results/{results_name}_convergence/"):
    if os.path.exists(f"temp_results/{results_name}_convergence_previous/"):
        os.system(f"rm -rf temp_results/{results_name}_convergence_previous/")
    os.system(f"mv temp_results/{results_name}_convergence/ temp_results/{results_name}_convergence_previous/")

os.makedirs(f"temp_results/{results_name}_convergence/", exist_ok=True)

for i in range(args.runs):
    # Calculate the number of points in each dimension for the current resolution
    nxyz = args.base_nxyz + (2 * i)
    
    # Create the command to run the par_file_writer.py script
    cmd = f"python3 par_file_writer.py --nxyz {nxyz} --tmax {args.tmax} --output convergence --out_0d_every {args.out_every} --out_1d_every {args.out_every}"
    if args.amr:
        cmd += f" --amr {args.amr}"
    if args.amp:
        cmd += f" --amp {args.amp}"
    if args.gamma1:
        cmd += f" --gamma1 {args.gamma1}"
    if args.gamma2:
        cmd += f" --gamma2 {args.gamma2}"
    if args.source:
        cmd += f" --source {args.source}"
    if args.cartoon:
        cmd += f" --cartoon {args.cartoon}"
    if args.reflect:
        cmd += f" --reflect {args.reflect}"
    
    # Run the command
    os.system(cmd)

    # Renames the parameter file
    os.system(f"mv parameters.par {results_name}_convergence_nxyz{nxyz}.par")

    # Moves the par_file to the bamps executable directory
    os.system(f"mv {results_name}_convergence_nxyz{nxyz}.par ../bamps/exe/")

    # Change directory to the bamps executable directory
    os.chdir("../bamps/exe/")

    # Run the bamps executable with the generated par_file
    os.system(f"mpirun -np {args.np} ./bamps {results_name}_convergence_nxyz{nxyz}.par")

    # Delete the par_file created from bamps executable directory
    os.system(f"rm {results_name}_convergence_nxyz*.par")

    # Move the results to the results directory
    os.system(f"mv {results_name}_convergence_nxyz{nxyz} ../../bamps_convergence/temp_results/{results_name}_convergence/")

    # Change back to the original directory
    os.chdir("../../bamps_convergence/")