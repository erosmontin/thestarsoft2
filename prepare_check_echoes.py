
import pandas as pd
import numpy as np
import os
import time
import glob
import pynico_eros_montin.pynico as pn
def makeSlurm(jobName, dicomdir,tmp,app,outputdir,db, partition='cpu_short', time='02:00:00', nodes='1', ntasks='1', cpus='2', mem='10G'):
    FN = jobName + '.sh'
    slurm = open(FN, 'w')
    # get path of FN
    FN_dir = os.path.dirname(os.path.abspath(FN))
    FN_name = os.path.basename(FN)
    
    
    # A=pn.Pathable(outputdir)
    # A.ensureDirectoryExistence()
    # P=j.getPath()
    # P=P.split('/')[-2]
    # A.addBaseName(f'{P}echo.txt')

    slurm.write('#!/bin/bash\n')
    slurm.write('#SBATCH --job-name='+FN_name+'\n')
    slurm.write('#SBATCH --output=/gpfs/data/denizlab/Users/montie01/T2/log/' + FN_name +'.out\n')
    slurm.write('#SBATCH --partition=' + partition + '\n')
    slurm.write('#SBATCH --time=' + time + '\n')
    slurm.write('#SBATCH --nodes=' + nodes + '\n')
    slurm.write('#SBATCH --ntasks=' + ntasks + '\n')
    slurm.write('#SBATCH --cpus-per-task=' + cpus + '\n')
    slurm.write('#SBATCH --mem=' + mem + '\n')

    slurm.write('module add dcm2niix/20211006\n')
        
    slurm.write(f'FAKE={tmp}\n')
    slurm.write('rm -rf $FAKE\n')
    slurm.write(f'DICOM={dicomdir}\n')
    slurm.write(f'OUTPUTDIR={outputdir}\n')
    slurm.write(f'APP={app}\n\n')
    
    slurm.write('FAKE_DICOM=$FAKE/dicom\n')
    slurm.write('FAKE_NIFTI=$FAKE/nifti\n')
    
    
    slurm.write('mkdir -p $FAKE_DICOM\n')
    slurm.write('mkdir -p $FAKE_NIFTI\n\n')
    
    slurm.write('echo "Copying DICOM files to $FAKE_DICOM"\n')
    slurm.write('cp $DICOM/* $FAKE_DICOM/\n\n')
    
    slurm.write('rm -f $FAKE_DICOM/*.nii\n')
    slurm.write('rm -f $FAKE_DICOM/*.json\n')
    slurm.write('rm -f $FAKE_DICOM/*.nii.gz\n\n')
    
    slurm.write('echo "Converting DICOM to NIFTI"\n')
    slurm.write('dcm2niix $FAKE_DICOM/ && \\\n\n')
    
    slurm.write('echo "Moving NIFTI files to $FAKE_NIFTI"\n')
    slurm.write('mv $FAKE_DICOM/*.nii $FAKE_NIFTI/\n')
    slurm.write('mv $FAKE_DICOM/*.json $FAKE_NIFTI/\n\n')
    
    slurm.write(f'python {app} $FAKE_NIFTI/ $OUTPUTDIR/\n\n')
    slurm.write(f'rm -rf $FAKE\n')
    slurm.close()
    return FN

def prepare_and_submit_jobs(file_path, DB, APP, TMP,JOB_DIR,outdir):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.xlsx':
        df = pd.read_excel(file_path)
    elif file_extension == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file extension. Only .xlsx and .csv are supported.")

    # Ensure directories exist
    FN = len(df)
    JOBLIST = []
    for a in range(0, FN):
        p = df.iloc[a]
        # Specify the path to the output directory
        SERIES = p['SeriesDescription']
        PID=p['ParticipantID']
        NAME=f'{PID}{SERIES}'
        OUTDIR = f'{outdir}/00m/'
        os.makedirs(OUTDIR, exist_ok=True)
        tmp=TMP+'/'+NAME
        os.makedirs(tmp, exist_ok=True)

        dicom=f'/gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}'
        if len(glob.glob(f'{dicom}/*'))<90:
            print(f'No files in {dicom}')
            continue
        job = f'{JOB_DIR}/job_{PID}_{SERIES}'
        
       
        fn=makeSlurm(f'{job}', dicom,tmp,APP,OUTDIR,DB,partition='cpu_short', time='02:00:00', nodes='1', ntasks='1', cpus='2', mem='10G')
        JOBLIST.append(fn)
    
    return JOBLIST

# Example usage





file_path = 'Book1.csv'
DB = '/gpfs/home/montie01/PROJECTS/T2/thestarsoft2/db/VA23_Knee_7ETL_10TE.mat'
APP='/gpfs/home/montie01/PROJECTS/T2/thestarsoft2/check_echoes.py'
JOB_DIR = '/gpfs/data/denizlab/Users/montie01/T2/_JOBS'
try:
    os.rmdir(JOB_DIR)
except:
    pass

OUTDIR = '/gpfs/data/denizlab/Users/montie01/T2/_ECHOS'
TMP='/gpfs/data/denizlab/Users/montie01/T2/_TMP'
os.makedirs(TMP, exist_ok=True)
JOBLIST = prepare_and_submit_jobs(file_path, DB, APP, JOB_DIR,TMP,OUTDIR)

for job in JOBLIST:
    os.system(f'sbatch {job}')
    print(f'sbatch {job}')
print('All jobs submitted')
