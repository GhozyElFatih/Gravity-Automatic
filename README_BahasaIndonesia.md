# Gravity-Automatic
## Mengunduh, ekstraksi, mengolah, dan memplot data gravitasi. Dari laman web Topex hingga kontur anomali bouguer sederhana (bahkan lebih dari itu!)
Apakah kamu mahasiswa Geofisika, sedang melakukan penelitian menggunakan data gravitasi satelit?
Kode ini mungkin cocok untukmu!

Saya membuat kode ini agar kamu dapat mengunduh, mengekstrak, mengolah, dan memplot data gravitasi secara otomatis dari laman web Topex.

Bagaimana caranya?

[![image](https://user-images.githubusercontent.com/85453675/135860020-ef577d1d-b8f9-4fbc-ace7-dd6caa7c7f3f.png)](https://youtu.be/JIzfRTNMiEc)

### 1. Pastikan kamu punya python IDE pada komputermu
Kode ini ditulis dalam bahasa pemrograman python. Untuk menjalankannya, kamu (tentu saja) membutuhkan python IDE versi 3.7 atau lebih. Kamu bisa menggunakan IDE apa saja
(rekomendasi saya : Spyder, PyCharm)

### 2. Instal modul yang dibutuhkan
Kamu membutuhkan beberapa paket modul untuk menjalankan kode ini. Jika kamu belum punya, pastikan instal modul-modul dibawah ini :
- NumPy
- Pandas
- Matplotlib
- SciPy
- Selenium
- scikit-learn (sklearn)

Untuk menginstalnya, cukup ketik :
```
pip install numpy pandas matplotlib scipy selenium sklearn
```
pada konsol / python command prompt kamu. Tunggu hingga seluruh proses pengunduhan dan instalasi selesai, setelah itu muat ulang konsol (atau IDE).

### 3. Install webdriver
Untuk mengontrol browser secara otomatis menggunakan modul Selenium, kamu membutuhkan webdriver.
Kamu dapat mengunjungi laman https://www.selenium.dev/downloads/ dan cari bagian 'Platforms Supported by Selenium' di bawah, lalu pilih browser yang akan kamu gunakan.

![image](https://user-images.githubusercontent.com/85453675/135839875-d1e61e4c-d445-45fc-b008-ea401b0a3704.png)

Klik pada tulisan 'documentation' yang mengarah kepada laman webdriver yang akan kamu gunakan. Pada tutorial ini, saya menggunakan Chrome.

Buka melalui laman https://chromedriver.chromium.org/ atau klik tulisan 'documentation' seperti pada gambar di atas.

![image](https://user-images.githubusercontent.com/85453675/135840343-1de3c615-a86c-498d-a1e0-edd4e81f8c84.png)

Lalu, klik pada tulisan Download di 'All versions available in Downloads'

![image](https://user-images.githubusercontent.com/85453675/135840490-9e7321da-a766-4a0d-8b27-c0f891ed8cc4.png)

Unduh webdriver yang sesuai dengan versi Chrome kamu. Untuk mengetahuinya, lihat pada Control Panel --> Uninstall a Program.
Kamu dapat melihat versi aplikasi yang kamu miliki pada kolom paling kanan.

![image](https://user-images.githubusercontent.com/85453675/135841249-8e56ade9-3692-4352-8d83-c760a3be7a9f.png)

Kembali ke laman Chrome webdriver, klik pada versi yang sesuai.

![image](https://user-images.githubusercontent.com/85453675/135841482-5149221f-ca64-40f3-ae92-7366675db364.png)

Pilih chromedriver_win32.zip jika kamu menggunakan Windows.

Setelah sukses mengunduh, ekstrak chromedriver.exe dari file ekstensi .zip yang telah kita unduh, lalu letakkan di C:\Windows

![image](https://user-images.githubusercontent.com/85453675/135842160-e94410fd-677b-41c6-a879-b4c946e0149e.png)
![image](https://user-images.githubusercontent.com/85453675/135842314-09a4d0cd-aa19-4615-99c9-8f8d197ca79c.png)

### 4. Mengatur IDE agar muncul secara interaktif ketika memplot (hanya untuk Spyder)
Apabila kamu menggunakan Spyder dari Anaconda, kamu harus mengatur mekanisme plot. Klik Tools --> Preferences yang terdapat di bagian atas.

![image](https://user-images.githubusercontent.com/85453675/135843466-3bbfc1a0-6553-45ca-b6ab-458d5d4098e1.png)

Pilih IPython Console, lalu tab Graphics, atur Graphics Backend dari semula Inline menjadi Automatic.

![image](https://user-images.githubusercontent.com/85453675/135843639-4b72ff43-7247-46df-aee9-2a167792c5e5.png)

Tutup dan buka kembali Spyder. Untuk IDE lain, harap cari tau sendiri caranya.

### 5. Jalankan!
Sekarang, (semoga) semuanya telah diatur dengan benar. Buka [topex_auto.py](https://github.com/GhozyElFatih/Gravity-Automatic/raw/main/topex_auto.py) pada IDE. Lalu klik Run atau pencet tombol F5.

Masukkan koordinat area yang ingin kamu dapatkan datanya

![image](https://user-images.githubusercontent.com/85453675/135853538-16ef1621-dbc2-4038-b157-79205a68f7ea.png)

Anomali Bouguer Sederhana telah didapatkan!

![image](https://user-images.githubusercontent.com/85453675/135853571-25c745ab-4abb-4a98-9d8e-d6f6a8097147.png)

Memilih batas regional dan residual melalui analisis spektrum

![image](https://user-images.githubusercontent.com/85453675/135853708-8e04016c-a854-4669-b8d6-747905b6f7d1.png)

Memisahkan data regional dan residual dengan moving average filter

![image](https://user-images.githubusercontent.com/85453675/135853822-d9b976f0-5918-4cd9-9a97-d481e1e8f4d9.png)

Data residual digunakan untuk mendapatkan First Horizontal Derivative dan Second Vertical Derivative

![image](https://user-images.githubusercontent.com/85453675/135853957-66273439-4af2-45c9-9865-7bac42e6ad2e.png)
![image](https://user-images.githubusercontent.com/85453675/135853988-2f0f502e-741e-4db7-a3d6-878f61d40dcb.png)

### Selamat mencoba
