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

def save_hasil(name):
    hasil_name = name+'.txt'
    hasil_save = os.path.join(hasil_name)
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
print("Data downloaded succesfully!")
