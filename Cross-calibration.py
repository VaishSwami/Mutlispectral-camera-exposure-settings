# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 02:16:06 2024

@author: swami
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels,os, seaborn



sheetnames=['B','G', 'R', 'RE', 'NIR']
out_path=r'.\Exposure Settings Data\Cross-calibration dataset\\'


#Part1
for sheetname in sheetnames:
    img_list=[]
    data1= pd.read_excel(out_path+'TarpRefl-Batch1.xlsx', sheet_name=sheetname)
    data2= pd.read_excel(out_path+'TarpRefl-Batch2.xlsx', sheet_name=sheetname)
    data3= pd.read_excel(out_path+'TarpRefl-Batch3.xlsx', sheet_name=sheetname)
    data4= pd.read_excel(out_path+'TarpRefl-Batch4.xlsx', sheet_name=sheetname)
    data5= pd.read_excel(out_path+'TarpRefl-Batch5.xlsx', sheet_name=sheetname)
    df1=pd.DataFrame(data1);df2=pd.DataFrame(data2);df3=pd.DataFrame(data3);df4=pd.DataFrame(data4);df5=pd.DataFrame(data5)
    df1=df1.fillna(0);df2=df2.fillna(0);df3=df3.fillna(0);df4=df4.fillna(0);df5=df5.fillna(0)
    for i in range (0, len(df1)):
        block= df1[i:i+1];block2= df2[i:i+1];block3= df3[i:i+1];block4= df4[i:i+1];block5= df5[i:i+1]
        X=block;X2=block2;X3=block3;X4=block4;X5=block5
        Band=sheetname
        x=[]; y=[]
        #Change this 
        # x.append(X['Black tarp reflectance UNC'].values[0]);x.append(X['Gray tarp reflectance UNC'].values[0]);x.append(X['White tarp reflectance UNC'].values[0]);y.append(X['Black ASD'].values[0]);y.append(X['Gray ASD'].values[0]);y.append(X['White ASD'].values[0])
        # x.append(X2['Black tarp reflectance UNC'].values[0]);x.append(X2['Gray tarp reflectance UNC'].values[0]);x.append(X2['White tarp reflectance UNC'].values[0]);y.append(X['Black ASD'].values[0]);y.append(X['Gray ASD'].values[0]);y.append(X['White ASD'].values[0])
        # x.append(X3['Black tarp reflectance UNC'].values[0]);x.append(X3['Gray tarp reflectance UNC'].values[0]);x.append(X3['White tarp reflectance UNC'].values[0]);y.append(X['Black ASD'].values[0]);y.append(X['Gray ASD'].values[0]);y.append(X['White ASD'].values[0])
        if Band =='B' or Band =='G' or Band =='R':
            x.append(X['Black tarp reflectance']);x.append(X['Gray tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD'])
            x.append(X2['Black tarp reflectance']);x.append(X2['Gray tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD'])
            x.append(X3['Black tarp reflectance']);x.append(X3['Gray tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD'])
            x.append(X4['Black tarp reflectance']);x.append(X4['Gray tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD'])
            x.append(X5['Black tarp reflectance']);x.append(X5['Gray tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD'])
        elif Band =='RE':
            x.append(X['Black tarp reflectance']);x.append(X['Gray tarp reflectance']);x.append(X['White tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD']);y.append(X['White ASD'])
            x.append(X2['Black tarp reflectance']);x.append(X2['Gray tarp reflectance']);x.append(X2['White tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD']);y.append(X['White ASD'])
            x.append(X3['Black tarp reflectance']);x.append(X3['Gray tarp reflectance']);x.append(X3['White tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD']);y.append(X['White ASD'])
            x.append(X4['Black tarp reflectance']);x.append(X4['Gray tarp reflectance']);x.append(X4['White tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD']);y.append(X['White ASD'])
            x.append(X5['Black tarp reflectance']);x.append(X5['Gray tarp reflectance']);x.append(X5['White tarp reflectance']);y.append(X['Black ASD']);y.append(X['Gray ASD']);y.append(X['White ASD'])
        elif Band =='NIR':
            x.append(X['Gray tarp reflectance']);x.append(X['White tarp reflectance']);y.append(X['Gray ASD']);y.append(X['White ASD'])
            x.append(X2['Gray tarp reflectance']);x.append(X2['White tarp reflectance']);y.append(X2['Gray ASD']);y.append(X['White ASD'])
            x.append(X3['Gray tarp reflectance']);x.append(X3['White tarp reflectance']);y.append(X3['Gray ASD']);y.append(X['White ASD'])
            x.append(X4['Gray tarp reflectance']);x.append(X4['White tarp reflectance']);y.append(X4['Gray ASD']);y.append(X['White ASD'])
            x.append(X5['Gray tarp reflectance']);x.append(X5['White tarp reflectance']);y.append(X5['Gray ASD']);y.append(X['White ASD'])
        x=np.array(x); y=np.array(y)
        LR_model= LinearRegression().fit(x.reshape((-1, 1)),y)
        m= float(LR_model.coef_[0])
        b= float(LR_model.intercept_)
        str_y= str(m)+'x'+str(b)
        row=[df1['Gain'].values[i],df1['Exposure Time'].values[i],df1['Image Name'].values[i], df1['Black tarp reflectance'].values[i],df1['Gray tarp reflectance'].values[i],df1['White tarp reflectance'].values[i],df1['Black ASD'].values[i],df1['Gray ASD'].values[i],df1['White ASD'].values[i],m,b]
        row2=[df2['Gain'].values[i],df2['Exposure Time'].values[i],df2['Image Name'].values[i], df2['Black tarp reflectance'].values[i],df2['Gray tarp reflectance'].values[i],df2['White tarp reflectance'].values[i],df1['Black ASD'].values[i],df1['Gray ASD'].values[i],df1['White ASD'].values[i],m,b]
        row3=[df3['Gain'].values[i],df3['Exposure Time'].values[i],df3['Image Name'].values[i], df3['Black tarp reflectance'].values[i],df3['Gray tarp reflectance'].values[i],df3['White tarp reflectance'].values[i],df1['Black ASD'].values[i],df1['Gray ASD'].values[i],df1['White ASD'].values[i],m,b]
        row4=[df4['Gain'].values[i],df4['Exposure Time'].values[i],df4['Image Name'].values[i], df4['Black tarp reflectance'].values[i],df4['Gray tarp reflectance'].values[i],df4['White tarp reflectance'].values[i],df1['Black ASD'].values[i],df1['Gray ASD'].values[i],df1['White ASD'].values[i],m,b]
        row5=[df5['Gain'].values[i],df5['Exposure Time'].values[i],df5['Image Name'].values[i], df5['Black tarp reflectance'].values[i],df5['Gray tarp reflectance'].values[i],df5['White tarp reflectance'].values[i],df1['Black ASD'].values[i],df1['Gray ASD'].values[i],df1['White ASD'].values[i],m,b]
        img_list.append(row);img_list.append(row2);img_list.append(row3);img_list.append(row4);img_list.append(row5)
        
    df_out=pd.DataFrame(img_list, columns= ['Gain', 'Exposure Time','Image Name', 'Black tarp reflectance','Gray tarp reflectance','White tarp reflectance','Black ASD','Gray ASD','White ASD','LR_Slope', 'LR_Intercept'])
    output_file_name= out_path+'TarpRefl Regression piecewise-5Batches.xlsx'
    if not os.path.exists(output_file_name):
      df_out.to_excel(output_file_name, sheet_name= sheetname)
    
    else:
        with pd.ExcelWriter(output_file_name,engine="openpyxl", mode='a') as fn:
            df_out.to_excel(fn, sheet_name= sheetname)
            fn.save()
            
#Part 2

for sheetname in sheetnames:
    data= pd.read_excel(out_path+'TarpRefl Regression piecewise-5Batches.xlsx', sheet_name=sheetname)
    df=pd.DataFrame(data)
    df=df.fillna(0)
    df_dupe=df.drop_duplicates(subset=['Gain','Exposure Time'],keep='first')
    indexes= df_dupe['Gain'].astype(str)+'X'+(1000*df_dupe['Exposure Time']).round(5).astype(str)
    img_list=[]
    MAPE_mat= np.zeros(shape=(len(df_dupe), len(df_dupe)))
   
    ##OELM 
    for i in range (0,len(df),5):
        
        X=df[i:i+1]
        m = X['LR_Slope'].values[0]; c= X['LR_Intercept'].values[0]
        for j in range(0,len(df),5):
            X1= df[j:j+1];X2= df[j+1:j+2];X3= df[j+2:j+3];X4= df[j+3:j+4];X5= df[j+4:j+5]
            x=[]; y=[]
            Band=sheetname
         
            if Band =='B' or Band =='G' or Band =='R':
                x.append(X1['Black tarp reflectance'].values[0]);x.append(X1['Gray tarp reflectance'].values[0])
                x.append(X2['Black tarp reflectance'].values[0]);x.append(X2['Gray tarp reflectance'].values[0])
                x.append(X3['Black tarp reflectance'].values[0]);x.append(X3['Gray tarp reflectance'].values[0])
                x.append(X4['Black tarp reflectance'].values[0]);x.append(X4['Gray tarp reflectance'].values[0])
                x.append(X5['Black tarp reflectance'].values[0]);x.append(X5['Gray tarp reflectance'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0])
            elif Band =='RE':
                x.append(X1['Black tarp reflectance'].values[0]);x.append(X1['Gray tarp reflectance'].values[0]);x.append(X1['White tarp reflectance'].values[0])
                x.append(X2['Black tarp reflectance'].values[0]);x.append(X2['Gray tarp reflectance'].values[0]);x.append(X2['White tarp reflectance'].values[0])
                x.append(X3['Black tarp reflectance'].values[0]);x.append(X3['Gray tarp reflectance'].values[0]);x.append(X3['White tarp reflectance'].values[0])
                x.append(X4['Black tarp reflectance'].values[0]);x.append(X4['Gray tarp reflectance'].values[0]);x.append(X4['White tarp reflectance'].values[0])
                x.append(X5['Black tarp reflectance'].values[0]);x.append(X5['Gray tarp reflectance'].values[0]);x.append(X5['White tarp reflectance'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0]);y.append(X1['White ASD'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0]);y.append(X1['White ASD'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0]);y.append(X1['White ASD'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0]);y.append(X1['White ASD'].values[0])
                y.append(X1['Black ASD'].values[0]);y.append(X1['Gray ASD'].values[0]);y.append(X1['White ASD'].values[0])
            elif Band =='NIR':
                x.append(X1['Gray tarp reflectance'].values[0]);x.append(X1['White tarp reflectance'].values[0])
                x.append(X2['Gray tarp reflectance'].values[0]);x.append(X2['White tarp reflectance'].values[0])
                x.append(X3['Gray tarp reflectance'].values[0]);x.append(X3['White tarp reflectance'].values[0])
                x.append(X4['Gray tarp reflectance'].values[0]);x.append(X4['White tarp reflectance'].values[0])
                x.append(X5['Gray tarp reflectance'].values[0]);x.append(X5['White tarp reflectance'].values[0])
                y.append(X1['Gray ASD'].values[0]);y.append(X1['White ASD'].values[0])
                y.append(X2['Gray ASD'].values[0]);y.append(X2['White ASD'].values[0])
                y.append(X3['Gray ASD'].values[0]);y.append(X3['White ASD'].values[0])
                y.append(X3['Gray ASD'].values[0]);y.append(X3['White ASD'].values[0])
                y.append(X3['Gray ASD'].values[0]);y.append(X3['White ASD'].values[0])
            x=np.array(x); y=np.array(y)
            x_cor = m*x+c
            APE=  100.0* abs(x_cor-y)/y
            MAPE= APE.mean()
            i_m=int(i/5);j_m=int(j/5)
            MAPE_mat[i_m,j_m]=MAPE
    df_out=pd.DataFrame(MAPE_mat, index= indexes, columns= indexes)
    output_file_name= out_path+'TarpRefl Cross Calibration MAPE-OELM 5Batches.xlsx'
    if not os.path.exists(output_file_name):
      df_out.to_excel(output_file_name, sheet_name= sheetname)
    
    else:
        with pd.ExcelWriter(output_file_name,engine="openpyxl", mode='a') as fn:
            df_out.to_excel(fn, sheet_name= sheetname)
            fn.save()