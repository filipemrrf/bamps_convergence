"""
 " @file par_file_writer.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief Writes a parameter file for the hyperboloidal wave equation project in bamps
 " @version 1.0
 " @date 2025-05-20
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process the arguments to get the data')

# Add arguments to the parser
parser.add_argument('--nxyz', type=int, required=True, help='Number of points in each dimension')
parser.add_argument('--cartoon', type=str, help='Cartoon axis (default: none)')
parser.add_argument('--reflect', type=str, help='Reflect axis (default: none)')
parser.add_argument('--tmax', type=float, required=True, help='Maximum time for the simulation')
parser.add_argument('--out_every', type=int, default=10, help='Output frequency (default: 10)')

# Parse the arguments
args = parser.parse_args()
nxyz = args.nxyz  # Number of points in each dimension
tmax = args.tmax  # Maximum time for the simulation
out_every = args.out_every  # Output frequency

# Opens the file in write mode
PAR_FILE = open(f"hyp_wave_convergence_nxyz{nxyz}.par", 'w')

# Writes the header
PAR_FILE.write(f"###############################################################################\n")
PAR_FILE.write(f"# hyp_wave_convergence_nxyz{nxyz}.par\n")
PAR_FILE.write(f"#                                                                             #\n")
PAR_FILE.write(f"# Evolves hyperboloidal wave equation project to make a convergence test      #\n")
PAR_FILE.write(f"###############################################################################\n")
PAR_FILE.write("\n")

# Writes the grid parameters
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("# Grid parameters                                                             #\n")
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("\n")

PAR_FILE.write("grid = cubedball\n")
PAR_FILE.write("\n")

PAR_FILE.write("grid.cube.max         = 1.5\n")
PAR_FILE.write("grid.cubesphere.max.x = 4.5\n")
PAR_FILE.write("grid.sphere.max.x     = 10\n")
PAR_FILE.write("\n")

PAR_FILE.write("grid.sub.xyz          = 2\n")
PAR_FILE.write("grid.cubesphere.sub.x = 1\n")
PAR_FILE.write("grid.sphere.sub.x     = 1\n")
PAR_FILE.write("\n")

if args.cartoon:
    PAR_FILE.write(f"grid.cartoon = {args.cartoon}\n")
    PAR_FILE.write("\n")

if args.reflect:
    PAR_FILE.write(f"grid.reflect = {args.reflect}\n")
    PAR_FILE.write("\n")

PAR_FILE.write("grid.amr.h = no\n")
PAR_FILE.write("grid.amr.p = no\n")
PAR_FILE.write("grid.amr.t = no\n")
PAR_FILE.write("\n")

PAR_FILE.write(f"grid.n.xyz = {nxyz}\n")
PAR_FILE.write("\n")

PAR_FILE.write("tensor.indexstyle = letters\n")
PAR_FILE.write("\n")

PAR_FILE.write("timer = on\n")
PAR_FILE.write(f"\n")

# Writes the filter parameters
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("# Filter parameters                                                           #\n")
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("\n")

PAR_FILE.write("filter = 1\n")
PAR_FILE.write("\n")

# Writes the evolution parameters
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("# Evolution parameters                                                        #\n")
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("\n")

PAR_FILE.write(f"evolve           = 1\n")
PAR_FILE.write(f"evolve.dtfactor  = .25\n")
PAR_FILE.write(f"evolve.finaltime = {tmax}\n")
PAR_FILE.write("\n")

# Writes the project parameters
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("# Project parameters                                                          #\n")
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("\n")

PAR_FILE.write("project = hyp_wave\n")
PAR_FILE.write("\n")

PAR_FILE.write("hyp_wave.initialdata                = gaussian\n")
PAR_FILE.write("hyp_wave.initialdata.gaussian.amp   = 1.0\n")
PAR_FILE.write("hyp_wave.initialdata.gaussian.sigma = 1\n")
PAR_FILE.write("hyp_wave.initialdata.gaussian.x0    = 0\n")
PAR_FILE.write("hyp_wave.initialdata.gaussian.y0    = 0\n")
PAR_FILE.write("hyp_wave.initialdata.gaussian.z0    = 0\n")
PAR_FILE.write("\n")

PAR_FILE.write("hyp_wave.boundary.patch = penalty\n")
PAR_FILE.write("hyp_wave.boundary.inner = none\n")
PAR_FILE.write("hyp_wave.boundary.outer = none\n")
PAR_FILE.write("\n")

PAR_FILE.write("hyp_wave.scri = 10\n")
PAR_FILE.write("\n")

# Writes the output parameters
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("# Output parameters                                                           #\n")
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("\n")

PAR_FILE.write("output.sd.every = 10\n")
PAR_FILE.write("output.sd.mode  = grid0 magicnumber\n")
PAR_FILE.write("\n")

PAR_FILE.write(f"output.0d.every    = {out_every}\n")
PAR_FILE.write(f"output.0d.mode     = integral\n")
PAR_FILE.write(f"output.0d.integral = ana.Bx ana.By ana.Bz\n")

PAR_FILE.write(f"output.1d.every = {out_every}\n")
PAR_FILE.write(f"output.1d.dim   = x y z\n")
PAR_FILE.write(f"output.1d       = u.psi ana.Bx ana.By ana.Bz\n")

# Closes the file
PAR_FILE.close()

# Prints a message indicating that the file has been created
print(f"File hyp_wave_convergence_nxyz{nxyz}.par created successfully.")