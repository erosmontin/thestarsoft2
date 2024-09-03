
import pandas as pd
import numpy as np
import os
def makeSlurm(jobName, job, partition='cpu_short', time='cpu_long', nodes='1', ntasks='1', cpus='2', mem='10G',modules=[]):
    slurm = open(jobName, 'w')
    slurm.write('#!/bin/bash\n')
    slurm.write('#SBATCH --job-name=' + jobName + '\n')
    slurm.write('#SBATCH --output=' + jobName + '.out\n')
    slurm.write('#SBATCH --partition=' + partition + '\n')
    slurm.write('#SBATCH --time=' + time + '\n')
    slurm.write('#SBATCH --nodes=' + nodes + '\n')
    slurm.write('#SBATCH --ntasks=' + ntasks + '\n')
    slurm.write('#SBATCH --cpus-per-task=' + cpus + '\n')
    slurm.write('#SBATCH --mem=' + mem + '\n')
    for module in modules:
        slurm.write(f'module load {module}\n')
    slurm.write(f'{job}\n')
    slurm.close()

def prepare_and_submit_jobs(file_path, DB, APP, JOB_DIR):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.xlsx':
        df = pd.read_excel(file_path)
    elif file_extension == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file extension. Only .xlsx and .csv are supported.")


    # Ensure directories exist
    os.makedirs(APP, exist_ok=True)
    os.makedirs(JOB_DIR, exist_ok=True)
    
    MODULES = ['singularity/3.9.8']
    JOBLIST = []
    FN = len(df)
    FN = 2 
    
    for a in range(0, FN):
        p = df.iloc[a]
        # Specify the path to the output directory
        OUTDIR = f'/gpfs/data/denizlab/Datasets/OAI/T2/00m/{p["ParticipantID"]}/'
        os.makedirs(OUTDIR, exist_ok=True)
        
        # Command to check files and run Singularity
        cmd = f'''
        if [ -f "{OUTDIR}/T2_MAPS_EMC.nii.gz" ] && [ -f "{OUTDIR}/T2_MAPS_MONOEXP_WITHOUT_1ST_ECHO.nii.gz" ] && [ -f "{OUTDIR}/T2_MAPS_MONOEXP.nii.gz" ]; then
            singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti -B {DB}:/db -B {APP}:/app docker://erosmontin/thestarsoft2:latest /bin/bash -c "cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"
        else
            echo "Skipping {OUTDIR}, required files not found."
        fi
        '''
        
        job = f'{JOB_DIR}/job_{p["ParticipantID"]}'
        makeSlurm(f'{job}', cmd, partition='cpu_short', modules=MODULES, time='02:00:00')
        JOBLIST.append(job)
    
    return JOBLIST

# Example usage
file_path = 'Book1.csv'
DB = '/gpfs/home/montie01/PROJECTS/OAI/'
APP = '/gpfs/home/montie01/PROJECTS/T2/APP'
JOB_DIR = '/gpfs/home/montie01/PROJECTS/T2/JOBS'

JOBLIST = prepare_and_submit_jobs(file_path, DB, APP, JOB_DIR)

for job in JOBLIST:
    os.system(f'sbatch {job}')
    print(f'sbatch {job}')
print('All jobs submitted')
