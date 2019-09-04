#!/usr/bin/python
# -*- coding: utf-8 -*-

# Test modbus multiples registros para SB modelos 2.5 y superiores y Sunny Island
# @autor: JanusHL para Control FV Copyright (c) 2019 JanusHL
# @creado: 25/05/2019
# @versión: 0.1beta
# @créditos: Diseñado a partir de una idea de 'stoberblog' https://github.com/stoberblog/sunspec-modbus
#            Copyright (c) 2017 stoberblog para las clases ctypes incluidas en el fichero sma.py
#
# @licencia: Uso libre de este script si se respeta el copyright (c) de los autores. 


"""
# registros comunes al SB (Sunny Boy)
30201	"Condition:
	35 = Fault
	303 = Off
	307 = Ok
	455 = Warning"		U32
30217	"Grid relay/contactor:
    51 = Closed
    311 = Open
    16777213 = Information not available"		U32

30513	Total yield	Wh	U64
30517	Daily yield	Wh	U64
30521	Operating time	s	U64
30525	Feed-in time	s	U64
30529	Total yield	Wh	U32
30531	Total yield	kWh	U32
30533	Total yield	MWh	U32
30535	Daily yield	Wh	U32
30537	Daily yield	kWh	U32
30539	Daily yield	MWh	U32
30541	Operating time	s	U32
30543	Feed-in time	s	U32
30559	Number of events for user		U32
30561	Number of events for installer		U32
30563	Number of events for service		U32
30581	Counter reading of power drawn counter	Wh	U32
30583	Grid feed-in counter reading	Wh	U32
30599	Number of grid connections		U32
30775	Power	W	S32
30777	Power L1	W
30779	Power L2	W
30781	Power L3	W
30783	Grid voltage phase L1	V
30785	Grid voltage phase L2	V
30787	Grid voltage phase L3	V
30789	Grid voltage phase L1 against L2	V
30791	Grid voltage phase L2 against L3	V
30793	Grid voltage phase L3 against L1	V
30795	Grid current	A
30803	Grid frequency	Hz
30805	Reactive power	VAr
30807	Reactive power L1	VAr
30809	Reactive power L2	VAr
30811	Reactive power L3	VAr
30813	Apparent power	VA
30815	Apparent power L1	VA
30817	Apparent power L2	VA
30819	Apparent power L3	VA
34113	Internal temperature	°C	S32
40135	Nominal frequency	Hz	U32

--------------------------------------------
# registros comunes al SI (Sunny Island)
30837	Active power limitation P, active power configuration	W	U32
30839	Active power limitation P, active power configuration	%	U32
30843	Battery current	A	S32
30845	Current battery state of charge	%	U32
30847	Current battery capacity	%	U32
30849	Battery temperature	°C	S32
30851	Battery voltage	V	U32
30855	Current battery charging set voltage	V	U32
30865	Power drawn	W	S32
30867	Power grid feed-in	W	S32
-------------------------------------------
Este programa sirve para testear los equipos SMA, teniendo en cuenta ciertos parámetros:
TCP_IP --> es la dirección IP del equipo que queremos testear.
UNIT_ID --> es la unidad modbus que tiene asignada el equipo, normalmente es 3 pero debemos estar seguros
de ello, sobre todo cuando existen varios equipos SMA en la misma red.
PORT --> suele ser 502 por defecto, salvo que se haya modificado por alguna razón.
Registros a leer:
Hay definida una lista de registros para los SB en el diccionario sbRegs{} que se codifica en una matriz/tuple
smaDat.
El campo "name" contiene la etiqueta que define el registro a leer.
El campo "addr" contiene la dirección modbus del registro a leer. (No es necesario restar -1)
El campo "leng" contiene el número de registros que debemos leer para que nos de un valor válido.
   (comprobar la lista superior o la original de SMA para saber si son 2 (U32/S32) o 4 (U64)
El campo "unit" contiene la unidad del registro leido y se muestra la final de la línea impresa.

El programa consta del fichero test_sb.py y el módulo de 'clase' sma.py, que deben estar en la misma carpeta.
Inicialmente se leen los valores más importantes y además se graban en el fichero (datos_sma.txt) en la misma
carpeta donde tengamos el programa.

"""


import os
import time
from collections import namedtuple
# importamos modulo desde sma.py
import sma
from sma import convert2 as c2

# Registros

 
# Direccion TCP/IP para el equipo a testear
TCP_IP = '192.168.0.253' # aquí pones la IP del SMA
UNIT_ID = 3 # unidad modbus del equipo SMA (suele ser 3)
PORT=502

# definimos los diccionarios de conversion registros 30201 y 30217
sbstt={35:'Fallo',303:'Off',307:'Ok',455:'Alarma', 51:'Cerrado',311:'Abierto'}
#sbrele={51:'Cerrado',311:'Abierto'}

# definimos los registros que queremos acceder en el SB
sbRegs={}
smaDat=namedtuple('smaDat','name addr leng unit mult')
sbRegs[0]=smaDat("Estado:", 30201, 2, 'Stt', 0)
sbRegs[1]=smaDat("Conexión:", 30217, 2, 'on/off', 0)
sbRegs[2]=smaDat("Producción Total:", 30529, 2, 'kWh',0.001 ) # Convertido a Kwh
sbRegs[3]=smaDat("Producción Diaria:", 30535, 2,'kWh',0.001) # Convertido a Kwh
sbRegs[4]=smaDat("Potencia Actual:", 30775, 2,'W',0.01)
sbRegs[5]=smaDat("DC Amps:", 30769, 2,'A',0.001)
sbRegs[6]=smaDat("DC Volt:", 30771, 2,'V',0.001)
sbRegs[7]=smaDat("DC Watts:", 30773, 2,'W',0.01)
sbRegs[8]=smaDat("Temp. Interna:",34113,2,'°C', 1)
sbRegs[9]=smaDat("Frecuencia:",40135,2,'Hz', 1)

def save_data(reg_ini,data):
    f=open("datos_sma.txt","a")
    f.write("RegIni: " + str(reg_ini) + "\n")
    f.write(str(data) + "\n")
    f.close()

try:

    try:
        mbus = sma.mbusTCP(UNIT_ID, TCP_IP, PORT)
        mbus.openTCP()
    except:
        print ("error Iniciando proceso...")
        raise
        
    try:
        #leemos tabla de registros del SB 
        for i in range(0, len(sbRegs)):
            data = mbus.read_data(sbRegs[i].addr, sbRegs[i].leng)
            #data=[0x00,0xFA]
            Translate=c2()
            Translate.u16.h = data[1]
            Translate.u16.l = data[0]
            valor=Translate.uint32
            if i<2:
                unit=(sbstt.get(valor))                    
                print(sbRegs[i].name, unit)
                #save_data(sbRegs[i].name,valor, unit)
            else:
                print (sbRegs[i].name,valor * sbRegs[i].mult, sbRegs[i].unit )
                #save_data(sbRegs[i].name,valor * sbRegs[i].mult, sbRegs[i].unit )

    except:
        print ("error leyendo datos...")
        raise
        
finally:
    # desconectamos los sockets 
    print('\nCLOSING '+ TCP_IP)
    mbus.closeTCP()

    
