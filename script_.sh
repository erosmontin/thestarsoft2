#!/bin/bash

#!/bin/bash



PT=$(pwd)
mkdir /tmp/dicom
cp /dcm/* /tmp/dicom

rm /tmp/dicom/*.nii
rm /tmp/dicom/*.json
rm /tmp/dicom/*.nii.gz

echo "Converting DICOM to NIFTI"
cd /tmp/dicom
dcm2niix .

echo "Moving NIFTI files to /tmp/NIFTI"
mkdir /tmp/NIFTI
mv /tmp/dicom/*.nii /tmp/NIFTI/
mv /tmp/dicom/*.json /tmp/NIFTI/

echo "Running Julia script"
cd $PT
# Call the Julia script
julia fittingT2Maps.jl /tmp/NIFTI/ /db/$1 /nifti/

echo "Fixing geometry"
python fix_geometry.py /tmp/NIFTI/ /nifti/

