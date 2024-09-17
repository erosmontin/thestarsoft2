import argparse
import pyable_eros_montin.imaginable as ima
import datetime
import platform
import os
import numpy as np
parser = argparse.ArgumentParser(description='Chec Directories')

def checkDirEndsWithSlash(_dir):
    # Ensure image_dir ends with a separator
    if not _dir.endswith(os.path.sep):
        _dir += os.path.sep
    return _dir
def getPlatformInfo():
    return {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "user": os.getlogin()
    }
# Add the arguments
parser.add_argument('-l', '--labelmap', type=str, required=True, help='path to the labelmap')
parser.add_argument('-i', '--image', type=str, required=True, help='path to the image directory')
# Create a mutually exclusive group for out and outdir
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-o', '--out', type=str, help='output JSON filename')
group.add_argument('-O', '--outdir', type=str, help='output directory for the JSON file')

# Parse the arguments
args = parser.parse_args()


labelmap = args.labelmap
image_dir = args.image
out = args.out
out_dir = args.outdir

print(f'Labelmap: {labelmap}')
image_dir = checkDirEndsWithSlash(image_dir)
print(f'Image Directory: {image_dir}')
if out:
    print(f'Output JSON Filename: {out}')
if out_dir:
    out_dir = checkDirEndsWithSlash(out_dir)
    print(f'Output Directory: {out_dir}')



IMG=['T2_MAPS_EMC.nii.gz','T2_MAPS_MONOEXP_WITHOUT_1ST_ECHO.nii.gz','T2_MAPS_MONOEXP.nii.gz']
# IMG=['fo.nii','wo.nii']
MAPS = [os.path.join(image_dir, img) for img in IMG]
# Check if all MAPS exist
for map_file in MAPS:
    if not os.path.exists(map_file):
        print(f"Error: {map_file} does not exist.")
        exit()

if not os.path.exists(labelmap):
    print(f"Error: {labelmap} does not exist.")
    exit()

ROI = ima.Imaginable(labelmap)
ROIV=ROI.getImageUniqueValues()

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


for r in ROIV:
    ROI = ima.Roiable(labelmap, roivalue=r)
    for m in MAPS:
        IM=ima.Imaginable(m)
        filename = os.path.basename(m)
        IM.resampleOnTargetImage(ROI)
        N=ima.getMaskedNunmpyArray(IM,ROI)
        N=N.astype(np.float64)
        v=int(np.array(len(N)).astype(np.float64))
        V=int(np.array(v*IM.getVoxelVolume()))
        V={"mean":N.mean(),"std":N.std(),"max":N.max(),"min":N.min(),"numerosity":v,"volume":V}
        OUT['data'].append({"roi_value":int(r),"map":filename,"values":V})
        
import pynico_eros_montin.pynico as pn

print(OUT)
A=pn.Pathable(out)
A.ensureDirectoryExistence()
A.writeJson(OUT)

