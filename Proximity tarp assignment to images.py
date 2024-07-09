# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:29:05 2023

@author: Vaishali.Swaminathan
"""
import pandas as pd
import numpy as np
import os

def closest_irrad(img, tarps):
    tarps = np.asarray(tarps)
    dist = (tarps - img)**2
    return np.argmin(dist)

sheetnames=['B','G','R', 'RE','NIR']
out_path=r'G:\My Drive\Intermediate\Ground\SampleUAV\09July2020\Tarp Images\\'
for sheetname in sheetnames:
    Tdf= pd.read_excel(out_path+'Tarps Metadata.xlsx', sheet_name=sheetname)
    Idf=pd.read_excel(out_path+'All image metadata.xlsx', sheet_name=sheetname)
    
    
    Tarps_irrad= Tdf['Irradiance Value'].astype(float)
    final_list=[]
    for i in range(len(Idf['Image Name'])):
        Img_irrad= Idf['Irradiance Value'][i].astype(float)
        tarp_loc=closest_irrad(Img_irrad, Tarps_irrad)
        j = tarp_loc
        
        row= [Idf['Image Name'][i],Idf['Irradiance Value'][i],Tdf['Image Name'][j],Tdf['Tarp Number'][j], Tdf['Irradiance Value'][j],Tdf['LR_Slope'][j],Tdf['LR_Intercept'][j]]
        final_list.append(row)
    
    
    df_out=pd.DataFrame(final_list, columns= ['Image Name', 'Image Irradiance Value','Tarp Name','Tarp Number','Tarp Irradiance Value','LR_Slope', 'LR_Intercept'])
    output_file_name= out_path+'Irradiance proximity calibration list.xlsx'
    if not os.path.exists(output_file_name):
      df_out.to_excel(output_file_name, sheet_name= sheetname)
    
    else:
        with pd.ExcelWriter(output_file_name,engine="openpyxl", mode='a') as fn:
            df_out.to_excel(fn, sheet_name= sheetname)
            fn.save()