Food Safety Consortium Sample
==================================

# Scenario
The repository contains and end-to-end food safety scenario that uses Azure Blockchain Service and Azure IoT Hub.  It provides a reference architecture for a multi-party consortium using Blockchain as a shared, distributed ledger for tracking the lifecycle of food.  Temperature and humidity sensors are used on top of Raspberry Pi to capture the current state.

# Client Python Dependencies for Raspberry Pi
The client code makes use of the Adafruit_Python_DHT Python module.  You can find the code repository at https://github.com/adafruit/Adafruit_Python_DHT.

Installing
----------

### Dependencies

For all platforms (Raspberry Pi and Beaglebone Black) make sure your system is
able to compile and download Python extensions with **pip**:

On Raspbian or Beaglebone Black's Debian/Ubuntu image you can ensure your
system is ready by running one or two of the following sets of commands:

Python 2:

````sh
sudo apt-get update
sudo apt-get install python-pip
sudo python -m pip install --upgrade pip setuptools wheel
````

Python 3:

````sh
sudo apt-get update
sudo apt-get install python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel
````

### Install with pip

Use `pip` to install from PyPI.

Python 2:

```sh
sudo pip install Adafruit_DHT
```

Python 3:

```sh
sudo pip3 install Adafruit_DHT
```
