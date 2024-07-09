# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:10:45 2023

@author: Vaishali.Swaminathan
"""
import skimage.color
import skimage.io
import skimage.viewer
import micasense.image as image
import micasense.panel as panel
import micasense.metadata as metadata
import micasense.utils as msutils
import micasense.capture as capture
import micasense.dls as dls
import datetime, pytz, os, glob,timeit
from math import pi
import subprocess
from PIL import Image
from joblib import Parallel, delayed

import pandas as pd
import numpy as np
import os


exiftoolPath=os.path.normpath(os.environ.get('exiftoolpath'))
start_time= timeit.default_timer()
rootpath=r'G:\My Drive\Intermediate\Ground\SampleUAV\09July2020\\'
input_path= rootpath[0:-1]+'Output2\\'
output_path=rootpath[0:-1]+'PPC-Irradiance Proximity\\'

if not os.path.exists(output_path):
    os.makedirs(output_path)
    
TdfB= pd.read_excel(rootpath+'Tarp Images\Irradiance proximity calibration list.xlsx', sheet_name='B')
TdfG= pd.read_excel(rootpath+'Tarp Images\Irradiance proximity calibration list.xlsx', sheet_name='G')
TdfR= pd.read_excel(rootpath+'Tarp Images\Irradiance proximity calibration list.xlsx', sheet_name='R')
TdfRE= pd.read_excel(rootpath+'Tarp Images\Irradiance proximity calibration list.xlsx', sheet_name='RE')
TdfNIR= pd.read_excel(rootpath+'Tarp Images\Irradiance proximity calibration list.xlsx', sheet_name='NIR')
Tdf= pd.concat([TdfB, TdfG, TdfR, TdfRE, TdfNIR])

def PPC(SI):
# for SI in glob.glob(input_path[0:-1]+'\*4.tif'):
    shadow_image = skimage.io.imread(SI, as_gray=True)    #variable name for shadow dataset
    img_name =SI.split("\\")[-1]
    
    row= Tdf.loc[Tdf['Image Name']== img_name]   # retrives the row corresponding to the image from the DF
    row_loc=row.index[row['Image Name']== img_name].tolist()[0]
    m = row['LR_Slope'][row_loc].astype(float); c = row['LR_Intercept'][row_loc].astype(float)
    PPC_img= shadow_image * m + c    # post processing calibration 
        
    output_name= img_name
    im = Image.fromarray(PPC_img.astype(np.float32))     ###Change this to reflectance                    
    im.save(output_path+output_name)
    cmd= '{} -TagsFromFile "{}" -XMP "{}"'.format(exiftoolPath,SI, output_path+output_name)
    subprocess.call(cmd)
    cmd= '{} -TagsFromFile "{}" -Composite "{}"'.format(exiftoolPath,SI, output_path+output_name)
    subprocess.call(cmd)


Parallel(n_jobs=8, prefer= 'threads')(delayed(PPC)(SI) for SI in glob.glob(input_path[0:-1]+'\*5.tif'))
for or_files in glob.glob(output_path+'*_original'):
# for or_files in glob.glob(op_path+'*\*_original'):   ##only for calibration panel (Amrit's)
    os.remove(or_files)     
        
stop_time=timeit.default_timer()
print("Computation time=", stop_time-start_time)