# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 17:50:29 2022

@author: Vaishali.Swaminathan
"""
import glob, shutil, os, skimage,timeit, random , cv2
import numpy as np
import pandas as pd
import skimage.io
import micasense.metadata as metadata
import subprocess
from joblib import Parallel, delayed

exiftoolPath=os.path.normpath(os.environ.get('exiftoolpath'))
start_time= timeit.default_timer()
input_path= r'I:\Cotton2022\Auto Exposure\02June2022\75mAGL\DLS-Corrected_NoPanel\\'
out_path= r'I:\Cotton2022\Auto Exposure\02June2022\75mAGL\Tarp Images\\'
img_list=[[],[],[],[],[]]

# def copy_to_folder(Img):

for Img in glob.glob(input_path[0:-1]+'*.tif'):

    img_name= Img.split('\\')[-1]
    tarp_num= Img.split('\\')[-2]
    band_index= int(img_name.split('.')[0].split('_')[-1])-1
    meta = metadata.Metadata(Img, exiftoolPath=exiftoolPath)
    band=meta.get_item('XMP:BandName')
    exptime=meta.get_item('EXIF:ExposureTime')
    irrad= meta.get_item('XMP:Irradiance')
    gain=meta.get_item('EXIF:ISOSpeed')/100.0
    timestamp = meta.get_item('XMP:TimeStamp')
    lat= meta.get_item('EXIF:GPSLatitude')
    longi=meta.get_item('EXIF:GPSLongitude')
    
    ##uncomment for tarps
    # panelraw= skimage.io.imread(Img)
    # coord=np.zeros((3,2),np.int)
    
    # counter=0
    # def click_event(event, x, y, flags, params):
    #     global counter
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         coord[counter]=int(x),int(y)
    #         counter+=1
            
    # cv2.imshow('select center x,y', panelraw)
    # cv2.setMouseCallback('select center x,y', click_event)
    # cv2.waitKey(0)
    # cv2.destroyWindow('select center x,y')
    # x1=coord[0][0]; y1=coord[0][1]
    # x2=coord[1][0]; y2=coord[1][1]
    # x3=coord[2][0]; y3=coord[2][1]
    
    # z=2   #window for bounding box
    # ulx_b=x1-z ;uly_b=y1+z ;lrx_b=x1+z ; lry_b= y1-z #black panel
    # ulx_g=x2-z ;uly_g=y2+z ;lrx_g=x2+z ; lry_g= y2-z #gray panel
    # ulx_w=x3-z ;uly_w=y3+z ;lrx_w=x3+z ; lry_w= y3-z #white panel
    
    # panelRegion_b= panelraw[lry_b:uly_b, ulx_b:lrx_b]
    # panelRegion_g= panelraw[lry_g:uly_g, ulx_g:lrx_g]
    # panelRegion_w= panelraw[lry_w:uly_w, ulx_w:lrx_w]
    
    # cv2.rectangle(panelraw,(ulx_b,uly_b),(lrx_b,lry_b),(0,0,255),1)
    # cv2.rectangle(panelraw,(ulx_g,uly_g),(lrx_g,lry_g),(0,0,255),1)
    # cv2.rectangle(panelraw,(ulx_w,uly_w),(lrx_w,lry_w),(0,0,255),1)
    # cv2.imshow( 'Panel region in radiance image',panelraw)
    # cv2.waitKey(0)
    # cv2.destroyWindow('Panel region in radiance image')
    
    # meanRadiance_b = panelRegion_b.mean()
    # meanRadiance_g = panelRegion_g.mean()
    # meanRadiance_w = panelRegion_w.mean()
    
    # col= [img_name, tarp_num,irrad, 'BLACK','', meanRadiance_b]
    # img_list[band_index].append(col)
    # col= [img_name, tarp_num,irrad, 'GRAY','', meanRadiance_g]
    # img_list[band_index].append(col)
    # col= [img_name, tarp_num,irrad, 'WHITE','', meanRadiance_w]
    # img_list[band_index].append(col)
    
    ##### For regular images --non-tarp reference images
    row=[img_name, irrad, lat, longi,timestamp ]
    img_list[band_index].append(row)  

for ind in range(5): 
    # df= pd.DataFrame(img_list[ind], columns= [ 'Image Name', 'Tarp Number','Irradiance Value','Tarp Color','Actual reflectance', 'Image reflectance'])
    df= pd.DataFrame(img_list[ind], columns= [ 'Image Name','Irradiance Value','Latitude','Longitude', 'Timestamp'])
    output_file_name= out_path+'All image metadata.xlsx'
    if not os.path.exists(output_file_name):
      df.to_excel(output_file_name, sheet_name= str(ind+1))
        
    else:
        with pd.ExcelWriter(output_file_name,engine="openpyxl", mode='a') as fn:
            df.to_excel(fn, sheet_name= str(ind+1))
            fn.save()
    
   
# Parallel(n_jobs=8, prefer= 'threads')(delayed(copy_to_folder)(Img) for Img in glob.glob(input_path[0:-1]+'*\*.tif'))

# Step 2: Extract samples--- Run separately 

