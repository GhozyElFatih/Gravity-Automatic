# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 18:31:49 2021

@author: Ghozy El Fatih
For academic and non-profit purposes only
Any question, suggestion, or anything, kindly reach me through fatih.el.ghozy@gmail.com
"""
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

ngrid = 50 #can be set up freely depend on smoother (and heavier process) result
long_grid= np.linspace(np.min(Longitude), np.max(Longitude), ngrid)
lat_grid= np.linspace(np.min(Latitude), np.max(Latitude), ngrid)
x,y = np.meshgrid(long_grid, lat_grid)

#interpolate using Radial Basis Function
import matplotlib.pyplot as plt
import scipy.interpolate as inter

interpolasi = inter.Rbf(Longitude,Latitude,SBA,method='cubic')
SBA_interpolasi = interpolasi(x,y)

#plotting
plt.contourf(x,y,SBA_interpolasi,cmap='jet',levels=50)
plt.colorbar(label='Percepatan Gravitasi (mGal)')
mayor = plt.contour(x, y, SBA_interpolasi, colors='black', levels=5, linewidths=1)
plt.contour(x,y,SBA_interpolasi,levels=25,linewidths=0.5)
plt.suptitle('Data Simple Bouguer Anomaly pada Area Lat ({},{}) Long ({},{})'.format(format(N,".2f"),format(S,".2f"),
            format(W,".2f"),format(E,".2f")),fontsize='20',fontweight='bold')
plt.xlabel('Longitude', fontsize='15')
plt.ylabel('Latitude', fontsize='15')
plt.text(np.min(Longitude),np.max(Latitude),'Densitas Rata-rata = {}'.format(rho),backgroundcolor='white')
plt.clabel(mayor,mayor.levels,inline=True,fontsize=6)
print("Done!")
