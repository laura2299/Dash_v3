from constantes import style
MODES={
    "LINEAL":"Lineal",
    "RADAR":"Radar",
    "POLAR":"Polar",
    "TORTA":"Torta"
}
TITULOS={
    "EMPRESA":"empresa",
    "AREA":"area",
    "TIPO":"tipo",
    "SISTEMA":"sistema",
    "NODO":"nodo",
    "KV":"kv",
    "CENTRAL":"central",
    "UNIDAD":"unidad"
}


from tkinter import *
from tkinter import ttk
from functools import partial
from datetime import date, datetime
import calendar




class miCalendario1:
    def __init__(self,master,padre):
        self.padre = padre
        self.master=master
        self.master.title("Calendario")
        self.master.geometry("230x200+650+50")
        self.master.config(bg="lavender")
        self.master.resizable(0,0)
        # obtengo la fecha actual
        today = date.today()
        m=today.month # tipo numerico (1,2,3,,,12) obt el mes actual, para el combobox (1,2,3)
        a=today.year # tipo numerico,(2019,2020,2021) obt el año actual, para el combobox ()

        # creo combox para los meses
        lMes=("Enero","febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiebre","Octubre",
              "Noviembre","Diciembre")
        self.cmbMes=ttk.Combobox(self.master, values=lMes, width=10, state="readonly",
                                  font=("arial",10,"bold"))
        self.cmbMes.place(x=10,y=5)
        self.cmbMes.current(m-1) # defaul el mes actual en el combobox, current da el index 0,1,2,3,4
        
        # lleno la lista con los años para el combobox de los años
        lAno=[] # este arreglo recibira, el rango de años habilitados
        for c in range(1980,today.year+1):
            lAno.append(c) # corgo la lista con el rango de años desde a
        #print(lAno)    

        # creo los titulos
        lbl2=Label(self.master,text="Año :", bg="lavender", font=("arial",10,"bold")).place(x=110,y=5)
        # creo combobox para los años
        self.cmbAno=ttk.Combobox(self.master, values=lAno, state="readonly",
                                 font=("arial",10,"bold"), width=5)
        self.cmbAno.place(x=155,y=5)
        self.cmbAno.set(a) # hago como opc, predefinida en año actual
        
        # creo la caja de texto para mostrar el calendario
        self.txt=Text(self.master, width=24, height=8,bg="lightblue", bd=3, padx=5)
        self.txt.place(x=10,y=30)
        
        # llamo la funcion para que muestre x primera vez todo actualizado                                              
        self.MostrarCalendario(self.cmbMes,self.cmbAno,self.txt)
                                                    
        #creao el botton para mostrar el calendario
        btn=Button(self.master,text="Actualice",bg="skyblue", font=("arial",9,"bold"), 
                command=lambda: self.MostrarCalendario(self.cmbMes,self.cmbAno,self.txt))
        btn.place(x=12,y=168)
        
        btnD=Button(self.master,text="Selec Dia",bg="skyblue", font=("arial",9,"bold"), 
                command=lambda: self.DiaSelecionado(self.cmbMes,self.cmbAno,self.txt))
        btnD.place(x=150,y=168)
        
    
    # la funcion q muestra el calendario
    def MostrarCalendario(self, mBox, aBox,txt):
        self.mBox=mBox
        self.aBox=aBox
        self.txt=txt

        self.mesBox=self.mBox.current()+1
        self.anoBox=int(self.aBox.get()) # viene tipo txt, paso a numerico, hay controlar esto
    
        
        self.txt.config(state=NORMAL)
        cal=calendar.month(self.anoBox,self.mesBox)
        self.txt.delete(0.0, END)
        self.txt.insert(INSERT, cal)
        self.txt.config(state=DISABLED)

    def DiaSelecionado(self, mBox, aBox,txt):
        try:
            if self.txt.get(SEL_FIRST, SEL_LAST).isdigit() and len(self.txt.get(SEL_FIRST, SEL_LAST)) <=2:
                print( "Texto Seleccionado: '%s'" % self.txt.get(SEL_FIRST, SEL_LAST) )
                rDia=self.txt.get(SEL_FIRST, SEL_LAST)
                rMes=str(self.mBox.current()+1)
                rAno=self.aBox.get()
                xFecha=rDia+"/"+rMes+"/"+rAno
                self.rFecha=xFecha
                print(self.rFecha)
                # llamo al metodo  para asignar la fecha escogida en el calendario
                #self.padre.fechaIEntry.
                self.padre.fechaIEntry.set(self.rFecha)
                #xf=principalV2.FechaCalendario(self.rFecha) 
                # la instancia da esto: NameError: name 'principalV2' is not defined

        except TclError:
            print( "Seleccione el dia" )


class miCalendario2:
    def __init__(self,master,padre):
        self.padre = padre
        self.master=master
        self.master.title("Calendario")
        self.master.geometry("230x200+650+50")
        self.master.config(bg="lavender")
        self.master.resizable(0,0)
        # obtengo la fecha actual
        today = date.today()
        m=today.month # tipo numerico (1,2,3,,,12) obt el mes actual, para el combobox (1,2,3)
        a=today.year # tipo numerico,(2019,2020,2021) obt el año actual, para el combobox ()

        # creo combox para los meses
        lMes=("Enero","febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiebre","Octubre",
              "Noviembre","Diciembre")
        self.cmbMes=ttk.Combobox(self.master, values=lMes, width=10, state="readonly",
                                  font=("arial",10,"bold"))
        self.cmbMes.place(x=10,y=5)
        self.cmbMes.current(m-1) # defaul el mes actual en el combobox, current da el index 0,1,2,3,4
        
        # lleno la lista con los años para el combobox de los años
        lAno=[] # este arreglo recibira, el rango de años habilitados
        for c in range(1980,today.year+1):
            lAno.append(c) # corgo la lista con el rango de años desde a
        #print(lAno)    

        # creo los titulos
        lbl2=Label(self.master,text="Año :", bg="lavender", font=("arial",10,"bold")).place(x=110,y=5)
        # creo combobox para los años
        self.cmbAno=ttk.Combobox(self.master, values=lAno, state="readonly",
                                 font=("arial",10,"bold"), width=5)
        self.cmbAno.place(x=155,y=5)
        self.cmbAno.set(a) # hago como opc, predefinida en año actual
        
        # creo la caja de texto para mostrar el calendario
        self.txt=Text(self.master, width=24, height=8,bg="lightblue", bd=3, padx=5)
        self.txt.place(x=10,y=30)
        
        # llamo la funcion para que muestre x primera vez todo actualizado                                              
        self.MostrarCalendario(self.cmbMes,self.cmbAno,self.txt)
                                                    
        #creao el botton para mostrar el calendario
        btn=Button(self.master,text="Actualice",bg="skyblue", font=("arial",9,"bold"), 
                command=lambda: self.MostrarCalendario(self.cmbMes,self.cmbAno,self.txt))
        btn.place(x=12,y=168)
        
        btnD=Button(self.master,text="Selec Dia",bg="skyblue", font=("arial",9,"bold"), 
                command=lambda: self.DiaSelecionado(self.cmbMes,self.cmbAno,self.txt))
        btnD.place(x=150,y=168)
        
    
    # la funcion q muestra el calendario
    def MostrarCalendario(self, mBox, aBox,txt):
        self.mBox=mBox
        self.aBox=aBox
        self.txt=txt

        self.mesBox=self.mBox.current()+1
        self.anoBox=int(self.aBox.get()) # viene tipo txt, paso a numerico, hay controlar esto
    
        
        self.txt.config(state=NORMAL)
        cal=calendar.month(self.anoBox,self.mesBox)
        self.txt.delete(0.0, END)
        self.txt.insert(INSERT, cal)
        self.txt.config(state=DISABLED)

    def DiaSelecionado(self, mBox, aBox,txt):
        try:
            if self.txt.get(SEL_FIRST, SEL_LAST).isdigit() and len(self.txt.get(SEL_FIRST, SEL_LAST)) <=2:
                print( "Texto Seleccionado: '%s'" % self.txt.get(SEL_FIRST, SEL_LAST) )
                rDia=self.txt.get(SEL_FIRST, SEL_LAST)
                rMes=str(self.mBox.current()+1)
                rAno=self.aBox.get()
                xFecha=rDia+"/"+rMes+"/"+rAno
                self.rFecha=xFecha
                print(self.rFecha)
                # llamo al metodo  para asignar la fecha escogida en el calendario
                #self.padre.fechaIEntry.
                self.padre.fechaFEntry.set(self.rFecha)
                #xf=principalV2.FechaCalendario(self.rFecha) 
                # la instancia da esto: NameError: name 'principalV2' is not defined

        except TclError:
            print( "Seleccione el dia" )

class grafico:
    def __init__(self,master,padre):
        self.padre = padre
        self.master=master
        self.master.title("Grafico")
        self.master.geometry("700x500+650+50")
        self.master.config(bg="lavender")
        self.master.resizable(0,0)

        
        optionsFrame=Frame(self.master)
        optionsFrame.configure(background=style.COMPONENT
                               )
        optionsFrame.pack(
            side=TOP,
            fill=BOTH,
            expand=True,
            padx=22,
            pady=11
        )
        import os
        import csv
        import matplotlib.pyplot as plt
        import numpy as np
        archivo_txt = "C:\\Users\\PC LAURA\\Desktop\\proyecto sellin\\ficheros\\Datos Almacenados\\BTUDO\\0264"  # Ruta del archivo de texto

        # Listas para almacenar los elementos
        arrays = []

        # Leer el archivo de texto
        with open(archivo_txt, "r") as file:
            # Recorrer cada línea del archivo
            for linea in file:
                elementos = linea.strip().split(',')
                arrays.append(elementos)
        tamanio=15
        valores =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        valores=np.empty(tamanio)
        for i in range(len(arrays)):
            subarray = arrays[i]
            valores[0]+=subarray[12]
            valores[1]+=subarray[13]
            valores[2]+=subarray[14]
            valores[3]+=subarray[15]
            valores[4]+=subarray[16]
            valores[5]+=subarray[17]
            valores[6]+=subarray[18]
            valores[7]+=subarray[19]
            valores[8]+=subarray[20]
            valores[9]+=subarray[21]
            valores[10]+=subarray[22]
            valores[11]+=subarray[23]
            valores[12]+=subarray[24]
            valores[13]+=subarray[25]
            valores[14]+=subarray[26]
        etiquetas= ["H1","H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12","H13","H14","H15"]
        
        plt.bar(etiquetas, valores)

        # Añadir etiquetas a las barras
        for i in range(len(etiquetas)):
            plt.text(i, valores[i], str(valores[i]), ha='center', va='bottom')

        # Ajustar el diseño del gráfico
        plt.xlabel('Horas')
        plt.ylabel('Cantidad total')
        plt.title('Suma por horas')
        plt.xticks(rotation=45)
        plt.show()



