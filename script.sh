#!/bin/bash

#!/bin/bash



PT=$(pwd)
cd /dcm
dcm2niix .

cd $PT
# Call the Julia program with the arguments
echo julia fittingT2Maps.jl /dcm/ /db/$1 /nifti/
julia fittingT2Maps.jl /dcm/ /db/$1 /nifti/

