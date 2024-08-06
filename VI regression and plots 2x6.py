# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:53:32 2023

@author: Vaishali.Swaminathan
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats
import statsmodels.api as sma
# from sklearn.metrics import mean_absolute_percentage_error as mape

# Define function for linear regression
def perform_linear_regression(x, y):
    x = np.array(x).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    return model

# Define function for quadratic regression
def perform_quadratic_regression(x, y):
    x = np.array(x).reshape(-1, 1)
    poly = PolynomialFeatures(degree=2)
    x_poly = poly.fit_transform(x)
    model = LinearRegression()
    model.fit(x_poly, y)
    return model, poly

# Compute MAPE
# def compute_mape(y_true, y_pred):
#     return mape(y_true, y_pred)
# Load the data from the Excel file
file_path=r"G:\My Drive\Prelims and Dissertation\Papers\Autoexposure\Additional Analysis\VI\Vegetation Index-Fixed vs Auto-N plots gm2.xlsx"
file_name = pd.ExcelFile(file_path)
sheets= file_name.sheet_names
fig, ax = plt.subplots(6, 2, sharex=True, sharey=True)
ax = ax.flatten()
i=0
labels=['A', 'G','B','H','C','I', 'D','J', 'E','K', 'F', 'L' ]
for sht in sheets:
    print(sht)
    data=pd.read_excel(file_path, sheet_name=sht)
    # Extract the x and y values from the data
    X= ['Fixed-exposure Calibrated','Auto-exposure Calibrated']
    y = data['Total N (g/plant)'].values.reshape(-1, 1)
    for k in X:
        x=data[k].values.reshape(-1,1)
        # Perform linear regression
        if sht in ['NDRE', 'NDVI','GNDVI','RDVI', 'CIRE','TGI','CIG']:
            regressor_linear = LinearRegression()
            regressor_linear.fit(x, y)
            slope = regressor_linear.coef_[0][0]
            intercept = regressor_linear.intercept_[0]
            y_pred_linear = regressor_linear.predict(x)
            r2_linear = r2_score(y, y_pred_linear)
            rmse_linear = np.sqrt(mean_squared_error(y, y_pred_linear))
            mse_linear = mean_squared_error(y, y_pred_linear)
            nrmse_linear = np.sqrt(mean_squared_error(y, y_pred_linear))/(np.max(y)-np.min(y))
            mape_linear = np.mean(100*np.abs(y - y_pred_linear)/y)
            smape_linear =100* np.mean(2*np.abs(y - y_pred_linear)/(y+y_pred_linear))
            mae_linear= np.mean(np.abs(y - y_pred_linear))
            
            x2  = sma.add_constant(x)
            reg_lin=sma.OLS(y, x2)
            reg_lin2=reg_lin.fit()
            p_values = reg_lin2.summary2().tables[1]['P>|t|']
            if p_values['x1']<0.05:
                p_val='*'
            else:
                p_val=''
            leg ="R\xb2 = {:.2f}{}\nMAPE = {:.2f}".format(r2_linear,p_val,mape_linear)
            ax[i].scatter(y_pred_linear, y, color='black', s=4.5)
            ax[i].plot([-0.1,3],[-0.1,3], linestyle='dashed', color='crimson', label=leg)
            ax[i].text(1.6,0,leg)
            ax[i].text(0.0,2.5, labels[i], fontsize=12, fontweight='bold')
        
        # x2  = sma.add_constant(x)
        # reg_lin=sma.OLS(y, x2)
        # reg_lin2=reg_lin.fit()
        # p_values = reg_lin2.summary2().tables[1]['P>|t|']
        # if p_values['x1']<0.05:
        #     p_val='<0.05'
        # else:
        #     p_val='>=0.05'
        # if sht in ['']:
        #     # if sht=='CIre':
        #         # column=column.replace('CIre','CIrededge')
        #     # Quadratic Regression
        #     quadratic_model, poly = perform_quadratic_regression(x, y)
        #     x_poly = poly.transform(x)
        #     quadratic_predictions = quadratic_model.predict(x_poly)
        #     quadratic_r_squared = r2_score(y, quadratic_predictions)
        #     # quadratic_mape = compute_mape(y, quadratic_predictions)
        #     quadratic_smape =100* np.mean(2*np.abs(y - quadratic_predictions)/(y+quadratic_predictions))
        #     m2= round(quadratic_model.coef_[0][2],2)
        #     m1= round(quadratic_model.coef_[0][1],2)
        #     c_= round(quadratic_model.intercept_[0],2)
        #     leg ="R\xb2 = {:.2f}, p {}\nsMAPE = {:.2f}".format(quadratic_r_squared,p_val,quadratic_smape)
        #     ax[i].scatter(quadratic_predictions, y, color='black', s=4.5)
        #     ax[i].plot([0,3],[0,3], linestyle='dashed', color='crimson', label=leg)
        
        # corr_coeff_linear = np.corrcoef(y_pred_linear.reshape(-1), y.reshape(-1))[0, 1]
        # corr_coeff_quadratic = np.corrcoef(y_pred_quadratic.reshape(-1), y.reshape(-1))[0, 1]

        # Print the results
        # print("Linear Regression: R2 = {:.2f}, RMSE = {:.2f},MAPE = {:.2f}, Correlation Coefficient = {:.2f}".format(r2_linear, rmse_linear,mape_linear, corr_coeff_linear))
        # print("Quadratic Regression: R2 = {:.2f}, RMSE = {:.2f}, Correlation Coefficient = {:.2f}".format(r2_quadratic, rmse_quadratic, corr_coeff_quadratic))
        # print("Correlation Coefficient (x, y) = {:.2f}".format(corr_coeff))
        
        # ax[i].legend(loc='upper right', fontsize=7)
        
        if sht=='CIG':
            sht='CIgreen'
        if sht=='CIRE':
            sht='CIrededge'
        if i < 2:
            ax[i].set_title(k.replace('Calibrated',''), fontsize=13,fontweight='bold')
        i+=1
        if (i+1)%2==0:
            ax[i].yaxis.set_label_position('right')
            ax[i].set_ylabel(sht,fontsize=11,fontweight='bold', rotation = 270, labelpad=10)
        if sht=='CIgreen':
            sht='CIG'
        if sht=='CIrededge':
            sht='CIRE'   
# Plot the results
# plt.scatter(x, y, color='blue', label='Data')
# plt.plot(x, y_pred_linear, color='red', label='Linear Regression')
# plt.plot(x, y_pred_quadratic, color='green', label='Quadratic Regression')
# plt.legend()
# plt.title('Regression Analysis')
fig.supxlabel('Actual PNU (g/m\xb2)',x=0.51,y=0.05,fontsize=13,fontweight='bold')
fig.supylabel('Predicted PNU (g/m\xb2)',x=0.05, fontsize=13,fontweight='bold')
# ax[0,1].yaxis.set_label_position('right')
# ax[0,0].set_ylabel('Fixed Exposure')
# ax[1,0].set_ylabel('Auto Exposure')
# ax[0,0].legend(loc='upper left')

# plt.show()