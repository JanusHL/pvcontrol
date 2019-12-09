#!/usr/bin/python
# -*- coding: utf-8 -*-

# Modbus RS485-RTU para Grid Inverter Growatt
# portions of this module are taken from internet free programs
# JanusHL - 09/12/2019
# 
# This class is similar to others that query modbus data
# Growatt returns data in bytes, conversion here differs fron other classes
# look at  the code for comments
#----------------------------------------------------------------
# Frame format:
#	Read command（function code 04 - read input registers）
### Send Frame
#   Inverter ID 1 byte (0x01)
#   Function code 1 byte (0x04)
#   Register address 2 byte (hi - lo)
#   Data number 2 byte (hi -lo)
#   CRC 2 byte
### Receive frame
#   Inverter ID 1 byte
#   Function code 1 byte
#   Data lenght n  1 byte
#   Data area n  bytes
#   CRC 2 byte


import serial
import time
import struct

byte2int = lambda b: b

class Growatt:

    def __init__(self, com, timeout=2.0):

        self.ser = serial.Serial(
            port=com,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout = timeout)
            
        if self.ser.isOpen():
            self.ser.close()
            self.ser.open()

    def CRCcal(self, msg):
        #CRC (Cyclical Redundancy Check) Calculation
        CRC = 0xFFFF
        CRCHi = 0xFF
        CRCLo = 0xFF
        CRCLSB = 0x00
        for i in range(0, len(msg)-2,+1):
            CRC = (CRC ^ msg[i])
            for j in range(0, 8):
                CRCLSB = (CRC & 0x0001);
                CRC = ((CRC >> 1) & 0x7FFF)

                if (CRCLSB == 1):
                    CRC = (CRC ^ 0xA001)
        CRCHi = ((CRC >> 8) & 0xFF)
        CRCLo = (CRC & 0xFF)
        return (CRCLo,CRCHi)

#CRC Validation
    def CRCvalid(self, resp):
        CRC = self.CRCcal(resp)
        if (CRC[0]==resp[len(resp)-2]) & (CRC[1]==resp[len(resp)-1]):return True
        return False  
    
#------------------------------------------
#modbus function 04 = Read Input registers

    def f04Modbus(self, slave,start, NumOfRegs):
        # function to read modbus registers in DDS
        # NumOfRegs=3 (voltage, current, power)
        Function=4
        msg = [0 for i in range(8)]

        #index0 = Address Modbus slave
        msg[0] = slave #1
        #index1 = Modbus Function
        msg[1] = Function
        #index2 = Address Hi
        msg[2] = ((start >> 8)& 0xFF)
        #index3 = Address Lo
        msg[3] = (start & 0xFF)
        #index4 = Registers to read Hi
        msg[4] = ((NumOfRegs >> 8)& 0xFF)
        #index5 = Registers to read Lo
        msg[5] = (NumOfRegs & 0xFF)

        CRC = self.CRCcal(msg)

        #index6= CRC Lo
        msg[len(msg) - 2] = CRC[0]#CRCLo
        #index7 = CRC Hi
        msg[len(msg) - 1] = CRC[1]#CRCHi

    # slave communication

        response=''
        data=[]
        bseq = bytes(msg)    # python 3.x
        self.ser.write(bseq) # python 3.x
        #self.ser.write("".join(chr(h) for h in msg)) # python 2.x
        resp = 5 + (2 * NumOfRegs)
        time.sleep(0.2)
         
        while self.ser.inWaiting() > 0:
            temp = self.ser.read(1)
            data.append(temp)
            
        response=b"".join(data) # convert to bytes
        
        if len(response)==resp:
            CRCok = self.CRCvalid(response)
            if CRCok & (response[0]==slave) & (response[1]==Function):
                return response 
        return()

    def close(self):
        self.ser.close()

    def readAll(self):
        #Read Registers
        ArrayValue = self.f04Modbus(1,0,15) # slave,init, num registers

        if len(ArrayValue)>0:
            return self.decode(ArrayValue) # return just real values
        else:
            return(0,0,0,0,0,0)
                    

    def decode(self, data):
        #    Decode a register response packet
        #    :param data: The request to decode
    
        byte_count = byte2int(data[2])
        registers = []
        for i in range(3, byte_count + 1, 2):
            registers.append(struct.unpack('>H', data[i:i + 2])[0])  

        return registers    
                  
#--Main Program

if __name__ == "__main__":
    
    #sensor = Growatt('/dev/ttyUSB0')
    sensor = Growatt('COM1:')
    

    try:
        print("Checking...")
        Data1=sensor.readAll()
        print (Data1)
        #print (sensor.readAll())
        print ("Status: ", Data1[0])
        print ("In Power: ", Data1[2]/10)
        print ("Volt: ", Data1[3]/10)
        print ("Current: ", Data1[4]/10)
        print ("Out Power: ", Data1[12]/10)
        print("Freq:", Data1[13] / 100 )# Divide by 100


    finally:
        sensor.close()

