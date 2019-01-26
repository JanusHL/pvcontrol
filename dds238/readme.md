# DDS238 energy meter

![alt text](https://raw.githubusercontent.com/janusHL/pvcontrol/master/dds238/dds238.jpg)

Recently I've purchased the HIKING "single phase energy meter" from aliexpress.
This meter can be accesed by a simple modbus RTU python routine.
I've implemented a new python class that do this job, and I can read the data from my Raspberry PI unit.
The goal is to read the power from a line of microinverters and pass the data to PVControl database.

# Necessary Hardware

* DDS238 module
* USB to RS485 converter
![alt text](https://raw.githubusercontent.com/janusHL/pvcontrol/master/dds238/USB_2_rs485.jpg)
* Raspberry PI (the most economical option)


# Phyton module

The class can be run separately: python class_dds.py
but I put de data_DDS.py test program that read the data in a loop.
Even this module has more data I've read only 3 values: voltage, current, and power.
Actually I only need Power, the two others are not necessary for my proyect and anyone can implemented the rest of the data.
