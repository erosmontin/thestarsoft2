
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

# Specify the path to your .xlsx file
file_path = 'Book1.xlsx'
# Read the .xlsx file
df = pd.read_excel(file_path)
#directory with the MAT files
DB = '/gpfs/home/montie01/PROJECTS/OAI/'
MODULES=['singularity/3.9.8']
APP='/gpfs/home/montie01/tmp/app'
os.makedirs(APP, exist_ok=True)
JOB_DIR = '/gpfs/home/montie01/tmp/jobs'
os.makedirs(JOB_DIR, exist_ok=True)
JOBLIST=[]
FN=len(df)
FN=1
for a in range(0, FN):
    p=df.iloc[a]
    # Specify the path to the output directory
    OUTDIR = f'/gpfs/data/denizlab/Datasets/OAI/T2/00m/{p['PartecipantID']}/'
    os.makedirs(OUTDIR, exist_ok=True)
    
    # cmd=f'singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti -B {DB}:/db -B {APP}:/app  docker://erosmontin/thestarsoft2:latest  /bin/bash -c "cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"'
    cmd=f'''
    if [ -f "{OUTDIR}/T2_MAPS_EMC.nii.gz" ] && [ -f "{OUTDIR}/T2_MAPS_MONOEXP_WITHOUT_1ST_ECHO.nii.gz" ] && [ -f "{OUTDIR}/T2_MAPS_MONOEXP.nii.gz" ]; then
        singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti -B {DB}:/db -B {APP}:/app docker://erosmontin/thestarsoft2:latest /bin/bash -c "cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"
    else
        echo "Skipping {OUTDIR}, required files not found."
    fi
    '''
    job=f'{JOB_DIR}/job_{p["PartecipantID"]}'
    makeSlurm(f'{job}', cmd, partition='cpu_short', modules=MODULES, time='02:00:00')
    JOBLIST.append(job)

for job in JOBLIST:
    os.system(f'sbatch {job}')
    print(f'sbatch {job}')
print('All jobs submitted')
