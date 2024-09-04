#!/bin/bash
#SBATCH --partition=cpu_short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=10G
module add dcm2niix/20211006
module add julia/1.9.4

mkdir -p /gpfs/data/denizlab/Users/montie01/aaa/dicom
cp /gpfs/data/denizlab/Datasets/OAI_original/00m/0.C.2/9000296/20040909/10693717 * /gpfs/data/denizlab/Users/montie01/aaa
rm -f /gpfs/data/denizlab/Users/montie01/aaa/dicom*.nii
rm -f /gpfs/data/denizlab/Users/montie01/aaa/dicom*.json
rm -f /gpfs/data/denizlab/Users/montie01/aaa/dicom*.nii.gz
echo "Converting DICOM to NIFTI"

dcm2niix /gpfs/data/denizlab/Users/montie01/aaa/dicom && \
echo "Moving NIFTI files to /gpfs/data/denizlab/Users/montie01/aaa/nifti" && \
mkdir -p /gpfs/data/denizlab/Users/montie01/aaa/nifti && \
mv /gpfs/data/denizlab/Users/montie01/aaa//dicom*.nii /gpfs/data/denizlab/Users/montie01/aaa/nifti/ && \
mv /gpfs/data/denizlab/Users/montie01/aaa//dicom*.json /gpfs/data/denizlab/Users/montie01/aaa/nifti/ && \
echo "Running Julia script" && \

julia  /gpfs/home/montie01/PROJECTS/T2/thestarsoft2/OAI_DataProcessing/fittingT2Maps.jl /gpfs/data/denizlab/Users/montie01/aaa/nifti/ /app/db/VA23_Knee_7ETL_10TE.mat /nifti/ && \
python fix_geometry.py /gpfs/data/denizlab/Users/montie01/aaa/nifti/ /data/denizlab/Users/montie01//T2/OUTDIR/00m/9000296SAG_T2_MAP_RIGHT
