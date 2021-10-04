# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 19:07:34 2021

@author: Ghozy El Fatih
For academic and non-profit purposes only
Any question, suggestion, or anything, kindly reach me through fatih.el.ghozy@gmail.com
"""
import numpy as np

data = np.loadtxt('data_overall.txt',skiprows=1)
Longitude = data[:,0]
Latitude = data[:,1]
SBA = data[:,5]

ngrid = 128 #can be set up freely depend on smoother (and heavier process) result
long_grid= np.linspace(np.min(Longitude), np.max(Longitude), ngrid)
lat_grid= np.linspace(np.min(Latitude), np.max(Latitude), ngrid)
x,y = np.meshgrid(long_grid, lat_grid)

#interpolate using Radial Basis Function
import matplotlib.pyplot as plt
import scipy.interpolate as inter

interpolasi = inter.Rbf(Longitude,Latitude,SBA,method='cubic')
SBA_interpolasi = interpolasi(x,y)

#spectrum analysis
from scipy import fft

spec_x = np.arange(1,129)
dt = 25800
f = (spec_x/2)/dt
k = 2*np.pi*f

spec_y_1 = SBA_interpolasi[:,42].tolist()
spec_yfft_1 = abs(fft.fft(spec_y_1))
lnA_1 = np.log(spec_yfft_1)

spec_y_2 = SBA_interpolasi[64,:].tolist()
spec_yfft_2 = abs(fft.fft(spec_y_2))
lnA_2 = np.log(spec_yfft_2)

spec_y_3 = SBA_interpolasi[:,84].tolist()
spec_yfft_3 = abs(fft.fft(spec_y_3))
lnA_3 = np.log(spec_yfft_3)

#plotting spectrum analysis
plt.figure()
ax1 = plt.subplot(131)
ax1.scatter(k[:64],lnA_1[:64],color='orange',marker=".",linewidths=1,picker=True)
ax1.set_xlim(-0.001,np.max(k[:64])+0.001)
ax2 = plt.subplot(132)
ax2.scatter(k[:64],lnA_2[:64],color='green',marker=".",linewidths=1,picker=True)
ax2.set_xlim(-0.001,np.max(k[:64])+0.001)
ax3 = plt.subplot(133)
ax3.scatter(k[:64],lnA_3[:64],color='black',marker=".",linewidths=1,picker=True)
ax3.set_xlim(-0.001,np.max(k[:64])+0.001)

pick_regional = plt.ginput(-1,timeout=0)
pick_regional = np.array(pick_regional)
print(pick_regional)

pick_residual = plt.ginput(-1,timeout=0)
pick_residual = np.array(pick_residual)
print(pick_residual)

reg1 = np.logical_and(k[:64] > pick_regional[0][0],k[:64] < pick_regional[1][0])
regional_x1 = k[:64][reg1]
regional_y1 = lnA_1[:64][reg1]
res1 = np.logical_and(k[:64] > pick_residual[0][0],k[:64] < pick_residual[1][0])
residual_x1 = k[:64][res1]
residual_y1 = lnA_1[:64][res1]

reg2 = np.logical_and(k[:64] > pick_regional[2][0],k[:64] < pick_regional[3][0])
regional_x2 = k[:64][reg2]
regional_y2 = lnA_2[:64][reg2]
res2 = np.logical_and(k[:64] > pick_residual[2][0],k[:64] < pick_residual[3][0])
residual_x2 = k[:64][res2]
residual_y2 = lnA_2[:64][res2]

reg3 = np.logical_and(k[:64] > pick_regional[4][0],k[:64] < pick_regional[5][0])
regional_x3 = k[:64][reg3]
regional_y3 = lnA_3[:64][reg3]
res3 = np.logical_and(k[:64] > pick_residual[4][0],k[:64] < pick_residual[5][0])
residual_x3 = k[:64][res3]
residual_y3 = lnA_3[:64][res3]

from sklearn.linear_model import LinearRegression

nama_regionalx = [regional_x1,regional_x2,regional_x3]
nama_regionaly = [regional_y1,regional_y2,regional_y3]
nama_residualx = [residual_x1,residual_x2,residual_x3]
nama_residualy = [residual_y1,residual_y2,residual_y3]

nama_model_regional = ['model_regional1','model_regional2','model_regional3']
nama_model_residual = ['model_residual1','model_residual2','model_residual3']

regional_out,residual_out,intercept,gradien = [],[],[],[]

for i,j,k,l,m,n in zip(nama_regionalx,nama_regionaly,nama_residualx,
                       nama_residualy,nama_model_regional,nama_model_residual):
    m = LinearRegression().fit(i.reshape(-1, 1),j.reshape(-1, 1))
    n = LinearRegression().fit(k.reshape(-1, 1),l.reshape(-1, 1))
    intercept.extend((m.intercept_,n.intercept_))
    gradien.extend((m.coef_,n.coef_))
    y_reg = m.intercept_ + m.coef_ * i
    y_res = n.intercept_ + n.coef_ * k
    regional_out.append(y_reg)
    residual_out.append(y_res)

for i in range(len(gradien)):
    gradien[i] = gradien[i].flatten()

ax1.plot(regional_x1,regional_out[0].flatten(),color='black')
ax1.plot(residual_x1,residual_out[0].flatten(),color='cyan')
ax1.text(0,np.max(lnA_1[:64])-np.min(lnA_1[:64]),'Regional \n y = {}x + {}'.format(format(gradien[0][0],
         ".2f"),format(intercept[0][0],".3f")))
ax1.text(((np.max(k[:64])-np.min(k[:64]))/2),np.max(residual_out[0]),'Residual \n y = {}x + {}'
         .format(format(gradien[1][0],".2f"),format(intercept[1][0],".3f")))

ax2.plot(regional_x2,regional_out[1].flatten(),color='red')
ax2.plot(residual_x2,residual_out[1].flatten(),color='yellow')
ax2.text(0,np.max(lnA_2[:64])-abs(np.min(lnA_2[:64])),'Regional \n y = {}x + {}'.format(format(gradien[2][0],
         ".2f"),format(intercept[2][0],".3f")))
ax2.text(((np.max(k[:64])-np.min(k[:64]))/2),np.max(residual_out[1]),'Residual \n y = {}x + {}'
         .format(format(gradien[3][0],".2f"),format(intercept[3][0],".3f")))

ax3.plot(regional_x3,regional_out[2].flatten())
ax3.plot(residual_x3,residual_out[2].flatten(),color='lime')
ax3.text(0,np.max(lnA_3[:64])-np.min(lnA_3[:64]),'Regional \n y = {}x + {}'.format(format(gradien[4][0],
         ".2f"),format(intercept[4][0],".3f")))
ax3.text(((np.max(k[:64])-np.min(k[:64]))/2),np.max(residual_out[2]),'Residual \n y = {}x + {}'
         .format(format(gradien[5][0],".2f"),format(intercept[5][0],".3f")))
