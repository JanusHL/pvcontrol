# Tools for Raspberry PI

I will be uploading in this section some python tools that I'm using in my RPi.

*test_ports.py

This is a good tool if you need to know what driver is associated to each /dev/ttyUSBx port.
I use the function chkport(driver) in order to know what USB port is using two devices I've conected
and override to pass data via command line to the main program. This is udefull when the program runs as a service.

![alt text](https://raw.githubusercontent.com/janusHL/pvcontrol/master/tools/test_ports.jpg)

