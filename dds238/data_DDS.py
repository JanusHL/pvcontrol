#!/usr/bin/python
# -*- coding: utf-8 -*-

# data_DDS.py
# Lee datos de DDS238 - Medidor de energía HIKING
# FAM para Control FV - 25/01/2019
#----------------------------------------------------

import struct
import time, datetime
import class_dds
import MySQLdb

# Abrir BBDD aqui

try:
   sensor = class_dds.DDS()
except:
   print('Error DDS...')

while True:   
    Data=sensor.readAll()

    print time.strftime("%Y-%m-%d %H:%M:%S")    
    print "Voltaje: ", Data[0]/10
    print "Intensidad: ", float(Data[1])/100
    print "Potencia: ", Data[2]
    print "----------------------"
    
    time.sleep(3)
   

