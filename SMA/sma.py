#!/usr/bin/python
# -*- coding: utf-8 -*-

# @module: sma.py 
# @description: Python Class to get data from a SMA unit via pymodbusTCP
#               Clase Python para tomar datos de un equipo SMA utilizando pymodbusTCP
# @autor: Pac0 Arriaza (JanusHL) (except indicated...)
# @created: 20/05/2019
# @license: free use of this module class if no changes in the copyright from the autors are made.       
#
#--------------------------------------------------------------------------

from pyModbusTCP.client import ModbusClient
import ctypes

import time
import sys


'''
 These classes/structures/unions, allow easy conversion between
 modbus 16bit registers and ctypes (a useful format)
 Copyright (c) 2017 stoberblog
'''

# Single register (16 bit) based types
class convert1(ctypes.Union):
    _fields_ = [("u16", ctypes.c_uint16),
                ("s16", ctypes.c_int16)]
    
# Two register (32 bit) based types
class x2u16Struct(ctypes.Structure):
    _fields_ = [("h", ctypes.c_uint16),
                ("l", ctypes.c_uint16)]
class convert2(ctypes.Union):
    _fields_ = [("float", ctypes.c_float),
                ("u16", x2u16Struct),
                ("sint32", ctypes.c_int32),
                ("uint32", ctypes.c_uint32)]
    
# Four register (64 bit) based types
class x4u16Struct(ctypes.Structure):
    _fields_ = [("hh", ctypes.c_uint16),
                ("hl", ctypes.c_uint16),
                ("lh", ctypes.c_uint16),
                ("ll", ctypes.c_uint16)]
class convert4(ctypes.Union):
    _fields_ = [("u16", x4u16Struct),
                ("sint64", ctypes.c_int64),
                ("uint64", ctypes.c_uint64)]

#--- end of copyrighted code -----------------------------


class mbusTCP:

    def __init__(self, ID, TCPaddress, PORT): #, TCPaddress

    # Modbus instance
    #debug=True (quitar cuando no sea necesario el modo debug)
        
        try:
            self.mb_device = ModbusClient(host=TCPaddress, port=PORT, timeout=10, debug=True, unit_id=ID)
            self.functionCode = 3 # Function Code
            self.dict = {}
        except:
            print (self.mb_device)
            #return mb_device.last_error()
            raise   
        
    def read_data(self, reg_ini, num_regs):
        try:
            data = self.mb_device.read_holding_registers(int(reg_ini), num_regs)
            return data
        except:    
            print (self.mb_device.last_error())
            #return mb_device.last_error()
            raise
            
    def openTCP(self):
        try:
            self.mb_device.open()
            #time.sleep(1)
        except:    
            print ("\nError abriendo conexión TCP...")
            
    def closeTCP(self):
        try:
            self.mb_device.close()
            time.sleep(1)
            
        except:    
            print ("\nError cerrando conexión TCP...")

###-----the two functions below are only for documentation purposes in how to read U32/U64 registers

    def device_read_U64(self, ini_reg):
        regs = self.mb_device.read_holding_registers(ini_reg-1, 4)
        Translate=convert4()
        Translate.u16.hh = regs[3]
        Translate.u16.hl = regs[2]
        Translate.u16.lh = regs[1]
        Translate.u16.ll = regs[0]
        return Translate.uint64
                 
    def device_read_U32(self, ini_reg):
        regs = self.mb_device.read_holding_registers(ini_reg-1, 2)
        Translate=convert2()
        Translate.u16.h = regs[1]
        Translate.u16.l = regs[0]
        return Translate.uint32

    
if __name__ == '__main__':
    mbus = mbusTCP(1, '192.168.20.41', 502) #sys.argv[1]
    mbus.openTCP()
    data = mbus.read_data(30201,2)
    mbus.closeTCP()
    
    print (data)
 
 
