#!/bin/bash
#SBATCH --partition=cpu_short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=10G
module add dcm2niix/20211006
module add julia/1.9.4

python preparemap.py --TMPDIR /gpfs/data/denizlab/Users/montie01/aaa --DICOMDIR /gpfs/data/denizlab/Datasets/OAI_original/00m/0.C.2/9000296/20040909/10693717 

julia -e /gpfs/home/montie01/PROJECTS/T2/thestarsoft2/OAI_DataProcessing/fittingT2Maps.jl /gpfs/data/denizlab/Users/montie01/aaa/nifti /gpfs/home/montie01/PROJECTS/T2/thestarsoft2/db/VA23_Knee_7ETL_10TE.mat  /data/denizlab/Users/montie01//T2/OUTDIR/00m/9000296SAG_T2_MAP_RIGHT

python fix_geometry.py /gpfs/data/denizlab/Users/montie01/aaa /data/denizlab/Users/montie01//T2/OUTDIR/00m/9000296SAG_T2_MAP_RIGHT