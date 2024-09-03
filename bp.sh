
# first
mkdir /gpfs/home/montie01/PROJECTS/OAI/TS3

singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/0.C.2/9000296/20040909/10693717/:/dcm \
                 -B /gpfs/home/montie01/PROJECTS/OAI/TS:/nifti \
                 -B /gpfs/home/montie01/PROJECTS/OAI/:/db \
                 -B /gpfs/home/montie01/tmp/app:/app \
                 docker://erosmontin/thestarsoft2:latest \
                 /bin/bash -c "echo \$PWD && cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"






singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/0.C.2/9000296/20040909/10693717/:/dcm \
                 -B /gpfs/home/montie01/PROJECTS/OAI/TS2:/nifti \
                 docker://erosmontin/thestarsoft2:singularity \
                 /bin/bash -c "echo \$PWD && cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"



mkdir /gpfs/home/montie01/PROJECTS/OAI/TS_
mkdir /gpfs/home/montie01/PROJECTS/OAI/_
singularity exec -B /gpfs/data/denizlab/Datasets/OAI_original/00m/0.C.2/9000296/20040909/10693717/:/dcm \
                 -B /gpfs/home/montie01/PROJECTS/OAI/TS_:/nifti \
                 -B /gpfs/home/montie01/PROJECTS/OAI/:/db \
                 -B /gpfs/home/montie01/tmp/app:/app \
                 -B /gpfs/home/montie01/PROJECTS/OAI/_:/tmp \
                 docker://erosmontin/thestarsoft2:latest \
                 /bin/bash -c "echo \$PWD && cd /app && bash script.sh VA23_Knee_7ETL_10TE.mat"
