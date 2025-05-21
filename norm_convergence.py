"""
 " @file norm_convergence.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief Script to plot the norm of the constraints as a function of time
 " @version 1.0
 " @date 2025-05-21
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import os
import argparse
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

    # Read the data from the specified folder
    for resolution in os.listdir(folder):
        # Skip folders created by this script
        if resolution.startswith("norm_convergence"):
            continue

        # Initialize the lists to store the data
        t = []
        C = []

        # Check if the resolution is a directory
        if os.path.isdir(f"{folder}/{resolution}"):
            # Read the data from the file
            read_file(f"{folder}/{resolution}/output_0d/integral/ana.{constraint}", t, C)

        # Calculate the norm as a function of time
        plt.plot(t, C, label=f"nxyz={resolution.lstrip('hyp_wave_convergence_nxyz')}")
            
    # Plot the norms
    plt.xlabel("Time")
    plt.ylabel(f"Norm of {constraint}")
    plt.legend()
    plt.savefig(f"{folder}/norm_convergence/norm_{constraint}.png")

    # Clear the plot
    plt.clf()