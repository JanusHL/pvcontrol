#!/usr/bin/python
# -*- coding: utf-8 -*-

# module: classic.py 
# Python Class to get data from a Midnite Classic via Modbus-TCP
# Clase Python para tomar datos de un Midnite Classic via Modbus-TCP
# Pac0 Arriaza (Janus) - 18/04/2018
# 24/04/2018 - función closeSCK que cierra el socket TCP
#            - función get_dict que envia los datos en formato diccionario
#--------------------------------------------------------------------------

import socket
import struct
import time
import sys

# Registros

valor =['VBat', 'VPlaca', 'IBat', 'Kwh', 'Watt', 'Stat','IPlaca','LVoc','Res','MPS','AmpH', 'Temp']

TCP_PORT = 502
BUFFER_SIZE = 0

class mbusread:

    def __init__(self, TCPaddress):
        
        self.TCPport = TCPaddress
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sck.connect((TCPaddress, TCP_PORT))
        self.unitId = 1 # Unidad Modbus
        self.functionCode = 3 # Function Code
        self.startRegister = 4114 # Registro inicial (4115) - 1
        self.numRegister = 18 # Registros a leer
        self.dict = {}
        		
    def read_data(self):		
        try:
            # estructura paquete petición de datos
            req = struct.pack('>3H 2B 2H', 0, 0, 6, int(self.unitId), int(self.functionCode), int(self.startRegister), int(self.numRegister))
            self.sck.send(req)
         
            # Calculo la estructura y buffer de datos

            BUFFER_SIZE = (3*2) + (3*1) + (int(self.numRegister)*2)

            rec = self.sck.recv(BUFFER_SIZE)
            s = struct.Struct('>3H 3B 18H')
            data = s.unpack(rec)
            return data
        except:    
            print "error..."
    
    def closeSCK(self):
        try:
            #print('\nCLOSING SOCKET')
            time.sleep(1);
            self.sck.close()
        except:    
            print "\nError cerrando conexión TCP..."

    def get_dict(self):
        data = self.read_data()
        for i in range(6, 6+11):
            key = valor[i-6]
            self.dict[key] = set() # key
            value = data[i] # *0.10
            self.dict[key] = value

        sttchg = data[11]/256
        if sttchg>7:
            sttchg=8
        
        key = valor[5] # Stat
        self.dict[key] = set()
        self.dict[key] = sttchg
        key = valor[11] # Temp
        self.dict[key] = data[23]
        return self.dict
    
if __name__ == '__main__':
    mbus = mbusread(sys.argv[1])
    data = mbus.read_data()
    mbus.closeSCK()
    
# Print cabecera de datos (solo a efectos de debug)
    
    print("\nMODBUS PACKET HEADER")
    print(" Transaction Identifier : %s" %data[0])
    print(" Protocol Identifier : %s" %data[1])
    print(" Length : %s" %data[2])
    print(" Unit Identifier : %s" %data[3])
    print(" Function Code : %s" %data[4])
    print(" Byte Count : %s" %data[5])
 
    # Print valores de los registros
    print("\nREGISTER VALUES")
    for i in range(6, 6+11):
        currentRegister = str((i - 6) + int(4115)).zfill(2)
        print(" Register #%s %s: %s " %(currentRegister, valor[i-6],data[i]*0.10))
    