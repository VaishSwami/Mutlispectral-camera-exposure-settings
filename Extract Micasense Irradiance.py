# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 12:59:39 2023

@author: Vaishali.Swaminathan
"""
"""
This is a script to extract and plot irradiance from the Micasense raw image files
The function below has tips to extract other metadata information like exposure time, Lat, Long 
Change the input file path
To install Micasense-image processing packages and dependencies: 
    https://micasense.github.io/imageprocessing/MicaSense%20Image%20Processing%20Setup.html
"""

import numpy as np
import skimage.color
import skimage.io
import skimage.viewer
#from matplotlib import pyplot as plt
#import micasense.image as image
# import micasense.panel as panel
import micasense.metadata as metadata
import micasense.utils as msutils
import micasense.capture as capture
import micasense.dls as dls
import datetime, pytz, os, glob,timeit
from math import pi
import subprocess
from PIL import Image
from joblib import Parallel, delayed
import matplotlib.pyplot as plt

R1=[];R2=[];R3=[];R4=[];R5=[]
x=[];y=[]

def get_irrad_profile(SI):
    shadow_meta = metadata.Metadata(SI, exiftoolPath=exiftoolPath)
    shadow_incident= shadow_meta.get_item('XMP:Irradiance')
    exptime=shadow_meta.get_item('EXIF:ExposureTime')
    gain=shadow_meta.get_item('EXIF:ISOSpeed')/100.0
    si_location=(shadow_meta.get_item('Composite:GPSLongitude'),shadow_meta.get_item('Composite:GPSLatitude'))
#    si_dls_pose=(float(shadow_meta.get_item('XMP:Yaw')),float(shadow_meta.get_item('XMP:Pitch')),float(shadow_meta.get_item('XMP:Roll')))
#    si_utc_time= datetime.datetime.strptime(shadow_meta.get_item('EXIF:CreateDate'), '%Y:%m:%d %H:%M:%S')
#    si_utc_time= pytz.utc.localize(si_utc_time)
    if shadow_meta.get_item('XMP:BandName')=='Blue':
        x.append(si_location[0]);y.append(si_location[1])   ## To add information location only once
        R1.append(shadow_incident)
      
    elif shadow_meta.get_item('XMP:BandName')=='Green':
        R2.append(shadow_incident)

    elif shadow_meta.get_item('XMP:BandName')=='Red':
        R3.append(shadow_incident)
       
    elif shadow_meta.get_item('XMP:BandName')=='NIR':
        R4.append(shadow_incident)
        
    elif shadow_meta.get_item('XMP:BandName')=='Red edge':
        R5.append(shadow_incident)

exiftoolPath=os.path.normpath(os.environ.get('exiftoolpath'))
start_time= timeit.default_timer()
input_path=r'H:\Cotton2021\...\...'  #### Enter the complete file path here
fig, ax = plt.subplots(nrows=5, ncols=1, sharex='col')#,sharey=True)
fig.subplots_adjust(wspace=0.10, hspace=0.10)
   
Parallel(n_jobs=8, prefer= 'threads')(delayed(get_irrad_profile)(SI) for SI in glob.glob(input_path+'\\0*\*.tif')) 
 ## The *.tif reads all tiff files    
 ## 0*\\*.tif is helpful if you have saved the raw images in folders named 000, 001,002 so on...the traditional Micasense storage format
 ## If not just use input_path+'\*.tif' 
   

## Plots the irradiance profile for each band   
ax[0].plot(R1[15:-20], color= 'b',label='Blue')
ax[1].plot(R2[15:-20], color= 'g',label='Green')
ax[2].plot(R3[15:-20], color= 'r',label='Red')
ax[3].plot(R5[15:-20], color= 'm',label='Red edge')
ax[4].plot(R4[15:-20], color= 'black',label='NIR')

## Plots irradiance for one band at each location. Change the variable for 'c' parameter to plot different bands
# sc=plt.scatter(x[10:-5],y[10:-5],c=R1[10:-5])
# plt.colorbar(sc)
# plt.show()

stop_time=timeit.default_timer()
print("Computation time=", stop_time-start_time)
