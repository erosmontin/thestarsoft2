#!/bin/bash

# Define directories
SOURCE_DIR="/gpfs/data/denizlab/Datasets/OAI/NiftiFiles/Kaggle_DESS_Masks_REMAPPED/V00_00m"
IMAGES_DIR="/gpfs/data/denizlab/Datasets/OAI/NiftiFiles/T2_Maps/00m/"
OUTPUT_DIR="/gpfs/data/denizlab/Datasets/OAI/NiftiFiles/T2_Maps/OUTPUT/"

# Iterate over each file in the source directory
for roi in "$SOURCE_DIR"/*; do
    base_name=$(basename "$roi")

    number=$(echo "$base_name" | grep -oP '\d+' | head -n 1)
    side=$(echo "$base_name" | grep -oP 'LEFT|RIGHT')
    echo "Number: $number"
    echo "Side: $side"
    imagedir=$(find "$IMAGES_DIR" -type d -name "*$number*" | grep "$side")


    # Remove the extension "nii" or "nii.gz" from the base name
    base_name="${base_name%.nii}"
    base_name="${base_name%.nii.gz}"
    base_name="${base_name%_0}"
    # Append the base name to the target directories
    outputdir="$OUTPUT_DIR$base_name.json"
    
    # Print the target paths (for debugging purposes)
    echo "Target Image: $imagedir"
    echo "Target Output: $outputdir"
    # Check if the IMAGES directory exists
    if [ -d "$imagedir" ]; then
        # Run the Python script
        python check_maps.py -l $roi -i "$imagedir" -o "$outputdir"
    # else
    #     echo "IMAGES directory does not exist."
    fi
done