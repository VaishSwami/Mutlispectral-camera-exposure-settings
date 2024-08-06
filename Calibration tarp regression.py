# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 18:53:59 2023

@author: Vaishali.Swaminathan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
import math
import statsmodels.api as sma

# Load the data from the Excel file
file_path=r".\Exposure Settings Data\Radiometric accuracy targets\Tarp Refl-Fixed vs Auto-16June2022.xlsx"
file_name = pd.ExcelFile(file_path)
sheets= file_name.sheet_names
fig, ax = plt.subplots(2,5, sharex=True, sharey=True)
ax = ax.flatten()
i=0
X= ['Fixed Exposure','Auto Exposure']
labels=['A', 'B','C', 'D', 'E', 'F', 'G','H', 'I', 'J']
for k in X:
    for sht in sheets:
        data=pd.read_excel(file_path, sheet_name=sht)
        # Extract the x and y values from the data
        ##Piecewise calibration 
        if sht =='Blue' or sht =='Green' or sht =='Red':
            y = data['ASD'][7:].values.reshape(-1, 1)   #16June=[7:]    17June=[0:8]
            x=data[k][7:].values.reshape(-1,1)
        elif sht =='Red Edge':
            y = data['ASD'][0:12].values.reshape(-1, 1)
            x=data[k][0:12].values.reshape(-1,1)
        elif sht=='NIR':
            y = data['ASD'][:13].values.reshape(-1, 1)   ##16June=[:13]    17June=[4:12]
            x=data[k][:13].values.reshape(-1,1)
            
        ##Full range calibration
        # y = data['ASD'].values.reshape(-1, 1)
        # x=data[k].values.reshape(-1,1)
        
        # Perform linear regression
        regressor_linear = LinearRegression()
        regressor_linear.fit(x, y)
        slope = regressor_linear.coef_[0][0]
        intercept = regressor_linear.intercept_[0]
        y0= slope*0+intercept
        y1= slope*1+intercept
        if intercept<0:
            sign=''
        else:
            sign='+'
        y_pred_linear = regressor_linear.predict(x)
        r2_linear = r2_score(y, y_pred_linear)
        rmse_linear = np.sqrt(mean_squared_error(y, y_pred_linear))
        mape_linear = np.mean(100*np.abs(y - y_pred_linear)/y)
        
        corr_coeff_linear = np.corrcoef(y_pred_linear.reshape(-1), y.reshape(-1))[0, 1]
        
        x2  = sma.add_constant(x)
        reg_lin=sma.OLS(y, x2)
        reg_lin2=reg_lin.fit()
        p_values = reg_lin2.summary2().tables[1]['P>|t|']
        if p_values['x1']<0.001:
            p_val='**'
        elif p_values['x1']<0.05:
            p_val='*'
        else:
            p_val=''

        # Print the results
        print("Linear Regression: R\xb2 = {:.2f}, RMSE = {:.2f},MAPE = {:.2f}, Correlation Coefficient = {:.2f}".format(r2_linear, rmse_linear,mape_linear, corr_coeff_linear))
        leg ="y={:.2f}x{}{:.2f}\nR\xb2 = {}{}\nMAPE = {:.2f}".format(slope,sign, intercept,str(r2_linear)[:4],p_val,mape_linear)
        leg ="y={:.2f}x{}{:.2f}\nR\xb2 = {}{}\nMAPE = {:.2f}".format(slope,sign, intercept,str(r2_linear)[:4],p_val,mape_linear)
        ax[i].scatter(y_pred_linear, y, color='black', s=7.5)
        # ax[i].plot([0,1],[y0,y1], linestyle='dashed', color='black', label=leg)
        ax[i].plot([0,1],[0,1], linestyle='dashed', color='crimson', label=leg)
        # ax[i].legend(loc='upper right', fontsize=7)
        ax[i].text(0.5,0.01,leg,  fontsize=14) #,fontweight='bold'
        ax[i].text(0.02,0.95, labels[i], fontsize=14, fontweight='bold')
        ax[i].set_aspect('equal', adjustable = 'box')
        if i < 5:
            ax[i].set_title(sht, fontsize=16, fontweight='bold')
        i+=1
        if (i+1)%5==0:
            ax[i].yaxis.set_label_position('right')
            ax[i].set_ylabel(k,fontsize=16, fontweight='bold',rotation = 270, labelpad=15)
            
# Plot the results
# plt.scatter(x, y, color='blue', label='Data')
# plt.plot(x, y_pred_linear, color='red', label='Linear Regression')
# plt.plot(x, y_pred_quadratic, color='green', label='Quadratic Regression')
# plt.legend()
# plt.title('Regression Analysis')
fig.subplots_adjust(wspace=0.05, hspace=-0.3)
fig.supxlabel('Image estimated reflectance',x=0.51,y=0.135,fontsize=17,fontweight='bold')
fig.supylabel('ASD measured reflectance',x=0.095, fontsize=17,fontweight='bold')
# ax[0,1].yaxis.set_label_position('right')
# ax[0,0].set_ylabel('Fixed Exposure')
# ax[1,0].set_ylabel('Auto Exposure')
# ax[0,0].legend(loc='upper left')

# plt.show()
