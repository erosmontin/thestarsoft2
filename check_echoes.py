import pynico_eros_montin.pynico as pn
import pyable_eros_montin.imaginable as ima
import sys
import sqlite3
INDIR=pn.checkDirEndsWithSlash(sys.argv[1])
OUTDIR=pn.checkDirEndsWithSlash(sys.argv[2])
T=pn.Pathable(INDIR)
T.addBaseName('t2.nii')
OUT=[]
INFO=["EchoTime"]
for t in sorted(T.getFilesInPathByExtension()):
    j=pn.Pathable(t)
    j.changeExtension('json')
    OUT.append(ima.dcm2niixFieldsToJson(j.getPosition(),INFO))
A=pn.Pathable(OUTDIR)
A.ensureDirectoryExistence()
P=j.getPath()
P=P.split('/')[-2]
A.addBaseName(f'{P}echo.txt')
print(A.getPosition())
with open(A.getPosition(), 'w') as f:
    for o in OUT:
        f.write(str(o["EchoTime"]))
        if o!=OUT[-1]:
            f.write(',')
        else:
            f.write('\n')
            


