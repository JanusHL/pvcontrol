#!/usr/bin/python
# -*- coding: utf-8 -*-
# bmvsimple.py - Class --> bmv, para leer el monitor BMV7xx
# # 28/05/2018 - JanusHL - modificado para ControlFV
# Lo simple si bueno 10 veces bueno...

import os, serial, sys

class bmv:

    def __init__(self, serialport):
        if serialport!=None and serialport!='':
            self.serialport = serialport
            self.ser = serial.Serial(serialport, 19200, timeout=10)
            self.crlf = '\r\n'
            self.tab = '\t'
            self.key = ''
            self.value = ''
            self.dict = {}
            self.cont = 0
        else:
            raise Exception ('/dev/ttyUSB0 - No conectado')

    def ser_close(self):
        self.ser.close()

    def read_data_single(self):
        self.dict={}

        try:
            while True:
                data = self.ser.readline()
                data=data.strip('\r\n')
                data=data.split('\t')
                if data[0]=="V":
                    self.dict["V"]=data[1]
                    self.cont+=1
                elif data[0]=="I":
                    self.dict["I"]=data[1]
                    self.cont+=1
                elif data[0]=="SOC":
                    self.dict["SOC"]=data[1]
                    self.cont+=1
                elif data[0]=="P":
                    self.dict["P"]=data[1]
                    self.cont+=1
                #else:
                    # si se quieren procesar todos los datos solo se necesita esto
                    #self.key=data[0]
                    #self.dict[self.key]=data[1]
                 #  if data[0]=="Checksum":
                 #      return self.dict
 
                if self.cont==4:
                    self.cont=0
                    return self.dict
                
        except:
            print "bmvsimple - Error en datos..."
            return None
            #self.ser.close()
    
               
if __name__ == '__main__':
    
    if len(sys.argv) < 1:
        print "Se necesita el periférico en el argumento"
        print "Ejemplo :"
        print "     python vedirect.py /dev/ttyUSB0)"
        exit()
        
    ve = bmv(sys.argv[1])
    datos = ve.read_data_single()
    print datos
    
    
