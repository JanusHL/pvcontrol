#!/usr/bin/python
# -*- coding: utf-8 -*-

# buscador de puertos usb conectados para Raspberry PI
# 2019 - K@PG Design - JanusHL

""" Inicialmente desarrollé esta utilidad utilizando dmesg para conectar dos puertos USB al
    programa ControlFV. Pero existe un problema con dmesg y es que no devuelve el string
    del puerto cuando el log lleva varios dias por lo tanto la solución más aceptable es
    hacer un ls -l al directorio /sys/.... y buscar en el string del listado el puerto USB y su driver conectado
    
    Esta utilidad sirve para saber que puerto utiliza cada uno de los dispositivos y poder conectarlos
    desde otro programa sin errores cuando en un reinicio de la Rpi se cambian de lugar.
    
    chkport(driver) devueve el puerto /dev/ttyUSBx de un driver especifico, hay dos de ejemplo.
    he añadido la búsqueda inversa con chkdriver() que lista todos los puertos ttyUSBx y su driver asociado
    y devuelve un diccionario con los resultados.

"""
import subprocess

chkcp210="cp210x"
chkch341="ch341-uart"
dummy ="dummy"
command="ls -l /sys/class/tty/ttyUSB*/device/driver"
 
def chkport(driver):
# busca puerto activo para cada driver USB
    try:
        #msg= subprocess.check_output( "dmesg | grep -i " + driver, stderr=subprocess.STDOUT, shell=True)
        msg= subprocess.check_output( command, stderr=subprocess.STDOUT, shell=True)
        if msg.find(driver):
            pos= msg.rindex(driver)
            
        if pos !=-1:
            inip=pos - 75
            port= msg[inip:inip+7]
            return port
        else:
            print ("Puerto no encontrado...")
            return "none"   
    except:
        return "Error en subproceso..."
        
        
def chkdriver():
# busca driver activo para cada puertor USB
    try:

        msg= subprocess.check_output( command, stderr=subprocess.STDOUT, shell=True)
        i=0
        dicc={}
        pos=0
        while pos != -1:
            pos = msg.find('ttyUSB',pos + 8)
            port= msg[pos:pos+7]
            driver=msg[pos+75:pos+ 85]
            if "\n" in driver:
                driver=driver[:len(driver)-1]
            #print (pos, port, driver)
            if pos>1:
                key=port
                dicc[key] = set()
                dicc[key] = driver

        return dicc
            
    except:
        
        return "Error en subproceso..."
        
# ---------- Uso de las funciones----------------------------

print ("Puertos encontrados...", chkdriver ())
print ("Puerto " + chkcp210 + " en --> " + chkport(chkcp210))
print ("Puerto " + chkch341 + " en --> " + chkport(chkch341))

