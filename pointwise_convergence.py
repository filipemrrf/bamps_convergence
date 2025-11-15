import glob
import os
import argparse
import pymuninn
import numpy as np
import re

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process the arguments to get the data')

# Add arguments to the parser
parser.add_argument('folder', metavar='F', type=str, nargs='+', help='folder of the data')
parser.add_argument('--exact', type=int, default=0)
parser.add_argument('--debug', type=bool, default=False)
parser.add_argument('--generate', type=bool, default=False)

# Parse the arguments
args = parser.parse_args()
folder = args.folder[0].rstrip('/')  # Folder of the data

# Create the results directory if it doesn't exist
if not os.path.exists(f"{folder}/pointwise_convergence/"):
    os.makedirs(f"{folder}/pointwise_convergence/")

if args.exact:
    if not args.debug:
        out_fields = ['u.psi']
    else:
        out_fields = ['u.psi', 'u.pi', 'u.phix', 'u.phiy', 'u.phiz', 'ru.psi', 'ru.pi', 'ru.phix', 'ru.phiy', 'ru.phiz', 'stat.Omega', 'stat.alpha', 'stat.betax', 'stat.betay', 'stat.betaz', 'stat.gammaxx', 'stat.gammaxy', 'stat.gammaxz', 'stat.gammayy', 'stat.gammayz', 'stat.gammazz', 'stat.Christgammaxxx', 'stat.Christgammaxxy', 'stat.Christgammaxxz', 'stat.Christgammaxyy', 'stat.Christgammaxyz', 'stat.Christgammaxzz', 'stat.Christgammayxx', 'stat.Christgammayxy', 'stat.Christgammayxz', 'stat.Christgammayyy', 'stat.Christgammayyz', 'stat.Christgammayzz', 'stat.Christgammazxx', 'stat.Christgammazxy', 'stat.Christgammazxz', 'stat.Christgammazyy', 'stat.Christgammazyz', 'stat.Christgammazzz', 'stat.accelx', 'stat.accely', 'stat.accelz', 'stat.dbetaxx', 'stat.dbetaxy', 'stat.dbetaxz', 'stat.dbetayx', 'stat.dbetayy', 'stat.dbetayz', 'stat.dbetazx', 'stat.dbetazy', 'stat.dbetazz', 'stat.oomboxom', 'stat.oom2dom2']

    for resolution in sorted(os.listdir(folder)):
        if resolution.startswith("norm_convergence") or resolution.startswith("pointwise_convergence"):
            continue
        if os.path.isdir(f"{folder}/{resolution}"):
            # Extract nxyz as an integer using regex
            match = re.search(r'(\d+)', resolution)
            if not match:
                continue  # skip if not found
            n = int(match.group(1))

            exact_sol_generated = False

            for field in out_fields:
                # Gets the muninn data from the solution
                file = f"{folder}/{resolution}/output_1d/x/{field}"
                sol_data = pymuninn.MuninnData(file)
                sol_grid = sol_data.as_grid()

                os.chdir(f"{folder}/pointwise_convergence/")

                if args.generate:
                    if not exact_sol_generated:
                        # Generates the aux file
                        AUX = open("aux.csv", 'w')
                        AUX.write(",".join(f"{t:.16g}" for t in sol_grid.ts) + "\n")
                        AUX.write(",".join(f"{r:.16g}" for r in sol_grid.xss[0]) + "\n")
                        AUX.close()

                        # Generates the exact solution
                        if not args.debug:
                            os.system("wolframscript -file ../../../Exact_Solution.wls")
                        else:
                            os.system("wolframscript -file ../../../Exact_Solution-Debug.wls")

                        exact_sol_generated = True
                else:
                    os.system(f"cp ../../_exact_sol_cache/exact.*.n={n} .")

                # Gets the muninn data from the exact solution
                exact_data = pymuninn.MuninnData(f"exact.{field}")
                exact_grid = exact_data.as_grid()

                # Outputs the pointwise error
                OUT = open(f"pointwise_error.{field}.n={n}", 'w')

                for i, t in zip(range(len(sol_grid.ts)), sol_grid.ts):
                    OUT.write(f"\"Time = {t}\n")

                    for j, r in zip(range(len(sol_grid.xss[i])), sol_grid.xss[i]):
                        if r == 0 or r == 30:
                            continue
                        OUT.write(f"{r}\t{abs(exact_grid.values[i][j-1] - sol_grid.values[i][j])}\n")

                    OUT.write("\n")

                OUT.close()

                os.system(f"mv exact.{field} exact.{field}.n={n}")

                if args.generate:
                    os.system(f"cp exact.* ../../_exact_sol_cache/")

                os.chdir("../../../")

    os.system(f"rm {folder}/pointwise_convergence/aux.csv")