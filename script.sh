#!/bin/bash

#!/bin/bash



PT=$(pwd)
cd /dcm
dcm2niix .

mkdir /tmp/NIFTI
mv /dcm/*.nii /tmp/NIFTI/
mv /dcm/*.json /tmp/NIFTI/
cd $PT
# Call the Julia program with the arguments
echo julia fittingT2Maps.jl /dcm/ /db/$1 /nifti/
julia fittingT2Maps.jl /tmp/NIFTI/ /db/$1 /nifti/


