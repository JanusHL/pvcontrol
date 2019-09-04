#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
# smatron.py Beta v1
# 2019 - JanusHL
# 
# 

import os, sys, time
import time
from collections import namedtuple
import webbrowser
import threading

# importamos modulo desde sma.py
import sma
from sma import convert2 as c2

try:
    # Python 2.x
    from Tkinter import *
    import ttk
    import tkFont
    import ScrolledText as tkst
    print('2.x')
except ImportError:
    # Python 3.x
    from tkinter import *
    from tkinter import ttk
    from tkinter.font import Font
    import tkinter.scrolledtext as tkst
    print('3.x')

# Direccion TCP/IP para el equipo a testear
TCP_IP = '192.168.0.253' # aquí pones la IP del SMA
UNIT_ID = 3 # unidad modbus del equipo SMA (suele ser 3)
PORT=502

class Aplicacion():
    
    
    def __init__(self):
        # ventana principal
        self.raiz = Tk()
        
        # dimensiones de la pantalla para centrar la pantalla y dialogos
        self.width = round(self.raiz.winfo_screenwidth(),0)
        self.height = round(self.raiz.winfo_screenheight(),0)
        
        winx = int(self.width/2-300)
        winy = int(self.height/2-300)
        
        tamypos = '600x420+'+str(winx)+ \
                  '+'+ str(winy)
        self.raiz.geometry(tamypos)
        self.raiz.resizable(0,1)
        self.raiz.title('SMAtron beta 0.1')

        # barra de menú
        barramenu = Menu(self.raiz)
        self.raiz['menu'] = barramenu

        # menu principal
        menu1 = Menu(barramenu, tearoff=0)
        self.menu2 = Menu(barramenu, tearoff=0)
        menu3 = Menu(barramenu, tearoff=0)
        barramenu.add_cascade(menu=menu1, label='Archivo')
        barramenu.add_cascade(menu=self.menu2, label='Opciones')
        barramenu.add_cascade(menu=menu3, label='Ayuda')

        menu1.add_command(label='Salir', command=self.f_exit,
                          underline=0, accelerator="Ctrl+Q",
                          compound=LEFT)

        # menu opciones (tipos de equipos)


        # menu ayuda
        menu3.add_command(label='Web', command=self.f_web)
        menu3.add_command(label="Acerca de",
                          command=self.about_box)
        # DECLARAR TECLAS DE ACCESO RAPIDO:
        #self.raiz.bind("<Control-a>", lambda event: self.f_conectar())
        self.raiz.bind("<Control-g>", lambda event: self.save_filecmd())
        self.raiz.bind("<Control-q>", lambda event: self.f_exit())     

         
        self.lbl1 = ttk.Label(self.raiz, width=16, font=('Arial', '14', 'italic'),relief=RAISED,text="Parámetro:")
        self.lbl1.grid(column=0, row=0, padx=5, sticky=SW)
        self.lbl2 = ttk.Label(self.raiz, width=12, font=('Arial', '14', 'italic'),relief=RAISED,text="Valor:")
        self.lbl2.grid(column=1, columnspan=2,row=0, sticky=SW)

        try:
            fontt = Font(family="Arial", size=10, weight='bold')
        except:
            fontt = tkFont.Font(family="Arial", size=10, weight='bold')
        try:
            self.fontr = Font(family="Arial", size=10)
        except:
            self.fontr = tkFont.Font(family="Arial", size=10)
        
        self.sbRegs={}
        smaDat=namedtuple('smaDat','name addr leng unit mult')
        self.labels=[]

        #Registros a leer en fichero externo sd_regs.py
        from sb_regs import sb_regs
        i=0
        for row in sb_regs:
            self.sbRegs[i]=smaDat(row[0], row[1], row[2], row[3], row[4])
            self.labels.append(ttk.Label(self.raiz, width=25, font=fontt, relief=GROOVE, text=row[0]))
            self.labels[i].grid(column=0, row=i+1, padx=5, sticky=SW)
            i=i+1
            
         # botón enviar comando
        self.btn_cmd = ttk.Button(self.raiz, text='Solicitar datos', command=self.cmd_send)
        self.btn_cmd.grid(row=i+1, column=0, sticky=S)
        
        self.enabled = IntVar()
        self.enabled.set(0)
        self.chk_btn = ttk.Checkbutton(self.raiz, text='auto 5 segs.', variable=self.enabled)
        self.chk_btn.grid(row=i+2, column=0, sticky=S)
        self.logo = PhotoImage(file='sb1.png')
        self.logo = self.logo.subsample(4, 4)
        
        # boton salir de la app lo he anulado, pero no he quitado el codigo
        #btn_exit = ttk.Button(self.raiz, text='Exit', 
        #           command=self.f_exit)
        #btn_exit.grid(row=4, column=0,  pady=15, sticky=S)

        # creamos una Frame para las cajas de texto con scroll
        #txt_frm = ttk.Frame(self.raiz, width=50, height=40, fill='blue')

        # que se pueda estirar 
        #txt_frm.grid_rowconfigure(0, weight=1)
        #txt_frm.grid_columnconfigure(0, weight=2)
        #txt_frm.grid(row=i+3, column=0, padx=10)
        
        self.lbl3 = ttk.Label(self.raiz, text="Log:")
        self.lbl3.grid(row=i+3, column=0, padx=2, pady=2, sticky=SW)
        
        # datos del dispositivo - scrolledText widget
        self.Tdata = tkst.ScrolledText(self.raiz, height=6, width=40, wrap='word')
        self.Tdata.grid(row=i+4, columnspan=3, padx=5, pady=5, sticky=NW )

                     
        self.raiz.mainloop()
#---------------------------------------------        
    def crc_opt(self):
         return self.var.get()

    def about_box(self):
        self.dialogo = Toplevel()
        posx = int(self.width/2-150)
        posy = int(self.height/2-100)
        
        tamypos = '300x300+'+str(posx)+ \
                  '+'+ str(posy)
        self.dialogo.geometry(tamypos)
        self.dialogo.resizable(0,0)
        titulo = "Acerca de SMAtron"
        self.dialogo.title(titulo)

        marco1 = ttk.Frame(self.dialogo, padding=(10, 10, 10, 10),
                           relief=RAISED)
        marco1.pack(side=TOP, fill=BOTH, expand=True)

        logo = PhotoImage(file='fvcontrol.png')
        #logo = logo.subsample(4, 4)
        imagen1 = ttk.Label(marco1, image=logo, anchor="center")
        imagen1.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)

        lbl1= Label(marco1,
                      text="SMAtron Beta v1.a ")
        lbl1.pack(side=TOP, padx=10)
        lbl2= Label(marco1,
                      text="2019 JanusHL")
        lbl2.pack(side=TOP, padx=10)

        # Define el botón 'Cerrar' que cuando sea
        # presionado cerrará (destruirá) la ventana 
        # 'self.dialogo' llamando al método
        # 'self.dialogo.destroy'

        boton = ttk.Button(self.dialogo, text='Cerrar',
                           command=self.dialogo.destroy)
        boton.pack(side=BOTTOM, padx=20, pady=20)
        self.raiz.wait_window(self.dialogo)

    # selecciona equipo
    def f_cambiaropc(self):
        #Habilitar opción 'Guardar' al elegir alguna opción
        self.menu2.entryconfig("Guardar", state="normal")

    # Abrir página web en navegador Internet
    def f_web(self):

      pag1 = 'https://adnsolar.eu/'
      webbrowser.open_new_tab(pag1)

            
    def log_clear(self):
        self.Tlog.delete(1.0, END)
        self.Tlog.update()
        self.Tdata.delete(1.0, END)
        self.Tdata.update()

    # salir de la app
    def f_exit(self):
 #       self.f_guardarconfig()
        self.raiz.destroy()

# envia comando del combobox al dispositivo /dev/hidraw
    def cmd_send(self):

        # bonus!!!
        
        self.imagen1 = ttk.Label(self.raiz, image=self.logo, anchor="center")
        self.imagen1.grid(column=3, row=1, rowspan=10, sticky="se")
        self.thread = threading.Thread(target=self.worker)
        self.thread.start()
        
    def worker(self):
        # muestreo de datos
        # definimos los diccionarios de conversion registros 30201 y 30217
        sbstt={35:'Fallo',303:'Off',307:'Ok',455:'Alarma',51:'Cerrado',311:'Abierto'}
        #sbrele={51:'Cerrado',311:'Abierto'}
        # definimos los registros que queremos acceder en el SB y los añadimos 
        self.lbdat=[]
        self.lbunit=[]

        try:

            try:
                #if stt !=None:
                msg="Iniciando proceso..."
                #else:
                #    msg="error de conexión TCP..."
                self.Tdata.insert(END, msg)
                self.Tdata.see(END)
                mbus = sma.mbusTCP(UNIT_ID, TCP_IP, PORT)
                stt=mbus.openTCP()
                if stt == None: sys.exit()
                
            except:
                msg="error de conexión TCP..."
                self.Tdata.insert(END, msg)
                self.Tdata.see(END)
                #print ("error Iniciando proceso...")
                raise
                
            n=0
            automode=1   
            while automode==1: #and stt !=None:
                   
                try:
            #leemos tabla de registros del SB 
                    for i in range(0, len(self.sbRegs)):
                        data = mbus.read_data(self.sbRegs[i].addr, self.sbRegs[i].leng)
                        #data=[0x00,0xFA]
                        Translate=c2()
                        Translate.u16.h = data[1]
                        Translate.u16.l = data[0]
                        valor=Translate.uint32
                        if i<2:
                            unit=(sbstt.get(valor))                    
                            print(self.sbRegs[i].name, unit)
                            #save_data(sbRegs[i].name,valor, unit)
                        else:
                            print (self.sbRegs[i].name,valor * self.sbRegs[i].mult, self.sbRegs[i].unit )
                            unit=valor * self.sbRegs[i].mult
                            #save_data(sbRegs[i].name,valor * sbRegs[i].mult, sbRegs[i].unit )
                        
                        self.lbdat.append(ttk.Label(self.raiz, width=8, font=self.fontr, anchor=E,relief=SUNKEN,text=str(unit)))
                        self.lbdat[i].grid(column=1, row=i+1, sticky="nw")
                         
                        self.lbunit.append(ttk.Label(self.raiz, width=8, font=self.fontr, anchor=W,text=self.sbRegs[i].unit))
                        self.lbunit[i].grid(column=2, row=i+1, sticky="w")
                         

                except:
                    print ("error leyendo datos...")
                    raise

                automode=self.enabled.get()
                n+=1
                self.Tdata.insert(END, '\nLectura nº --> '+ str(n))
                self.Tdata.see(END)

                if automode==0: # salimos del loop si no estamos en automode
                     break
                else:
                    self.btn_cmd.state(['disabled'])
                    
                time.sleep(5)
            
        finally:
            # desconectamos los sockets 
            #print('\nCLOSING '+ TCP_IP)
            self.Tdata.insert(END, '\nCLOSING '+ TCP_IP)
            self.Tdata.see(END)
            self.btn_cmd.state(['!disabled'])
            mbus.closeTCP()

#----------------------------------------------------------------
### main app ###
#----------------------------------------------------------------
def main():
    mi_app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()
