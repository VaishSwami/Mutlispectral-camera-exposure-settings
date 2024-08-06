# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 13:41:45 2023

@author: Vaishali.Swaminathan
"""
import os, glob
import shutil
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
input_path=r'Exposure Settings Data\Object based exposure\16June2022'
output_path= input_path+'\\Targets\\'
# lst=[334,335,383,384,387,436]
# # for pth in glob.glob(input_path+'\\0*\\'):
# #     for img in lst:
# #         for imgpath in glob.glob(pth+str(img)+'*.tif'):
# #             img_name=imgpath.split('\\')[-1]
# #             shutil.copy(imgpath,output_path+img_name)
# for img in lst:
#     for pth in glob.glob(input_path+'\\*\\*'+str(img)+'*.tif'):
#         img_name=pth.split('\\')[-1]
#         shutil.copy(pth, output_path+img_name)
        
        
        
## Merge all files 

file_name = pd.ExcelFile(input_path+'\\Exposure variations AE- Targets.xlsx')
sheets= file_name.sheet_names
out_path= input_path+'\\Exposure variations- comprehensive4.xlsx'
new_df= pd.DataFrame()
for sht in sheets:
    for fl in glob.glob(input_path+'\\Exposure variations AE-*.xlsx'):
        obj= fl.split('\\')[-1].split('.')[0].split('-')[-1]
        df= pd.read_excel(fl, sheet_name=sht)
        df['Exposure time']=df['Exposure time']*1000
        rows=df.loc[df['Gain'] > 0]     
        rows['Object']=obj
        rows['Band']=sht
        new_df=new_df.append(rows)
        
        # new_df = pd.DataFrame(columns=df.columns)
    
if not os.path.exists(out_path):
    new_df.to_excel(out_path, index= False)
else:
    with pd.ExcelWriter(out_path,engine="openpyxl", mode='a') as zfn:
        new_df.to_excel(zfn)
        zfn.save()
       
##Box plot 
df= pd.read_excel(out_path)
sns.set(font_scale=1.5)
sns.catplot(data= df, x='Object', y='Exposure time (ms)', hue= 'Gain', col='Band', order=['Targets','Canopy','Soil'],kind='box', legend=True)
# sns.show()
# sea = sns.FacetGrid(df, col = "Band", hue='Gain')
# sea.map(sns.boxplot, data=df, x="Object",y= "Exposure time")
# sea.add_legend()
