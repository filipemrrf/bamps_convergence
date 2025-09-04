"""
 " @file norm_convergence.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief Script to plot the norm of the constraints as a function of time
 " @version 2.0
 " @date 2025-09-04
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import os
import argparse
import re
import matplotlib.pyplot as plt

""" Function to get the data from the specified file """
def read_file(filename, t, C):
    # Open the file in read mode
    IN = open(filename, "r")

    next(IN)  # Skip the first line

    # Read the file line by line
    for line in IN:
        # Split the line into words
        words = line.split()

        # Check if the line contains the data we want
        if words[0] != "\n" and words[0] != "#":
            # Append the t value to the list
            t.append(float(words[0]))

            # Append the C norm value to the list
            C.append(float(words[1]))

    # Close the file
    IN.close()

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process the arguments to get the data')

# Add arguments to the parser
parser.add_argument('folder', metavar='F', type=str, nargs='+', help='folder of the data')

# Parse the arguments
args = parser.parse_args()
folder = args.folder[0].rstrip('/')  # Folder of the data

# Create the results directory if it doesn't exist
if not os.path.exists(f"{folder}/norm_convergence/"):
    os.makedirs(f"{folder}/norm_convergence/")


# Loops through the constraints
for constraint in ['Bx', 'By', 'Bz']:
    # Shows the current constraint
    print(f"Processing {constraint}...")

    # Create a figure for the plot
    plt.figure(figsize=(8, 6))

    # Collect (n, t, C) for each resolution
    data = []
    for resolution in os.listdir(folder):
        if resolution.startswith("norm_convergence"):
            continue
        if os.path.isdir(f"{folder}/{resolution}"):
            # Extract nxyz as an integer using regex
            match = re.search(r'(\d+)', resolution)
            if not match:
                continue  # skip if not found
            n = int(match.group(1))
            t = []
            C = []
            read_file(f"{folder}/{resolution}/output_0d/integral/ana.{constraint}", t, C)
            data.append((n, t, C))

    # Sort by nxyz
    data.sort(key=lambda x: x[0])

    # Plot in order
    for n, t, C in data:
        plt.plot(t, C, label=f"n={n}")
    
    # Plot the norms
    plt.xlabel("Time")
    plt.ylabel(f"Norm of {constraint}")
    plt.yscale('log')
    #plt.ylim(1e-12, 1e-2)
    plt.legend()
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.tight_layout()
    plt.savefig(f"{folder}/norm_convergence/norm_{constraint}.png")

    # Clear the plot
    plt.clf()