#!/bin/bash

#!/bin/bash



PT=$(pwd)
mkdir /tmp/dicom
cp /dcm/* /tmp/dicom

rm /tmp/dicom/*.nii
rm /tmp/dicom/*.json
rm /tmp/dicom/*.nii.gz
cd /tmp/dicom
dcm2niix .

mkdir /tmp/NIFTI
mv /tmp/dicom/*.nii /tmp/NIFTI/
mv /tmp/dicom/*.json /tmp/NIFTI/
cd $PT
# Call the Julia program with the arguments
julia fittingT2Maps.jl /tmp/NIFTI/ /db/$1 /nifti/





# #!/bin/bash



# PT=$(pwd)
# mkdir /tmp/dicom
# # Create symbolic links for all files in /tmp/dicom to /dcm
# for file in `ls -d /dcm/*`
# do
#     ln -s $file /tmp/dicom/
# done

# cd /tmp/dicom
# donedcm2niix .

# mkdir /tmp/NIFTI
# mv /tmp/dicom/*.nii /tmp/NIFTI/
# mv /tmp/dicom/*.json /tmp/NIFTI/
# cd $PT
# # Call the Julia program with the arguments

# julia fittingT2Maps.jl /tmp/NIFTI/ /db/$1 /nifti/

# # Remove the symbolic links

# rm -rf /tmp/dicom
# rm -rf /tmp/NIFTI