# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 18:31:49 2021

@author: Acer
"""
area_name = ['north','south','west','east']

N = input('Masukkan Batas Utara Area : ')
S = input('Masukkan Batas Selatan Area : ')
W = input('Masukkan Batas Barat Area : ')
E = input('Masukkan Batas Timur Area : ')

area_input = [N,S,W,E]

from selenium import webdriver

url = "https://topex.ucsd.edu/cgi-bin/get_data.cgi"
driver = webdriver.Chrome()
driver.get(url)

for i,j in zip(area_name, area_input):
    driver.find_element_by_name(i).send_keys(j)

topografi = driver.find_element_by_xpath("//input[@value='1']").click()
get_topografi = driver.find_element_by_xpath("//input[@value='get data']").click()

import os
import codecs

path = 'C:/Users/Acer/OneDrive - UNIVERSITAS INDONESIA/Desktop'
save_path = os.path.expanduser(path)

def save_hasil(name):
    hasil_name = name+'.txt'
    hasil_save = os.path.join(save_path, hasil_name)
    hasil_object = codecs.open(hasil_save, "w", "utf-8")
    html = driver.page_source
    return (hasil_object.write(html))

nama_topografi = 'topografi'
save_hasil(nama_topografi)

driver.back()

gravity = driver.find_element_by_xpath("//input[@value='0.1']").click()
get_gravity = driver.find_element_by_xpath("//input[@value='get data']").click()

nama_gravity = 'gravity'
save_hasil(nama_gravity)

driver.close()

import numpy as np

with open(path+'/'+nama_topografi+'.txt') as f:
    n = len(list(f))-2

data_topografi = np.loadtxt(path+'/'+nama_topografi+'.txt',skiprows=1,max_rows=n)
data_gravity = np.loadtxt(path+'/'+nama_gravity+'.txt',skiprows=1,max_rows=n)

data_overall = np.zeros((n,6))
data_overall[:,:3] = data_topografi
data_overall[:,3] = data_gravity[:,2]

Long = data_overall[:,0]
Lat = data_overall[:,1]
Z = data_overall[:,2]
FAA = data_overall[:,3]
###
BC = 0.04192 * Z

matriks_1 = np.ones(n)
G = np.vstack((matriks_1,BC)).T
Gt = G.T
d = FAA.T

GtG = np.dot(Gt,G)
Gtd = np.dot(Gt,d)

m = np.dot(np.linalg.inv(GtG),Gtd)

if m[1] < 1.9 or m[1] > 3.1:
    BC = BC*2.7
    rho = str(2.7)+' gr/cc'
else:
    BC = BC*m[1]
    rho = str(format(m[1], "%.3f"))+' gr/cc'

SBA = FAA - BC

data_overall[:,4] = BC
data_overall[:,5] = SBA

np.savetxt('data_overall.txt',data_overall,fmt="%.3f",header="Long Lat Z FAA BC SBA")

ngrid = 50
long_grid= np.linspace(np.min(Long), np.max(Long), ngrid) #grid koordinat
lat_grid= np.linspace(np.min(Lat), np.max(Lat), ngrid)
x,y = np.meshgrid(long_grid, lat_grid)

import matplotlib.pyplot as plt
import scipy.interpolate as inter

interpolasi = inter.Rbf(Long,Lat,SBA,method='cubic')
SBA_interpolasi = interpolasi(x,y)

### Plotting
plt.contourf(x,y,SBA_interpolasi,cmap='jet',levels=50)
plt.colorbar(label='Percepatan Gravitasi (mGal)')
mayor = plt.contour(x, y, SBA_interpolasi, colors='black', levels=5, linewidths=1)
plt.contour(x,y,SBA_interpolasi,levels=25,linewidths=0.5)
plt.suptitle('Data Simple Bouguer Anomaly pada Area Lat ({},{}) Long ({},{})'.format(N,S,W,E),
             fontsize='20',fontweight='bold')
plt.xlabel('Longitude', fontsize='15')
plt.ylabel('Latitude', fontsize='15')
plt.text(np.min(Long),np.max(Lat),'Densitas Rata-rata = {}'.format(rho),backgroundcolor='white')
plt.clabel(mayor,mayor.levels,inline=True,fontsize=6)