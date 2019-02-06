# -*- coding: utf-8 -*-

import machine, time, bme280, ssd1306
from umqtt.simple import MQTTClient

# NodeMCU pins used
# D1 (Pin5) -> SCL
# D2 (Pin4) -> SDA

def lee_bme280(i2c):

    bme = bme280.BME280(i2c=i2c,address=0x76)
    temp,pa,hum = bme.values 
    data=[temp, pa, hum]
    return data # values list


def do_connect():
    import network

    SSID = 'SSID_Router'
    PASSWORD = 'password'

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Network configuration:', sta_if.ifconfig())

   
# main
# connecting to local LAN    
do_connect()

#config mqtt change SERVER, USER, PASSWORD and TOPIC to mach your own data
SERVER = "192.168.20.xxx"
PORT = 1883
USER = "user"
PASSWORD = "pasword"
TOPIC = b'kapgdom/Meteo' # change it to match your desire topic
#CLIENT_ID = ubinascii.hexlify(machine.unique_id())
CLIENT_ID = machine.unique_id()
keepalive = 60 
c = MQTTClient(CLIENT_ID, server=SERVER, port=PORT, user=USER, password=PASSWORD, keepalive=keepalive)

###pinScl      = 22  #ESP8266 GPIO5 (D1)
###pinSda      = 18  #ESP8266 GPIO4 (D2)
addrOled    = 60  #0x3c
addrBME280  = 118 #0x76
hSize       = 64  # display heigh in pixels
wSize       = 128 # display width in pixels

oledIsConnected = False
bmeIsConnected  = False
    
# initializing I2C bus
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
# scanning i2c bus for connected devices
print('Scan i2c bus...')
devices = i2c.scan()
if len(devices) == 0:
    print("Device i2c unavaible...")
else:
    print('i2c devices -->:',len(devices))
    for device in devices: 
        if device == addrOled:
            oledIsConnected = True
        if device == addrBME280:
            bmeIsConnected = True
        print(device)
# main loop
while True:
    if bmeIsConnected:
        data=lee_bme280(i2c)
        if data:
            print("BME280 values:")
            print ("Temp Ext: %s" % data[0])
            print ("PAtm: %s" % data[1])
            print ("Hum Ext: %s" %data[2])
            c.connect()
            c.publish(TOPIC+'/TExte', str(data[0]))
            c.publish(TOPIC+'/PA', str(data[1]))
            c.publish(TOPIC+'/HExte', str(data[2]))
            c.disconnect()

        if oledIsConnected:
            oled = ssd1306.SSD1306_I2C(wSize, hSize, i2c, addrOled)
            oled.fill(0)
            if bmeIsConnected:
                oled.text("T.Ext. "+round(data[0],1), 0, 0)
                oled.text("PAtm. "+int(data[1]), 0, 10)
                oled.text("Hum. "+round(data[2],1), 0, 20)
                oled.text("KaPG-PV - 2018",0, 40)
                oled.show()
            else:   
                oled.text("BME KO", 0, 0)
                oled.show()
        else:
            print('! No i2c display')            

    time.sleep(60) #datos cada 60 segundos
    

