# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 16:22:59 2021

@author: vaishaliswaminathan
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May  3 16:36:42 2021

@author: vaishaliswaminathan
"""

import numpy as np
import skimage.color
import skimage.io
import skimage.viewer
#from matplotlib import pyplot as plt
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

exiftoolPath=os.path.normpath(os.environ.get('exiftoolpath'))
start_time= timeit.default_timer()
# rootpath=r'I:\Cotton2022\30mAGL\02June2022\30mAGL\\'
# input_path=r'I:\Cotton2022\30mAGL\02June2022\30mAGL\001\\'
input_path=r'I:\Cotton2022\UAV Shadows\UAV Tarps\23June2022\Tarps\Sorted Samples-Batch5\\'
# output_path=rootpath[0:-1]+'SampleDLSCorr2\\'
op_path= r'I:\Cotton2022\UAV Shadows\UAV Tarps\23June2022\Tarps\Sorted DLS Reflectance-Batch5\\'

# if not os.path.exists(output_path):
#     os.makedirs(output_path)
if not os.path.exists(op_path):
    os.makedirs(op_path)
# useDLS=0
#panelimg=glob.glob(input_path[0:-1]+'000\IMG_0009_*.tif')
#panelCap = capture.Capture.from_filelist(panelimg)
#
#if panelCap is not None:
#     #RedEdge band_index order
##    panel_radiance = np.array(panelCap.panel_radiance())
#    panel_reflect = np.array(panelCap.panel_reflectance())
#    img_type = "reflectance"
#panel_reflectance_by_band = [0.5344, 0.5346, 0.5331, 0.5293, 0.5319]
##panel_corr= panel_reflectance_by_band/panel_radiance
#panel_corr= panel_reflectance_by_band/panel_reflect


panel_corr= [1.0,1.0,1.0,1.0,1.0]

def img_refl(SI):

    shadow_image = skimage.io.imread(SI, as_gray=True)    #variable name for shadow dataset
    shadow_meta = metadata.Metadata(SI, exiftoolPath=exiftoolPath)
    shadow_incident= shadow_meta.get_item('XMP:Irradiance')
    band=shadow_meta.get_item('XMP:BandName')
#    si_location=(shadow_meta.get_item('Composite:GPSLongitude'),shadow_meta.get_item('Composite:GPSLatitude'))
#    si_dls_pose=(float(shadow_meta.get_item('XMP:Yaw')),float(shadow_meta.get_item('XMP:Pitch')),float(shadow_meta.get_item('XMP:Roll')))
#    si_utc_time= datetime.datetime.strptime(shadow_meta.get_item('EXIF:CreateDate'), '%Y:%m:%d %H:%M:%S')
#    si_utc_time= pytz.utc.localize(si_utc_time)
    
#    dls_orientation_vector = np.array([0,0,-1])
#    (sun_vector_ned,    # Solar vector in North-East-Down coordinates
#    sensor_vector_ned, # DLS vector in North-East-Down coordinates
#    sun_sensor_angle,  # Angle between DLS vector and sun vector
#    solar_elevation,   # Elevation of the sun above the horizon
#    solar_azimuth,     # Azimuth (heading) of the sun
#    )= dls.compute_sun_angle(si_location,si_dls_pose,si_utc_time,dls_orientation_vector)
#    fresnel_coeff= dls.fresnel(sun_sensor_angle)
#    percent_dif=1/6.0
#    shadow_incident_cor= (shadow_incident*(percent_dif+np.sin(solar_elevation)))/(fresnel_coeff*(percent_dif+np.cos(sun_sensor_angle)))


#only for calibration panel (Amrit's), move it outside for loop for regular applications
    output_path=op_path +band+'\\'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    
    shadow_radianceImage= msutils.raw_image_to_radiance(shadow_meta, shadow_image)[0]
    shadow_refl=100*pi*shadow_radianceImage*panel_corr[int(SI[-5])-1]/shadow_incident
    

    output_name= SI.split("\\")[-1]
    im = Image.fromarray(shadow_refl.astype(np.float32))     ###Change this to reflectance                    
    im.save(output_path+output_name)
    cmd= '{} -TagsFromFile "{}" -XMP "{}"'.format(exiftoolPath,SI, output_path+output_name)
    subprocess.call(cmd)
    cmd= '{} -TagsFromFile "{}" -Composite "{}"'.format(exiftoolPath,SI, output_path+output_name)
    subprocess.call(cmd)


Parallel(n_jobs=8, prefer= 'threads')(delayed(img_refl)(SI) for SI in glob.glob(input_path[0:-1]+'*\*.tif'))
# for or_files in glob.glob(output_path+'*_original'):
for or_files in glob.glob(op_path+'*\*_original'):   ##only for calibration panel (Amrit's)
    os.remove(or_files)     
        
stop_time=timeit.default_timer()
print("Computation time=", stop_time-start_time)