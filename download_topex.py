area_name = ['north','south','west','east']

N = float(input('Masukkan Batas Utara Area : '))
W = float(input('Masukkan Batas Barat Area : '))
S = float(input('Masukkan Batas Selatan Area : '))
while S <= N and S > 0:
    S = float(input('Batas Area Tidak Sesuai, Masukkan Ulang Batas Selatan : '))
    
E = float(input('Masukkan Batas Timur Area : '))
while E <= W and E > 0:
    E = float(input('Batas Area Tidak Sesuai, Masukkan Ulang Batas Timur : '))

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