"""
 " @file par_file_writer.py
 " @author Filipe Ficalho (filipe.ficalho@tecnico.ulisboa.pt)
 " @brief Writes a parameter file for the hyperboloidal wave equation project in bamps
 " @version 3.0
 " @date 2025-09-04
 " 
 " @copyright Copyright (c) 2025
 " 
"""

import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process the arguments to get the data')

# Add arguments to the parser
parser.add_argument('--scri', type=float, default=30.0, help='Location of scri (default: 30.0)')
parser.add_argument('--cartoon', type=str, help='Cartoon axis (default: none)')
parser.add_argument('--reflect', type=str, help='Reflect axis (default: none)')
parser.add_argument('--amr', type=bool, default=False, help='AMR (default: False)')
parser.add_argument('--nh', type=int, default=2, help='Number of subdivisions per patch')
parser.add_argument('--nxyz', type=int, default=15, help='Number of points in each dimension')
parser.add_argument('--tmax', type=float, required=True, help='Maximum time for the simulation')
parser.add_argument('--amp', type=float, default=1.0, help='Amplitude of the initial data (default: 1.0)')
parser.add_argument('--sigma', type=float, default=1.0, help='Standard deviation of the initial data (default: 1.0)')
parser.add_argument('--layers', type=bool, default=False, help='Use layers (default: False)')
parser.add_argument('--gamma1', type=float, default=-1, help='Gamma1 parameter for the project (default: -1)')
parser.add_argument('--gamma2', type=float, default=2, help='Gamma2 parameter for the project (default: 2)')
parser.add_argument('--source', type=str, default='none', help='Source type (default: none)')
parser.add_argument('--output', type=str, required=True, help='Output fields')
parser.add_argument('--out_0d_every', type=int, default=10, help='Output frequency (default: 10)')
parser.add_argument('--out_1d_every', type=int, default=10, help='Output frequency (default: 10)')
parser.add_argument('--exact', type=bool, default=False, help='Use exact solution (default: False)')
parser.add_argument('--debug', type=bool, default=False, help='Use debug mode (default: False)')

# Parse the arguments
args = parser.parse_args()

# Opens the file in write mode
PAR_FILE = open("parameters.par", 'w')

# Writes the header
PAR_FILE.write(f"###############################################################################\n")
PAR_FILE.write(f"#                                                                             #\n")
PAR_FILE.write(f"# Evolves hyperboloidal wave equation project to make a convergence test      #\n")
PAR_FILE.write(f"#                                                                             #\n")
PAR_FILE.write(f"###############################################################################\n")
PAR_FILE.write("\n")

# Writes the grid parameters
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("# Grid parameters                                                             #\n")
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("\n")

PAR_FILE.write("grid = cubedball\n")
PAR_FILE.write("\n")

PAR_FILE.write("grid.cube.max         = 2\n")
PAR_FILE.write("grid.cubesphere.max.x = 6\n")
PAR_FILE.write(f"grid.sphere.max.x     = {args.scri}\n")
PAR_FILE.write("\n")

PAR_FILE.write(f"grid.sub.xyz          = {args.nh}\n")
PAR_FILE.write(f"grid.cubesphere.sub.x = {args.nh}\n")
PAR_FILE.write(f"grid.sphere.sub.x     = {int(2*args.nh*args.scri/10)}\n")
PAR_FILE.write("\n")

if args.cartoon:
    PAR_FILE.write(f"grid.cartoon = {args.cartoon}\n")
    PAR_FILE.write("\n")

if args.reflect:
    PAR_FILE.write(f"grid.reflect = {args.reflect}\n")
    PAR_FILE.write("\n")

if args.amr:
    PAR_FILE.write("grid.amr.h = yes\n")
    PAR_FILE.write("grid.amr.p = no\n")
    PAR_FILE.write("grid.amr.hlmax = 5\n")
    PAR_FILE.write("\n")

    PAR_FILE.write("grid.amr.evolve = yes\n")
    PAR_FILE.write("grid.amr.coarsen = yes\n")
    PAR_FILE.write("\n")

    PAR_FILE.write("grid.amr.h.indicator = error\n")
    PAR_FILE.write("grid.amr.h.indicator.variables = u.psi\n")
    PAR_FILE.write("grid.amr.h.indicator.min = 1e-13\n")
    PAR_FILE.write("grid.amr.h.indicator.max = 1e-11\n")
    PAR_FILE.write("\n")

    #PAR_FILE.write("grid.amr.p.indicator = error\n")
    #PAR_FILE.write("grid.amr.p.indicator.variables = u.psi\n")
    #PAR_FILE.write("\n")

    #PAR_FILE.write("grid.amr.p.indicator.max = 1.e-10\n")
    #PAR_FILE.write("grid.amr.p.indicator.min = 1.e-12\n")
    #PAR_FILE.write("\n")

#    PAR_FILE.write("grid.amr.noise.threshold = 1.e-7\n")
#    PAR_FILE.write("grid.amr.noise.threshold.abs = 1.e-20\n")
#    PAR_FILE.write("\n")

    PAR_FILE.write("grid.amr.every = 100\n")
    PAR_FILE.write("grid.error.mode = smooth\n")
    PAR_FILE.write("\n")

    PAR_FILE.write("grid.amr.nmax = 31\n")
    PAR_FILE.write("grid.amr.nstep = 2\n")
    PAR_FILE.write("\n")

    PAR_FILE.write("grid.amr.initialdata = interpolate\n")
    PAR_FILE.write("\n")
else:
    PAR_FILE.write("grid.amr.h = no\n")
    PAR_FILE.write("grid.amr.p = no\n")
    PAR_FILE.write("\n")

PAR_FILE.write(f"grid.n.xyz = {args.nxyz}\n")
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
PAR_FILE.write(f"evolve.dtfactor  = .2\n")
PAR_FILE.write(f"evolve.finaltime = {args.tmax}\n")
PAR_FILE.write("\n")

# Writes the project parameters
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("# Project parameters                                                          #\n")
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("\n")

PAR_FILE.write("project = hyp_wave\n")
PAR_FILE.write("\n")

if args.exact or args.debug:
    PAR_FILE.write(f"hyp_wave.initialdata                     = debug\n")
else:
    PAR_FILE.write(f"hyp_wave.initialdata                     = gaussianshell\n")
PAR_FILE.write(f"hyp_wave.initialdata.gaussianshell.amp   = {args.amp}\n")
PAR_FILE.write(f"hyp_wave.initialdata.gaussianshell.sigma = {args.sigma}\n")
PAR_FILE.write(f"hyp_wave.initialdata.gaussianshell.r0    = 0\n")
PAR_FILE.write(f"\n")

PAR_FILE.write("hyp_wave.boundary.patch = penalty\n")
PAR_FILE.write("hyp_wave.boundary.inner = none\n")
PAR_FILE.write("hyp_wave.boundary.outer = none\n") #bjorhus
PAR_FILE.write("\n")

if args.layers:
    PAR_FILE.write(f"hyp_wave.metric = hyp_layers_minkowski\n")
    PAR_FILE.write(f"hyp_wave.Rinterface = 10\n")
    PAR_FILE.write(f"hyp_wave.translen = 10\n")
else:
    PAR_FILE.write(f"hyp_wave.metric = hyp_minkowski\n")

PAR_FILE.write(f"hyp_wave.scri    = {args.scri}\n")
PAR_FILE.write(f"hyp_wave.gamma1  = {args.gamma1}\n")
PAR_FILE.write(f"hyp_wave.gamma2  = {args.gamma2}\n")
PAR_FILE.write(f"hyp_wave.sources = {args.source}\n")
PAR_FILE.write("\n")

# Writes the output parameters
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("# Output parameters                                                           #\n")
PAR_FILE.write("###############################################################################\n")
PAR_FILE.write("\n")

if args.debug:
    PAR_FILE.write("output.ru = 1\n")
    PAR_FILE.write("\n")

PAR_FILE.write(f"output.sd.every = {args.out_0d_every}\n")
PAR_FILE.write("output.sd.mode  = grid0 magicnumber\n")
PAR_FILE.write("\n")

PAR_FILE.write(f"output.ru = 1\n")
PAR_FILE.write("\n")

if args.output == "convergence":
    PAR_FILE.write(f"output.0d.every    = {args.out_0d_every}\n")
    PAR_FILE.write(f"output.0d.mode     = integral\n")
    PAR_FILE.write(f"output.0d.integral = ana.E ana.Bx ana.By ana.Bz\n")

    PAR_FILE.write(f"output.1d.every = {args.out_1d_every}\n")
    if args.cartoon == "x":
        PAR_FILE.write(f"output.1d.dim   = x\n")
    elif args.cartoon == "xz":
        PAR_FILE.write(f"output.1d.dim   = x z\n")
    else:
        PAR_FILE.write(f"output.1d.dim   = x y z\n")
    if args.debug:
        PAR_FILE.write(f"output.1d       = u.psi u.pi u.phix u.phiy u.phiz ana.E ana.Bx ana.By ana.Bz ana.cpx ana.cmx stat.Omega stat.alpha stat.betax stat.betay stat.betaz stat.gammaxx stat.gammaxy stat.gammaxz stat.gammayy stat.gammayz stat.gammazz stat.Christgammaxxx stat.Christgammaxxy stat.Christgammaxxz stat.Christgammaxyy stat.Christgammaxyz stat.Christgammaxzz stat.Christgammayxx stat.Christgammayxy stat.Christgammayxz stat.Christgammayyy stat.Christgammayyz stat.Christgammayzz stat.Christgammazxx stat.Christgammazxy stat.Christgammazxz stat.Christgammazyy stat.Christgammazyz stat.Christgammazzz stat.accelx stat.accely stat.accelz stat.Kxx stat.Kxy stat.Kxz stat.Kyy stat.Kyz stat.Kzz stat.dbetaxx stat.dbetaxy stat.dbetaxz stat.dbetayx stat.dbetayy stat.dbetayz stat.dbetazx stat.dbetazy stat.dbetazz stat.oomboxom stat.oom2dom2 ru.psi ru.pi ru.phix ru.phiy ru.phiz\n")
    else:
        PAR_FILE.write(f"output.1d       = u.psi u.pi u.phix u.phiy u.phiz ana.Bx ana.By ana.Bz\n")

elif args.output == "blowup":
    PAR_FILE.write(f"output.0d.every    = {args.out_0d_every}\n")
    PAR_FILE.write(f"output.0d.mode     = origin max\n")
    PAR_FILE.write(f"output.0d.origin   = u.psi u.pi u.phix u.phiy u.phiz\n")
    PAR_FILE.write(f"output.0d.max      = u.psi u.pi u.phix u.phiy u.phiz\n")

    PAR_FILE.write(f"output.1d.every = {args.out_1d_every}\n")
    if args.cartoon == "x":
        PAR_FILE.write(f"output.1d.dim   = x\n")
    elif args.cartoon == "xz":
        PAR_FILE.write(f"output.1d.dim   = x z\n")
    else:
        PAR_FILE.write(f"output.1d.dim   = x y z\n")
    PAR_FILE.write(f"output.1d       = u.psi u.pi ana.tPsi\n")

# Closes the file
PAR_FILE.close()

# Prints a message indicating that the file has been created
print(f"Parameter file created successfully.")