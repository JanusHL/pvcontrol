# New tkinter graphical version

![alt text](https://raw.githubusercontent.com/janusHL/pvcontrol/master/SMA/tkinter/smaon_image.jpg)
Not tested

Registers now outside the program in the sb_regs.py file. Modify to match your requirements...

You need to copy in the same folder you have the text #sma.py module:
* smatron.py
* sb_regs.py
* sb1.png
* fvcontrol.png

# Usage:

* Edit sb_regs.py if you need other registers to be shown
* start the program with #$ python3 smatron.py
* The main window shows a list of parameters to read
* press the button <Solicitar datos> and wait the response to appear in the right
* If <auto 5 segs> is checked the program read de device every five seconds
* Log textbox shows messages and errors
* if you are in "auto" mode, uncheck de button to close connection before exit.
* Exit the program using the Menu or Ctrl+Q


JanusHL 27/05/2019
