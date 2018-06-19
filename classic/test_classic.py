#!/usr/bin/python
# -*- coding: utf-8 -*-

# Test modbus multiples registros
# JanusHL para Control FV - 04/04/2018
# 05/04/2018 valores de los registros y estado
# 24/04/2018 Lectura de dos classics mediante módulo de clase classic.py
#---------------------------------
# Modbus Function Codes
# 1 : B, # Read Coils (1 byte)
# 2 : B, # Read Input Discrete Registers (1 byte)
# 3 : H, # Read Holding Registers (2 byte)
# 4 : H  # Read Input Registers (2 byte)
#-------------------------------------------------
# Opciones Modbus para leer 11 registros en el Classic
# 4115 Battery Voltage
# 4116 Input Voltage
# 4117 Output Current
# 4118 kWh
# 4119 Watts
# 4120 Charge Stage = [4120]MSB State = [4120]LSB
# 4121 Input Current
# 4122 LastVoc
# 4123 Reservado
# 4124 MatchPointShadow
# 4125 Amp Hours
# 4132 Batt Temp ºC
#-----------------------------------------------------

import struct
import time
import classic

# Registros

valor =['VBat', 'VPlaca', 'IBat', 'Kwh', 'Watt', 'Stat','IPlaca','LVoc','Res','MPS','AmpH']
bcs = ['Resting', 'n/a', 'n/a', 'Absorb','Bulk Mppt', 'Float', 'FloatMppt','Equalize', 'EQMppt']
 
# Direcciones TCP/IP para Classic1 y Classic2
TCP_IP = '192.168.20.41'
TCP_IP2 = '192.168.20.42'

try:

    try:
        mbus = classic.mbusread(TCP_IP)
    # leemos por diccionario
        dicc = mbus.get_dict()
        print dicc
        print("\nVALORES Classic en: " + TCP_IP + " Diccionario")    
        for i in range(0,10):
            key = valor[i]
            print(" %s: %s " %(key, dicc[key] *0.10))
    
        sttchg = dicc['Stat']
        print dicc['Stat']
        print("Current Status: %s - %s" %(sttchg, bcs[sttchg]))
        print("Battery Temp: %s ºC" %(dicc['Temp']* 0.10))
    except:
        print "error en Classic1"
    
    try:   
    
        mbus1 = classic.mbusread(TCP_IP2)
        #leemos por array
        data = mbus1.read_data()
        #Print valores de los registros
        print("\nVALORES Classic en: " + TCP_IP2)
        for i in range(6, 6+11):
            print(" %s: %s " %(valor[i-6],data[i]*0.10))
        
# status de carga actual
        print "12->", data[11]
        sttchg = data[11]/256
        if sttchg>7:
            sttchg=8
       
        print("Current Status: %s - %s" %(sttchg, bcs[sttchg]))

#  registro 4132 temperatura
        print("Battery Temp: %s ºC" %(data[23]* 0.10))
    except:
        print "Error en Classic2"

# Esperamos dos segundos antes de desconectar
    
    #time.sleep(2);
 
finally:
    # desconectamos los sockets 
    print('\nCLOSING '+ TCP_IP)
    mbus.closeSCK()
    print('\nCLOSING ' + TCP_IP2)
    mbus1.closeSCK()
    
