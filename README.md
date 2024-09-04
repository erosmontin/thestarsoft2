# The stars of t2
Contenerized version of the t2 map script in

## OAI Data
Ozkan CigDem Ph.D.


## julia code 
Elisa Marchetto Ph.D.

## Architecture
Eros Montin Ph.D.


### Build
```
git clone https://github.com/erosmontin/thestarsoft2
cd thestarsoft2
docker build -t t2julia .

```

### Run 
```
docker run -v /home/eros/Downloads/Example/Example/10424416/:/dcm -v /g/nifti:/nifti -v /home/eros/Downloads/Example/Example/db:/db erosmontin/thestarsoft2:latest VA23_Knee_7ETL_10TE.mat
```




### singularity
pull the image
```
 singularity pull --name ~/thestarsoft2.sif docker://erosmontin/thestarsoft2:singularity
 rm -rf ../_TMP/ ../OUTDIR/ ../JOBS/

```

[*Dr. Eros Montin, PhD*](http://biodimensional.com)
**46&2 just ahead of me!**