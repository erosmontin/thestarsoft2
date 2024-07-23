# T2 maps geometry informaitn are not correct,
#let's fix it using the info of the original t2 images
import pyable_eros_montin.imaginable as ima

import pynico_eros_montin.pynico as pn
def fixrois(target_image_file,source_image_file,output_image_file):
    t=ima.Imaginable(target_image_file)
    labelmap=ima.Imaginable(source_image_file)
    labelmap.setImageDirection(t.getImageDirection())
    labelmap.setImageSpacing(t.getImageSpacing())
    labelmap.setImageOrigin(t.getImageOrigin())
    labelmap.writeImageAs(output_image_file)
    

import shutil
if __name__ == '__main__':
    import sys
    
    
    target_destination=sys.argv[1]
    if target_destination[-1]!='/':
        target_destination+='/'

    source_destination=sys.argv[2]
    if source_destination[-1]!='/':
        source_destination+='/'
    T=pn.Pathable(target_destination)
    T.addBaseName('t2.nii')
    
    S=pn.Pathable(source_destination)
    S.addBaseName('t2.nii.gz')
    F=[d for d in T.getFilesInPathByExtension()]
    
    
    
    for s in S.getFilesInPathByExtension():
        fixrois(F[-1],s,s)
        
    shutil.copyfile(F[-1],source_destination+'Echo.nii')