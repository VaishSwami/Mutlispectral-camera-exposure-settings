# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 14:00:59 2023

@author: Vaishali.Swaminathan
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sheets=['B','G','R','RE','NIR']
band_dict= {'B':'Blue', 'G':'Green', 'R': 'Red', 'RE': 'Red Edge', 'NIR': 'NIR'}
fig, ax = plt.subplots(nrows=5, ncols=1, figsize=(5,5), sharex='col',sharey=True)
fig.subplots_adjust(wspace=0.10, hspace=0.1)

##for 1x gain
f1_l=[0.24,0.18,0.31,0.42,0.42]
f1_u=[0.42,0.31,0.76,0.99,0.76]
o1_l=[0.24,0.18,0.31,0.42,0.42]
o1_u=[0.59,0.42,0.99,0.99,0.76]

#for 2x gain
f1_l=[0.09,0.09,0.18,0.13,0.17]
f1_u=[0.18,0.13,0.31,0.42,0.42]
o1_l=[0.09,0.09,0.18,0.13,0.17]
o1_u=[0.248,0.18,0.42,0.42,0.42]

for sht,i in zip(sheets,[0,1,2,3,4]):
    df= pd.read_excel(r'.\Exposure Settings Data\Cross-calibration dataset\TarpRefl.xlsx', sheet_name=sht).dropna(subset=['Black tarp reflectance'])
    # x_1x= df.query('Gain==1')['Exposure Time']*1000
    # b_1x= df.query('Gain==1')['Black tarp reflectance']
    # g_1x= df.query('Gain==1')['Gray tarp reflectance']
    # w_1x= df.query('Gain==1')['White tarp reflectance']
    # b_ASD= df.query('Gain==1')['Black ASD']
    # g_ASD= df.query('Gain==1')['Gray ASD']
    # w_ASD= df.query('Gain==1')['White ASD']
    
    # # ax[i,0].scatter(x_1x, b_1x, marker='o', c='black', label= 'Black reflectance')
    # # ax[i,0].scatter(x_1x, g_1x, marker='o', c='gray', label= 'Gray reflectance')
    # # ax[i,0].scatter(x_1x, w_1x, marker='o', c='silver', label= 'White reflectance')
    # # ax[i,0].plot(x_1x, b_ASD,  c='black', label= 'Black ASD')
    # # ax[i,0].plot(x_1x, g_ASD,  c='gray', label= 'Gray ASD')
    # # ax[i,0].plot(x_1x, w_ASD,  c='silver', label= 'White ASD')
    # # ax[i,0].set_ylim(0,1.0)
    # # start, end = ax[i,0].get_xlim()
    # # ax[i,0].xaxis.set_ticks(np.arange(0, end, 0.25))
    # # ax[i,0].set_ylabel(band_dict[sht])
    # # ax[i,0].set_xlim(start,2.01)
    # # ax[i,0].set_box_aspect(0.20)
    
    # ax[i].scatter(x_1x, b_1x, marker='o', c='black', label= 'Black reflectance')
    # ax[i].scatter(x_1x, g_1x, marker='o', c='gray', label= 'Gray reflectance')
    # ax[i].scatter(x_1x, w_1x, marker='o', c='silver', label= 'White reflectance')
    # ax[i].plot(x_1x, b_ASD,  c='black', label= 'Black ASD')
    # ax[i].plot(x_1x, g_ASD,  c='gray', label= 'Gray ASD')
    # ax[i].plot(x_1x, w_ASD,  c='silver', label= 'White ASD')
    # ax[i].plot([f1_u[i],f1_u[i]], [0.02,0.95], linestyle='dashed', c='red', label='FS upper limit')
    # ax[i].plot([o1_u[i],o1_u[i]], [0.02,0.95], linestyle='dotted', c='blue', label='OB upper limit')
    # ax[i].set_ylim(0,1.0)
    # start, end = ax[i].get_xlim()
    # ax[i].xaxis.set_ticks(np.arange(0, end, 0.25))
    # ax[i].set_ylabel(band_dict[sht])
    # ax[i].set_xlim(start,4.01)
    # ax[i].set_box_aspect(0.20)
    
    
    x_2x= df.query('Gain==2')['Exposure Time']*1000
    b_2x= df.query('Gain==2')['Black tarp reflectance']
    g_2x= df.query('Gain==2')['Gray tarp reflectance']
    w_2x= df.query('Gain==2')['White tarp reflectance']
    b_ASD= df.query('Gain==2')['Black ASD']
    g_ASD= df.query('Gain==2')['Gray ASD']
    w_ASD= df.query('Gain==2')['White ASD']
    
    # ax[i,1].scatter(x_2x, b_2x, marker='o', c='black')
    # ax[i,1].scatter(x_2x, g_2x, marker='o', c='gray')
    # ax[i,1].scatter(x_2x, w_2x, marker='o', c='silver')
    # ax[i,1].plot(x_2x, b_ASD,  c='black')
    # ax[i,1].plot(x_2x, g_ASD,  c='gray')
    # ax[i,1].plot(x_2x, w_ASD,  c='silver')
    # ax[i,1].set_ylim(0,1.0)  
    # start, end = ax[i,1].get_xlim()
    # ax[i,1].xaxis.set_ticks(np.arange(0, end+0.25, 0.25))
    # ax[i,1].set_xlim(0,1.01)
    # ax[i,1].set_box_aspect(0.20)
    
    ax[i].scatter(x_2x, b_2x, marker='o', c='black', label= 'Black reflectance')
    ax[i].scatter(x_2x, g_2x, marker='o', c='gray', label= 'Gray reflectance')
    ax[i].scatter(x_2x, w_2x, marker='o', c='silver',label= 'White reflectance')
    ax[i].plot(x_2x, b_ASD,  c='black', label= 'Black ASD')
    ax[i].plot(x_2x, g_ASD,  c='gray', label= 'Gray ASD')
    ax[i].plot(x_2x, w_ASD,  c='silver', label= 'White ASD')
    ax[i].plot([f1_u[i],f1_u[i]], [0.02,0.95], linestyle='dashed', c='red', label='FS upper limit')
    ax[i].plot([o1_u[i],o1_u[i]], [0.02,0.95], linestyle='dotted', c='blue', label='OB upper limit')
    ax[i].set_ylim(0,1.0)  
    start, end = ax[i].get_xlim()
    ax[i].xaxis.set_ticks(np.arange(0, end+0.25, 0.25))
    ax[i].set_ylabel(band_dict[sht])
    ax[i].set_xlim(0,2.01)
    ax[i].set_box_aspect(0.20)
    
# ax[0,0].set_title('1x Gain')
# # ax[0,1].set_title('2x Gain')
# ax[4,0].set_xlabel('Exposure time (ms)')
# # ax[4,1].set_xlabel('Exposure time (ms)')
# ax[0,0].legend(loc='upper right',prop={'size': 6})
# fig.ylabel('Reflectnce')
# plt.show()

# ax[0].set_title('1x Gain')
ax[0].set_title('2x Gain')
ax[4].set_xlabel('Exposure time (ms)')
# ax[4].set_xlabel('Exposure time (ms)')
ax[0].legend(loc='upper right',prop={'size': 6})
fig.supylabel('Reflectance')
plt.show()




