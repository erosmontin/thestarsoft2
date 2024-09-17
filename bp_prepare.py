def makeslurm(shfile,j,output):
    with open(shfile, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --ntasks=1\n")
        f.write("#SBATCH --cpus-per-task=2\n")
        f.write("#SBATCH --time=5-00:00:00\n")
        f.write("#SBATCH --mem=10G\n")
        f.write("#SBATCH --partition=cpu_medium\n\n")
        f.write(f"python 05_extraction.py --JSON {j} --RESULTSOUTPUT {output}/\n")
        
import argparse
def main():
    parser = argparse.ArgumentParser(description='Prepare the slurm file for caluclate t2 map')
    parser.add_argument('T2', required=True, help='Path to the JSON file')
    parser.add_argument('--OUTPUT', required=True, help='Path to the output directory')
    args = parser.parse_args()
    



    makeslurm(f"{args.OUTPUT}/extraction.sh",args.JSON,args.OUTPUT)