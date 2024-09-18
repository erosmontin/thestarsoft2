import argparse
import pyable_eros_montin.imaginable as ima
import datetime
import platform
import os
import numpy as np
parser = argparse.ArgumentParser(description='Chec Directories')

from pynico_eros_montin.pynico import checkDirEndsWithSlash, getPlatformInfo

# Add the arguments
parser.add_argument('-l', '--labelmap', type=str, required=True, help='path to the labelmap')

# Create a mutually exclusive group for image and multiple-input
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--image', type=str, help='path to the image directory',default=None)
group.add_argument('-m', '--multipleinput', nargs='+', help='path to the multiple input files',default=[])

parser.add_argument('-r', '--roivalues', nargs='+', help="roivalues (don't specify if you want all roivalues)",default=[])
# Create a mutually exclusive group for out and outdir
group2 = parser.add_mutually_exclusive_group(required=True)
group2.add_argument('-o', '--out', type=str, help='output JSON filename')
group2.add_argument('-O', '--outdir', type=str, help='output directory for the JSON file')

# Add the -p/--print argument
parser.add_argument('-p', '--print', dest='print', action='store_true', help='print the output')

# Add the -no-p argument
parser.add_argument('-no-p','--no-print', dest='print', action='store_false', help='do not print the output')

parser.add_argument('-s','--structural', type=str, help='path to the structural image',default=None)
# Set the default value for the print option
parser.set_defaults(print=False)

# Parse the arguments
args = parser.parse_args()


labelmap = args.labelmap
image_dir = args.image
out = args.out
out_dir = args.outdir
MAPS = args.multipleinput
ROIV=args.roivalues
print_plot=args.print

structural=args.structural
print(f'Labelmap: {labelmap}')

if len(MAPS) ==0:
    image_dir = checkDirEndsWithSlash(image_dir)
    IMG=['T2_MAPS_EMC.nii.gz','T2_MAPS_MONOEXP_WITHOUT_1ST_ECHO.nii.gz','T2_MAPS_MONOEXP.nii.gz']
    # IMG=['fo.nii','wo.nii']
    MAPS = [os.path.join(image_dir, img) for img in IMG]
# Check if all MAPS exist

print(f'Images')
for map_file in MAPS:
    if not os.path.exists(map_file):
        print(f"Error: {map_file} does not exist.")
        exit()
    else:
        if map_file == MAPS[-1]:
            print(map_file)
        else:
            print(map_file,end=', ')

print('\n')

        




if out:
    print(f'Output JSON Filename: {out}')
    plotdir=checkDirEndsWithSlash(os.path.dirname(out))
if out_dir:
    out_dir = checkDirEndsWithSlash(out_dir)
    print(f'Output Directory: {out_dir}')
    plotdir=out_dir

if not os.path.exists(plotdir):
    os.makedirs(plotdir)
    

if not os.path.exists(labelmap):
    print(f"Error: {labelmap} does not exist.")
    exit()

if len(ROIV) > 0:
    ROIV = [int(r) for r in ROIV]
else:
    ROI = ima.Imaginable(labelmap)
    ROIV=ROI.getImageUniqueValues()
    ROIV = [int(r) for r in ROIV if int(r)>0]
OUT={
    "hdr": {
        "version": "0.1",
        "calculation":{
        "labelmap": labelmap,
        "image_dir": image_dir,
        "out": out
    },
    "platform": getPlatformInfo()
    },
    "data": []
}
import matplotlib.pyplot as plt

import math
n = len(MAPS)
if math.isqrt(n)**2 == n:  # n is a perfect square
    cols = n
elif n > 4:  # n is not a perfect square and greater than 4
    cols = int(math.sqrt(n))
else:  # n is not a perfect square and less than or equal to 4
    cols = n
rows = math.ceil(n / cols)

AXIS=0

import SimpleITK as sitk
from scipy import ndimage
FILTERD=[None,None,None]
for r in ROIV:


    subplot_size = 6
    fig=plt.figure(figsize=(cols * subplot_size, rows * subplot_size))
    n=0
    J=os.path.basename(out).replace('.json','')
    max=None
    for _n,m in enumerate(MAPS):
        ROI = ima.Roiable(labelmap, roivalue=r)
        ROI.dicomOrient('RPI')
        IM=ima.Imaginable(m)
        filename = os.path.basename(m)
        IM.dicomOrient('RPI')            
        ROI.resampleOnTargetImage(IM)
        N=ima.getMaskedNunmpyArray(IM,ROI).astype(np.float64)
        N=N[N>0]
        N=N[N<10]
        v=int(np.array(len(N)).astype(np.float64))
        V=int(np.array(v*IM.getVoxelVolume()))
        V={"mean":N.mean(),"std":N.std(),"max":N.max(),"min":N.min(),"numerosity":v,"volume":V}
        OUT['data'].append({"roi_value":int(r),"map":filename,"values":V})
        if print_plot:
            n+=1
            ax = fig.add_subplot(rows, cols, n)  # Add a subplot to the figure
            if structural==None:
                structural=m        
            S=ima.Imaginable(structural)
            S.resampleOnTargetImage(IM)
            S.dicomOrient('RPI')
            IM.multiply(ROI)
            map=os.path.basename(m).replace('.nii.gz','')
            map=map.replace('.nii','').replace('T2_MAPS_','')
            _B=ROI.getBoundingBox() 
            B=[int(b) for b in np.mean(np.array(_B),axis=0)]
            
            _B=list(_B)

            _B[1]=_B[1]+1

            # S.cropImage(_B[0].astype(list),_B[1].astype(list))
            # IM.cropImage(_B[0].astype(list),_B[1].astype(list))
            
            # # Assuming ROI is your region of interest
            # ROI.cropImage(_B[0].astype(list),_B[1].astype(list))
            centroid = ROI.getCenterOfGravityIndex()
            S.overlayAble(IM,AXIS,int(centroid[AXIS]),show=False,title=f'{map} ROI {r}',alpha_value=0.3,image_cmap='gray',labelmap_cmap='jet',labelmap_vmin=0,labelmap_vmax=0.2,image_vmin=0,image_vmax=500)

    FN=os.path.join(plotdir,f'{J}__ROI_{r}.png')            
    fig.savefig(FN,dpi=300)
    plt.close(fig)            
            

import pynico_eros_montin.pynico as pn

print(OUT)
A=pn.Pathable(out)
A.ensureDirectoryExistence()
A.writeJson(OUT)

