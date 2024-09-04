
import pandas as pd
import numpy as np
import os
import time
import glob
def makeSlurm(jobName, job,partition='cpu_short', time='cpu_long', nodes='1', ntasks='1', cpus='2', mem='10G',modules=[]):
    FN=jobName+ '.sh'
    slurm = open(FN, 'w')
    slurm.write('#!/bin/bash\n')
    # slurm.write('#SBATCH --job-name=' + jobName + '\n')
    slurm.write('#SBATCH --output=' + jobName + '.out\n')
    slurm.write('#SBATCH --partition=' + partition + '\n')
    slurm.write('#SBATCH --time=' + time + '\n')
    slurm.write('#SBATCH --nodes=' + nodes + '\n')
    slurm.write('#SBATCH --ntasks=' + ntasks + '\n')
    slurm.write('#SBATCH --cpus-per-task=' + cpus + '\n')
    slurm.write('#SBATCH --mem=' + mem + '\n')
    if len(modules) > 0:
        for module in modules:
            slurm.write(f'module load {module}\n')
    slurm.write(f'{job}\n')
    slurm.close()
    return FN

def prepare_and_submit_jobs(file_path, DB, APP, JOB_DIR,outdir,tmpdir,sif):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.xlsx':
        df = pd.read_excel(file_path)
    elif file_extension == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file extension. Only .xlsx and .csv are supported.")


    # Ensure directories exist
    os.makedirs(APP, exist_ok=True,mode=0o775)
    os.makedirs(JOB_DIR, exist_ok=True,mode=0o775)
    MODULES=[]
    # MODULES = ['singularity/3.9.8']
    JOBLIST = []
    FN = len(df)
    
    for a in range(0, FN):
        p = df.iloc[a]
        # Specify the path to the output directory
        SERIES = p['SeriesDescription']
        PID=p['ParticipantID']
        NAME=f'{PID}{SERIES}'
        OUTDIR = f'{outdir}/00m/{PID}{SERIES}/'
        os.makedirs(OUTDIR, exist_ok=True)
        # os.makedirs(app, exist_ok=True)
        tmp=tmpdir+'/'+NAME
        os.makedirs(tmp, exist_ok=True,mode=0o777)
               # Wait until the directory is created and accessible
        while not (os.path.exists(tmp) and os.access(tmp, os.W_OK)):
            time.sleep(1)

        DCM=f'/gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}'
        if len(glob.glob(f'{DCM}/*'))>90:
            print(f'No files in {DCM}')
            continue
        # cmd = f'''mkdir -p -m 0777 {tmp} && singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti  -B {tmp}:/tmp docker://erosmontin/thestarsoft2:singularity /bin/bash -c "cd /app && bash script_sy.sh"'''
        cmd = f''' singularity exec -B {DCM}:/dcm -B {OUTDIR}:/nifti  -B {tmp}:/tmp {sif} /bin/bash -c "cd /app && bash script_sy.sh" && rm -rf {tmp}'''

        job = f'{JOB_DIR}/job_{PID}_{SERIES}'
        # out= f'{OUTDIR}/job_{p["ParticipantID"]}.out'
        fn=makeSlurm(f'{job}', cmd, partition='cpu_short', modules=MODULES, time='02:00:00')
        JOBLIST.append(fn)
    
    return JOBLIST

# Example usage
file_path = 'debug.csv'
DB = '/gpfs/home/montie01/PROJECTS/OAI/'
APP = '/gpfs/home/montie01/tmp/app'
JOB_DIR = '/gpfs/home/montie01/PROJECTS/T2/JOBS'
OUTDIR = '/gpfs/data/denizlab/Users/montie01//T2/OUTDIR'
TMP='/gpfs/data/denizlab/Users/montie01/T2/_TMP'
SIF='/gpfs/home/montie01/PROJECTS/T2/sif/thestarsoft2.sif'
JOBLIST = prepare_and_submit_jobs(file_path, DB, APP, JOB_DIR,outdir=OUTDIR,tmpdir=TMP,sif=SIF)

# for job in JOBLIST:
#     os.system(f'sbatch {job}')
#     print(f'sbatch {job}')
# print('All jobs submitted')
