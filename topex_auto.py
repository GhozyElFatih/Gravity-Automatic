# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 18:31:49 2021

@author: Ghozy El Fatih
For academic and non-profit purposes only
Any question, suggestion, or anything, kindly reach me through fatih.el.ghozy@gmail.com
"""
import time
t0 = time.process_time()

area_name = ['north','south','west','east']

N = float(input('Input North Boundary : '))
W = float(input('Input West Boundary : '))
S = float(input('Input South Boundary : '))
while S >= N:
    S = float(input('The south boundary is wrong, try again : '))
    
E = float(input('Input East Boundary : '))
while E <= W:
    E = float(input('The east boundary is wrong, try again : '))

print("Boundary is ready \n Downloading data, please wait...")

area_input = [str(N),str(S),str(W),str(E)]

from selenium import webdriver #must be pip install first if you don't have one

url = "https://topex.ucsd.edu/cgi-bin/get_data.cgi" #Topex Website for Downloading Satellite Gravity Data

driver = webdriver.Chrome() #Define browser you'll use
driver.get(url)

for i,j in zip(area_name, area_input):
    driver.find_element_by_name(i).send_keys(j)

#Getting topography data
topografi = driver.find_element_by_xpath("//input[@value='1']").click()
get_topografi = driver.find_element_by_xpath("//input[@value='get data']").click()

import os
import codecs

def save_hasil(name):
    hasil_name = name+'.txt' #save file as txt
    hasil_save = os.path.join(hasil_name)
    hasil_object = codecs.open(hasil_save, "w", "utf-8")
    html = driver.page_source
    return (hasil_object.write(html))

nama_topografi = 'topografi'
save_hasil(nama_topografi)

driver.back()

#getting gravity data
gravity = driver.find_element_by_xpath("//input[@value='0.1']").click()
get_gravity = driver.find_element_by_xpath("//input[@value='get data']").click()

nama_gravity = 'gravity'
save_hasil(nama_gravity)

driver.close()

#downloading data is done
#now for simple bouguer anomaly processing
print("Data downloaded succesfully \n Now processing to Simple Bouguer Anomaly...")

import numpy as np

with open(nama_topografi+'.txt') as f:
    n = len(list(f))-2

data_topografi = np.loadtxt(nama_topografi+'.txt',skiprows=1,max_rows=n)
data_gravity = np.loadtxt(nama_gravity+'.txt',skiprows=1,max_rows=n)

data_overall = np.zeros((n,6))
data_overall[:,:3] = data_topografi
data_overall[:,3] = data_gravity[:,2]

Longitude = data_overall[:,0]
Latitude = data_overall[:,1]
Z = data_overall[:,2]
FAA = data_overall[:,3]

BC = 0.04192 * Z

#getting average density using parasnis method through simple inversion
matrix_1 = np.ones(n)
G = np.vstack((matrix_1,BC)).T
Gt = G.T
d = FAA.T

GtG = np.dot(Gt,G)
Gtd = np.dot(Gt,d)

m = np.dot(np.linalg.inv(GtG),Gtd)

#in case if we didn't get make sense density result, we use 2.7 (average continental crust density)
if m[1] < 1.9 or m[1] > 3.1:
    BC = BC*2.7
    rho = str(2.7)+' gr/cc'
else:
    BC = BC*m[1]
    rho = str(format(m[1], ".3f"))+' gr/cc'

SBA = FAA - BC

data_overall[:,4] = BC
data_overall[:,5] = SBA

np.savetxt('data_overall.txt',data_overall,fmt="%.3f",header="Long Lat Z FAA BC SBA")

ngrid = 128 #can be set up freely depend on smoother (and heavier process) result
long_grid= np.linspace(np.min(Longitude), np.max(Longitude), ngrid)
lat_grid= np.linspace(np.min(Latitude), np.max(Latitude), ngrid)
x,y = np.meshgrid(long_grid, lat_grid)

#interpolate using Radial Basis Function
import matplotlib.pyplot as plt
import scipy.interpolate as inter

interpolasi = inter.Rbf(Longitude,Latitude,SBA,method='cubic')
SBA_interpolasi = interpolasi(x,y)

#plotting contour
plt.figure(1)
plt.contourf(x,y,SBA_interpolasi,cmap='jet',levels=50)
#plt.plot(x[:,42],y[:,42])
#plt.plot(x[64,:],y[64,:])
#plt.plot(x[:,84],y[:,84])
plt.colorbar(label='Percepatan Gravitasi (mGal)')
mayor = plt.contour(x, y, SBA_interpolasi, colors='black', levels=5, linewidths=1)
plt.contour(x,y,SBA_interpolasi,levels=25,linewidths=0.5)
plt.suptitle('Data Simple Bouguer Anomaly pada Area Lat ({},{}) Long ({},{})'.format(format(N,".2f"),format(S,".2f"),
            format(W,".2f"),format(E,".2f")),fontsize='20',fontweight='bold')
plt.xlabel('Longitude', fontsize='15')
plt.ylabel('Latitude', fontsize='15')
plt.text(np.min(Longitude),np.max(Latitude),'Densitas Rata-rata = {}'.format(rho),backgroundcolor='white')
plt.clabel(mayor,mayor.levels,inline=True,fontsize=6)

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
plt.figure(2)
plt.suptitle('Pick regional range first from each spectrum \n Left-click for pick, Right-click for cancel, Middle-click for done',
             fontsize='15',fontweight='bold')
ax1 = plt.subplot(131)
ax1.scatter(k[:64],lnA_1[:64],color='orange',marker=".",linewidths=1,picker=True)
ax1.set_xlim(-0.001,np.max(k[:64])+0.001)
ax1.set_ylabel('Ln(A)')
ax2 = plt.subplot(132)
ax2.scatter(k[:64],lnA_2[:64],color='green',marker=".",linewidths=1,picker=True)
ax2.set_xlim(-0.001,np.max(k[:64])+0.001)
ax2.set_xlabel('k (wavenumber)')
ax3 = plt.subplot(133)
ax3.scatter(k[:64],lnA_3[:64],color='black',marker=".",linewidths=1,picker=True)
ax3.set_xlim(-0.001,np.max(k[:64])+0.001)
#picking regional range
pick_regional = plt.ginput(6,timeout=0)
pick_regional = np.array(pick_regional)
print('Picking Result')
print('Regional Boundary')
print(pick_regional)
#picking resdiual range
plt.suptitle('Pick residual range from each spectrum',fontsize='15',fontweight='bold')
pick_residual = plt.ginput(6,timeout=0)
pick_residual = np.array(pick_residual)
print('Residual Boundary')
print(pick_residual)
plt.suptitle('Regional and Residual picking are done',fontsize='15',fontweight='bold')

#set up regional and residual range for linear regression
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

#linear regression to get gradient and intercept (+c)
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

#moving average    
# (c_residual - c_regional)/(m_regional - m_residual)
x_1 = (intercept[1][0] - intercept[0][0])/(gradien[0][0] - gradien[1][0])
x_2 = (intercept[3][0] - intercept[2][0])/(gradien[2][0] - gradien[3][0])
x_3 = (intercept[5][0] - intercept[4][0])/(gradien[4][0] - gradien[5][0])

X = np.array([x_1, x_2, x_3])
lamda_x = (2*np.pi)/X
N = lamda_x/200
N_mean = np.mean(N) 

import math
from scipy.signal import convolve2d

def movingaverage(input_array, n_mean):
    n = math.floor(n_mean)
    Filter = np.ones([n, n])/n**2
    result = convolve2d(input_array, Filter, mode='same', boundary='symm')
    return result

anomali_regional = movingaverage(SBA_interpolasi, N_mean)
anomali_residual = SBA_interpolasi - anomali_regional

#plot
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

aaa=plt.figure(3,figsize=(10,20))
aaa.tight_layout()
plt.subplot(131)
plt.contourf(x,y,SBA_interpolasi,cmap='jet',levels=50)
plt.colorbar()
mayor1 = plt.contour(x, y, SBA_interpolasi, colors='black', levels=5, linewidths=1)
plt.contour(x,y,SBA_interpolasi,levels=25,linewidths=0.5)
plt.title('Simple Bouguer Anomaly',fontsize='15',fontweight='bold')
plt.ylabel('Latitude', fontsize='10')
plt.xticks(rotation=45)
plt.yticks(rotation=90)
plt.clabel(mayor1,mayor1.levels,inline=True,fontsize=6)

plt.subplot(132)
plt.contourf(x,y,anomali_regional,cmap='jet',levels=50)
plt.colorbar()
mayor2 = plt.contour(x, y, anomali_regional, colors='black', levels=5, linewidths=1)
plt.contour(x,y,anomali_regional,levels=25,linewidths=0.5)
plt.title('Regional \n Simple Bouguer Anomaly',fontsize='15',fontweight='bold')
plt.xlabel('Longitude', fontsize='10')
plt.xticks(rotation=45)
plt.yticks(rotation=90)
plt.clabel(mayor2,mayor2.levels,inline=True,fontsize=6)

plt.subplot(133)
plt.contourf(x,y,anomali_residual,cmap='jet',levels=50)
plt.colorbar(label='Percepatan Gravitasi (mGal)')
mayor3 = plt.contour(x, y, anomali_residual, colors='black', levels=5, linewidths=1)
plt.contour(x,y,anomali_residual,levels=25,linewidths=0.5)
plt.title('Residual \n Simple Bouguer Anomaly',fontsize='15',fontweight='bold')
plt.xticks(rotation=45)
plt.yticks(rotation=90)
plt.clabel(mayor3,mayor3.levels,inline=True,fontsize=6)

#fhd
fhd_vert = np.array([[-1,0,1],
                     [-1,0,1],
                     [-1,0,1]])
fhd_hor = np.array([[-1,-1,-1],
                    [0,0,0],
                    [1,1,1]])

fhd_vert_conv = convolve2d(anomali_residual,fhd_vert,mode='same',boundary='symm')
fhd_hor_conv = convolve2d(anomali_residual,fhd_hor,mode='same',boundary='symm')

FHD = fhd_vert_conv + fhd_hor_conv

plt.figure(4)
plt.contourf(x,y,FHD,cmap='jet',levels=50)
plt.colorbar()
mayor4 = plt.contour(x, y, FHD, colors='black', levels=5, linewidths=1)
plt.contour(x,y,FHD,levels=25,linewidths=0.5)
plt.suptitle('First Horizontal Derivative',fontsize='20',fontweight='bold')
plt.ylabel('Latitude', fontsize='15')
plt.xlabel('Longitude',fontsize='15')
plt.clabel(mayor4,mayor4.levels,inline=True,fontsize=6)

#svd
def svd_elkins(input_array):
    matrix_elkins = np.array([[0.00000,-0.0833,0.00000,-0.0833,0.00000],
                              [-0.0833,-0.0667,-0.0334,-0.0667,-0.0833],
                              [0.000000,-0.0334,1.0668,-0.0334,0.00000],
                              [-0.0833,-0.0667,-0.0334,-0.0667,-0.0833],
                              [0.00000,-0.0833,0.00000,-0.0833,0.00000]])
    svdelkins = convolve2d(input_array,matrix_elkins,mode='same',boundary='symm')
    return svdelkins

def svd_rosenbach(input_array):
    matrix_rosenbach = np.array([[0.00000,0.0416,0.00000,0.0416,0.00000],
                                 [0.0416,-0.3332,-0.7500,-0.3332,0.0416],
                                 [0.00000,-0.7500,1.0668,-0.7500,0.0000],
                                 [0.0416,-0.3332,-0.7500,-0.3332,0.0416],
                                 [0.00000,0.0416,0.00000,0.0416,0.00000]])
    svdrosen = convolve2d(input_array,matrix_rosenbach,mode='same',boundary='symm')
    return svdrosen

def svd_henderson(input_array):
    matrix_henderson = np.array([[0.00000,0.0000,-0.0838,0.00000,0.00000],
                                 [0.00000,1.00000,-2.6667,1.00000,0.0000],
                                 [-0.0838,-2.6667,17.000,-2.6667,-0.0838],
                                 [0.0000,1.00000,-2.6667,1.00000,0.00000],
                                 [0.00000,0.00000,-0.0838,0.0000,0.00000]])
    svdhend = convolve2d(input_array,matrix_henderson,mode='same',boundary='symm')
    return svdhend

elkins = svd_elkins(SBA_interpolasi)
rosenbach = svd_rosenbach(SBA_interpolasi)
henderson = svd_henderson(SBA_interpolasi)

plt.figure(5,figsize=(10,20))
plt.suptitle('Second Vertical Derivative')
plt.subplot(131)
plt.contourf(x,y,elkins,cmap='jet',levels=50)
plt.colorbar()
mayor5 = plt.contour(x, y, elkins, colors='black', levels=5, linewidths=1)
plt.contour(x,y,elkins,levels=25,linewidths=0.5)
plt.title('Elkins',fontsize='15',fontweight='bold')
plt.ylabel('Latitude', fontsize='10')
plt.xticks(rotation=45)
plt.yticks(rotation=90)
plt.clabel(mayor5,mayor5.levels,inline=True,fontsize=6)

plt.subplot(132)
plt.contourf(x,y,rosenbach,cmap='jet',levels=50)
plt.colorbar()
mayor6 = plt.contour(x, y, rosenbach, colors='black', levels=5, linewidths=1)
plt.contour(x,y,rosenbach,levels=25,linewidths=0.5)
plt.title('Rosenbach',fontsize='15',fontweight='bold')
plt.xlabel('Longitude', fontsize='10')
plt.xticks(rotation=45)
plt.yticks(rotation=90)
plt.clabel(mayor6,mayor6.levels,inline=True,fontsize=6)

plt.subplot(133)
plt.contourf(x,y,henderson,cmap='jet',levels=50)
plt.colorbar(label='Percepatan Gravitasi (mGal)')
mayor7 = plt.contour(x, y, henderson, colors='black', levels=5, linewidths=1)
plt.contour(x,y,henderson,levels=25,linewidths=0.5)
plt.title('Henderson & Zieltz',fontsize='15',fontweight='bold')
plt.xticks(rotation=45)
plt.yticks(rotation=90)
plt.clabel(mayor7,mayor7.levels,inline=True,fontsize=6)

t1 = time.process_time()
t = t1-t0
tt = t/60
print("Done!")
print('Process time:',int(tt),'minutes',(tt-int(tt))*60,'second')
