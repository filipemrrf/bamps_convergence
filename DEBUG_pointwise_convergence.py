import os
import argparse
import pymuninn
import numpy as np
import re

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process the arguments to get the data')

# Add arguments to the parser
parser.add_argument('folder', metavar='F', type=str, nargs='+', help='folder of the data')

# Parse the arguments
args = parser.parse_args()
folder = args.folder[0].rstrip('/')  # Folder of the data

# Create the results directory if it doesn't exist
if not os.path.exists(f"{folder}/pointwise_convergence/"):
    os.makedirs(f"{folder}/pointwise_convergence/")

    # Gets the muninn data from the solution
    file = f"{folder}/output_1d/x/u.psi"
    sol_data = pymuninn.MuninnData(file)
    sol_grid = sol_data.as_grid()

    os.chdir(f"{folder}/pointwise_convergence/")

    # Generates the aux file
    AUX = open("aux.csv", 'w')
    AUX.write(",".join(f"{t:.16g}" for t in sol_grid.ts) + "\n")
    AUX.write(",".join(f"{r:.16g}" for r in sol_grid.xss[0]))
    AUX.close()

    # Generates the exact solution
    #os.system("wolframscript -file /home/filipe/bamps_convergence/DEBUGExact_Solution.wls")

    # Gets the muninn data from the exact solution
    exact_data = pymuninn.MuninnData("exact_sol.txt")
    exact_grid = exact_data.as_grid()

    # Outputs the pointwise error
    OUT = open(f"pointwise_error.txt", 'w')

    for i, t in zip(range(len(sol_grid.ts)), sol_grid.ts):
        OUT.write(f"\"Time = {t}\n")

        for j, r in zip(range(len(sol_grid.xss[i])), sol_grid.xss[i]):
            if r == 0 or r == 30:
                continue
            OUT.write(f"{r}\t{abs(exact_grid.values[i][j-1] - sol_grid.values[i][j])}\n")

        OUT.write("\n")

    OUT.close()

    os.chdir("../../../")

    #os.system(f"rm {folder}/pointwise_convergence/aux.csv")