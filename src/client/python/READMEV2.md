Python IoT Hub SDK v2
==================================

# Raspberry Pi Installation
The Azure IoT Hub SDK v2 takes advantage of lauguage features in Python that require version 3.7+ of the language.
Raspberry Pi's apt-get repository does not contain an 3.7 installation version at the time, so running the sample on a Raspberry Pi will require building Python 3.7 from source.

There is a very good resource on how to install Python 3.7 on Raspbian that you can read at https://github.com/instabot-py/instabot.py/wiki/Installing-Python-3.7-on-Raspberry-Pi.  

Once Python 3.7 is installed, you can install the two required Azure IoT packages with the following commands:
````sh
sudo pip3.7 install azure
sudo pip3.7 install azure-iot-device
````

Once those packages are installed, you should be able to execute the client application with:
````sh
python3.7 appv2.py
````
