# The stars of t2


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
docker run -v /home/eros/Downloads/Example/Example/10424416/:/dcm -v /g/nifti:/nifti -v /home/eros/Downloads/Example/Example/db:/db t2julia VA23_Knee_7ETL_10TE.mat
```

[*Dr. Eros Montin, PhD*](http://biodimensional.com)
**46&2 just ahead of me!**