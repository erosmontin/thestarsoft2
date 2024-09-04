#!/bin/bash
PT=$(pwd)
mkdir -p /tmp/dicom
cp /dcm/* /tmp/dicom
rm -f /tmp/dicom/*.nii
rm -f /tmp/dicom/*.json
rm -f /tmp/dicom/*.nii.gz
echo "Converting DICOM to NIFTI"
cd /tmp/dicom
# dcm2niix .
# echo "Moving NIFTI files to /tmp/NIFTI"
# mkdir /tmp/NIFTI
# mv /tmp/dicom/*.nii /tmp/NIFTI/
# mv /tmp/dicom/*.json /tmp/NIFTI/
# echo "Running Julia script"
# cd $PT
# julia /app/fittingT2Maps.jl /tmp/NIFTI/ /app/db/VA23_Knee_7ETL_10TE.mat /nifti/
# echo "Fixing geometry"
# python fix_geometry.py /tmp/NIFTI/ /nifti/
dcm2niix . && \
echo "Moving NIFTI files to /tmp/NIFTI" && \
mkdir -p /tmp/NIFTI && \
mv /tmp/dicom/*.nii /tmp/NIFTI/ && \
mv /tmp/dicom/*.json /tmp/NIFTI/ && \
echo "Running Julia script" && \
cd $PT && \
julia OAI_DataProcessing/fittingT2Maps.jl /tmp/NIFTI/ /app/db/VA23_Knee_7ETL_10TE.mat /nifti/ && \
echo "Fixing geometry" && \
python fix_geometry.py /tmp/NIFTI/ /nifti/