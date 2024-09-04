#!/bin/bash
#SBATCH --output=/data/denizlab/Users/montie01/T2/OUTDIR/00m/9000296SAG_T2_MAP_RIGHT.out
#SBATCH --partition=cpu_short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=10G

python preparethesbatches2.py --TMPDIR /data/denizlab/Users/montie01/aaa --DICOMDIR /gpfs/data/denizlab/Datasets/OAI_original/00m/0.C.2/9000296/20040909/10693717 --FITPATH /gpfs/home/montie01/PROJECTS/T2/thestarsoft2/OAI_DataProcessing --DB /gpfs/home/montie01/PROJECTS/T2/thestarsoft2/db/VA23_Knee_7ETL_10TE.mat --OUTDIR /data/denizlab/Users/montie01//T2/OUTDIR/00m/9000296SAG_T2_MAP_RIGHT
