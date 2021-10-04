# Gravity-Automatic
## Download, extract, process, and plot gravity data. From Topex website to simple bouguer anomaly contour (even more!)
Are you a Geophysics Student, doing research using satellite gravity data?
You may love this code!

I created code that could make you able to download, extract, process, and plot gravity data automatically from Topex website.

How to get started?

### 1. Make sure you have python IDE on your PC
This code was written in python language. To run it, you need python IDE (of course) with the version 3.7 or above. You can use any IDE (my recommend : Spyder, pyCharm).

### 2. Install necessary packages
You need to install some packages that may be you didn't have before. These packages list are :
- numpy
- pandas
- matplotlib
- scipy
- selenium
- sklearn

To install these packages, simple write :
```
pip install numpy pandas matplotlib scipy selenium sklearn
```
on your console / python command prompt.

### 3. Install webdriver
To automatically control the browser by using Selenium package, you'll need webdriver.
You can visit https://www.selenium.dev/downloads/ and scroll down to 'Platforms Supported by Selenium', then, choose your browser

![image](https://user-images.githubusercontent.com/85453675/135839875-d1e61e4c-d445-45fc-b008-ea401b0a3704.png)

Click on the 'documentation' link from one of browser you'll use. For this tutorial, I'll use Chrome.

Open https://chromedriver.chromium.org/ or documentation link from image above.

![image](https://user-images.githubusercontent.com/85453675/135840343-1de3c615-a86c-498d-a1e0-edd4e81f8c84.png)

Then, click download link on 'All versions available in Downloads'

![image](https://user-images.githubusercontent.com/85453675/135840490-9e7321da-a766-4a0d-8b27-c0f891ed8cc4.png)

Download webdriver that match with your Chrome version. To check your Chrome version, you can see it on Control Panel --> Uninstall a program.
There you can check you apps version

![image](https://user-images.githubusercontent.com/85453675/135841249-8e56ade9-3692-4352-8d83-c760a3be7a9f.png)

Now back to Chrome webdriver site and click to match version of yours

![image](https://user-images.githubusercontent.com/85453675/135841482-5149221f-ca64-40f3-ae92-7366675db364.png)

Choose chromedriver_win32.zip if you are using Windows.

After you succesfully downloaded it, extract chromedriver.exe from .zip file and place it on C:\Windows

![image](https://user-images.githubusercontent.com/85453675/135842160-e94410fd-677b-41c6-a879-b4c946e0149e.png)
![image](https://user-images.githubusercontent.com/85453675/135842314-09a4d0cd-aa19-4615-99c9-8f8d197ca79c.png)


