
import pandas as pd
import numpy as np
import os
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
        # os.makedirs(OUTDIR, exist_ok=True)
        app=APP+'/'+NAME
        # os.makedirs(app, exist_ok=True)
        tmp=tmpdir+'/'+NAME
        os.makedirs(tmp, exist_ok=True,mode=0o775)
        
        # Command to check files and run Singularity
        # cmd = f'''
        # if [ -f "{OUTDIR}/T2_MAPS_EMC.nii.gz" ] && [ -f "{OUTDIR}/T2_MAPS_MONOEXP_WITHOUT_1ST_ECHO.nii.gz" ] && [ -f "{OUTDIR}/T2_MAPS_MONOEXP.nii.gz" ]; then
        #     singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti -B {DB}:/db -B {APP}:/app docker://erosmontin/thestarsoft2:latest /bin/bash -c "cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"
        # else
        #     echo "Skipping {OUTDIR}, required files not found."
        # fi
        # '''

        # cmd = f'''singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti -B {DB}:/db -B {app}:/app docker://erosmontin/thestarsoft2:latest /bin/bash -c "cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"'''

        # cmd = f'''
        # mkdir -p -m 0777 {OUTDIR}
        # mkdir -p -m 0777 {tmp}
        # mkdir -p -m 0777 {app}
        # singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti \
        #         -B {DB}:/db -B {app}:/app \
        #         -B {tmp}:/tmp \
        #         docker://erosmontin/thestarsoft2:latest \
        #         /bin/bash -c "echo \$PWD && cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"
        # rm -rf {tmp}
        # '''


        # cmd = f'''mkdir -p -m 0777 {tmp} && singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti  -B {tmp}:/tmp docker://erosmontin/thestarsoft2:singularity /bin/bash -c "cd /app && bash script_sy.sh"'''
        cmd = f'''mkdir -p -m 0777 {tmp} && singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/{p["Folder"]}:/dcm -B {OUTDIR}:/nifti  -B {tmp}:/tmp {sif} /bin/bash -c "cd /app && bash script_sy.sh"'''

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
OUTDIR = '/gpfs/home/montie01/PROJECTS/T2/OUTDIR'
TMP='/gpfs/home/montie01/PROJECTS/T2/_TMP'
SIF='/gpfs/home/montie01/PROJECTS/T2/sif/thestarsoft2'
JOBLIST = prepare_and_submit_jobs(file_path, DB, APP, JOB_DIR,outdir=OUTDIR,tmpdir=TMP,SIF=SIF)

for job in JOBLIST:
    os.system(f'sbatch {job}')
    print(f'sbatch {job}')
print('All jobs submitted')
