#!/usr/bin/python
# -*- coding: utf-8 -*-

# Modbus para DDS238 energy meter
# JanusHL - 26/01/2019
# portions of this module are taken from internet free programs
#----------------------------------------------------------------
# Frame format:
#	Read command（function code 03）
### Send Frame
#   Meter ID 1 byte
#   Function code 1 byte
#   Register address 2 byte
#   Data number 2 byte
#   CRC 2 byte
### Receive frame
#   Meter ID 1 byte
#   Function code 1 byte
#   Data lenght n  1 byte
#   Data area n byte
#   CRC 2 byte


import serial
import time

class DDS:

    def __init__(self, com="/dev/ttyUSB1", timeout=2.0):

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
    
#--------------------------------
#modbus func code 03 = Read registers

    def f03Modbus(self, slave,start, NumOfRegs):
        # function to read modbus registers in DDS
        # NumOfRegs=3 (voltage, current, power)
        Function=3
        msg = [0 for i in range(8)]

        #index0 = Address Modbus slave
        msg[0] = slave #1
        #index1 = Modbus Function
        msg[1] = 3
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

        reading=''
        self.ser.write("".join(chr(h) for h in msg))
        resp = 5 + (2 * NumOfRegs)
        
        time.sleep(0.2)
        while self.ser.inWaiting() > 0:
            reading += self.ser.read(1)
        
        response = [0 for i in range(len(reading))]
        for i in range(0, len(reading)):
            response[i] = ord(reading[i])
       
        if len(response)==resp:
            CRCok = self.CRCvalid(response)
            #CRCok = True
            if CRCok & (response[0]==slave) & (response[1]==Function):
            #Byte Count in index 3 = responseFunc3[2]
            #Number of Registers = byte count / 2 = responseFunc3[2] / 2
                registers = ((response[2] / 2)& 0xFF)
                values = [0 for i in range(registers)]
                for i in range(0, len(values)):
                #Data Hi and Registers1 from Index3
                    values[i] = response[2 * i + 3]
                #Move to Hi
                    values[i] <<= 8
                #Data Lo and Registers1 from Index4
                    values[i] += response[2 * i + 4]
                    negatif = values[i]>>15
                    if negatif==1:values[i]=values[i]*-1
                return values
        return()

    def close(self):
        self.ser.close()

    def readAll(self):
        #Read Registers
        ArrayValue = self.f03Modbus(1,12,3) # slave,init, num registers
        #print "ArrayValue: " , len(ArrayValue)
        if len(ArrayValue)>0:
            return ArrayValue
        else:
            return(0,0,0)
                
#--Main Program

if __name__ == "__main__":
    sensor = DDS()
    try:
        print("Checking...")
        Data=sensor.readAll()
        #print (sensor.readAll())
        print "Voltage: ", Data[0]/10
        print "Current: ", float(Data[1])/100
        print "Power: ", Data[2]

    finally:
        sensor.close()		
