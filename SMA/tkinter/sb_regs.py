#!/usr/bin/python
# -*- coding: utf-8 -*-

# Sunny Boy - Modbus registers
# @name: sb_regs.py
# @autor: JanusHL
# @date: 26/05/2019
#------------------------------------
# Use this file to add or modify modbus registers you want to read from device
# The list is read sequentially and shown in the main window in the same format.
# parameters in the list:
# name: label to shown
# address: modbus addres to read
# lenght: number of registers to read (U32/S32=2) (U64=4)
# unit: label that match the value read
# mult: factor to convert value
#------------------------------------
# name address lenght unit mult
sb_regs = [
["Estado:", 30201, 2, 'Stt', 0],
["Conexión:", 30217, 2, 'on/off', 0],
["Producción Total:", 30529, 2, 'kWh',0.001],
["Producción Diaria:", 30535, 2,'kWh',0.001],
["Potencia Actual:", 30775, 2,'W',0.01],
["DC Amps:", 30769, 2,'A',0.001],
["DC Volt:", 30771, 2,'V',0.001],
["DC Watts:", 30773, 2,'W',0.01],
["Temp. Interna:",34113,2,'°C', 1],
["Frecuencia:",40135,2,'Hz', 1]
]
