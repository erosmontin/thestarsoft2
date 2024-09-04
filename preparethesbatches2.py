import os
import shutil
import subprocess
import glob
import argparse
def run_command(command):
    """Run a shell command and check for errors."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        raise Exception(f"Command failed: {command}")
    else:
        print(result.stdout)

def main(DICOM,TMPDIR='/tmp',FITPATH='/fit.jl',DB='/db',OUTDIR='/out'):
    # Set the current working directory
    PT = os.getcwd()

    DICOMDIR = os.path.join(TMPDIR, 'dicom')
    NIFTIDIR = os.path.join(TMPDIR, 'nifti')
    
    os.makedirs(DICOMDIR, exist_ok=True)
    for file in os.listdir(DICOM):
        shutil.copy(os.path.join('/dcm', file), DICOMDIR)

    # Remove any existing NIfTI and JSON files in /tmp/dicom
    for ext in ['*.nii', '*.json', '*.nii.gz']:
        for file in glob.glob(f'/tmp/dicom/{ext}'):
            os.remove(file)

    # Convert DICOM to NIFTI
    print("Converting DICOM to NIFTI")
    run_command(f'dcm2niix {DICOMDIR}')

    # Move NIFTI files to /tmp/NIFTI
    print("Moving NIFTI files to /tmp/NIFTI")
    os.makedirs(NIFTIDIR, exist_ok=True)
    for ext in ['*.nii', '*.json']:
        for file in glob.glob(f'/tmp/dicom/{ext}'):
            shutil.move(file, NIFTIDIR)

    # Run Julia script
    print("Running Julia script")
    os.chdir(PT)
    run_command(f'julia {FITPATH} {NIFTIDIR} {DB} {OUTDIR}')

    # Fix geometry
    print("Fixing geometry")
    run_command(f'python fix_geometry.py {NIFTIDIR} {OUTDIR}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process DICOM files and convert them to NIFTI.')
    parser.add_argument('--DICOMDIR', type=str, help='Directory containing DICOM files')
    parser.add_argument('--TMPDIR', type=str, default='/tmp', help='Temporary directory for processing')
    parser.add_argument('--FITPATH', type=str, default='/fit.jl', help='Path to the Julia script for fitting T2 maps')
    parser.add_argument('--DB', type=str, default='/db', help='Path to the database file')
    parser.add_argument('--OUTDIR', type=str, default='/out', help='Output directory for results')

    args = parser.parse_args()
    DICOM = args.DICOMDIR
    TMPDIR = args.TMPDIR
    FITPATH = args.FITPATH
    DB = args.DB
    OUTDIR = args.OUTDIR
    os.makedirs(TMPDIR, exist_ok=True)
    
    main(DICOM, TMPDIR, FITPATH, DB, OUTDIR)

    os.rmdir(TMPDIR, exist_ok=True)

