"""
 " @file norm_convergence.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief Script to plot the norm of the constraints as a function of time
 " @version 1.1
 " @date 2025-06-17
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

    # Collect (nxyz, t, C) for each resolution
    data = []
    for resolution in os.listdir(folder):
        if resolution.startswith("norm_convergence"):
            continue
        if os.path.isdir(f"{folder}/{resolution}"):
            # Extract nxyz as an integer using regex
            match = re.search(r'nxyz(\d+)', resolution)
            if not match:
                continue  # skip if not found
            nxyz = int(match.group(1))
            t = []
            C = []
            read_file(f"{folder}/{resolution}/output_0d/integral/ana.{constraint}", t, C)
            data.append((nxyz, t, C))

    # Sort by nxyz
    data.sort(key=lambda x: x[0])

    # Plot in order
    for nxyz, t, C in data:
        plt.plot(t, C, label=f"nxyz={nxyz}")
    
    # Plot the norms
    plt.xlabel("Time")
    plt.ylabel(f"Norm of {constraint}")
    plt.yscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.tight_layout()
    plt.savefig(f"{folder}/norm_convergence/norm_{constraint}.png")

    # Clear the plot
    plt.clf()


# amr plot hack
#for constraint in ['Bx', 'By', 'Bz']:
#    print(f"Processing {constraint}...")
#    plt.figure(figsize=(8, 6))

    # Hack: look for AMR and non-AMR folders
#    amr_labels = [("hyp_cubic_wave_convergence_nxyz", "w/o AMR"),
#                  ("hyp_cubic_wave_convergence_amr_nxyz", "w/ AMR")]

#    for prefix, label in amr_labels:
        # Find the folder that matches the prefix
#        for resolution in os.listdir(folder):
#            if resolution.startswith(prefix) and os.path.isdir(f"{folder}/{resolution}"):
#                t = []
#                C = []
#                read_file(f"{folder}/{resolution}/output_0d/integral/ana.{constraint}", t, C)
#                plt.plot(t, C, label=label)
#                break  # Only plot the first match for each type

#    plt.xlabel("Time")
#    plt.ylabel(f"Norm of {constraint}")
#    plt.yscale('log')
#    plt.legend()
#    plt.grid(True, which="both", ls="--", lw=0.5)
#    plt.tight_layout()
#    plt.savefig(f"{folder}/norm_convergence/norm_{constraint}.png")
#    plt.clf()