import tarfile
from zipfile import ZipFile 
import patoolib

import os
import shutil

def unzip(INPATH, OUTPATH):
    z = ZipFile(INPATH, 'r')
    z.extractall(OUTPATH)
    z.close()

def untar(INPATH, OUTPATH):
    t = tarfile.open(INPATH)
    t.extractall(OUTPATH)
    t.close()

def unrar(INPATH, OUTPATH):
    if os.path.isdir(OUTPATH):
        shutil.rmtree(OUTPATH)
    
    os.mkdir(OUTPATH)
    patoolib.extract_archive(INPATH, verbosity=-1, outdir=OUTPATH)
