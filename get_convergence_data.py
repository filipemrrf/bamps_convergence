"""
 " @file get_data_local.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief Script to run the hyperboloidal wave equation project in bamps with several resolutions on my own computer
 " @version 3.0
 " @date 2025-09-04
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import os
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process the arguments to get the data')

# Add arguments to the parser
parser.add_argument('--runs', type=int, default=1, help='Number of resolutions to run')
parser.add_argument('--convergence_type', type=str, default='p', help='Type of convergence (default: p)')
parser.add_argument('--np', type=int, default=1, help='Number of processors to use (default: 1)')
parser.add_argument('--scri', type=float, default=30.0, help='Location of scri (default: 30.0)')
parser.add_argument('--cartoon', type=str, help='Cartoon axis (default: none)')
parser.add_argument('--reflect', type=str, help='Reflect axis (default: none)')
parser.add_argument('--amr', type=bool, default=False, help='AMR (default: False)')
parser.add_argument('--base_nxyz', type=int, default=15, help='Number of points in each dimension')
parser.add_argument('--tmax', type=float, required=True, help='Maximum time for the simulation')
parser.add_argument('--amp', type=float, default=1.0, help='Amplitude of the initial data (default: 1.0)')
parser.add_argument('--sigma', type=float, default=1.0, help='Standard deviation of the initial data (default: 1.0)')
parser.add_argument('--layers', type=bool, default=False, help='Use layers (default: False)')
parser.add_argument('--gamma1', type=float, default=-1, help='Gamma1 parameter for the project (default: -1)')
parser.add_argument('--gamma2', type=float, default=2, help='Gamma2 parameter for the project (default: 2)')
parser.add_argument('--source', type=str, default='none', help='Source type (default: none)')
parser.add_argument('--out_every', type=int, default=10, help='Output frequency (default: 10)')
parser.add_argument('--exact', type=bool, default=False, help='Use exact solution (default: False)')
parser.add_argument('--debug', type=bool, default=False, help='Use debug mode (default: False)')

# Parse the arguments
args = parser.parse_args()

# Determine the results folder name
results_name = ""
if args.layers:
    results_name += "hyp_layers_"
else:
    results_name += "hyp_"
if args.source != "none":
    results_name += f"{args.source}_wave"
else:
    results_name += f"wave"
results_name += f"_{args.convergence_type}convergence"
if args.cartoon == 'x':
    results_name += "-cartoon_x"
elif args.cartoon == 'xz':
    results_name += "-cartoon_xz"

# Create the results directory if it doesn't exist
if os.path.exists(f"temp_results/{results_name}/"):
    if os.path.exists(f"temp_results/{results_name}-previous/"):
        os.system(f"rm -rf temp_results/{results_name}-previous/")
    os.system(f"mv temp_results/{results_name}/ temp_results/{results_name}-previous/")

os.makedirs(f"temp_results/{results_name}/", exist_ok=True)

# Initial number of subdivisions per patch and number of points in each subdivision
nh = 2
nxyz = args.base_nxyz

# Loop over the number of runs
for i in range(args.runs):    
    # Create the command to run the par_file_writer.py script
    cmd = f"python3 par_file_writer.py --nh {nh} --nxyz {nxyz} --tmax {args.tmax} --output convergence --out_0d_every {args.out_every} --out_1d_every {args.out_every} --scri {args.scri} --gamma1 {args.gamma1} --gamma2 {args.gamma2} --source {args.source}"
    if args.cartoon:
        cmd += f" --cartoon {args.cartoon}"
    if args.reflect:
        cmd += f" --reflect {args.reflect}"
    if args.amr:
        cmd += f" --amr {args.amr}"
    if args.amp:
        cmd += f" --amp {args.amp}"
    if args.sigma:
        cmd += f" --sigma {args.sigma}"
    if args.layers:
        cmd += f" --layers {args.layers}"
    if args.exact:
        cmd += f" --exact {args.exact}"
    if args.debug:
        cmd += f" --debug {args.debug}"
    
    # Run the command
    os.system(cmd)

    # Renames the parameter file
    if args.convergence_type == 'h':
        parfilename = f"{results_name}-nh={nh}"
    if args.convergence_type == 'p':
        parfilename = f"{results_name}-np={nxyz}"
        
    os.system(f"mv parameters.par {parfilename}.par")

    # Moves the par_file to the bamps executable directory
    os.system(f"mv {parfilename}.par ../bamps/exe/")

    # Change directory to the bamps executable directory
    os.chdir("../bamps/exe/")

    # Run the bamps executable with the generated par_file
    os.system(f"mpirun -np {args.np} ./bamps {parfilename}.par")

    # Delete the par_file created from bamps executable directory
    os.system(f"rm {parfilename}.par")

    # Move the results to the results directory
    os.system(f"mv {parfilename} ../../bamps_convergence/temp_results/{results_name}/")

    # Change back to the original directory
    os.chdir("../../bamps_convergence/")

    # Update nh and nxyz based on the convergence type
    if args.convergence_type == 'h':
        nh *= 2
    elif args.convergence_type == 'p':
        nxyz += 2