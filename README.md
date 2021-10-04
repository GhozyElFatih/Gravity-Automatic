# Gravity-Automatic
## Download, extract, process, and plot gravity data. From Topex website to simple bouguer anomaly contour (even more!)
Are you a Geophysics Student, doing research using satellite gravity data?
You may love this code!

I created code that could make you able to download, extract, process, and plot gravity data automatically from Topex website.

How to get started?

[![image](https://user-images.githubusercontent.com/85453675/135860020-ef577d1d-b8f9-4fbc-ace7-dd6caa7c7f3f.png)](https://youtu.be/JIzfRTNMiEc)

### 1. Make sure you have python IDE on your PC
This code was written in python language. To run it, you need python IDE (of course) with the version 3.7 or above. You can use any IDE (my recommend : Spyder, PyCharm).

### 2. Install necessary packages
You need to install some packages that maybe you didn't have before. These packages list are :
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
on your console / python command prompt. Wait until all of these have succesfully installed, then restart your kernel (or restart your IDE).

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
There you can check you apps version on the rightmost column.

![image](https://user-images.githubusercontent.com/85453675/135841249-8e56ade9-3692-4352-8d83-c760a3be7a9f.png)

Now back to Chrome webdriver site and click to match version of yours.

![image](https://user-images.githubusercontent.com/85453675/135841482-5149221f-ca64-40f3-ae92-7366675db364.png)

Choose chromedriver_win32.zip if you are using Windows.

After you succesfully downloaded it, extract chromedriver.exe from .zip file and place it on C:\Windows

![image](https://user-images.githubusercontent.com/85453675/135842160-e94410fd-677b-41c6-a879-b4c946e0149e.png)
![image](https://user-images.githubusercontent.com/85453675/135842314-09a4d0cd-aa19-4615-99c9-8f8d197ca79c.png)

### 4. Settings your IDE to 'pop-up' when plotting (Spyder tutorial only)
If you are using Spyder IDE from Anaconda, you have to set up plotting style. Go to Tools --> Preferences on the top of the bar.

![image](https://user-images.githubusercontent.com/85453675/135843466-3bbfc1a0-6553-45ca-b6ab-458d5d4098e1.png)

Move to IPython Console and Graphics tab, then, set the Graphics Backend from Inline to Automatic.

![image](https://user-images.githubusercontent.com/85453675/135843639-4b72ff43-7247-46df-aee9-2a167792c5e5.png)

Close and re-open your Spyder. For another IDE, please check how to set up interactive tools.

### 5. Run the code!
Now everything have been set up properly (hopefully). Open topex_auto.py file to your IDE. It's time to run the code with a simply pressing F5 or Run button.

Input your area coordinates

![image](https://user-images.githubusercontent.com/85453675/135853538-16ef1621-dbc2-4038-b157-79205a68f7ea.png)

You've got your Simple Bouguer Anomaly

![image](https://user-images.githubusercontent.com/85453675/135853571-25c745ab-4abb-4a98-9d8e-d6f6a8097147.png)

Picking regional and residual boundary range in the spectrum analysis

![image](https://user-images.githubusercontent.com/85453675/135853708-8e04016c-a854-4669-b8d6-747905b6f7d1.png)

Then, we were able to separate regional and residual data

![image](https://user-images.githubusercontent.com/85453675/135853822-d9b976f0-5918-4cd9-9a97-d481e1e8f4d9.png)

Residual data was used to get First Horizontal Derivative and Second Vertical Derivative

![image](https://user-images.githubusercontent.com/85453675/135853957-66273439-4af2-45c9-9865-7bac42e6ad2e.png)
![image](https://user-images.githubusercontent.com/85453675/135853988-2f0f502e-741e-4db7-a3d6-878f61d40dcb.png)

### Now it's your turn to try



