#!/bin/bash

# Define directories
SOURCE_DIR="/gpfs/data/denizlab/Datasets/OAI/NiftiFiles/Kaggle_DESS_Masks_REMAPPED/V00_00m"
IMAGES_DIR="/gpfs/data/denizlab/Datasets/OAI/NiftiFiles/T2_Maps/00m/"
OUTPUT_DIR="/gpfs/data/denizlab/Datasets/OAI/NiftiFiles/T2_Maps/OUTPUT/"
STRUCTURAL_DIR="/gpfs/data/denizlab/Datasets/OAI/NiftiFiles/SAG_3D_DESS/00m/"
# Iterate over each file in the source directory
for roi in "$SOURCE_DIR"/*; do
    base_name=$(basename "$roi")

    number=$(echo "$base_name" | grep -oP '\d+' | head -n 1)
    side=$(echo "$base_name" | grep -oP 'LEFT|RIGHT')

    imagedir=$(find "$IMAGES_DIR" -type d -name "*$number*" | grep "$side")

    structural=$(find "$STRUCTURAL_DIR" -depth -name "$number*" | grep "$side" | grep ".nii.gz")


    # Remove the extension "nii" or "nii.gz" from the base name
    base_name="${base_name%.nii}"
    base_name="${base_name%.nii.gz}"
    base_name="${base_name%_0}"
    # Append the base name to the target directories
    outputdir="$OUTPUT_DIR$base_name.json"
    
    # Print the target paths (for debugging purposes)
    echo "--------------------"
    echo "BASE NAME: $base_name"
    echo "ROI: $roi"
    echo "IMAGES: $imagedir"
    echo "OUTPUT: $outputdir"
    echo "STRUCTURAL: $structural"
    echo "--------------------"
    # Check if the IMAGES directory exists
    if [ -d "$imagedir" ]; then
        if [ -f "$structural" ]; then      

        # Run the Python script
        echo "Number: $number"
        echo "Side: $side"
        echo "Running Python script..."
        echo "python check_maps2.py -l $roi -i \"$imagedir\" -o \"$outputdir\" -p -s \"$structural\""
        python check_maps2.py -l $roi -i "$imagedir" -o "$outputdir" -p -s "$structural"
    else
        echo "$structural  does not exist."
    fi
    else
        echo "$imagedir directory does not exist."
    fi
done