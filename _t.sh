#!/bin/bash
#SBATCH --job-name=fittingT2Maps
#SBATCH --output=fittingT2Maps.out
#SBATCH --partition=cpu_short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=10G
module add dcm2niix/20211006
module add julia/1.9.4

FAKE=/gpfs/data/denizlab/Users/montie01/aaa
rm -rf $FAKE
DICOM=gpfs/data/denizlab/Datasets/OAI_original/00m/0.C.2/9000296/20040909/10693717
OUTPUTDIR=/gpfs/data/denizlab/Users/montie01/T2/OUTDIR/00m/9000296SAG_T2_MAP_RIGHT
APP=/gpfs/home/montie01/PROJECTS/T2/thestarsoft2/OAI_DataProcessing/fittingT2Maps.jl

FAKE_DICOM=$FAKE/dicom
FAKE_NIFTI=$FAKE/nifti
_DB=/gpfs/home/montie01/PROJECTS/T2/thestarsoft2/db/VA23_Knee_7ETL_10TE.mat

mkdir -p $FAKE_DICOM
mkdir -p $FAKE_NIFTI 

echo "Copying DICOM files to $FAKE_DICOM"
cp $DICOM/* $FAKE_DICOM/

rm -f $FAKE_DICOM/*.nii
rm -f $FAKE_DICOM/*.json
rm -f $FAKE_DICOM/*.nii.gz

echo "Converting DICOM to NIFTI"

dcm2niix $FAKE_DICOM/ && \

echo "Moving NIFTI files to $FAKE_NIFTI" 
mv $FAKE_DICOM/*.nii  && \
mv $FAKE_DICOM/*.json $FAKE_NIFTI/ && \
echo "Running Julia script"

echo julia $APP $FAKE_NIFTI/ $_DB $OUTPUTDIR/ 

julia $APP $FAKE_NIFTI/ $_DB $OUTPUTDIR/ 
python fix_geometry.py $FAKE_NIFTI/ $OUTPUTDIR/
