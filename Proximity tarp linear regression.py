# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 14:33:18 2022

@author: Vaishali.Swaminathan
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels,os

sheetnames=['B','G','R', 'RE','NIR']
out_path=r'G:\My Drive\Intermediate\Ground\SampleUAV\09July2020\Tarp Images\\'


for sheetname in sheetnames:
    data= pd.read_excel(out_path+'Individual Tarp Refl.xlsx', sheet_name=sheetname)
    df=pd.DataFrame(data)
    img_list=[]
    for i in range (0, len(df), 3):
        block= df[i:i+3]
        X={}; Y={}
        for j in range(i+3):
            X[df['Tarp Color'].values[j]]=df['Image reflectance'].values[j]
            Y[df['Tarp Color'].values[j]]=df['Actual reflectance'].values[j]
        Band= int(df['Image Name'].values[i].split('_')[-1].split('.')[0])
        x=[]; y=[]
        ##Change this based on the calibration for each date 
        if Band ==1 or Band ==2 or Band ==3:
            x.append(X['BLACK']);x.append(X['GRAY']);y.append(Y['BLACK']);y.append(Y['GRAY'])
        elif Band ==5:
            x.append(X['BLACK']);x.append(X['GRAY']);x.append(X['WHITE']);y.append(Y['BLACK']);y.append(Y['GRAY']);y.append(Y['WHITE'])
        elif Band ==4:
            x.append(X['GRAY']);x.append(X['WHITE']);y.append(Y['GRAY']);y.append(Y['WHITE'])
            
        x=np.array(x); y=np.array(y)
        LR_model= LinearRegression().fit(x.reshape((-1, 1)),y)
        m= LR_model.coef_[0]
        b= LR_model.intercept_
        str_y= str(m)+'x'+str(b)
        row=[df['Image Name'].values[i], df['Tarp Number'].values[i],df['Irradiance Value'].values[i],m,b]
        img_list.append(row)
        
    df_out=pd.DataFrame(img_list, columns= ['Image Name', 'Tarp Number','Irradiance Value','LR_Slope', 'LR_Intercept'])
    output_file_name= out_path+'Individual Tarp Regression.xlsx'
    if not os.path.exists(output_file_name):
      df_out.to_excel(output_file_name, sheet_name= sheetname)
    
    else:
        with pd.ExcelWriter(output_file_name,engine="openpyxl", mode='a') as fn:
            df_out.to_excel(fn, sheet_name= sheetname)
            fn.save()