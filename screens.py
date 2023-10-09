import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfiles
from tkinter import messagebox
import os
from constantes import style
from datetime import timedelta
from datetime import datetime as dt
import datetime

import numpy as np
import pandas as pd
from os import listdir
import shutil
import time
from shutil  import rmtree
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import jpype
import asposecells
jpype.startJVM()
from asposecells.api import Workbook,TxtLoadOptions
from tkinter import filedialog



filtros_form_grafico=[]

form_combobox = []

form_tabla = ""

def mostrar_tabla(nombre_tabla,columnas):
    # Obtener la lista de archivos en la carpeta "vtudo"
    
    carpeta = "Cache\Cache_Texto"
    archivos = os.listdir(carpeta)

    # Crear una ventana de Tkinter
    ventana = tk.Toplevel()
    ventana.title('Tabla de datos')
    ventana.geometry('800x600')
    
     # Crear el marco (frame) para contener la tabla
    options_frame = ttk.Frame(ventana)
    options_frame.pack(
        side =tk.TOP
        ,
        fill='both', expand=True)
    # Crear una tabla usando el widget Treeview
    tabla = ttk.Treeview(options_frame)
    #for widget in container.winfo_children():
    #   widget.destroy()
    # Crear una tabla usando el widget Treeview
    #tabla = ttk.Treeview(container)

    tk.Label(
            options_frame,
            text="Tabla "+nombre_tabla,
            justify=tk.CENTER,
            **style.STYLE2
            ).pack(
            side = tk.TOP,
            fill= tk.BOTH,
            #expand=True,
            padx= 22,
            pady= 11
            )

    # Crear una barra de desplazamiento horizontal
    scrollbar_horizontal = ttk.Scrollbar(options_frame, orient='horizontal', command=tabla.xview)
    scrollbar_horizontal.pack(fill='x', side='bottom')
    
    scrollbar_vertical = ttk.Scrollbar(options_frame, orient='vertical', command=tabla.yview)
    scrollbar_vertical.pack(fill='y', side="right")

    # Configurar la asociación entre la barra de desplazamiento y la tabla
    tabla.configure(xscrollcommand=scrollbar_horizontal.set)
    tabla.configure(yscrollcommand=scrollbar_vertical.set)
    # Leer y agregar los datos de cada archivo a la tabla
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r',encoding="utf-8") as archivo_txt:
                contenido = archivo_txt.read()
                filas = contenido.split('\n')
                datos = [fila.split(';;') for fila in filas]

                # Configurar encabezados de columna para el primer archivo
                linea_nombres= columnas_tabla(nombre_tabla)
                linea_nombres= linea_nombres[1:]
                if not tabla['columns']:
                    tabla['columns'] = tuple(range(len(linea_nombres)))
                    for i, encabezado in enumerate(linea_nombres):
                        tabla.heading(i, text=linea_nombres[i], anchor=tk.CENTER)

                # Agregar los datos a la tabla
                for fila in datos:
                    tabla.insert('', 'end', values=tuple(fila))

    # Empacar la tabla en la ventana
    tabla.pack(side = tk.LEFT,
            fill= tk.BOTH,
            expand=True
            )
    options_frame2 = ttk.Frame(ventana)
    options_frame2.pack(
        side =tk.TOP,
        fill='both', expand=True)
    
    tk.Label(
                options_frame2,
                text="Datos a considerar en la tabla:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.BOTH,
                #expand=True,
                padx= 22,
                pady= 11
                )
    #poner los datos por los que se busco :
    i=1
    for filtro_form in filtros_form_grafico:
        if type(filtro_form) == type(columnas):
            a=filtro_form[0]
            
            b=filtro_form[1]
            
        else:
            if filtro_form.get() != "":
                tk.Label(
                options_frame2,
                text="Dato "+str(i)+" "+filtro_form.get(),
                justify=tk.CENTER,
                **style.STYLE3
                ).pack(
                side = tk.TOP,
                fill= tk.BOTH,
                #expand=True,
                padx= 22,
                pady= 11
                )
                i+=1

def columnas_tabla(tabla):
    #print(tabla)
    with open("Ficheros/Datos_tablas/tablas.txt",encoding="utf-8") as archivo:
        for linea in archivo:
            linea=linea.strip("\n")
            linea=linea.split(",")
            #print("TABLA:")
            #print(linea[0])
            #print(tabla)
            if linea[0]== tabla:
                return linea

def devolver_floats(columnas):
    tipo_de_datos=tipos_datos(columnas)
    floats=[]
    for i,columna in enumerate (columnas):
        if(tipo_de_datos[i]=="FLOAT"):
            floats.append(columna)
    
    if(columnas[0]=="EVENTOS"):
        floats.append("Ahs-DEhs")
    return floats

def devolver_cadenas(columnas):
    
    cadenas=[]
    tipos=tipos_datos(columnas)
    for i,tipo in enumerate (tipos):
        #print(columnas[i])
        if(tipos[i] =="VALORES_UNICOS" ):
            cadenas.append(columnas[i])
    
    print("devolver cadenas:")
    print(cadenas)
    return cadenas

def detectar_tabla(columnas):
    tablas=[]
    with open("Ficheros/Datos_tablas/tablas.txt",encoding="utf-8") as archivo:
        for linea in archivo:
            linea=linea.strip("\n")
            linea=linea.split(",")
            if linea[1:] == columnas:
                tablas.append(linea[0])
    return tablas

def tipos_datos(columnas):
    #print("tipos datos:")
    #print(columnas)
    tipos = [0]*len(columnas)
    matriz = []
    with open("Ficheros/Datos_tablas/tipos_datos.txt",encoding="utf-8") as archivo:
        for linea in archivo:
            linea=linea.strip("\n")
            linea=linea.split(",")
            matriz.append(linea)
    c=1
    for columna in columnas[1:]:
        for tipo in matriz:
            if str(columna) in tipo:
                tipos[c]=tipo[0]
                break
        c+=1
    return tipos

def filtros_tablas(columnas, tipos):
    global filtros_form_grafico

    #print("Filtros Tablas")
    #print(tipos)
    tabla = columnas[0]
    num_datos_para_grafico=0
    nro_columnas=len(columnas)-1
    filtro_datos = [0]*(nro_columnas)
    columnas_grafico=[]
    lista_año = []
    lista_mes = []
    c=0
    sw_año = True
    sw_mes = False
    for filtro_form in filtros_form_grafico:
        if type(filtro_form) == type(columnas):
            if tipos[c] == "FECHA":
                #try:
                a = time.strptime(filtro_form[0].get(), "%d/%m/%Y")
                b = time.strptime(filtro_form[1].get(), "%d/%m/%Y")
                #print(filtro_form[0].get(),filtro_form[1].get())
                #print(a, b)
                #print(tabla)
                año_1 = a.tm_year
                año_2 = b.tm_year
                mes_1 = a.tm_mon
                mes_2 = b.tm_mon

                l_años = listdir("Ficheros/Tablas/"+tabla)
                l_mes = listdir("Ficheros/Tablas/"+tabla+"/"+l_años[0])

                l_aux = l_mes[0]
                len_aux = l_aux.count(",") +1
                l_m_a = []

                caux = 0
                m_a = []
                #m_a = ""
                for i in range(1,13):
                    m_a.append(i)
                    #m_a+=str(i)
                    caux+=1
                    if caux == len_aux:
                        caux = 0
                        l_m_a.append(m_a)
                        m_a = []
                        #m_a = ""
                l_mes = l_m_a
                #print(l_m_a)

                # Si es necesario guardar archivos por dia
                #l_dia = listdir("Ficheros/Tablas/"+tabla+"/"+l_años[0]+"/"+l_mes[0])
                
                #print(l_años)
                #print(l_mes)
                #print(dia_1, dia_2)

                lista_año = []
                lista_mes = []
                if a == b:
                    filtro_datos[c]="Igual Fecha"
                    if str(año_1) in l_años:
                        lista_año = [año_1]
                    else: 
                        sw_año = False
                    #print(l_mes)
                    for grupo_mes in l_mes:
                        if mes_1 in grupo_mes:
                            lista_mes = [grupo_mes]
                        else:
                            sw_mes = False
                else:
                    filtro_datos[c]="Entre Fechas"
                    if año_1 == año_2:
                        if str(año_1) in l_años:
                            lista_año = [año_1]
                        else: 
                            sw_año = False
                    else:
                        lista_año = []
                        for año in l_años:
                            if int(año) >= año_1 and int(año) <= año_2:
                                lista_año.append(año)
                        if lista_año == []:
                            sw_año = False

                    if mes_1 == mes_2:
                        for grupo_mes in l_mes:
                            if int(mes_1) in grupo_mes:
                                lista_mes.append(grupo_mes)
                                break
                        if lista_mes == []:
                            sw_mes = False
                    else:
                        lista_mes = []
                        #print(mes_1,mes_2)
                        for grupo_mes in l_mes:
                            #print(mes, grupo_mes)
                            for mes in grupo_mes:
                                if mes_1 <= mes and mes <= mes_2:
                                    lista_mes.append(grupo_mes)
                                    break
                        if lista_mes == []:
                            sw_mes = False
                #print(lista_año, sw_año)
                #print(lista_mes, sw_mes)
            elif tipos[c] == "AÑO":
                a = int(filtro_form[0].get())
                b = int(filtro_form[1].get())
                l_años = listdir("Ficheros/Tablas/"+tabla)
                #print(a, b)
                #print(l_años)
                if a == b:
                    filtro_datos[c]="Igual F"
                    if str(a) in l_años:
                        lista_año = [a]
                    else: 
                        lista_año = []
                        sw_año = False
                    #print("Lista Año:", lista_año)
                else:
                    filtro_datos[c]="Entre"
                    lista_año = []
                    for año in l_años:
                        if a <=int(año) and int(año) <= b:
                            lista_año.append(año)
                    if lista_año == []:
                        lista_año = []
                        sw_año = False
                    #print("Lista Año:", lista_año)
            elif tipos[c] == "MES" and sw_año:
                l_mes = listdir("Ficheros/Tablas/"+tabla+"/"+str(lista_año[0]))
                #print(l_mes)
                l_aux = l_mes[0]
                len_aux = l_aux.count(",") +1
                l_m_a = []

                caux = 0
                m_a = []
                #m_a = ""
                for i in range(1,13):
                    m_a.append(i)
                    #m_a+=str(i)
                    caux+=1
                    if caux == len_aux:
                        caux = 0
                        l_m_a.append(m_a)
                        m_a = []
                        #m_a = ""
                l_mes = l_m_a

                a = int(filtro_form[0].get())
                b = int(filtro_form[1].get())
                #print(a,b)
                if a == b:
                    filtro_datos[c]="Igual F"
                    for grupo_mes in l_mes:
                        if int(a) in grupo_mes:
                            lista_mes = [grupo_mes]
                            break
                    if lista_mes == []:
                        sw_mes = False
                    #print(lista_mes)
                else:
                    filtro_datos[c]="Entre"
                    lista_mes = []
                    #print(mes_1,mes_2)
                    for grupo_mes in l_mes:
                        #print(mes, grupo_mes)
                        for mes in grupo_mes:
                            if a <= int(mes) and int(mes) <= b:
                                lista_mes.append(grupo_mes)
                                break
                    if lista_mes == []:
                        sw_mes = False
            
            elif tipos[c] == "DIA":
                a = int(filtro_form[0].get())
                b = int(filtro_form[1].get())

                if a == b:
                    filtro_datos[c]="Igual F"
                else:
                    filtro_datos[c]="Entre"
        else:
            if filtro_form.get() == "":
                filtro_datos[c]="Pasar"
            else:
                #print(tipos[c])
                if tipos[c] == "CADENAS":
                    filtro_datos[c]="Igual"
                    #print(filtro_form.get(), type(filtro_form.get()))
                elif tipos[c] == "FLOAT":
                    if filtro_form.get()==1:
                        filtro_datos[c]="Sumar"
                        num_datos_para_grafico+=1
                        columnas_grafico.append(columnas[c+1])
                    else:
                        filtro_datos[c]="Pasar"
                elif tipos[c] == "VALORES_UNICOS":
                    filtro_datos[c]="Decodificar" 
                    #print("linea DEcodificada")
                elif tipos[c] == "DESCRIPCIÓN" or tipos[c] == "DESCRIPCION":
                    filtro_datos[c] = "DESCRIPCIÓN"
                elif tipos[c] == "HORAS":
                    filtro_datos[c] = "Horas" 
        c+=1
    #print(filtro_datos)
    if sw_año:
        lista_mes_aux = []
        #print(lista_mes)
        for grupo in lista_mes:
            grup = ""
            if len(grupo)<2:
                grup = str(grupo[0])
            else:
                for num in grupo[:-1]:
                    grup+=str(num)+","
                grup+=str(grupo[-1])
            lista_mes_aux.append(grup)
        #print(lista_mes_aux)
        lista_mes = lista_mes_aux
        #print(lista_año, lista_mes)
    else:
        messagebox.showerror('Error', 'No se encontro archivos con ese año')
    #if len(lista_mes_aux) == 0:
    #    messagebox.showerror('Error', 'No se encontro archivos con ese mes')
    return filtro_datos, lista_año, lista_mes

def sacar_Dat_Uni_tabla(tabla):
    archivo_unico = open("Datos Almacenados/Valores Unicos/"+tabla+".txt", "r", encoding="utf-8")
    columnas_unicas = []
    for linea in archivo_unico:
        linea=linea.strip("\n")
        linea=linea.split(";")
        columnas_unicas.append(linea)
    archivo_unico.close()
    return columnas_unicas

def filtrar_datos(tabla, ubi_cache, tipos, filtro_datos, nro_columnas, lista_año, lista_mes):
    rmtree("Cache/"+ubi_cache)   
    os.mkdir("Cache/"+ubi_cache)
    #print("Estos es filtrar")
    val_unicos = sacar_Dat_Uni_tabla(tabla)
    sw_decodificar=False
    lista_graficos = sacar_tablas_graficos()
    #print(filtro_datos)
    sw_Lleno = True
    sw_Error = False
    if tabla not in lista_graficos:    
        if "VALORES_UNICOS" in tipos:
            sw_decodificar=True
        num_datos_para_grafico = filtro_datos.count("Sumar")
        res=[0]*num_datos_para_grafico
        res_aux=[0]*num_datos_para_grafico
        sw=True
        for txt in listdir("Ficheros/Tablas/"+tabla):
            nom_Cache="cache"+txt
            file_cache = open("Cache/"+ubi_cache+"/"+nom_Cache, "w", encoding="utf-8")
            with open("Ficheros/Tablas/"+tabla+"/"+txt,"r",encoding="utf-8") as archivo:
                for linea in archivo:
                    linea=linea.strip("\n")
                    linea_aux=linea
                    linea=linea.split(";;")
                    sw=True
                    aux_c=0
                    #print(linea, len(linea), nro_columnas)
                    for i in range(nro_columnas):
                        filtro = filtro_datos[i]
                        casilla=linea[i]
                        if filtro=="Pasar":
                            #print("Paso")
                            pass
                        elif filtro=="Igual":
                            if filtros_form_grafico[i].get() != casilla:
                                sw=False
                                #print("No es Igual")
                                break
                        elif filtro=="Igual F":
                            #print(casilla)
                            if filtros_form_grafico[i][0].get() != casilla:
                                sw=False
                                #print("No es Igual Fecha")
                                break
                        elif filtro=="Entre":
                            filtros = filtros_form_grafico[i]
                            casilla= int(casilla)
                            #print(casilla)
                            inicial = int(filtros[0].get())
                            final = int(filtros[1].get())
                            if casilla >= inicial and casilla <= final:
                                pass
                            else:
                                sw=False
                                #print("No entre")
                                break
                        elif filtro == "Decodificar":
                            linea_uni = val_unicos[i]
                            val = filtros_form_grafico[i].get()
                            #print(linea_uni, val,linea_uni.index(val), casilla)
                            
                            if casilla != str(linea_uni.index(val)):
                                sw=False
                                break
                        elif filtro=="Sumar":
                            res_aux[aux_c]=float(casilla)
                            aux_c+=1
                        elif filtro == "DESCRIPCIÓN":
                            filtros = filtros_form_grafico[i]
                            casilla = casilla.split(" ")
                            if filtro in casilla:
                                pass
                            else:
                                sw = False
                                break
                        else:
                            sw_Error = True
                            #messagebox.showwarning('Peligro', 'Error al ejecutar filtros')
                            #print("Error al ejecutar filtros")
                            #print(tabla, txt)
                            #print(linea)
                    if sw:
                        
                        for i in range(num_datos_para_grafico):
                            res[i]+=res_aux[i]
                    
                        if sw_decodificar:
                            linea_aux = decodificar_linea(linea_aux,tipos,val_unicos)
                        if linea_aux != "":
                            sw_Lleno = False
                        file_cache.write(linea_aux+'\n')
            file_cache.close()

    else:
        if "VALORES_UNICOS" in tipos:
            sw_decodificar=True
        num_datos_para_grafico = filtro_datos.count("Sumar")
        res=[0]*num_datos_para_grafico
        res_aux=[0]*num_datos_para_grafico
        #print(lista_año,lista_mes)
        for año in lista_año:
            año= str(año)
            #print(año)
            
            for mes in listdir("Ficheros/Tablas/"+tabla+"/"+año):
                #print(mes)
                for grupo_mes in lista_mes:
                    #print(grupo_mes, mes, año)
                    if mes in grupo_mes:
                        #print("si")
                        for txt in listdir("Ficheros/Tablas/"+tabla+"/"+año+"/"+mes):
                            nom_Cache="c-"+año+"-"+mes+"-"+txt
                            file_cache = open("Cache/"+ubi_cache+"/"+nom_Cache, "w", encoding="utf-8")
                            with open("Ficheros/Tablas/"+tabla+"/"+año+"/"+mes+"/"+txt,"r",encoding="utf-8") as archivo:
                                for linea in archivo:
                                    linea=linea.strip("\n")
                                    linea_aux=linea
                                    linea=linea.split(";;")
                                    sw=True
                                    aux_c=0
                                    #print(linea)
                                    for i in range(nro_columnas):
                                        filtro = filtro_datos[i]
                                        casilla=linea[i]
                                        if filtro=="Pasar":
                                            #print("Paso")
                                            pass
                                        elif filtro=="Sumar":
                                            res_aux[aux_c]=float(casilla)
                                            aux_c+=1
                                            #print("sumar")
                                        elif filtro=="Igual":
                                            if filtros_form_grafico[i].get() != casilla:
                                                sw=False
                                                #print("No es Igual")
                                                break
                                        elif filtro=="Igual F":
                                            #print(casilla)
                                            #print(filtros_form_grafico[i][0].get())
                                            if int(filtros_form_grafico[i][0].get()) != int(casilla):
                                                sw=False
                                                #print("No es Igual Fecha")
                                                break
                                        elif filtro=="Igual Fecha":
                                            #print(casilla)
                                            #print(filtros_form_grafico[i][0].get())
                                            if filtros_form_grafico[i][0].get() != casilla:
                                                sw=False
                                                #print("No es Igual Fecha")
                                                break
                                        elif filtro=="Entre":
                                            filtros = filtros_form_grafico[i]
                                            casilla= int(casilla)
                                            inicial = int(filtros[0].get())
                                            final = int(filtros[1].get())
                                            if casilla >= inicial and casilla <= final:
                                                pass
                                            else:
                                                sw=False
                                                #print("No entre")
                                                break
                                        elif filtro=="Entre Fechas":
                                            filtros = filtros_form_grafico[i]
                                            casilla= time.strptime(casilla, "%d/%m/%Y")
                                            inicial = time.strptime(filtros[0].get(), "%d/%m/%Y")
                                            final = time.strptime(filtros[1].get(), "%d/%m/%Y")
                                            if casilla >= inicial and casilla <= final:
                                                pass
                                            else:
                                                sw=False
                                                #print("No entre Fechas")
                                                break
                                        elif filtro == "Decodificar":
                                            linea_uni = val_unicos[i]
                                            val = filtros_form_grafico[i].get()
                                            #print(linea_uni, val,linea_uni.index(val), casilla)
                                            
                                            if casilla != str(linea_uni.index(val)):
                                                sw=False
                                                break
                                        else:
                                            #print(filtro)
                                            #messagebox.showerror('Error', 'Error al ejecutar filtros')
                                            #print("Error al ejecutar filtros")
                                            #print(tabla, txt)
                                            #print(linea)
                                            sw_Error = True
                                    if sw:
                                        for i in range(num_datos_para_grafico):
                                            res[i]+=res_aux[i]
                                        if sw_decodificar:
                                            #print(linea_aux)
                                            #print(tipos)
                                            #print(val_unicos)
                                            linea_aux = decodificar_linea(linea_aux, tipos, val_unicos)
                                        if linea_aux != "":
                                            sw_Lleno = False
                                        
                                        file_cache.write(linea_aux+'\n')

                            file_cache.close()
    if sw_Lleno:
        messagebox.showinfo('Resultado Busqueda', 'No se encontró ningun dato')
    if sw_Error:
        messagebox.showerror('Error', 'Error al ejecutar filtros')
    
def Mostrar_filtros_datos(columnas,tipos):
    tipos=tipos[1:]
    tabla = columnas[0]
    filtro_datos, lista_año, lista_mes = filtros_tablas(columnas, tipos)
    nro_columnas=len(columnas)-1
    ubi_cache = "Cache_Texto"
    filtrar_datos(tabla, ubi_cache, tipos, filtro_datos, nro_columnas, lista_año, lista_mes)

    mostrar_tabla(tabla,columnas)

def form_llenar2(container, tabla):
    global filtros_form_grafico, form_tabla
    form_tabla=tabla
    filtros_form_grafico=[]
    for widget in container.winfo_children():
        widget.destroy()
    
    columnas = columnas_tabla(tabla)
    tipos=tipos_datos(columnas)
    val_uni = sacar_Dat_Uni_tabla(tabla)
    #print(columnas, tipos)
    titulo_formulario = tk.StringVar()
    titulo_formulario.set(tabla)

    lab = tk.Label(container, text="Formulario "+tabla,justify=tk.CENTER,
                **style.STYLE2).pack(side = tk.TOP,
                fill= tk.X,  pady=5, padx=10)
    #lab = tk.Label(container, text="").grid(column=0,row=1, columnspan=5)
    col_cad=0
    fila=4
    fila_F=5
    col_flo=0
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    mes = date.strftime("%m")
    #dia = date.strftime("%d")

    

    FrameAux_esp=tk.Frame(container, pady=10).pack()

    #FrameSam=tk.Frame(container)
    #FrameSam.configure(background=style.BACKGROUND, pady=5)
    #FrameSam.columnconfigure(0, weight=2)
    #FrameSam.columnconfigure(1, weight=1)
    #FrameSam.columnconfigure(2, weight=2)
    #FrameSam.columnconfigure(3, weight=1)
    #FrameSam.columnconfigure(4, weight=2)
    #FrameSam.columnconfigure(5, weight=1)
    #FrameSam.columnconfigure(6, weight=2)
    #FrameSam.columnconfigure(7, weight=1)
    #FrameSam.pack()

    #panel2 = tk.Canvas(container)
    #panel2.config(background="#F9F9F9", height="400", width="1000")
    #panel2.pack(side="left", fill="y")

    #scroll_vertical = tk.Scrollbar(panel2, orient='vertical', command=panel2.yview)
    #scroll_vertical.pack(side="left", fill="y")

    #panel2.configure(yscrollcommand=scroll_vertical.set)
    #panel2.bind("<Configure>", lambda e: panel2.configure(scrollregion=panel2.bbox("all")))

    

    #seg_frame = tk.Frame(panel2)
    FrameSam=tk.Frame(container)
    FrameSam.configure(background=style.BACKGROUND, pady=10, width="100")
    FrameSam.columnconfigure(0, weight=2)
    FrameSam.columnconfigure(1, weight=1)
    FrameSam.columnconfigure(2, weight=2)
    FrameSam.columnconfigure(3, weight=1)
    FrameSam.columnconfigure(4, weight=2)
    FrameSam.columnconfigure(5, weight=1)
    FrameSam.columnconfigure(6, weight=2)
    FrameSam.columnconfigure(7, weight=1)
    
    
    FrameValUni = tk.Frame(container)
    FrameValUni.configure(background=style.BACKGROUND, height=30, pady=10,width="100")
    FrameValUni.columnconfigure(0, weight=1)
    FrameValUni.columnconfigure(1, weight=1)
    FrameValUni.columnconfigure(2, weight=1)
    FrameValUni.columnconfigure(3, weight=1)
    FrameValUni.columnconfigure(4, weight=1)
    FrameValUni.columnconfigure(5, weight=1)
    
    
    #panel2.create_window((0,0), window=FrameSam, anchor="nw", width="200")
    i_cad=0
    aux_col = 0
    aux_fila = 0

    aux_val_col = 0
    aux_val_fila = 0
    #i_float=0
    for i in range(len(tipos)):
        sw_Cad=False
        sw_Flo=False
        
        match tipos[i]:
            
            case "FECHA":
                FrameFecha=tk.Frame(container)
                FrameFecha.configure(background=style.BACKGROUND, width=100)
                FrameFecha.pack(
                side=tk.TOP,
                fill=tk.X,
                #expand=True,
                padx=10,
                pady=3,
                ) 
                a=[]
                entry_fecha_ini=tk.StringVar()
                
                label = tk.Label(FrameFecha, text = columnas[i]+"INICIO" , font = ('calibre',8,'bold')).pack(side=tk.LEFT,fill=tk.X, ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,)
                ent = tk.Entry(FrameFecha,textvariable=entry_fecha_ini).pack(side=tk.LEFT,fill=tk.X,expand=True, ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,)
                entry_fecha_fin=tk.StringVar()
                label1 = tk.Label(FrameFecha, text = columnas[i]+"FIN" , font = ('calibre',8,'bold')).pack(side=tk.LEFT,fill=tk.X, ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,)
                ent1 = tk.Entry(FrameFecha,textvariable=entry_fecha_fin).pack(side=tk.LEFT,fill=tk.X,expand=True, ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,) 
                a.append(entry_fecha_ini)
                a.append(entry_fecha_fin)
                filtros_form_grafico.append(a)
            case "AÑO":
                FrameFecha=tk.Frame(container)
                FrameFecha.configure(background=style.BACKGROUND,width=100)
                FrameFecha.pack(
                side=tk.TOP,
                fill=tk.X,
                #expand=True,
                padx=22,
                pady=3,
                ) 

                b=[]
                entry_año_ini=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    #expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                ent2 = tk.Entry(FrameFecha, textvariable=entry_año_ini)
                ent2.insert(0,year)
                ent2.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                entry_año_fin=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    #expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                ent7 = tk.Entry(FrameFecha, textvariable=entry_año_fin)
                ent7.insert(0,year)
                ent7.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                b.append(entry_año_ini)
                b.append(entry_año_fin)
                filtros_form_grafico.append(b)
            case "MES":
                FrameFecha=tk.Frame(container)
                FrameFecha.configure(background=style.BACKGROUND,width=100)
                FrameFecha.pack(
                side=tk.TOP,
                fill=tk.X,
                #expand=True,
                padx=22,
                pady=3,
                ) 
                d=[]
                entry_mes_ini=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                ent3 = tk.Entry(FrameFecha,textvariable=entry_mes_ini,)
                ent3.insert(0,"01")
                ent3.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                entry_mes_fin=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                ent8 = tk.Entry(FrameFecha,textvariable=entry_mes_fin,)
                ent8.insert(0,mes)
                ent8.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                d.append(entry_mes_ini)
                d.append(entry_mes_fin)
                filtros_form_grafico.append(d)
            case "DIA":
                FrameFecha=tk.Frame(container)
                FrameFecha.configure(background=style.BACKGROUND,width=100)
                FrameFecha.pack(
                side=tk.TOP,
                fill=tk.X,
                #expand=True,
                padx=22,
                pady=3,
                ) 
                c=[]
                entry_dia_ini=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    #expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                ) 
                ent4 = tk.Entry(FrameFecha, textvariable=entry_dia_ini)
                ent4.insert(0,"1")
                ent4.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                entry_dia_fin=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    #expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                ) 
                ent10 = tk.Entry(FrameFecha, textvariable=entry_dia_fin)
                ent10.insert(0,"31")
                ent10.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                c.append(entry_dia_ini)
                c.append(entry_dia_fin)
                filtros_form_grafico.append(c)           
            case "CADENAS":
                sw_Cad=True
                
                if aux_col == 8:
                    aux_col = 0
                    aux_fila += 1

                entry_cad=tk.StringVar()
                label = tk.Label(FrameSam, text = columnas[i] , font = ('calibre',8,'bold')).grid(column=aux_col, row=aux_fila,
                    padx= 3,
                    pady= 3,
                    ipady=2,
                    ipadx=5
                )
                aux_col += 1 
                caja_texto=tk.Entry(FrameSam, textvariable=entry_cad).grid(column=aux_col, row=aux_fila,
                    padx= 3,
                    pady= 3,
                    ipady=2,
                    ipadx=5
                )
                filtros_form_grafico.append(entry_cad)
                aux_col+=1
            case "FLOAT":
                entry_cad=tk.StringVar()
                filtros_form_grafico.append(entry_cad)
            case "VALORES_UNICOS":
                if aux_val_col == 6:
                    aux_val_col = 0
                    aux_val_fila += 1
                    
                l_aux = val_uni[i-1]
                entry_cad=tk.StringVar()
                label = tk.Label(FrameValUni, text = columnas[i] , font = ('calibre',10,'bold')).grid(column=aux_val_col,row=aux_val_fila,
                    padx= 20,
                    pady= 5,
                    ipady=5,
                    ipadx=14)
                lista_opciones = ttk.Combobox(FrameValUni,textvariable=entry_cad)
                lista_opciones['values'] = l_aux[1:]
                lista_opciones['state'] = 'readonly'
                lista_opciones.bind("<<ComboboxSelected>>",elemento_seleccionado)
                aux_val_col+=1
                lista_opciones.grid(column=aux_val_col,row=aux_val_fila,padx= 20,
                    pady= 5,
                    ipady=5,
                    ipadx=15)
                aux_val_col+=1
                form_combobox.append(lista_opciones)
                filtros_form_grafico.append(entry_cad)
                sw_Cad=True
        if sw_Cad:
            col_cad+=2
            if col_cad==6:
                col_cad=0
                fila+=1
                fila_F=fila+1
        
        if sw_Flo:
            col_flo+=1
            if col_flo==6:
                col_flo=0
                fila_F+=1
    
    Frameboton = tk.Frame(container)
    Frameboton.configure(background=style.BACKGROUND)
    boton_enviar=tk.Button(Frameboton, text="Mostrar tabla", command=lambda: Mostrar_filtros_datos(columnas,tipos)).pack(
                side =tk.LEFT,
                fill=tk.X,
                padx=22,
                pady=11
                )
    FrameSam.pack()
    FrameValUni.pack()
    Frameboton.pack()
    boton_exportar=tk.Button(container, text="Exportar Datos", command=lambda: Exportar_datos(columnas,tipos,container)).pack(
                side =tk.LEFT,
                fill=tk.X,
                padx=22,
                pady=11
                )
    
#form llenar para graficos
def form_llenar(container, tabla):
    global filtros_form_grafico
    filtros_form_grafico=[]
    for widget in container.winfo_children():
        widget.destroy()
    
    columnas = columnas_tabla(tabla)
    tipos=tipos_datos(columnas)
    val_uni = sacar_Dat_Uni_tabla(tabla)
    #print(columnas, tipos)
    titulo_formulario = tk.StringVar()
    titulo_formulario.set(tabla)

    lab = tk.Label(container, text="Formulario "+tabla,justify=tk.CENTER,
                **style.STYLE2).pack(side = tk.TOP,
                fill= tk.X,  pady=5, padx=10)
    #lab = tk.Label(container, text="").grid(column=0,row=1, columnspan=5)
    col_cad=0
    fila=4
    fila_F=5
    col_flo=0
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    mes = date.strftime("%m")
    #dia = date.strftime("%d")

    FrameVal=tk.Frame(container)
    FrameVal.configure(background=style.BACKGROUND
                    )
    FrameVal.pack(
    side=tk.TOP,
    fill=tk.X,
    #expand=True,
    padx=22,
    pady=3,
    ) 
    FrameVal2=tk.Frame(container)
    FrameVal2.configure(background=style.BACKGROUND
                    )
    FrameVal2.pack(
    side=tk.TOP,
    fill=tk.X,
    #expand=True,
    padx=22,
    pady=3,
    ) 

    FrameCad=tk.Frame(container)
    FrameCad.configure(background=style.BACKGROUND
                    )
    FrameCad.pack(
    side=tk.TOP,
    fill=tk.X,
    #expand=True,
    padx=22,
    pady=3,
    ) 
    FrameCad2=tk.Frame(container)
    FrameCad2.configure(background=style.BACKGROUND
                    )
    FrameCad2.pack(
    side=tk.TOP,
    fill=tk.X,
    #expand=True,
    padx=22,
    pady=3,
    )  
    FrameCad3=tk.Frame(container)
    FrameCad3.configure(background=style.BACKGROUND
                    )
    FrameCad3.pack(
    side=tk.TOP,
    fill=tk.X,
    #expand=True,
    padx=22,
    pady=3,
    )
    FrameFloat1=tk.Frame(container)
    FrameFloat1.configure(background=style.BACKGROUND
                    )
    FrameFloat1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    FrameFloat2=tk.Frame(container)
    FrameFloat2.configure(background=style.BACKGROUND
                    )
    FrameFloat2.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    FrameFloat3=tk.Frame(container)
    FrameFloat3.configure(background=style.BACKGROUND
                    )
    FrameFloat3.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    FrameFloat4=tk.Frame(container)
    FrameFloat4.configure(background=style.BACKGROUND
                    )
    FrameFloat4.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    i_cad=0
    i_float=0
    i_val=0
    def elegir_graficas():
        #print("colunas")
        #print(columnas)
        if(columnas[0]=="EVENTOS"):
            #print("eventos")
            elige_eventos(container,columnas,tipos)

        elif(columnas[0]=="OPERATIONMARGIN"):
            #print("operationmargin")
            graficar_operationmargin(container,columnas,tipos)
        elif(columnas[0]=="EMBALSES"):
            #print("Embalses")
            elige_embalses(container,columnas,tipos)
        


        else:
            tipo_grafica(container,columnas,tipos)

    for i in range(len(tipos)):
        sw_Cad=False
        sw_Flo=False
        #today = date.today()
        
        match tipos[i]:
            
            case "FECHA":
                FrameFecha=tk.Frame(container)
                FrameFecha.configure(background=style.BACKGROUND
                                        )
                FrameFecha.pack(
                side=tk.TOP,
                fill=tk.X,
                #expand=True,
                padx=22,
                pady=3,
                ) 
                a=[]
                entry_fecha_ini=tk.StringVar()
                
                label = tk.Label(FrameFecha, text = columnas[i]+"INICIO" , font = ('calibre',10,'bold')).pack(side=tk.LEFT,fill=tk.X, ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,)
                ent = tk.Entry(FrameFecha,textvariable=entry_fecha_ini)
                ent.insert(0,"03/02/2023")
                ent.pack(side=tk.LEFT,fill=tk.X,expand=True, ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,)
               
                entry_fecha_fin=tk.StringVar()
                label1 = tk.Label(FrameFecha, text = columnas[i]+"FIN" , font = ('calibre',10,'bold')).pack(side=tk.LEFT,fill=tk.X, ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,)
                ent1 = tk.Entry(FrameFecha,textvariable=entry_fecha_fin)
                ent1.insert(0,"29/09/2023")
                ent1.pack(side=tk.LEFT,fill=tk.X,expand=True, ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,) 
                
                
                a.append(entry_fecha_ini)
                a.append(entry_fecha_fin)
                filtros_form_grafico.append(a)
            case "AÑO":
                FrameFecha=tk.Frame(container)
                FrameFecha.configure(background=style.BACKGROUND
                                        )
                FrameFecha.pack(
                side=tk.TOP,
                fill=tk.X,
                #expand=True,
                padx=22,
                pady=3,
                ) 

                b=[]
                entry_año_ini=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    #expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                ent2 = tk.Entry(FrameFecha, textvariable=entry_año_ini)
                ent2.insert(0,year)
                ent2.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                entry_año_fin=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    #expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                ent7 = tk.Entry(FrameFecha, textvariable=entry_año_fin)
                ent7.insert(0,year)
                ent7.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                b.append(entry_año_ini)
                b.append(entry_año_fin)
                filtros_form_grafico.append(b)
            case "MES":
                FrameFecha=tk.Frame(container)
                FrameFecha.configure(background=style.BACKGROUND
                                        )
                FrameFecha.pack(
                side=tk.TOP,
                fill=tk.X,
                #expand=True,
                padx=22,
                pady=3,
                ) 
                d=[]
                entry_mes_ini=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                ent3 = tk.Entry(FrameFecha,textvariable=entry_mes_ini,)
                ent3.insert(0,"01")
                ent3.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                entry_mes_fin=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                ent8 = tk.Entry(FrameFecha,textvariable=entry_mes_fin,)
                ent8.insert(0,mes)
                ent8.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                d.append(entry_mes_ini)
                d.append(entry_mes_fin)
                filtros_form_grafico.append(d)
            case "DIA":
                
                FrameFecha=tk.Frame(container)
                FrameFecha.configure(background=style.BACKGROUND
                                        )
                FrameFecha.pack(
                side=tk.TOP,
                fill=tk.X,
                #expand=True,
                padx=22,
                pady=3,
                ) 
                c=[]
                entry_dia_ini=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    #expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                ) 
                ent4 = tk.Entry(FrameFecha, textvariable=entry_dia_ini)
                ent4.insert(0,"1")
                ent4.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                entry_dia_fin=tk.StringVar()
                label = tk.Label(FrameFecha, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    #expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                ) 
                ent10 = tk.Entry(FrameFecha, textvariable=entry_dia_fin)
                ent10.insert(0,"31")
                ent10.pack(
                    side = tk.LEFT,
                    fill= tk.X,
                    expand=True,
                    ipadx= 10,
                    ipady= 5,
                    padx= 10,
                    pady= 5,
                )
                c.append(entry_dia_ini)
                c.append(entry_dia_fin)
                filtros_form_grafico.append(c) 
            case "VALORES_UNICOS":
               
                i_val =i_val+1 
                #print(i_cad)   
                if(i_val<=3):

                    l_aux = val_uni[i-1]
                    entry_cad=tk.StringVar()
                    label = tk.Label(FrameVal, text = columnas[i] , font = ('calibre',10,'bold')).pack(
                        side=tk.LEFT,fill=tk.X,
                        
                        padx= 5,
                        pady= 5,
                        ipady=6,
                        ipadx=10)
                    lista_opciones = ttk.Combobox(FrameVal,textvariable=entry_cad)
                    lista_opciones['values'] = l_aux[1:]
                    lista_opciones['state'] = 'readonly'
                    lista_opciones.bind("<<ComboboxSelected>>",elemento_seleccionado)
                    #aux_val_col+=1
                    lista_opciones.pack(
                        side=tk.LEFT,fill=tk.X,
                        expand=True,
                        padx= 5,
                        pady= 5,
                        ipady=6,
                        ipadx=10)
                    #aux_val_col+=1
                    form_combobox.append(lista_opciones)
                    filtros_form_grafico.append(entry_cad)
                    sw_Cad=True
                if (i_val>=4 and i_val <=6):
                    l_aux = val_uni[i-1]
                    entry_cad=tk.StringVar()
                    label = tk.Label(FrameVal2, text = columnas[i] , font = ('calibre',10,'bold')).pack(
                        side=tk.LEFT,fill=tk.X,
                       
                        padx= 5,
                        pady= 5,
                        ipady=6,
                        ipadx=10)
                    lista_opciones = ttk.Combobox(FrameVal2,textvariable=entry_cad)
                    lista_opciones['values'] = l_aux[1:]
                    lista_opciones['state'] = 'readonly'
                    lista_opciones.bind("<<ComboboxSelected>>",elemento_seleccionado)
                    #aux_val_col+=1
                    lista_opciones.pack(
                        side=tk.LEFT,fill=tk.X,
                        expand=True,
                        padx= 5,
                        pady= 5,
                        ipady=6,
                        ipadx=10)
                    #aux_val_col+=1
                    form_combobox.append(lista_opciones)
                    filtros_form_grafico.append(entry_cad)
                    sw_Cad=True
        
            case "CADENAS":
                i_cad =i_cad+1 
                #print(i_cad)   
                if(i_cad<=3):

                    entry_cad=tk.StringVar()
                    label = tk.Label(FrameCad, text = columnas[i] , font = ('calibre',10,'bold')).pack(
                        side = tk.LEFT,
                        fill= tk.X,
                        #expand=True,
                        ipadx= 10,
                        ipady= 5,
                        padx= 10,
                        pady= 5,
                    )
                    caja_texto=tk.Entry(FrameCad, textvariable=entry_cad).pack(
                        side = tk.LEFT,
                        fill= tk.X,
                        expand=True,
                        ipadx= 5,
                        ipady= 5,
                        padx= 10,
                        pady= 5,
                    )
                    filtros_form_grafico.append(entry_cad)
                    sw_Cad=True
                if (i_cad>=4 and i_cad <=6):
                    entry_cad=tk.StringVar()
                    label = tk.Label(FrameCad2, text = columnas[i] , font = ('calibre',10,'bold')).pack(
                        side = tk.LEFT,
                        fill= tk.X,
                        #expand=True,
                        ipadx= 10,
                        ipady= 5,
                        padx= 10,
                        pady= 5,
                    )
                    caja_texto=tk.Entry(FrameCad2, textvariable=entry_cad).pack(
                        side = tk.LEFT,
                        fill= tk.X,
                        expand=True,
                        ipadx= 5,
                        ipady= 5,
                        padx= 10,
                        pady= 5,
                    )
                    filtros_form_grafico.append(entry_cad)
                if(i_cad>6):
                    entry_cad=tk.StringVar()
                    label = tk.Label(FrameCad3, text = columnas[i] , font = ('calibre',10,'bold')).pack(
                        side = tk.LEFT,
                        fill= tk.X,
                        #expand=True,
                        ipadx= 10,
                        ipady= 5,
                        padx= 10,
                        pady= 5,
                    )
                    caja_texto=tk.Entry(FrameCad3, textvariable=entry_cad).pack(
                        side = tk.LEFT,
                        fill= tk.X,
                        expand=True,
                        ipadx= 5,
                        ipady= 5,
                        padx= 10,
                        pady= 5,
                    )
                    filtros_form_grafico.append(entry_cad)


            case "FLOAT":
                i_float=i_float+1
                #print("i_float")
                #print(i_float) 
                if(i_float<=6):
                      
                    check_button_var = tk.IntVar()
                    check_button_var.set(1)
                    check = tk.Checkbutton(FrameFloat1, text=columnas[i], font = ('calibre',10,'bold'), variable=check_button_var).pack(
                            side=tk.LEFT,
                            fill=tk.X,
                            expand=True, 
                            padx=5, 
                            pady=5)
                    #label = tk.Label(container, text = columnas[i] , font = ('calibre',10,'bold')).grid(column=col_flo,row=fila_F)
                    #sw_Flo=True
                    filtros_form_grafico.append(check_button_var)
                if(i_float>=7 and i_float <=12):
                    
                    check_button_var = tk.IntVar()
                    check_button_var.set(1)
                    check = tk.Checkbutton(FrameFloat2, text=columnas[i], font = ('calibre',10,'bold'), variable=check_button_var).pack(
                            side=tk.LEFT,
                            fill=tk.X,
                            expand=True, 
                            padx=5, 
                            pady=5)
                    #label = tk.Label(container, text = columnas[i] , font = ('calibre',10,'bold')).grid(column=col_flo,row=fila_F)
                    #sw_Flo=True
                    filtros_form_grafico.append(check_button_var)
                if(i_float >=13 and i_float<=18):

                
                    check_button_var = tk.IntVar()
                    check_button_var.set(1)
                    check = tk.Checkbutton(FrameFloat3, text=columnas[i], font = ('calibre',10,'bold'), variable=check_button_var).pack(
                            side=tk.LEFT,
                            fill=tk.X,
                            expand=True, 
                            padx=5, 
                            pady=5)
                    #label = tk.Label(container, text = columnas[i] , font = ('calibre',10,'bold')).grid(column=col_flo,row=fila_F)
                    #sw_Flo=True
                    filtros_form_grafico.append(check_button_var)
                if(i_float >18):

                   
                    check_button_var = tk.IntVar()
                    check_button_var.set(1)
                    check = tk.Checkbutton(FrameFloat4, text=columnas[i], font = ('calibre',10,'bold'), variable=check_button_var).pack(
                            side=tk.LEFT,
                            fill=tk.X,
                            expand=True, 
                            padx=5, 
                            pady=5)
                    #label = tk.Label(container, text = columnas[i] , font = ('calibre',10,'bold')).grid(column=col_flo,row=fila_F)
                    #sw_Flo=True
                    filtros_form_grafico.append(check_button_var)
    

        
        if sw_Cad:
            col_cad+=2
            if col_cad==6:
                col_cad=0
                fila+=1
                fila_F=fila+1
        
        if sw_Flo:
            col_flo+=1
            if col_flo==6:
                col_flo=0
                fila_F+=1
    exportar_filtros(tipos, columnas)
    boton_enviar=tk.Button(container, text="Siguiente", command= elegir_graficas).pack(
                side =tk.TOP,
                fill=tk.X,
                padx=22,
                pady=11
                )
   
#esto para las graficas de torta donde necesitamos nombres unicos para elegir   
def nombres_unicos_cadena(nombre_tabla,nombre_filtro):
    
    
    carpeta = f"Ficheros\Valores Unicos"
    nombre_archivo = f"{nombre_tabla}.txt"
    #archivos = os.listdir(carpeta)
    #archivo = os.path.join(carpeta, "{nombre_tabla}.txt")
    nombre_cadena=[]
    # Abrir el archivo en modo lectura
    ruta_archivo = os.path.join(carpeta, nombre_archivo)

    
    
    with open(ruta_archivo, "r",encoding="utf-8") as f:
        # Iterar sobre las líneas del archivo
        for linea in f:
            # Separar los elementos por comas en cada línea
            elementos = linea.strip().split(";")
            
            # Comparar el primer" elemento de cada línea con "nombre"
            #print("elemento 0: "+elementos[0])
            if elementos[0] == nombre_filtro:
                
                #print("El primer elemento de esta línea es igual a 'nombre_filtro'")
                
                nombre_cadena.extend(elementos[1:])
            
    return nombre_cadena
########################elige tablas excepcionales
#aqui se muestran las funviones para las tblas especiales
def elige_eventos(container,columnas,tipos):
    for widget in container.winfo_children():
        widget.destroy()
    global filtros_form_grafico
    
    #print(filtros_form_grafico)
    tipos=tipos[1:]
    tabla = columnas[0]
    nro_columnas=len(columnas)-1
    filtro_datos = [0]*(nro_columnas)
    filtro_datos, lista_año, lista_mes =filtros_tablas(columnas,tipos)
   
    ubi_cache = "Cache_Graficos"
    filtrar_datos(tabla, ubi_cache, tipos, filtro_datos, nro_columnas, lista_año, lista_mes)

    tk.Label(
                container,
                text="seleccione que va a graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    def guardar_datos():
        cadena = selected_var.get() 
        Grafica_eventos_elegir_seleccionados(tabla,columnas,filtro_datos,cadena,container)   
        #Grafica_barras_eventos(tabla,columnas,filtro_datos,cadena)

    selected_var = tk.StringVar()
    #nombre_filtro.set("1er filtro")
    opciones = devolver_cadenas(columnas)
    #cadena="EMPRESA"
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
            side=tk.LEFT,
            fill=tk.X, 
            #expand=True,
            padx=22,
            pady=3, 
        )
    tk.Button(container, text="Guardar datos y graficar", command=guardar_datos).pack()

def Grafica_eventos_elegir_seleccionados(nombre_tabla,columnas,filtro_datos,cadena,container):
    for widget in container.winfo_children():
        widget.destroy()
    nombres_u=nombres_unicos_cadena(nombre_tabla,cadena)
    #print(nombres_u)
    nombres=[]

    def guardar_seleccionados():
        seleccionados = []
        for index in list.curselection():
            seleccionados.append(list.get(index))
        #print("Elementos seleccionados:", seleccionados)
        Grafica_barras_eventos(nombre_tabla,columnas,filtro_datos,cadena,seleccionados)
        #Grafica_RADAR_segun_cadena_y_hora_ultimo(nombre_tabla,columnas,filtro_datos,cadena,seleccionados)
        
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    list = tk.Listbox(Frame1, selectmode="multiple")
    list.pack(expand=tk.YES, fill="both")

    for each_item in range(len(nombres_u)):
        list.insert(tk.END, nombres_u[each_item])
        #list.itemconfig(each_item,bg="yellow" if each_item % 2 == 0 else "cyan")

    

    btn_guardar = tk.Button(container, text="Guardar datos y graficar", command=guardar_seleccionados)
    btn_guardar.pack()
def Grafica_barras_eventos(tabla,columnas,filtro_datos,cadena,seleccionados):
    nro_columnas=len(columnas)-1
    #buscar posicion de DE:
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==cadena:
            posicion_cad=i
    #print("posicion cad:"+str(posicion_cad))

    for i in range(nro_columnas):
        if columnas_a[i]=="DE":
            posicion_De=i
    #print("posicion De:"+str(posicion_De))
    def convertir_horas(h1,h2):
        
        # Dividir la cadena en horas y minutos
        horas1, minutos1 = h1.split(':')
        # Formatear los minutos con dos dígitos
        hh1 = f"{horas1.zfill(2)}:{minutos1.zfill(2)}"

        horas2, minutos2 = h2.split(':')
        # Formatear los minutos con dos dígitos
        hh2 = f"{horas2}:{minutos2.zfill(2)}"
        

        # Convierte las cadenas en objetos de hora
        hora1 = dt.strptime(hh1, '%H:%M')
        hora2 = dt.strptime(hh2, '%H:%M')

        # Calcula la diferencia de tiempo
        diferencia = (hora2 - hora1).total_seconds() / 3600

        if diferencia < 0:
            dif=24+diferencia
        else:
            dif=diferencia

        # Imprime la diferencia
        print(f'Diferencia en horas y minutos como decimales: {diferencia:.2f} horas')
        return dif

    
    for i in range(nro_columnas):
        if columnas_a[i]=="A":
            posicion_a=i
    print("posicion_A:"+str(posicion_a))

    nombres=seleccionados
    #sumar por cadenas
    subsuma= [0]*(len(nombres))
    
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                
                for i in range(len(nombres)):
                    if linea[posicion_cad]==nombres[i]:
                        diferencia=convertir_horas(linea[posicion_De],linea[posicion_a])
                        subsuma[i]=subsuma[i]+float(diferencia)

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)
    figure.subplots_adjust(bottom=0.170)
    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    
    #Para el Gráfico de Barras
    axes.bar(nombres, subsuma)
    axes.set_xticklabels(nombres, rotation=45, ha="right")

    #axes.pie(subsuma, labels=None,colors=colores, autopct="%0.1f %%")
    axes.set_title("Cantidad de horas trabajadas segun "+cadena)
    axes.set_ylabel('Sumatoria de tiempo')
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)                
                                        
def graficar_operationmargin(container,columnas,tipos):
    tipos=tipos[1:]
    tabla = columnas[0]
    nro_columnas=len(columnas)-1
    filtro_datos = [0]*(nro_columnas)
    filtro_datos, lista_año, lista_mes =filtros_tablas(columnas,tipos)
   
    ubi_cache = "Cache_Graficos"
    filtrar_datos(tabla, ubi_cache, tipos, filtro_datos, nro_columnas, lista_año, lista_mes)



    
    #buscar posicion de DE:
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]=="H1":
            posicion_h=i
    print("posicion h1:"+str(posicion_h))
    subsuma= [0]*24
    sub_H=["H1","H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12","H13","H14","H15","H16","H17","H18","H19","H20","H21","H22","H23","H24"]
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                if columnas_a[posicion_h]=="H1":
                    for i in range(24):
                        subsuma[i]=subsuma[i]+float(linea[i+posicion_h])
    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)

    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    #Para grafico de pastel
    axes.pie(subsuma, labels=sub_H,autopct="%0.1f %%")
    axes.set_title("Distribución de Energía segun por horas ")
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def elige_embalses(container,columnas,tipos):
    for widget in container.winfo_children():
        widget.destroy()
    global filtros_form_grafico
    
    #print(filtros_form_grafico)
    tipos=tipos[1:]
    tabla = columnas[0]
    nro_columnas=len(columnas)-1
    filtro_datos = [0]*(nro_columnas)
    filtro_datos, lista_año, lista_mes =filtros_tablas(columnas,tipos)
   
    ubi_cache = "Cache_Graficos"
    filtrar_datos(tabla, ubi_cache, tipos, filtro_datos, nro_columnas, lista_año, lista_mes)

    tk.Label(
                container,
                text="seleccione que va a graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    def guardar_datos():
        cadena = selected_var.get()    
        Grafica_barras_embalses(tabla,columnas,filtro_datos,cadena)

    selected_var = tk.StringVar()
    #nombre_filtro.set("1er filtro")
    opciones = devolver_cadenas(columnas)
    #cadena="EMPRESA"
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
            side=tk.LEFT,
            fill=tk.X, 
            #expand=True,
            padx=22,
            pady=3, 
        )
    tk.Button(container, text="Guardar datos y graficar", command=guardar_datos).pack()

def Grafica_barras_embalses(tabla,columnas,filtro_datos,cadena):
    nro_columnas=len(columnas)-1
    #buscar posicion de DE:
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==cadena:
            posicion_cad=i
    print("posicion cad:"+str(posicion_cad))

    for i in range(nro_columnas):
        if columnas_a[i]=="INICIAL":
            posicion_I=i
    print("posicion INI:"+str(posicion_I))
    for i in range(nro_columnas):
        if columnas_a[i]=="FINAL":
            posicion_F=i
    print("posicion FIN:"+str(posicion_F))
    

    

    nombres=nombres_unicos_cadena(tabla,cadena)
    #sumar por cadenas
    subsuma= [0]*(len(nombres))
    
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                
                for i in range(len(nombres)):
                    if linea[posicion_cad]==nombres[i]:
                        linea_f = linea[posicion_F].replace(";", "")
                        diferencia=float(float(linea_f)-float(linea[posicion_I])
                                         )
                        subsuma[i]=subsuma[i]+float(diferencia)

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)
    figure.subplots_adjust(bottom=0.170)
    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    
    #Para el Gráfico de Barras
    axes.bar(nombres, subsuma)
    axes.set_xticklabels(nombres, rotation=45, ha="right")

    #axes.pie(subsuma, labels=None,colors=colores, autopct="%0.1f %%")
    axes.set_title("Diferencia de Final - Inicial segun "+cadena)
    axes.set_ylabel('Sumatoria de floats')
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)   

######################BOTON QUE LE PIDE QUE ELIja el tipo de grafica
def tipo_grafica(container,columnas,tipos):
    for widget in container.winfo_children():
        widget.destroy()
    global filtros_form_grafico
    #print("tipofiltro:")
    #print(filtros_form_grafico)
    #print(filtros_form_grafico)
    tipos=tipos[1:]
    tabla = columnas[0]
    num_datos_para_grafico=0
    nro_columnas=len(columnas)-1
    filtro_datos = [0]*(nro_columnas)
    columnas_grafico=[]

    filtro_datos, lista_año, lista_mes =filtros_tablas(columnas,tipos)
    res=[0]*num_datos_para_grafico
    res_aux=[0]*num_datos_para_grafico
    
    ubi_cache = "Cache_Graficos"
    filtrar_datos(tabla, ubi_cache, tipos, filtro_datos, nro_columnas, lista_año, lista_mes)

    tk.Label(
                container,
                text="seleccione el tipo de grafico:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    tk.Button(
            Frame1,
            text="Barras",
            command=lambda: elige_barras(container,columnas,filtro_datos),
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=22,
            pady=11
        )
    tk.Button(
            Frame1,
            text="Lineal",
            command=lambda: elige_lineal(container,columnas,filtro_datos,res,columnas_grafico),
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=22,
            pady=11
        )
    tk.Button(
            Frame1,
            text="Torta",
            command=lambda: elige_torta(container,columnas,filtro_datos,res,columnas_grafico),
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=22,
            pady=11
        )
    if "H1" in columnas or "H24" in columnas:
        tk.Button(
                Frame1,
                text="Polar",#en el polar le mandamos el año inicial y final
                command=lambda:elige_polar(container,columnas,filtro_datos,res,columnas_grafico),
                **style.STYLE2,
                relief= tk.FLAT,
                activebackground=style.BACKGROUND,
                activeforeground= style.TEXT,
            ).pack(
                side =tk.LEFT,
                fill=tk.X,
                expand=True,
                padx=22,
                pady=11
            )

#funciones para las graficas de barras
def elige_barras(container,columnas,filtro_datos):
    for widget in container.winfo_children():
        widget.destroy()
    
    tk.Label(
                container,
                text="Seleccione que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    tk.Button(
            Frame1,
            text="Cantidad de datos numericos por datos unicos",
            command=lambda:Grafica_barras_por_cadenas(container,filtro_datos,columnas),
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
    tipos = tipos_datos(columnas)
    if "FECHA" in tipos or "DIA" in tipos:
        tk.Button(
                Frame1,
                text="Cantidad de datos numericos por datos unicos por fechas ",
                command=lambda:graficar_barras_por_fechas(container,filtro_datos,columnas),
                **style.STYLE2,
                relief= tk.FLAT,
                activebackground=style.BACKGROUND,
                activeforeground= style.TEXT,
            ).pack(
                side =tk.LEFT,
                fill=tk.X,
                padx=22,
                pady=11
            )
    
def graficar_barras_por_fechas(container,filtro_datos,columnas):
    global filtros_form_grafico
    for filtro_form in filtros_form_grafico:
        if type(filtro_form)== type(columnas):
            a=filtro_form[0]
            b=filtro_form[1]
            if len(a.get())==4:
                if(columnas[3]=="DÍA"):
                    m=filtros_form_grafico[1]
                    d=filtros_form_grafico[2]
                    fechainicial=str(d[0].get()+"/"+m[0].get()+"/"+a.get())
                    fechafinal=str(d[1].get()+"/"+m[1].get()+"/"+b.get())
                else:
                    m=filtros_form_grafico[1]
                    
                    fechainicial=str("01"+"/"+m[0].get()+"/"+a.get())
                    fechafinal=str("27"+"/"+m[1].get()+"/"+b.get())  
            if len(a.get())>4:
                fechainicial=str(a.get())
                fechafinal=str(b.get())
    #print(fechainicial,fechafinal)
    fecha_inicial = datetime.datetime.strptime(fechainicial, "%d/%m/%Y").date()
    fecha_final = datetime.datetime.strptime(fechafinal, "%d/%m/%Y").date()

    diferencia = fecha_final - fecha_inicial
    cantidad_dias = diferencia.days

    print("Cantidad de días entre las fechas:", cantidad_dias)
    #dividimos las fechas
    inter = cantidad_dias // 15
    intervalo = timedelta(days=inter)
    fechas = []
   
    fechas.append(fecha_inicial)
    for i in range(1, 16):
        nueva_fecha = fecha_inicial + intervalo
        fechas.append(nueva_fecha)
        intervalo += timedelta(days=inter)
    #fechas.append(fecha_final)
    
    for fecha in fechas:
        print(fecha)
    #ahora le preguntamos si quiere graficar por empresas,area etc

    for widget in container.winfo_children():
        widget.destroy()
    nombre_tabla=columnas[0]
    
    tk.Label(
                container,
                text="seleccione sobre que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    
    def guardar_datos():
        cadena = selected_var.get()
        float_n = selected_float.get()
        Grafica_barras_segun_cadena_hora_fechas(container,nombre_tabla,columnas,filtro_datos,float_n,cadena,fechas)

    #nombre_filtro.set("1er filtro")
    opciones = devolver_cadenas(columnas)
    selected_var = tk.StringVar()
    selected_var.set(opciones[0])
    
    #print(opciones)
    

    #cadena="EMPRESA"
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
            side=tk.LEFT,
            fill=tk.X, 
            #expand=True,
            padx=22,
            pady=3, 
        )
   
    
    #estas opcines dos, hay que ver una forma de sacar del los float de la tabla que hayas elegido
    
    opciones2 = devolver_floats(columnas)

    #float_n="H2"
    #combo_var = tk.StringVar()
    tk.Label(
                container,
                text="seleccione el dato numérico:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame2=tk.Frame(container)
    Frame2.configure(background=style.BACKGROUND
                    )
    Frame2.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    )
     
    selected_float = tk.StringVar()
    selected_float.set(opciones2[0])
    combo_box = ttk.Combobox(Frame2, textvariable=selected_float,values=opciones2)
    
    combo_box.pack(
        side=tk.TOP,
        fill=tk.X,
        #expand=True,
        padx=22,
        pady=3, 
    )

    #guardamos en nombre los datos unicos de la cadena que se eligio
    
    tk.Button(container, text="Guardar datos", command=guardar_datos).pack()

def Grafica_barras_segun_cadena_hora_fechas(container,nombre_tabla,columnas,filtro_datos,float_n,cadena,fechas):
    for widget in container.winfo_children():
        widget.destroy()
    nombres_u=nombres_unicos_cadena(nombre_tabla,cadena)
    print(nombres_u)
    

    def guardar_seleccionados():
        seleccionados = []
        for index in list.curselection():
            seleccionados.append(list.get(index))
        print("Elementos seleccionados:", seleccionados)
        Grafica_BARRAS_segun_cadena_y_hora_fechas_ultimo(nombre_tabla,columnas,filtro_datos,cadena,seleccionados,float_n,fechas)
        
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    list = tk.Listbox(Frame1, selectmode="multiple")
    list.pack(expand=tk.YES, fill="both")

    for each_item in range(len(nombres_u)):
        list.insert(tk.END, nombres_u[each_item])
        #list.itemconfig(each_item,bg="yellow" if each_item % 2 == 0 else "cyan")

    

    btn_guardar = tk.Button(container, text="Guardar datos y graficar", command=guardar_seleccionados)
    btn_guardar.pack()

def Grafica_BARRAS_segun_cadena_y_hora_fechas_ultimo(nombre_tabla,columnas,filtro_datos,cadena,seleccionados,float_n,fechas):
    nombres=seleccionados

    nro_columnas=len(columnas)-1
    sum_total=0
    contador=0
    tabla=columnas[0]  

    cadena_hora = [[0] * len(fechas) for _ in range(len(nombres))]
    #buscar psocion de la cadena:
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==cadena:
            posicion_cadena=i
    
    
    #buscar posicion de float
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==float_n:
            posicion_H=i
    print("posicion H:"+str(posicion_H)) 

    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                
                    #la tabla tiene una columna tipo año
                if columnas_a[0]=="AÑO" and columnas_a[1]=="MES" and columnas_a[2]=="DÍA":
                        #ademas tiene mes y dia
                        fecha_x=str(linea[2]+"-"+linea[1]+"-"+linea[0])
                        #print(fecha_x)
                        fechax = datetime.datetime.strptime(fecha_x, "%d-%m-%Y").date()
                        #iteramos en nombres y ademas por fechas de nuestro array de fechas
                        for i, fecha in enumerate(fechas):
                            for j, nombre in enumerate(nombres):
                                #print(nombres[i].get())
                                if linea[posicion_cadena]==nombres[j]:
                                    
                                    if(i <len(fechas)-1):
                                        if (fechax >= fecha and fechax < fechas[i+1]) :
                                            cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])
                                            

                                    else:
                                        if (fechax == fechas[i]) :
                                            cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])
                            #if(i>0):
                            #    cadena_hora[j][i]=cadena_hora[j][i]+cadena_hora[j][i-1]
                if(columnas_a[0]=="FECHA"):
                    #la tabla tiene una columna de tipo fecha
                    fecha_x=str(linea[0])
                    fechax = datetime.datetime.strptime(fecha_x, "%d/%m/%Y").date()
                    #iteramos en nombres y ademas por fechas de nuestro array de fechas
                    for i, fecha in enumerate(fechas):
                            for j, nombre in enumerate(nombres):
                                #print(nombres[i].get())
                                if linea[posicion_cadena]==nombres[j]:
                                    
                                    if(i <len(fechas)-1):
                                        if (fechax >=fecha and fechax<fechas[i+1]) :
                                            cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])

                                    else:
                                        if (fechax == fechas[i]) :
                                            cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])
    

                else:
                    #no tiene dia
                    fecha_x=str("02"+"-"+linea[1]+"-"+linea[0])
                    fechax = datetime.datetime.strptime(fecha_x, "%d-%m-%Y").date()
                    #iteramos en nombres y ademas por fechas de nuestro array de fechas
                    for i, fecha in enumerate(fechas):
                        for j, nombre in enumerate(nombres):
                            #print(nombres[i].get())
                            if linea[posicion_cadena]==nombres[j]:
                                
                                if(i <len(fechas)):
                                    if (fechax >=fecha and fechax<fechas[i+1]) :
                                        cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])

                                else:
                                    if (fechax == fechas[i]) :
                                        cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])
                    
                        
            
                    
    def suma_con_resultado_anterior(array):
        resultado = []
        resultado_anterior = 0
        
        for numero in array:
            resultado_anterior +=  float(numero)
            resultado.append(resultado_anterior)
        
        return resultado

    
    
    new_cad_horas=[]
    for i,_ in enumerate(nombres):
        
        suma=suma_con_resultado_anterior(cadena_hora[i])
        new_cad_horas.append(suma)



    
    fechas_str=[]
    for fecha in fechas:
        fechas_str.append(str(fecha))

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico Lineal por fechas")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    #figure = Figure(figsize=(10,24),dpi=100)
    # Crear la figura
    figure = Figure(figsize=(8, 8), dpi=100)
    figure.subplots_adjust(left=0.11, right=0.76)
    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)
    
    # Crear los subplots para los gráficos
    ax1 = figure.add_subplot(111)
    
    # Calcular los ángulos para la gráfica polar
    
    colores = [
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow',
    'orange', 'purple', 'brown', 'pink', 'gray', 'olive',
    'lime', 'teal', 'navy', 'coral', 'indigo', 'silver',
    'gold', 'orchid'
    ]
    for i, nombre in enumerate(nombres):
        #print(cadena_hora[i])
        color = colores[i]
        ax1.bar(fechas_str, new_cad_horas[i],label=nombre,linewidth=2, linestyle='solid',color=color)
        
        
        ax1.set_title("Distribución de Energía de "+str(float_n)+ " por fechas comparando "+cadena)
        
        
    ax1.tick_params(axis='x', rotation=45)  # Rotación de etiquetas

    #ax1.set_xlabel('Fechas')
    #ax1.set_ylabel('Valores')
    ax1.legend(title=cadena,
                loc="upper right",
                bbox_to_anchor=(1, 0, 0.3, 1))
    
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)    

def Grafica_barras_por_cadenas(container,filtro_datos,columnas):
    for widget in container.winfo_children():
        widget.destroy()
    nombre_tabla=columnas[0]
    
    tk.Label(
                container,
                text="seleccione sobre que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    
    def guardar_datos():
        cadena = selected_var.get()
        float_n = selected_float.get()
        Grafica_barras_segun_cadena(nombre_tabla,columnas,filtro_datos,float_n,cadena)

    selected_var = tk.StringVar()
    nombre_filtro = tk.StringVar()
    #nombre_filtro.set("1er filtro")
    opciones = devolver_cadenas(columnas)
    
    #cadena="EMPRESA"
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    selected_var.set(opciones[0])
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
            side=tk.LEFT,
            fill=tk.X, 
            #expand=True,
            padx=22,
            pady=3, 
        )
   
    
    #estas opcines dos, hay que ver una forma de sacar del los float de la tabla que hayas elegido
    opciones2 = devolver_floats(columnas)
    #float_n="H2"
    #combo_var = tk.StringVar()
    tk.Label(
                container,
                text="seleccione el dato numerico:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame2=tk.Frame(container)
    Frame2.configure(background=style.BACKGROUND
                    )
    Frame2.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    )
     
    selected_float = tk.StringVar()
    selected_float.set(opciones2[0])
    combo_box = ttk.Combobox(Frame2, textvariable=selected_float,values=opciones2)
    
    combo_box.pack(
        side=tk.TOP,
        fill=tk.X,
        #expand=True,
        padx=22,
        pady=3, 
    )
    
    tk.Button(container, text="Guardar datos y graficar", command=guardar_datos).pack()

def Grafica_barras_segun_cadena(nombre_tabla,columnas,filtro_datos,float_n,cadena):
    #print("float: "+float_n)
    #print("cadena: "+cadena)
    nombres=nombres_unicos_cadena(nombre_tabla,cadena)
    nro_columnas=len(columnas)-1
    sum_total=0
    columna_posicion_float=0
    
    #buscar posicion de cadena:
    
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==cadena:
            posicion_cadena=i
    #print("posicion cad:"+str(posicion_cadena))

    
    for i in range(nro_columnas):
        if columnas_a[i]==float_n:
            columna_posicion_float=i
    #print("posicion float:"+str(columna_posicion_float))


    #sumar por cadenas
    subsuma= [0]*(len(nombres))
    porcentaje=[0]*(len(nombres))
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                
                for i in range(len(nombres)):
                    if linea[posicion_cadena]==nombres[i] and columna_posicion_float !=0 :

                        subsuma[i]=subsuma[i]+float(linea[columna_posicion_float])
                    
                    
    

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)
    figure.subplots_adjust(bottom=0.170)
    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    
    #Para grafico de pastel
    colores = [
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow',
    'orange', 'purple', 'brown', 'pink', 'gray', 'olive',
    'lime', 'teal', 'navy', 'coral', 'indigo', 'silver',
    'gold', 'orchid'
    ]
    #Para el Gráfico de Barras
    axes.bar(nombres, subsuma)
    axes.set_xticklabels(nombres, rotation=45, ha="right")

    #axes.pie(subsuma, labels=None,colors=colores, autopct="%0.1f %%")
    axes.set_title("Distribución de Energía segun "+cadena +" y segun "+float_n)
    axes.set_ylabel('Sumatoria de Energia')
    """axes.legend(nombres,
                title="Lista",
                loc="upper center",
                bbox_to_anchor=(1, 0, 0.5, 1))

                    """
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#funciones para las graficas lineales
def elige_lineal(container,columnas,filtro_datos,res,columnas_grafico):
    for widget in container.winfo_children():
        widget.destroy()
    
    tk.Label(
                container,
                text="Seleccione que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    tk.Button(
            Frame1,
            text="Cantidad de datos numericos por datos unicos",
            command=lambda:Grafica_lineal_por_cadenas(container,filtro_datos,columnas),
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
    tipos = tipos_datos(columnas)
    if "FECHA" in tipos or "DIA" in tipos:
        tk.Button(
                Frame1,
                text="Cantidad de datos numericos por datos unicos por fechas ",
                command=lambda:graficar_lineal_por_fechas(container,filtro_datos,columnas),
                **style.STYLE2,
                relief= tk.FLAT,
                activebackground=style.BACKGROUND,
                activeforeground= style.TEXT,
            ).pack(
                side =tk.LEFT,
                fill=tk.X,
                padx=22,
                pady=11
            )

def graficar_lineal_por_fechas(container,filtro_datos,columnas):
    global filtros_form_grafico
    for filtro_form in filtros_form_grafico:
        if type(filtro_form)== type(columnas):
            a=filtro_form[0]
            b=filtro_form[1]
            print(a.get())
            if len(a.get())==4:
                m=filtros_form_grafico[1]
                #print("Tiene dia?")
                if("DÍA" in columnas):
                    d=filtros_form_grafico[2]
                    #print("dia:::")
                    #print(d[0].get())
                    fechainicial=str(d[0].get()+"/"+m[0].get()+"/"+a.get())
                    fechafinal=str(d[1].get()+"/"+m[1].get()+"/"+a.get())
                else:
                    fechainicial=str("01"+"/"+m[0].get()+"/"+a.get())
                    fechafinal=str("27"+"/"+m[1].get()+"/"+b.get())

                
            if len(a.get())>4:
                fechainicial=str(a.get())
                fechafinal=str(b.get())
    
    fecha_inicial = datetime.datetime.strptime(fechainicial, "%d/%m/%Y").date()
    fecha_final = datetime.datetime.strptime(fechafinal, "%d/%m/%Y").date()

    diferencia = fecha_final - fecha_inicial
    cantidad_dias = diferencia.days

    print("Cantidad de días entre las fechas:", cantidad_dias)
    print(fecha_inicial)
    print(fecha_final)
    #dividimos las fechas
    inter = cantidad_dias // 15
    intervalo = timedelta(days=inter)
    fechas = []
   
    fechas.append(fecha_inicial)
    for i in range(1, 16):
        nueva_fecha = fecha_inicial + intervalo
        fechas.append(nueva_fecha)
        intervalo += timedelta(days=inter)
    
    
    #for fecha in fechas:
    #    print(fecha)
    #ahora le preguntamos si quiere graficar por empresas,area etc

    for widget in container.winfo_children():
        widget.destroy()
    nombre_tabla=columnas[0]
    
    tk.Label(
                container,
                text="seleccione sobre que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    
    def guardar_datos():
        cadena = selected_var.get()
        float_n = selected_float.get()
        Grafica_lineal_segun_cadena_hora_fechas(container,nombre_tabla,columnas,filtro_datos,float_n,cadena,fechas)

    
    #nombre_filtro.set("1er filtro")
    opciones = devolver_cadenas(columnas)
    selected_var = tk.StringVar()
    selected_var.set(opciones[0])

    #cadena="EMPRESA"
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
            side=tk.LEFT,
            fill=tk.X, 
            #expand=True,
            padx=22,
            pady=3, 
        )
   
    
    #estas opcines dos, hay que ver una forma de sacar del los float de la tabla que hayas elegido
    opciones2 = devolver_floats(columnas)
    #combo_var = tk.StringVar()
    tk.Label(
                container,
                text="seleccione el dato numérico:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame2=tk.Frame(container)
    Frame2.configure(background=style.BACKGROUND
                    )
    Frame2.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    )
     
    selected_float = tk.StringVar()
    selected_float.set(opciones2[0])
    combo_box = ttk.Combobox(Frame2, textvariable=selected_float,values=opciones2)
    
    combo_box.pack(
        side=tk.TOP,
        fill=tk.X,
        #expand=True,
        padx=22,
        pady=3, 
    )

    #guardamos en nombre los datos unicos de la cadena que se eligio
    
    tk.Button(container, text="Guardar datos", command=guardar_datos).pack()

def  Grafica_lineal_segun_cadena_hora_fechas(container,nombre_tabla,columnas,filtro_datos,float_n,cadena,fechas):
    for widget in container.winfo_children():
        widget.destroy()
    nombres_u=nombres_unicos_cadena(nombre_tabla,cadena)
    #print(nombres_u)
    

    def guardar_seleccionados():
        seleccionados = []
        for index in list.curselection():
            seleccionados.append(list.get(index))
        #print("Elementos seleccionados:", seleccionados)
        Grafica_LINEAL_segun_cadena_y_hora_ultimo(nombre_tabla,columnas,filtro_datos,cadena,seleccionados,float_n,fechas)
        
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    list = tk.Listbox(Frame1, selectmode="multiple")
    list.pack(expand=tk.YES, fill="both")

    for each_item in range(len(nombres_u)):
        list.insert(tk.END, nombres_u[each_item])
        #list.itemconfig(each_item,bg="yellow" if each_item % 2 == 0 else "cyan")

    

    btn_guardar = tk.Button(container, text="Guardar datos y graficar", command=guardar_seleccionados)
    btn_guardar.pack()

def Grafica_LINEAL_segun_cadena_y_hora_ultimo(nombre_tabla,columnas,filtro_datos,cadena,seleccionados,float_n,fechas):
    nombres=seleccionados
    print("rango de fechas:")
    
    nro_columnas=len(columnas)-1

    cadena_hora = [[0] * len(fechas) for _ in range(len(nombres))]
    #buscar psocion de la cadena:
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==cadena:
            posicion_cadena=i
    
    
    #buscar posicion de float
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==float_n:
            posicion_H=i
    #print("posicion H:"+str(posicion_H)) 

    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                if columnas_a[0]=="AÑO" and columnas_a[1]=="MES" and columnas_a[2]=="DÍA":
                    #la tabla tiene una columna tipo año,mes,dia
                    
                    #ademas tiene mes y dia
                    fecha_x=str(linea[2]+"-"+linea[1]+"-"+linea[0])

                    #print("fecha")
                    #print(fecha_x)
                    fechax = datetime.datetime.strptime(fecha_x, "%d-%m-%Y").date()
                    #print("fechax:")
                    #print(fechax)
                    #iteramos en nombres y ademas por fechas de nuestro array de fechas
                    for i, fecha in enumerate(fechas):
                        for j, nombre in enumerate(nombres):
                            #print(nombres[i].get())
                            if linea[posicion_cadena]==nombres[j]:
                                
                                if(i <(len(fechas)-1)):
                                    if (fechax >= fecha and fechax < fechas[i+1]) :
                                        cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])
                                        

                                else:
                                    if (fechax == fechas[i]) :
                                        cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])
                        #if(i>0):
                        #    cadena_hora[j][i]=cadena_hora[j][i]+cadena_hora[j][i-1]
                if(columnas_a[0]=="FECHA"):
                    #la tabla tiene una columna de tipo fecha
                    fecha_x=str(linea[0])
                    fechax = datetime.datetime.strptime(fecha_x, "%d/%m/%Y").date()
                    #iteramos en nombres y ademas por fechas de nuestro array de fechas
                    for i, fecha in enumerate(fechas):
                            for j, nombre in enumerate(nombres):
                                #print(nombres[i].get())
                                if linea[posicion_cadena]==nombres[j]:
                                    
                                    if(i <len(fechas)-1):
                                        if (fechax >=fecha and fechax<fechas[i+1]) :
                                            cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])

                                    else:
                                        if (fechax == fechas[i]) :
                                            cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])
    
                        
                else:
                    #no tiene dia
                        fecha_x=str("01"+"/"+linea[1]+"/"+linea[0])
                        fechax = datetime.datetime.strptime(fecha_x, "%d/%m/%Y").date()
                        #iteramos en nombres y ademas por fechas de nuestro array de fechas
                        for i, fecha in enumerate(fechas):
                            for j, nombre in enumerate(nombres):
                                #print(nombres[i].get())
                                if linea[posicion_cadena]==nombres[j]:
                                    
                                    if(i <len(fechas)-1):
                                        if (fechax >=fecha and fechax<fechas[i+1]) :
                                            cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])

                                    else:
                                        if (fechax == fechas[i]) :
                                            cadena_hora[j][i]=cadena_hora[j][i]+float(linea[posicion_H])
                    
                        
                    
    def suma_con_resultado_anterior(array):
        resultado = []
        resultado_anterior = 0
        
        for numero in array:
            resultado_anterior +=  float(numero)
            resultado.append(resultado_anterior)
        
        return resultado

    
    
    new_cad_horas=[]
    for i,_ in enumerate(nombres):
        
        suma=suma_con_resultado_anterior(cadena_hora[i])
        new_cad_horas.append(suma)



    for i, _ in enumerate(nombres):
        print("cantidad de h por fechas")
        print(cadena_hora[i])
    for i, _ in enumerate(nombres):
        print("cantidad de h por fechas modificada")
        print(new_cad_horas[i])
    
    fechas_str=[]
    for fecha in fechas:
        fechas_str.append(str(fecha))

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico Lineal por fechas")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    #figure = Figure(figsize=(10,24),dpi=100)
    # Crear la figura
    figure = Figure(figsize=(8, 8), dpi=100)
    figure.subplots_adjust(left=0.11, right=0.76)
    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)
    
    # Crear los subplots para los gráficos
    ax1 = figure.add_subplot(111)
    
    # Calcular los ángulos para la gráfica polar
    
    colores = [
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow',
    'orange', 'purple', 'brown', 'pink', 'gray', 'olive',
    'lime', 'teal', 'navy', 'coral', 'indigo', 'silver',
    'gold', 'orchid'
    ]
    for i, nombre in enumerate(nombres):
        #print(cadena_hora[i])
        color = colores[i]
        ax1.plot(fechas_str, new_cad_horas[i],label=nombre,linewidth=2, linestyle='solid',color=color)
        
        
        ax1.set_title("Distribución de Energía de "+str(float_n)+ " por fechas comparando "+cadena)
        
        
    ax1.tick_params(axis='x', rotation=45)  # Rotación de etiquetas

    #ax1.set_xlabel('Fechas')
    #ax1.set_ylabel('Valores')
    ax1.legend(title=cadena,
                loc="upper right",
                bbox_to_anchor=(1, 0, 0.3, 1))
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)            

def Grafica_lineal_por_cadenas(container,filtro_datos,columnas):
    for widget in container.winfo_children():
        widget.destroy()
    nombre_tabla=columnas[0]
    
    tk.Label(
                container,
                text="seleccione sobre que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    
    def guardar_datos():
        cadena = selected_var.get()
        float_n = selected_float.get()
        Grafica_lineal_segun_cadena(nombre_tabla,columnas,filtro_datos,float_n,cadena)



    
    nombre_filtro = tk.StringVar()
    #nombre_filtro.set("1er filtro")
    opciones = devolver_cadenas(columnas)
    selected_var = tk.StringVar()
    selected_var.set(opciones[0])
    #cadena="EMPRESA"
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
            side=tk.LEFT,
            fill=tk.X, 
            #expand=True,
            padx=22,
            pady=3, 
        )
    #print("nombre_filtro : "+nombre_filtro.get())
    
    #estas opcines dos, hay que ver una forma de sacar del los float de la tabla que hayas elegido
    opciones2 = devolver_floats(columnas)
   
    tk.Label(
                container,
                text="seleccione el dato numérico:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame2=tk.Frame(container)
    Frame2.configure(background=style.BACKGROUND
                    )
    Frame2.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    )
     
    selected_float = tk.StringVar()
    selected_float.set(opciones2[0])
    combo_box = ttk.Combobox(Frame2, textvariable=selected_float,values=opciones2)
    
    combo_box.pack(
        side=tk.TOP,
        fill=tk.X,
        #expand=True,
        padx=22,
        pady=3, 
    )
    
    
    tk.Button(container, text="Guardar datos y graficar", command=guardar_datos).pack()

def Grafica_lineal_segun_cadena(nombre_tabla,columnas,filtro_datos,float_n,nombre_filtro):
    nombres=nombres_unicos_cadena(nombre_tabla,nombre_filtro)
    nro_columnas=len(columnas)-1
    
    #buscar posicion de cadena:
    c=0
    
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==nombre_filtro:
            posicion_cadena=i
    print("posicion cad:"+str(posicion_cadena))
     #buscar posicion del primer H1:
    
    
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==float_n:
            posicion_H=i
    print("posicion H:"+str(posicion_H))
    #sumar por cadenas
    sub_suma=0
    suma_H= [0]*(len(nombres))
    porcentaje=[0]*(len(nombres))
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                for i in range(len(nombres)):
                    if linea[posicion_cadena]==nombres[i]:           
                        #print("j:"+str(j))
                        suma_H[i]=suma_H[i]+float(linea[posicion_H])
    #print(nombres)
    #print(suma_H)

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)

    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    #Para grafico de pastel
    
    axes.plot(nombres, suma_H, marker = "o", label = "suma de energia")
    axes.set_title("Distribución de Energía segun "+nombre_filtro)
    axes.tick_params(axis='x', rotation=45) 
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
#funciones para las graficas por torta
def elige_torta(container,columnas,filtro_datos,res,columnas_grafico):
    #preguntar si quiere grficar por cadenas o horas en total
    for widget in container.winfo_children():
        widget.destroy()
    
    tk.Label(
                container,
                text="Seleccione que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    tk.Button(
            Frame1,
            text="Porcentaje de datos numericos por datos unicos",
            command=lambda:Grafica_torta_por_cadenas(container,filtro_datos,columnas),
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
    
    if "H1" in columnas :
        tk.Button(
                Frame1,
                text="Porcentaje de energia por dias ",
                command=lambda:Grafica_torta_por_cadenas_por_dia(container,filtro_datos,columnas),
                **style.STYLE2,
                relief= tk.FLAT,
                activebackground=style.BACKGROUND,
                activeforeground= style.TEXT,
            ).pack(
                side =tk.LEFT,
                fill=tk.X,
                padx=22,
                pady=11
            )

def graficar_datos_torta_horas(columnas):            
    
    #print(columnas)
    columnas_grafico= devolver_floats(columnas)
    res= [0]*(len(columnas_grafico))
    
    nro_columnas=len(columnas)-1
    #buscar posicion de DE:
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==columnas_grafico[0]:
            posicion_F=i
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                
                if columnas_a[posicion_F]== columnas_grafico[0]:
                    for j in range(len(columnas_grafico)):
                        linea_x = linea[posicion_F+j].replace(";", "")
                        res[j]=res[j]+float(linea_x)

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)

    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    #Para grafico de pastel
    axes.pie(res, labels=columnas_grafico,autopct="%0.1f %%")
    axes.set_title("Distribución de Energía segun por horas ")
    #Para el Gráfico de Barras
    #axes.bar(columnas_grafico, res)
    #axes.set_title('Columnas de Gráfico')
    #axes.set_ylabel('Sumatoria de Datos')

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def Grafica_torta_por_cadenas(container,filtro_datos,columnas):
    
    for widget in container.winfo_children():
        widget.destroy()
    nombre_tabla=columnas[0]
    
    tk.Label(
                container,
                text="seleccione sobre que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    
    def guardar_datos():
        cadena = selected_var.get()
        float_n = selected_float.get()
        Grafica_Torta_segun_cadena_y_hora(nombre_tabla,columnas,filtro_datos,float_n,cadena)



    
   
    #nombre_filtro.set("1er filtro")
    opciones = devolver_cadenas(columnas)
    selected_var = tk.StringVar()
    selected_var.set(opciones[0])

    #cadena="EMPRESA"
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
            side=tk.LEFT,
            fill=tk.X, 
            #expand=True,
            padx=22,
            pady=3, 
        )
    

    
    #estas opcines dos, hay que ver una forma de sacar del los float de la tabla que hayas elegido
    opciones2 = devolver_floats(columnas)
    #float_n="H2"
    #combo_var = tk.StringVar()
    tk.Label(
                container,
                text="seleccione el dato numérico:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame2=tk.Frame(container)
    Frame2.configure(background=style.BACKGROUND
                    )
    Frame2.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    )
     
    selected_float = tk.StringVar()
    selected_float.set(opciones2[0])
    combo_box = ttk.Combobox(Frame2, textvariable=selected_float,values=opciones2)
    
    combo_box.pack(
        side=tk.TOP,
        fill=tk.X,
        #expand=True,
        padx=22,
        pady=3, 
    )
   
    tk.Button(container, text="Guardar datos y graficar", command=guardar_datos).pack()

def Grafica_torta_por_cadenas_por_dia(container,filtro_datos,columnas):
    for widget in container.winfo_children():
        widget.destroy()
    nombre_tabla=columnas[0]
    
    tk.Label(
                container,
                text="seleccione sobre que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    
    def guardar_datos():
        cadena = selected_var.get()
        Grafica_Torta_segun_cadena_por_dia(nombre_tabla,columnas,filtro_datos,cadena)


    opciones = devolver_cadenas(columnas)
    selected_var = tk.StringVar()
    selected_var.set(opciones[0])
    
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 

    #cadena="EMPRESA"
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
           side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3, 
        )
    
    
   
    tk.Button(container, text="Guardar datos y graficar", command=guardar_datos).pack()

def Grafica_Torta_segun_cadena_por_dia(nombres_tabla,columnas,filtro_datos,nombre_filtro):
    nombres=nombres_unicos_cadena(nombres_tabla,nombre_filtro)
    nro_columnas=len(columnas)-1
    
    #buscar posicion de cadena:
    c=0
    
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==nombre_filtro:
            posicion_cadena=i
    #print("posicion cad:"+str(posicion_cadena))
     #buscar posicion del primer H1:
    
    
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]=="H1":
            posicion_H=i
    #print("posicion H1:"+str(posicion_H))
    #sumar por cadenas
    sub_suma=0
    suma_H= [0]*(len(nombres))
    porcentaje=[0]*(len(nombres))
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                for i in range(len(nombres)):
                    if linea[posicion_cadena]==nombres[i]:
                        for j in range(24):
                            linea_x = linea[posicion_H+j].replace(";", "")
                            sub_suma=sub_suma+float(linea_x)
                            #print("j:"+str(j))
                        suma_H[i]=suma_H[i]+float(sub_suma)
    print(nombres)
    print(suma_H)

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)

    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    #Para grafico de pastel
    colores = [
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow',
    'orange', 'purple', 'brown', 'pink', 'gray', 'olive',
    'lime', 'teal', 'navy', 'coral', 'indigo', 'silver',
    'gold', 'orchid'
]
    axes.pie(suma_H, labels=None,colors=colores, autopct="%0.1f %%")
    axes.set_title("Distribución de Energía segun "+nombre_filtro +" por dia")
    axes.legend(nombres,
                title="Lista",
                loc="upper center",
                bbox_to_anchor=(1, 0, 0.5, 1))
    #axes.title('Gráfico de Pastel por dias en el periodo de fecha que eligio')
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)                           
#esto para las graficas de torta donde necesitamos nombres unicos para elegir   
              
def Grafica_Torta_segun_cadena_y_hora(nombres_tabla,columnas,filtro_datos,stringvar_Float,nombre_filtro):
   
    nombres=nombres_unicos_cadena(nombres_tabla,nombre_filtro)
    nro_columnas=len(columnas)-1
    sum_total=0
    
    
    #recorrer por la tabla cache de tabla
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                sw=True
                aux_c=0
                for i in range(nro_columnas):
                    filtro=filtro_datos[i]
                    casilla=linea[i]
                    columna_i=columnas[i+1]
                    if columnas[i+1]==stringvar_Float:
                        sum_total+=float(casilla)
                        
                        columna_posicion_float=i
    print("suma total: "+str(sum_total))
    #buscar posicion de cadena:
    c=0
    
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==nombre_filtro:
            posicion_cadena=i
    print("posicion cad:"+str(posicion_cadena))
    #sumar por cadenas
    subsuma= [0]*(len(nombres))
    porcentaje=[0]*(len(nombres))
    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                for i in range(len(nombres)):
                    if linea[posicion_cadena]==nombres[i]:

                        subsuma[i]=subsuma[i]+float(linea[columna_posicion_float])
                        
                    
    for i in range(len(nombres)):
        if subsuma[i]!= 0:
            porcentaje[i]=(subsuma[i]*100)/(sum_total)
        else:
            porcentaje[i]=0

    

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)

    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    #Para grafico de pastel
    colores = [
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow',
    'orange', 'purple', 'brown', 'pink', 'gray', 'olive',
    'lime', 'teal', 'navy', 'coral', 'indigo', 'silver',
    'gold', 'orchid'
    ]
    axes.pie(subsuma, labels=None,colors=colores, autopct="%0.1f %%")
    axes.set_title("Distribución de Energía segun "+nombre_filtro +" y segun "+stringvar_Float)
    axes.legend(nombres,
                title="Lista",
                loc="upper center",
                bbox_to_anchor=(1, 0, 0.5, 1))
    
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#funciones para la grafica radar/polar
def elige_polar(container,columnas,filtro_datos,res,columnas_grafico):
    for widget in container.winfo_children():
        widget.destroy()
    
    tk.Label(
                container,
                text="Seleccione que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    
    tk.Button(
            Frame1,
            text="Porcentaje de energia por horas ",
            command=lambda:graficar_datos_radar_horas(container,filtro_datos,columnas,res,columnas_grafico),
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
#graficarradar `por horas`
def graficar_datos_radar_horas(container,filtro_datos,columnas,res,columnas_grafico):
    for widget in container.winfo_children():
        widget.destroy()
    nombre_tabla=columnas[0]
    
    tk.Label(
                container,
                text="seleccione sobre que quiere graficar:",
                justify=tk.CENTER,
                **style.STYLE2
                ).pack(
                side = tk.TOP,
                fill= tk.X,
                #expand=True,
                ipadx= 20,
                ipady= 5,
                padx= 20,
                pady= 5,
                )
    
    def guardar_datos():
        cadena = selected_var.get()
        Grafica_RADAR_segun_cadena_y_hora(nombre_tabla,columnas,filtro_datos,cadena,container)
        #Grafica_RADAR_segun_cadena_y_hora_ultimo(nombre_tabla,columnas,filtro_datos,cadena)


    opciones = devolver_cadenas(columnas)
    selected_var = tk.StringVar()
    selected_var.set(opciones[0])
    
    #nombre_filtro.set("1er filtro")
    
    

    #cadena="EMPRESA"
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    for i in range(len(opciones)):
        opcion=opciones[i]
        radio = tk.Radiobutton(Frame1, text=opcion, variable=selected_var, value=opcion)
        radio.pack(
            side=tk.LEFT,
            fill=tk.X, 
            #expand=True,
            padx=22,
            pady=3, 
        )

    tk.Button(container, text="Guardar datos ", command=guardar_datos).pack()

def Grafica_RADAR_segun_cadena_y_hora(nombre_tabla,columnas,filtro_datos,cadena,container):
    for widget in container.winfo_children():
        widget.destroy()
    nombres_u=nombres_unicos_cadena(nombre_tabla,cadena)
    print(nombres_u)
    nombres=[]

    def guardar_seleccionados():
        seleccionados = []
        for index in list.curselection():
            seleccionados.append(list.get(index))
        #print("Elementos seleccionados:", seleccionados)
        Grafica_RADAR_segun_cadena_y_hora_ultimo(nombre_tabla,columnas,filtro_datos,cadena,seleccionados)
        
    Frame1=tk.Frame(container)
    Frame1.configure(background=style.BACKGROUND
                    )
    Frame1.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    #expand=True,
                    padx=22,
                    pady=3,
                    ) 
    list = tk.Listbox(Frame1, selectmode="multiple")
    list.pack(expand=tk.YES, fill="both")

    for each_item in range(len(nombres_u)):
        list.insert(tk.END, nombres_u[each_item])
        #list.itemconfig(each_item,bg="yellow" if each_item % 2 == 0 else "cyan")

    

    btn_guardar = tk.Button(container, text="Guardar datos y graficar", command=guardar_seleccionados)
    btn_guardar.pack()
  
def Grafica_RADAR_segun_cadena_y_hora_ultimo(nombre_tabla,columnas,filtro_datos,cadena,seleccionados):
    
    nombres=seleccionados
    nro_columnas=len(columnas)-1
    horas = [[0] * 24 for _ in range(len(nombres))]
    
    #buscar psocion de la cadena:
    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]==cadena:
            posicion_cadena=i
    print("posicion cad:"+str(posicion_cadena))

    columnas_a=columnas[1:]
    for i in range(nro_columnas):
        if columnas_a[i]=="H1":
            posicion_H=i
    print("posicion H1:"+str(posicion_H))


    for txt in listdir("Cache\Cache_Graficos"):
        with open("Cache/Cache_Graficos/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                for i, nombre in enumerate(nombres):
                    #print(nombres[i].get())
                    if linea[posicion_cadena]==nombres[i]:
                        
                        for j in range(24):
                            linea_x = linea[posicion_H+j].replace(";", "")
                            horas[i][j]=horas[i][j]+float(linea_x)

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico Radar")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    #figure = Figure(figsize=(10,24),dpi=100)
    # Crear la figura
    figure = Figure(figsize=(8, 8), dpi=100)
    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)
    

    # Crear los subplots para los gráficos
    ax1 = figure.add_subplot(111, polar=True)
    cad_horas=devolver_floats(columnas)
    #axes = figure.add_subplot()
    # Calcular los ángulos para la gráfica polar
    num_categorias = len(cad_horas)
    print("num_categorias")
    print(num_categorias)
    angulos = np.linspace(0, 2 * np.pi, num_categorias, endpoint=False)
    colores = [
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow',
    'orange', 'purple', 'brown', 'pink', 'gray', 'olive',
    'lime', 'teal', 'navy', 'coral', 'indigo', 'silver',
    'gold', 'orchid'
    ]
    for i, nombre in enumerate(nombres):
        sub_horas=horas[i]
        color = colores[i]
        sum_total=sum(sub_horas)
        #datos_normalizados = [d / sum_total for d in sub_horas]

        # Limpiar los arrays para cada iteración
        angulos_plot = angulos.copy()
        datos_plot = sub_horas.copy()

        # Unir el primer elemento con el último para cerrar los gráficos
        datos_plot += datos_plot[:1]
        angulos_plot = np.append(angulos_plot, angulos_plot[0])

        #print(sub_horas)
        
        
        # Graficar cada gráfico de radar en su subplot correspondiente
        ax1.plot(angulos_plot, datos_plot, label=nombre, linewidth=2, linestyle='solid',color=color)
        ax1.set_title("Distribución de Energía por horas, comparando "+cadena)
        ax1.fill(angulos_plot, datos_plot, alpha=0.25,color=color)
        ax1.set_thetagrids(np.degrees(angulos_plot)[:-1], cad_horas)
       
        ax1.legend(title=cadena,
                loc="upper center",
                bbox_to_anchor=(1, 0, 0.5, 1))
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)    

def form_llenar3(container, tabla):
    global filtros_form_grafico, form_combobox
    filtros_form_grafico=[]
    form_combobox=[]
    for widget in container.winfo_children():
        widget.destroy()
    
    columnas = columnas_tabla(tabla)
    tipos=tipos_datos(columnas)
    val_uni = sacar_Dat_Uni_tabla(tabla)
    #print(columnas, tipos)
    titulo_formulario = tk.StringVar()
    titulo_formulario.set(tabla)

    lab = tk.Label(container, text="Formulario "+tabla, font=("Helvetica", 24)).grid(column=0,row=0, sticky=tk.W, columnspan=3, pady=(5,10), padx=10)
    #lab = tk.Label(container, text="").grid(column=0,row=1, columnspan=5)
    col_cad=0
    fila=4
    fila_F=5
    col_flo=0
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    mes = date.strftime("%m")
    #dia = date.strftime("%d")
    for i in range(len(tipos)):
        sw_Cad=False
        sw_Flo=False
        match tipos[i]:
            case "FECHA":
                a=[]
                entry_fecha_ini=tk.StringVar()
                label = tk.Label(container, text = columnas[i]+"INICIO" , font = ('calibre',10,'bold')).grid(column=0,row=2,pady=(10,0))
                ent = tk.Entry(container,textvariable=entry_fecha_ini).grid(column=1,row=2,pady=(10,0)) 
                entry_fecha_fin=tk.StringVar()
                label1 = tk.Label(container, text = columnas[i]+"FIN" , font = ('calibre',10,'bold')).grid(column=0,row=3,pady=(10,0))
                ent1 = tk.Entry(container,textvariable=entry_fecha_fin).grid(column=1,row=3,pady=(10,0))  
                a.append(entry_fecha_ini)
                a.append(entry_fecha_fin)
                filtros_form_grafico.append(a)
            case "AÑO":
                b=[]
                entry_año_ini=tk.StringVar()
                label = tk.Label(container, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).grid(column=0,row=2,pady=(10,0))
                ent2 = tk.Entry(container, textvariable=entry_año_ini)
                ent2.insert(0,year)
                ent2.grid(column=1,row=2,pady=(10,0))  
                entry_año_fin=tk.StringVar()
                label = tk.Label(container, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).grid(column=0,row=3,pady=(10,0))
                ent7 = tk.Entry(container, textvariable=entry_año_fin)
                ent7.insert(0,year)
                ent7.grid(column=1,row=3,pady=(10,0)) 
                b.append(entry_año_ini)
                b.append(entry_año_fin)
                filtros_form_grafico.append(b)
            case "MES":
                d=[]
                entry_mes_ini=tk.StringVar()
                label = tk.Label(container, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).grid(column=2,row=2,pady=(10,0))
                ent3 = tk.Entry(container,textvariable=entry_mes_ini,)
                ent3.insert(0,"01")
                ent3.grid(column=3,row=2,pady=(10,0))
                entry_mes_fin=tk.StringVar()
                label = tk.Label(container, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).grid(column=2,row=3,pady=(10,0))
                ent8 = tk.Entry(container,textvariable=entry_mes_fin,)
                ent8.insert(0,mes)
                ent8.grid(column=3,row=3,pady=(10,0))
                d.append(entry_mes_ini)
                d.append(entry_mes_fin)
                filtros_form_grafico.append(d)
            case "DIA":
                c=[]
                entry_dia_ini=tk.StringVar()
                label = tk.Label(container, text = columnas[i]+" INICIO" , font = ('calibre',10,'bold')).grid(column=4,row=2,pady=(10,0)) 
                ent4 = tk.Entry(container, textvariable=entry_dia_ini)
                ent4.insert(0,"1")
                ent4.grid(column=5,row=2,pady=(10,0))
                entry_dia_fin=tk.StringVar()
                label = tk.Label(container, text = columnas[i]+" FIN" , font = ('calibre',10,'bold')).grid(column=4,row=3,pady=(10,0)) 
                ent10 = tk.Entry(container, textvariable=entry_dia_fin)
                ent10.insert(0,"31")
                ent10.grid(column=5,row=3,pady=(10,0))
                c.append(entry_dia_ini)
                c.append(entry_dia_fin)
                filtros_form_grafico.append(c)           
            case "CADENAS":
                entry_cad=tk.StringVar()
                label = tk.Label(container, text = columnas[i] , font = ('calibre',10,'bold')).grid(column=col_cad,row=fila,pady=(10,0))
                caja_texto=tk.Entry(container, textvariable=entry_cad).grid(column=col_cad+1,row=fila,pady=(10,0))
                filtros_form_grafico.append(entry_cad)
                sw_Cad=True
            case "VALORES_UNICOS":
                l_aux = val_uni[i-1]
                entry_cad=tk.StringVar()
                label = tk.Label(container, text = columnas[i] , font = ('calibre',10,'bold')).grid(column=col_cad,row=fila,pady=(10,0))
                lista_opciones = ttk.Combobox(container,textvariable=entry_cad)
                lista_opciones['values'] = l_aux[1:]
                lista_opciones['state'] = 'readonly'
                lista_opciones.bind("<<ComboboxSelected>>",elemento_seleccionado)
                lista_opciones.grid(column=col_cad+1,row=fila,pady=(10,0))
                form_combobox.append(lista_opciones)
                filtros_form_grafico.append(entry_cad)
                sw_Cad=True
            case "FLOAT":
                check_button_var = tk.IntVar()
                check_button_var.set(1)
                check = tk.Checkbutton(container, text=columnas[i], font = ('calibre',10,'bold'), variable=check_button_var).grid(column=col_flo,row=fila_F ,pady=(10,0))
                #label = tk.Label(container, text = columnas[i] , font = ('calibre',10,'bold')).grid(column=col_flo,row=fila_F)
                sw_Flo=True
                filtros_form_grafico.append(check_button_var)

        if sw_Cad:
            col_cad+=2
            if col_cad==6:
                col_cad=0
                fila+=1
                fila_F=fila+3
        
        if sw_Flo:
            col_flo+=1
            if col_flo==6:
                col_flo=0
                fila_F+=1
    
    boton_enviar=tk.Button(container, text="GRAFICAR", command=lambda: graficar_datos(columnas,tipos)).grid(column=9,row=fila_F+1 ,pady=(10,0))

def elemento_seleccionado(event):
    global filtros_form_grafico, form_combobox, form_tabla
    #for posicion in form_posiciones_val_unicos:
    #    print(filtros_form_grafico[posicion-1].get())
    #print(form_tabla)
    enlaces = sacar_enlaces(form_tabla)
    tipos = tipos_datos(columnas_tabla(form_tabla))
    matriz_uni = sacar_Dat_Uni_tabla(form_tabla)
    matriz_aux = []
    #print(enlaces)
    #print(tipos)
    longi = len(tipos)
    #print(matriz_uni)
    filtros_unicos = []
    sw = False
    for combo in form_combobox:
        valor = combo.get()
        filtros_unicos.append(valor)
        if valor != "":
            sw = True
    
    if sw:
        c=0
        for i in range(longi):
            if tipos[i] == 'VALORES_UNICOS':
                casilla = filtros_unicos[c]
                matriz_aux.append(matriz_uni[i-1])
                if casilla != "":
                    filtros_unicos[c] = matriz_uni[i-1].index(casilla)
                c+=1
        #print(filtros_unicos)
        #print(enlaces)
        #res = []
        col_fin = [0]*c
        for i in range(c):
            col_fin[i] = set()

        for enlace in enlaces:
            sw = True
            enlace = enlace.split(",")
            #print(enlace)
            for i in range(c):
                if filtros_unicos[i] != "":
                    #print(filtros_unicos[i], enlace[i])
                    if str(filtros_unicos[i]) != enlace[i]:
                        sw = False
                        break
            if sw:
                #res.append(enlace)
                for j in range(c):
                    col_fin[j].add(enlace[j]) 
        #print(res)
        #print("Cols")
        #print(col_fin)
        #print(matriz_aux)
        col_convert=[0]*c

        for i in range(c):
            if filtros_unicos[i] == "":
                col = col_fin[i]
                #print(col, matriz_aux[i])
                aux = []
                for can in col:
                    #print(can)
                    aux.append(matriz_aux[i][int(can)])
                col_convert[i] = aux
            else:
                col_convert[i] = matriz_aux[i]
        
        #print(col_convert)

        ai=0
        for combo in form_combobox:
            combo['values'] = col_convert[ai]
            ai+=1

def tabla_datos(columnas, tipos):
    global filtros_form_grafico
    tipos=tipos[1:]
    tabla = columnas[0]
    nro_columnas=len(columnas)-1
    filtro_datos = [0]*(nro_columnas)

    c=0
    #print(filtros_form_grafico)
    for filtro_form in filtros_form_grafico:
        #print(filtro_form)
        if type(filtro_form) == type(columnas):
            a=filtro_form[0]
            b=filtro_form[1]
            if int(a.get())==int(b.get()):
                filtro_datos[c]="Igual F"
            else:
                filtro_datos[c]="Entre"
            c+=1
        else:
            if filtro_form.get() == "":
                filtro_datos[c]="Pasar"
            elif tipos[c] == "FLOAT":
                filtro_datos[c]="Pasar"
            elif tipos[c] == "VALORES_UNICOS":
                filtro_datos[c]="Decodificar"
            else:
                if tipos[c] == "CADENAS":
                    filtro_datos[c]="Igual"
                    #print(filtro_form.get(), type(filtro_form.get()))
                       
            c+=1

    #print(filtro_datos)
    #print(tabla)
    
    rmtree("Cache/Cache_Texto")   
    os.mkdir("Cache/Cache_Texto")
    val_unicos = sacar_Dat_Uni_tabla(tabla)
    sw_decodificar=False
    if "VALORES_UNICOS" in tipos:
        sw_decodificar=True
    sw=True
    for txt in listdir("Ficheros/Tablas/"+tabla):
        nom_Cache="cache"+txt
        file_cache = open("Cache/Cache_Texto/"+nom_Cache, "w", encoding="utf-8")
        with open("Ficheros/Tablas/"+tabla+"/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";;")
                sw=True
                aux_c=0
                #print(linea, len(linea), nro_columnas)
                for i in range(nro_columnas):
                    filtro = filtro_datos[i]
                    casilla=linea[i]
                    if filtro=="Pasar":
                        #print("Paso")
                        pass
                    elif filtro=="Igual":
                        if filtros_form_grafico[i].get() != casilla:
                            sw=False
                            #print("No es Igual")
                            break
                    elif filtro=="Igual F":
                        if filtros_form_grafico[i][0].get() != casilla:
                            sw=False
                            #print("No es Igual Fecha")
                            break
                    elif filtro=="Entre":
                        filtros = filtros_form_grafico[i]
                        casilla= int(casilla)
                        inicial = int(filtros[0].get())
                        final = int(filtros[1].get())
                        if casilla >= inicial and casilla <= final:
                            pass
                        else:
                            sw=False
                            #print("No entre")
                            break
                    elif filtro == "Decodificar":
                        linea_uni = val_unicos[i]
                        val = filtros_form_grafico[i].get()
                        #print(linea_uni, val,linea_uni.index(val), casilla)
                        
                        if casilla != str(linea_uni.index(val)):
                            sw=False
                            break
                    else:
                        print("Error al ejecutar filtros")
                        print(tabla, txt)
                        print(linea)
                if sw:
                    if sw_decodificar:
                        linea_aux = decodificar_linea(linea_aux,tipos,val_unicos)
                    file_cache.write(linea_aux+'\n')
        file_cache.close()
    
def graficar_datos(columnas,tipos):
    global filtros_form_grafico
    #print(filtros_form_grafico)
    tipos=tipos[1:]
    tabla = columnas[0]
    num_datos_para_grafico=0
    nro_columnas=len(columnas)-1
    filtro_datos = [0]*(nro_columnas)
    columnas_grafico=[]

    #lista_año=[]
    #lista_mes = []
    #for filtro in filtros_form_grafico:
        #print(filtro)
    #print(filtros_form_grafico,columnas,tipos)
    #print(len(filtros_form_grafico), len(columnas), len(tipos))
    c=0
    for filtro_form in filtros_form_grafico:
        if type(filtro_form) == type(columnas):
            if tipos[c] == "FECHA":
                a = time.strptime(filtro_form[0].get(), "%Y-%m-%d")
                b = time.strptime(filtro_form[1].get(), "%Y-%m-%d")

                año_1 = a.tm_year
                año_2 = b.tm_year
                mes_1 = a.tm_mon
                mes_2 = b.tm_mon
                dia_1 = a.tm_mday
                dia_2 = b.tm_mday

                sw_año=True
                sw_mes=True
                sw_dia=True

                l_años = listdir("Ficheros/Tablas/"+tabla)
                l_mes = listdir("Ficheros/Tablas/"+tabla+"/"+l_años[0])

                l_aux = l_mes[0]
                len_aux = l_aux.count(",") +1
                l_m_a = []

                caux = 0
                m_a = []
                #m_a = ""
                for i in range(1,13):
                    m_a.append(i)
                    #m_a+=str(i)
                    caux+=1
                    if caux == len_aux:
                        caux = 0
                        l_m_a.append(m_a)
                        m_a = []
                        #m_a = ""
                l_mes = l_m_a
                #print(l_m_a)

                # Si es necesario guardar archivos por dia
                #l_dia = listdir("Ficheros/Tablas/"+tabla+"/"+l_años[0]+"/"+l_mes[0])
                
                #print(l_años)
                #print(l_mes)
                #print(dia_1, dia_2)

                lista_año = []
                lista_mes = []
                if a == b:
                    filtro_datos[c]="Igual F"
                    if año_1 in l_años:
                        lista_año = [año_1]
                    else: 
                        sw_año = False
                    
                    if mes_1 in l_mes:
                        lista_mes = [mes_1]
                    else: 
                        sw_mes = False
                else:
                    filtro_datos[c]="Entre Fechas"
                    
                    if año_1 == año_2:
                        if año_1 in l_años:
                            lista_año = [año_1]
                        else: 
                            sw_año = False
                    else:
                        lista_año = []
                        for año in l_años:
                            if int(año) >= año_1 and int(año) <= año_2:
                                lista_año.append(año)
                        if lista_año == []:
                            sw_año = False

                    if mes_1 == mes_2:
                        for grupo_mes in l_mes:
                            if int(mes_1) in grupo_mes:
                                lista_mes = [grupo_mes]
                                break
                        if lista_mes == []:
                            sw_mes = False
                    else:
                        lista_mes = []
                        #print(mes_1,mes_2)
                        for grupo_mes in l_mes:
                            #print(mes, grupo_mes)
                            for mes in grupo_mes:
                                if mes_1 <= mes and mes <= mes_2:
                                    lista_mes.append(grupo_mes)
                                    break
                        if lista_mes == []:
                            sw_mes = False
                #print(lista_año, sw_año)
                #print(lista_mes, sw_mes)

            elif tipos[c] == "AÑO":
                a = int(filtro_form[0].get())
                b = int(filtro_form[1].get())
                l_años = listdir("Ficheros/Tablas/"+tabla)
                #print(a, b)
                #print(l_años)
                if a == b:
                    filtro_datos[c]="Igual F"
                    if str(a) in l_años:
                        lista_año = [a]
                    else: 
                        lista_año = []
                        sw_año = False
                    #print("Lista Año:", lista_año)
                else:
                    filtro_datos[c]="Entre"
                    lista_año = []
                    for año in l_años:
                        if a <=int(año) and int(año) <= b:
                            lista_año.append(año)
                    if lista_año == []:
                        lista_año = []
                        sw_año = False
                    #print("Lista Año:", lista_año)

            elif tipos[c] == "MES":
                l_mes = listdir("Ficheros/Tablas/"+tabla+"/"+str(lista_año[0]))
                #print(l_mes)
                l_aux = l_mes[0]
                len_aux = l_aux.count(",") +1
                l_m_a = []

                caux = 0
                m_a = []
                #m_a = ""
                for i in range(1,13):
                    m_a.append(i)
                    #m_a+=str(i)
                    caux+=1
                    if caux == len_aux:
                        caux = 0
                        l_m_a.append(m_a)
                        m_a = []
                        #m_a = ""
                l_mes = l_m_a

                a = int(filtro_form[0].get())
                b = int(filtro_form[1].get())

                if a == b:
                    filtro_datos[c]="Igual F"
                    for grupo_mes in l_mes:
                        if int(a) in grupo_mes:
                            lista_mes = [grupo_mes]
                            break
                    if lista_mes == []:
                        sw_mes = False
                else:
                    filtro_datos[c]="Entre"
                    lista_mes = []
                    #print(mes_1,mes_2)
                    for grupo_mes in l_mes:
                        #print(mes, grupo_mes)
                        for mes in grupo_mes:
                            if a <= int(mes) and int(mes) <= b:
                                lista_mes.append(grupo_mes)
                                break
                    if lista_mes == []:
                        sw_mes = False
            
            elif tipos[c] == "DIA":
                a = int(filtro_form[0].get())
                b = int(filtro_form[1].get())

                if a == b:
                    filtro_datos[c]="Igual F"
                else:
                    filtro_datos[c]="Entre"
            c+=1
        else:
            if filtro_form.get() == "":
                filtro_datos[c]="Pasar"
            else:
                if tipos[c] == "CADENAS":
                    filtro_datos[c]="Igual"
                    #print(filtro_form.get(), type(filtro_form.get()))
                elif tipos[c] == "FLOAT":
                    if filtro_form.get()==1:
                        filtro_datos[c]="Sumar"
                        num_datos_para_grafico+=1
                        columnas_grafico.append(columnas[c+1])
                    else:
                        filtro_datos[c]="Pasar"
                elif tipos[c] == "VALORES_UNICOS":
                    filtro_datos[c]="Decodificar"         
            c+=1
    #print(filtro_datos)
    res=[0]*num_datos_para_grafico
    res_aux=[0]*num_datos_para_grafico

    #print(tabla)
    val_unicos = sacar_Dat_Uni_tabla(tabla)
    sw_decodificar=False
    if "VALORES_UNICOS" in tipos:
        sw_decodificar=True

    rmtree("Cache/Cache_Graficos")   
    os.mkdir("Cache/Cache_Graficos")
    sw=True
    #print(lista_mes)
    lista_mes_aux = []
    for grupo in lista_mes:
        grup = ""
        if len(grupo)<2:
            grup = str(grupo[0])
        else:
            for num in grupo[:-1]:
                grup+=str(num)+","
            grup+=str(grupo[-1])
        lista_mes_aux.append(grup)
    #print(lista_mes_aux)
    lista_mes = lista_mes_aux
    #print(lista_mes)
    for año in lista_año:
        año= str(año)
        #print(año)
        
        for mes in listdir("Ficheros/Tablas/"+tabla+"/"+año):
            #print(mes)
            for grupo_mes in lista_mes:
                #print(grupo_mes, mes, año)
                if mes in grupo_mes:
                    #print("si")
                    for txt in listdir("Ficheros/Tablas/"+tabla+"/"+año+"/"+mes):
                        nom_Cache="c-"+año+"-"+mes+"-"+txt
                        file_cache = open("Cache/Cache_Graficos/"+nom_Cache, "w", encoding="utf-8")

                        with open("Ficheros/Tablas/"+tabla+"/"+año+"/"+mes+"/"+txt,"r",encoding="utf-8") as archivo:
                            for linea in archivo:
                                linea=linea.strip("\n")
                                linea_aux=linea
                                linea=linea.split(";;")
                                sw=True
                                aux_c=0
                                for i in range(nro_columnas):
                                    filtro = filtro_datos[i]
                                    casilla=linea[i]
                                    if filtro=="Pasar":
                                        #print("Paso")
                                        pass
                                    elif filtro=="Sumar":
                                        res_aux[aux_c]=float(casilla)
                                        aux_c+=1
                                        #print("sumar")
                                    elif filtro=="Igual":
                                        if filtros_form_grafico[i].get() != casilla:
                                            sw=False
                                            #print("No es Igual")
                                            break
                                    elif filtro=="Igual F":
                                        if filtros_form_grafico[i][0].get() != casilla:
                                            sw=False
                                            #print("No es Igual Fecha")
                                            break
                                    elif filtro=="Entre":
                                        filtros = filtros_form_grafico[i]
                                        casilla= int(casilla)
                                        inicial = int(filtros[0].get())
                                        final = int(filtros[1].get())
                                        if casilla >= inicial and casilla <= final:
                                            pass
                                        else:
                                            sw=False
                                            #print("No entre")
                                            break
                                    elif filtro=="Entre Fechas":
                                        filtros = filtros_form_grafico[i]
                                        casilla= time.strptime(casilla, "%Y-%m-%d")
                                        inicial = time.strptime(filtros[0].get(), "%Y-%m-%d")
                                        final = time.strptime(filtros[1].get(), "%Y-%m-%d")
                                        if casilla >= inicial and casilla <= final:
                                            pass
                                        else:
                                            sw=False
                                            #print("No entre Fechas")
                                            break
                                    elif filtro == "Decodificar":
                                        linea_uni = val_unicos[i]
                                        val = filtros_form_grafico[i].get()
                                        #print(linea_uni, val,linea_uni.index(val), casilla)
                                        
                                        if casilla != str(linea_uni.index(val)):
                                            sw=False
                                            break
                                    else:
                                        #print(filtro)
                                        print("Error al ejecutar filtros")
                                        #print(tabla, txt)
                                        #print(linea)
                                        pass
                                if sw:
                                    for i in range(num_datos_para_grafico):
                                        res[i]+=res_aux[i]
                                    if sw_decodificar:
                                        linea_aux = decodificar_linea(linea_aux, tipos, val_unicos)
                                    file_cache.write(linea_aux+'\n')

                        file_cache.close()
                    #print(res)
                    #print(columnas_grafico)

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)

    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    #Para grafico de pastel
    #axes.pie(res, labels=columnas_grafico)
    
    #Para el Gráfico de Barras
    axes.bar(columnas_grafico, res)
    axes.set_title('Columnas de Gráfico')
    axes.set_ylabel('Sumatoria de Datos')

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    """
    for txt in listdir("Ficheros/Tablas/"+tabla):
        nom_Cache="cache"+txt
        file_cache = open("Cache/Cache_Graficos/"+nom_Cache, "w", encoding="utf-8")
        
        with open("Ficheros/Tablas/"+tabla+"/"+txt,"r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea_aux=linea
                linea=linea.split(";")
                sw=True
                aux_c=0
                for i in range(nro_columnas):
                    filtro = filtro_datos[i]
                    casilla=linea[i]
                    if filtro=="Pasar":
                        #print("Paso")
                        pass
                    elif filtro=="Sumar":
                        res_aux[aux_c]=float(casilla)
                        aux_c+=1
                        #print("sumar")
                    elif filtro=="Igual":
                        if filtros_form_grafico[i].get() != casilla:
                            sw=False
                            #print("No es Igual")
                            break
                    elif filtro=="Igual F":
                        if filtros_form_grafico[i][0].get() != casilla:
                            sw=False
                            #print("No es Igual Fecha")
                            break
                    elif filtro=="Entre":
                        filtros = filtros_form_grafico[i]
                        casilla= int(casilla)
                        inicial = int(filtros[0].get())
                        final = int(filtros[1].get())
                        if casilla >= inicial and casilla <= final:
                            pass
                        else:
                            sw=False
                            #print("No entre")
                            break
                    elif filtro == "Decodificar":
                        linea_uni = val_unicos[i]
                        val = filtros_form_grafico[i].get()
                        #print(linea_uni, val,linea_uni.index(val), casilla)
                        
                        if casilla != str(linea_uni.index(val)):
                            sw=False
                            break
                    else:
                        print("Error al ejecutar filtros")
                        print(tabla, txt)
                        print(linea)
                if sw:
                    for i in range(num_datos_para_grafico):
                        res[i]+=res_aux[i]
                    if sw_decodificar:
                        linea_aux = decodificar_linea(linea_aux, tipos, val_unicos)
                    file_cache.write(linea_aux+'\n')

        file_cache.close()
                    
    #print(res)
    #print(columnas_grafico)

    ventana_grafico = tk.Toplevel()
    ventana_grafico.title("Gráfico")
    ventana_grafico.minsize(400,500)
    ventana_grafico.config(background="#ccc")

    figure = Figure(figsize=(10,4),dpi=100)

    figure_canvas = FigureCanvasTkAgg(figure, ventana_grafico)

    NavigationToolbar2Tk(figure_canvas, ventana_grafico)

    axes = figure.add_subplot()
    #Para grafico de pastel
    #axes.pie(res, labels=columnas_grafico)
    
    #Para el Gráfico de Barras
    axes.bar(columnas_grafico, res)
    axes.set_title('Columnas de Gráfico')
    axes.set_ylabel('Sumatoria de Datos')

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    """
    #--- Separacion

    """
                    

                    l_mes = listdir("Ficheros/Tablas/"+tabla+"")
                    
                    
                    if año_1 == año_2:
                        lista_año = [año_1]
                    else:
                        lista_año = []
                        for año in l_años:
                            if año >= año_1 and año <= año_2:
                                lista_año.append(año)
                    
                    lista_mes = [mes_1]
                    lista_dia = [dia_1]

                print(año_1,año_2)
                print(mes_1,mes_2)
                print(dia_1,dia_2)



            else:
                a=filtro_form[0]
                b=filtro_form[1]
                if int(a.get())==int(b.get()):
                    filtro_datos[c]="Igual F"
                else:
                    filtro_datos[c]="Entre"
            print(a, b, filtro_datos[c])
            
    """

def decodificar_linea(linea, tipos, matriz):
    linea = linea.split(";;")
    longi = len(tipos)
    res = ""
    #print(linea, tipos, matriz, len(linea), len(tipos))
    for i in range(longi):
        if tipos[i] == "VALORES_UNICOS":
            linea[i] = matriz[i][int(linea[i])]
        res+=linea[i]+";;"
    return res[:-2]

class Grafico(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background= style.PLOMO)
        self.controller = controller
        self.graficoMode = tk.StringVar(self,value="Grafico")
        self.init_widgets()
        #self.menu_arriba()
        #self.lista_Tablas("GRAFICO")
        #self.form_grafico()


    def move_to_graficos(self):
        self.controller.mode= self.graficoMode.get()
        self.controller.show_frame(Grafico)
    def move_to_ftexto(self):
        self.controller.show_frame(Texto)
    def move_to_cargar(self):
        self.controller.show_frame(Excel)
    def move_to_agregar(self):
        self.controller.show_frame(Nuevo)

    def ventana_grafico(self):
        top1= tk.Toplevel(self.controller)
        top1.config.grafico(top1,self)

    def leer_tabla_de_grafico(self):
        archivo = open("Ficheros\Datos_tablas\TABLAS_DE_GRAFICOS.txt", "r")
        contenido = archivo.read()
        print(contenido)
        lineas_grafico = contenido.strip("\n")
        lineas_grafico = contenido.split(",")
        print("lineas grafico")
        print(lineas_grafico)
        archivo.close()
        return lineas_grafico
    
    
    def seleccionar_elemento(self,lista_tablas,options_frame, event):
        seleccion = lista_tablas.get(lista_tablas.curselection())
        form_llenar(options_frame,seleccion)

    def init_widgets(self):
        Frame1=tk.Frame(self)
        Frame1.configure(background=style.BACKGROUND
                               )
        Frame1.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            #expand=True,
            padx=12,
            pady=5
        )   
        tk.Button(
            Frame1,
            text="Cargar archivo",
            command=self.move_to_cargar,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )

        tk.Button(
            Frame1,
            text="Graficos",
            command=self.move_to_graficos,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Button(
            Frame1,
            text="Filtros de texto",
            command=self.move_to_ftexto,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Button(
            Frame1,
            text="Agregar/Eliminar",
            command=self.move_to_agregar,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Label(
            self,
            text="Graficos",
            justify=tk.CENTER,
            **style.STYLE
            ).pack(
            side = tk.TOP,
            fill= tk.BOTH,
            padx= 22,
            pady= 5
            )
        
        optionsFrame=tk.Frame(self)
        optionsFrame.configure(background="white"
                               )
        optionsFrame.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=True,
            padx=22,
            pady=11
        )
        tk.Label(
            self,
            text="Tablas:",
            justify=tk.CENTER,
            **style.STYLE
            ).pack(
            side = tk.TOP,
            fill= tk.X,
            ipadx= 20,
            ipady= 5,
            padx= 20,
            pady= 10,
            )
        lista_tablas=tk.Listbox(
            self,
            width=30, 
            height=20
            )
        lista_tablas.pack(
            side = tk.TOP,
            fill= tk.X,
            ipadx= 10,
            ipady= 5,
            padx= 20,
            pady= 10,
            )
        lista=self.leer_tabla_de_grafico()

        for elemento in lista:
            lista_tablas.insert(tk.END, elemento)
        
            
        lista_tablas.bind("<<ListboxSelect>>", lambda event: self.seleccionar_elemento(lista_tablas,optionsFrame, event))

        


    def lista_Tablas(self, tipo):
        menu_lista = tk.LabelFrame(self, width=400)
        menu_lista.config(background="#16979A")

        scroll_vertical = tk.Scrollbar(menu_lista, orient='vertical')

        if tipo == "TEXTO":
            archivo = open("Ficheros/Datos_tablas/TABLA_DE_TEXTO.txt", "r",encoding="utf-8")
        elif tipo == "GRAFICO":
            archivo = open("Ficheros/Datos_tablas/TABLAS_DE_GRAFICOS.txt", "r", encoding="utf-8")
        else:
            print("Error al abrir la archivo")

        lista=[]
        for linea in archivo:
            linea=linea.strip("\n")
            linea=linea.split(",")
        lista = linea

        archivo.close()
        
        for tabla in lista:
            bot = tk.Button(menu_lista, text=tabla, width=20, anchor="w", command=lambda texto=tabla:form_llenar(self.children['!labelframe3'],texto)).pack(pady=5, padx=10)

        #scroll_vertical.pack(side="left",fill="y")

        #scroll_vertical.config(command=tk.YView)
        menu_lista.pack(fill="y", side="left")

    def form_grafico(self):
        formulario = tk.LabelFrame(self)
        formulario.config(background="#D9D9D9")
        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(2, weight=1)
        formulario.columnconfigure(3, weight=1)
        formulario.columnconfigure(4, weight=1)
        formulario.columnconfigure(5, weight=1)
        formulario.columnconfigure(6, weight=1)
        formulario.columnconfigure(7, weight=1)
        formulario.columnconfigure(8, weight=1)
        formulario.columnconfigure(9, weight=1)
        formulario.pack(fill="both",expand=True)
         
lista_radio=[]
lista_variables=[]
lista_labels=[]
boton_guardar=0

def entry_excel(container):
    global lista_radio, lista_variables, lista_labels, boton_guardar
    files = askopenfiles(mode="r", filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')])
    aux_fila=1

    for widget in container.children['!labelframe'].winfo_children():
        widget.destroy()

    btn = tk.Button(container.children['!labelframe'], text ='Seleccionar Excel', command = lambda: entry_excel(container))
    btn.grid(column=0,row=0)

    lista_radio=[0]*len(files)
    lista_labels=[0]*len(files)
    lista_variables=[0]*len(files)
    c=0

    rmtree("Cache/Cache_Entrada")   
    os.mkdir("Cache/Cache_Entrada")
    
    sw=True
    for file in files:
        columnas=[]
        
        
        nombre = file.name.split("/")
        nombre = nombre[-1]
        nombre_Cache = nombre[:-5]

        file_cache = open("Cache/Cache_Entrada/"+str(c)+" "+nombre_Cache+".txt", "w", encoding="utf-8")

        excel = pd.read_excel(file.name)

        for columna in excel.columns:
            if "Unnamed" in str(columna):
                break
            else:
                columnas.append(columna) 
        #print(columnas)
        tablas = detectar_tabla(columnas)
        longitud = len(columnas)
        if len(tablas)>0:
            for i in excel.values:
                k=''
                for j in range(longitud-1):
                    a=i[j]
                    if type(a) == "str":
                        a=a.encode('utf-8')
                    k+=str(a)+';;' 
                f1=i[longitud-1]
                if type(a) == "str":
                    f1=f1.encode('utf-8')
                k+=str(f1)
                file_cache.write(k+'\n')
            file_cache.close()
        #print(tablas)
        
        # container.children['!labelframe2']

        label = tk.Label(container.children['!labelframe'], text=nombre).grid(column=0, row=aux_fila)
        #lista_labels[c] = tk.Label(container.children['!labelframe2'], text=tablas[0]).grid(column=1, row=aux_fila, pady=10)
        st_label=tk.StringVar()
        if len(tablas)==0:
            st_label=tk.StringVar(value="No se reconocio la tabla")
            label_aux = tk.Label(container.children['!labelframe'], textvariable=st_label).grid(column=1, row=aux_fila, pady=10)
        elif len(tablas)>1:
            sw=False
            #ayu=[]
            #aux = tk.StringVar(container.children['!labelframe2'], tabla)
            st_label=tk.StringVar(value="Escoje una opción")
            label_aux = tk.Label(container.children['!labelframe'], textvariable=st_label).grid(column=1, row=aux_fila, pady=10)
            aux= tk.StringVar()
            for tabla in tablas:
                
                lista_radio[c] = tk.Radiobutton(
                    container.children['!labelframe'],
                    text=tabla, value=tabla, variable = aux , command=lambda c=c: asignar_texto(c)
                ).grid(column=2,row=aux_fila)
                aux_fila+=1
                #ayu.append(aux)
            lista_variables[c]=aux
        else:
            st_label=tk.StringVar(value=tablas[0])
            label_aux = tk.Label(container.children['!labelframe'], textvariable=st_label).grid(column=1, row=aux_fila, pady=10)
        lista_labels[c]= st_label
        aux_fila+=1
        c+=1
    
    if sw:
        boton_guardar = tk.Button(container.children['!labelframe'], text ='Guardar Excel', command = lambda: guardar_excel())
        boton_guardar.grid(column=5,row=aux_fila)
    else:
        boton_guardar = tk.Button(container.children['!labelframe'], text ='Guardar Excel', command = lambda: guardar_excel(), state="disabled")
        boton_guardar.grid(column=5,row=aux_fila)

def asignar_texto(c):
    global lista_variables, lista_labels, boton_guardar
    #print(text, v.get())
    #print(lista_variables, lista_radio)
    #print(lista_variables[c], lista_radio[c])
    #print(lista_labels)
    
    tabla_Elegida = lista_variables[c].get()
    lista_labels[c].set(tabla_Elegida)

    sw=True
    for label in lista_labels:
        if label.get() == "Escoje una opción":
            sw=False
            break
    if sw:
        boton_guardar.config(state="normal")

    #print(tabla_Elegida, lista_radio[c], lista_labels[c])

def tiempoFormat_hms(entrada): 
    a = ""
    try: 
        formato_hora = time.strptime(entrada, '%H:%M:%S') 
        a = str(formato_hora.tm_hour) + ":" + str(formato_hora.tm_min)
        return True, a 
    except ValueError: 
        return False, a 

def tiempoFormat_hm(entrada): 
    a = ""
    try: 
        formato_hora = time.strptime(entrada, '%H:%M') 
        a = str(formato_hora.tm_hour) + ":" + str(formato_hora.tm_min)
        return True, a 
    except ValueError: 
        return False, a 

def tiempoFormat_f_hms(entrada): 
    a = ""
    try: 
        formato_hora = time.strptime(entrada, '%Y-%m-%d %H:%M:%S') 
        a = str(formato_hora.tm_hour) + ":" + str(formato_hora.tm_min)
        return True, a 
    except ValueError: 
        return False, a 

def tiempoFormat_f2_hms(entrada): 
    a = ""
    try: 
        formato_hora = time.strptime(entrada, '%Y/%m/%d %H:%M:%S') 
        a = str(formato_hora.tm_hour) + ":" + str(formato_hora.tm_min)
        return True, a 
    except ValueError: 
        return False, a 
    
def fechaFormat1(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%Y-%m-%d %H:%M:%S') 
        a = str(formato_fecha.tm_mday) + "/" + str(formato_fecha.tm_mon) + "/" + str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 

def fechaFormat2(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%Y/%m/%d %H:%M:%S') 
        a = str(formato_fecha.tm_mday) + "/" + str(formato_fecha.tm_mon) + "/" + str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 

def fechaFormat3(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%Y-%m-%d') 
        a = str(formato_fecha.tm_mday) + "/" + str(formato_fecha.tm_mon) + "/" + str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 

def fechaFormat4(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%Y/%m/%d') 
        a = str(formato_fecha.tm_mday) + "/" + str(formato_fecha.tm_mon) + "/" + str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 

def fechaFormat5(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%d-%m-%Y') 
        a = str(formato_fecha.tm_mday) + "/" + str(formato_fecha.tm_mon) + "/" + str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 

def fechaFormat6(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%d/%m/%Y') 
        a = str(formato_fecha.tm_mday) + "/" + str(formato_fecha.tm_mon) + "/" + str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 

def fechaFormat7(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%d-%m-%Y %H:%M:%S') 
        a = str(formato_fecha.tm_mday) + "/" + str(formato_fecha.tm_mon) + "/" + str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 

def fechaFormat8(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%d/%m/%Y %H:%M:%S') 
        a = str(formato_fecha.tm_mday) + "/" + str(formato_fecha.tm_mon) + "/" + str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 
    
def diaFormat(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%d') 
        a = str(formato_fecha.tm_mday)
        return True, a 
    except ValueError: 
        return False, a 
    
def mesFormat(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%m') 
        a = str(formato_fecha.tm_mon) 
        return True, a 
    except ValueError: 
        return False, a 
    
def añoFormat(entrada): 
    a = ""
    try: 
        formato_fecha = time.strptime(entrada, '%Y') 
        a = str(formato_fecha.tm_year)
        return True, a 
    except ValueError: 
        return False, a 
    
def guardar_excel():
    dic_unicas=dict()
    dic_enlaces = dict()
    lista_cache = listdir("Cache/Cache_Entrada")
    global lista_labels

    #-- Sacar las matrices con los datos unicos requeridos --
    # eliminando las posibles repeticiones de tablas
    aux_cache = 0

    for label in lista_labels:
        tabla = label.get()
        if tabla != "No se reconocio la tabla":
            nombre_unico_txt(lista_cache[aux_cache], tabla)
            aux_cache+=1
            if tabla not in dic_unicas: 
                dic_unicas[tabla]=sacar_Dat_Uni_tabla(tabla)
                dic_enlaces[tabla]=sacar_enlaces(tabla)
    
    c = 0
    lista_cache = listdir("Cache/Cache_Entrada")

    lista_ubi = []

    for label in lista_labels:
        tabla = label.get()
        if tabla != "No se reconocio la tabla":
            nom = lista_cache[c]
            nom = nom[2:]
            ubi = tabla+"/"+nom
            lista_ubi.append(ubi)
            archivo = open("Ficheros/Tablas/"+tabla+"/"+nom,"w",encoding="utf-8")

            cache = open("Cache/Cache_Entrada/"+lista_cache[c], "r", encoding="utf-8")
            
            matriz_unico = dic_unicas[tabla]
            matriz_enlace = dic_enlaces[tabla]
            tipos = tipos_datos(columnas_tabla(tabla))
            tipos = tipos[1:]
            if "VALORES_UNICOS" in tipos:
                sw_enlaces = True
            else:
                sw_enlaces = False

            if "HORAS" in tipos:
                sw_horas = True
            else:
                sw_horas = False

            if "FLOAT" in tipos:
                sw_float = True
            else:
                sw_float = False

            if "FECHA" in tipos or "AÑO" in tipos or "MES" in tipos or "DIA" in tipos:
                sw_fecha_Rev = True
            else:
                sw_fecha_Rev = False

            sw_fecha = False
            fecha_mayor = "1/1/1900"
            fecha_menor = "31/12/2200"
            sw_año = False
            sw_mes = False
            mes = set()
            sw_float_neg =False
            #print(tipos)
            #print(matriz_unico)
            #print("Enlaces sacar")
            #print(matriz_enlace)
            sw_error_año = False
            sw_error_mes = False
            sw_error_dia = False
            sw_error_fecha = False
            sw_error_hora = False
            sw_eliminar = False
            casilla_error = ""
            cont_linea = 0
            for linea in cache:
                linea_aux = ""
                linea=linea.strip("\n")
                linea=linea.split(";;")
                cont_linea += 1
                #print(linea)
                aux_col = 0
                if sw_enlaces or sw_fecha_Rev or sw_horas or sw_float:
                    enlaces_aux = []
                    #print(linea)
                    for casilla in linea:
                        #print(aux_col)
                        tipo = tipos[aux_col]
                        
                        if tipo == "VALORES_UNICOS":
                            # -- Revisamos si ya esta en los datos unicos
                            if casilla not in matriz_unico[aux_col]:
                                matriz_unico[aux_col].append(casilla)
                            id_enlace = matriz_unico[aux_col].index(casilla)
                            
                            enlaces_aux.append(str(id_enlace))
                            
                            linea_aux += (";;" + str(id_enlace))
                        elif tipo == "HORAS":
                            sw_horita1, horita1 = tiempoFormat_hms(casilla)
                            sw_horita2, horita2 = tiempoFormat_hm(casilla)
                            sw_horita3, horita3 = tiempoFormat_f_hms(casilla)
                            sw_horita4, horita4 = tiempoFormat_f2_hms(casilla)
                            if sw_horita1:
                                casilla = horita1
                            elif sw_horita2:
                                casilla = horita2
                            elif sw_horita3:
                                casilla = horita3
                            elif sw_horita4:
                                casilla = horita4
                            else:
                                casilla_error=casilla
                                sw_error_hora = True
                            linea_aux += (";;" + casilla) 
                        elif tipo == "FLOAT":
                            if float(casilla) < 0:
                                casilla = 0
                                sw_float_neg = True
                            linea_aux += (";;" + casilla) 
                        else:
                            if tipo == "FECHA":
                                sw_fechita1, fechita1 = fechaFormat1(casilla)
                                sw_fechita2, fechita2 = fechaFormat2(casilla)
                                sw_fechita3, fechita3 = fechaFormat3(casilla)
                                sw_fechita4, fechita4 = fechaFormat4(casilla)
                                sw_fechita5, fechita5 = fechaFormat5(casilla)
                                sw_fechita6, fechita6 = fechaFormat6(casilla)
                                sw_fechita7, fechita7 = fechaFormat7(casilla)
                                sw_fechita8, fechita8 = fechaFormat8(casilla)
                                formato_fecha_mayor = time.strptime(fecha_mayor, "%d/%m/%Y")
                                formato_fecha_menor = time.strptime(fecha_menor, "%d/%m/%Y")
                                if sw_fechita1:
                                    casilla = fechita1
                                    sw_fecha = True
                                    formato_fecha = time.strptime(fechita1, '%d/%m/%Y') 
                                    if formato_fecha_mayor < formato_fecha:
                                        fecha_mayor = casilla
                                    if formato_fecha_menor > formato_fecha:
                                        fecha_menor = casilla
                                elif sw_fechita2:
                                    casilla = fechita2
                                    sw_fecha = True
                                    formato_fecha = time.strptime(fechita1, '%d/%m/%Y') 
                                    if formato_fecha_mayor < formato_fecha:
                                        fecha_mayor = casilla
                                    if formato_fecha_menor > formato_fecha:
                                        fecha_menor = casilla
                                elif sw_fechita3:
                                    casilla = fechita3
                                    sw_fecha = True
                                    formato_fecha = time.strptime(fechita1, '%d/%m/%Y') 
                                    if formato_fecha_mayor < formato_fecha:
                                        fecha_mayor = casilla
                                    if formato_fecha_menor > formato_fecha:
                                        fecha_menor = casilla
                                elif sw_fechita4:
                                    casilla = fechita4
                                    sw_fecha = True
                                    formato_fecha = time.strptime(fechita1, '%d/%m/%Y') 
                                    if formato_fecha_mayor < formato_fecha:
                                        fecha_mayor = casilla
                                    if formato_fecha_menor > formato_fecha:
                                        fecha_menor = casilla
                                elif sw_fechita5:
                                    casilla = fechita5
                                    sw_fecha = True
                                    formato_fecha = time.strptime(fechita1, '%d/%m/%Y') 
                                    if formato_fecha_mayor < formato_fecha:
                                        fecha_mayor = casilla
                                    if formato_fecha_menor > formato_fecha:
                                        fecha_menor = casilla
                                elif sw_fechita6:
                                    casilla = fechita6
                                    sw_fecha = True
                                    formato_fecha = time.strptime(fechita1, '%d/%m/%Y') 
                                    if formato_fecha_mayor < formato_fecha:
                                        fecha_mayor = casilla
                                    if formato_fecha_menor > formato_fecha:
                                        fecha_menor = casilla
                                elif sw_fechita7:
                                    casilla = fechita7
                                    sw_fecha = True
                                    formato_fecha = time.strptime(fechita1, '%d/%m/%Y') 
                                    if formato_fecha_mayor < formato_fecha:
                                        fecha_mayor = casilla
                                    if formato_fecha_menor > formato_fecha:
                                        fecha_menor = casilla
                                elif sw_fechita8:
                                    casilla = fechita8
                                    sw_fecha = True
                                    formato_fecha = time.strptime(fechita1, '%d/%m/%Y') 
                                    if formato_fecha_mayor < formato_fecha:
                                        fecha_mayor = casilla
                                    if formato_fecha_menor > formato_fecha:
                                        fecha_menor = casilla
                                else:
                                    casilla_error=casilla
                                    sw_error_fecha = True
                            elif tipo == "AÑO":
                                sw_añito1, añito1 = añoFormat(casilla)
                                if sw_añito1:
                                    casilla = añito1
                                else:
                                    casilla_error=casilla
                                    sw_error_año = True
                                sw_año = True
                                año = casilla
                            elif tipo == "MES":
                                sw_mesito1, mesito1 = mesFormat(casilla)
                                if sw_mesito1:
                                    casilla = mesito1
                                else:
                                    casilla_error=casilla
                                    sw_error_mes = True
                                sw_mes = True
                                mes.add(casilla)
                            elif tipo == "DIA":
                                sw_diita1, diita1 = diaFormat(casilla)
                                if sw_diita1:
                                    casilla = diita1
                                else:
                                    casilla_error=casilla
                                    sw_error_dia = True
                                
                            linea_aux += (";;" + casilla) 
                        aux_col+=1
                    archivo.write(linea_aux[2:]+"\n")
                else:
                    archivo.write(linea+"\n")
                #print(enlaces_aux)
                #print(matriz_enlace)
                if(sw_enlaces):
                    enl=""
                    for i in range(len(enlaces_aux)-1):
                        enl += enlaces_aux[i]+","
                    enl+=enlaces_aux[-1]
                    if enl not in matriz_enlace:
                        matriz_enlace.append(enl)
                    
                #print(matriz_enlace)

                if sw_error_hora or sw_error_fecha or sw_error_año or sw_error_mes or sw_error_dia:
                    sw_eliminar=True
                    messagebox.showinfo(message="Error en archivo:"+nom+",Formato no aceptado en linea:"+str(cont_linea)+" casilla:"+casilla_error, title="Error Cargar Excel")
                    break

            archivo.close()
            cache.close()    
        c+=1

        for unica in dic_unicas:
            escribir_Dat_Uni_tabla(unica, dic_unicas[unica])
        
        for enlace in dic_enlaces:
            escribir_enlaces_tabla(enlace, dic_enlaces[enlace])
        
        if sw_fecha:
            #print(fecha_mayor, fecha_menor)
            ti_may = time.strptime(fecha_mayor, "%d/%m/%Y")
            ti_men = time.strptime(fecha_menor, "%d/%m/%Y")
            #print(ti_may, ti_men)
            lista_tabla = listdir("Ficheros/Tablas/"+tabla+"/")
            #print(lista_tabla)
            año = str(ti_may.tm_year)
            if año not in lista_tabla:
                os.mkdir("Ficheros/Tablas/"+tabla+"/"+str(año)+"/")
            nom_mes = ""
            for kl in range(ti_men.tm_mon,ti_may.tm_mon):
                nom_mes += str(kl) + ","
            nom_mes += str(ti_may.tm_mon)
            lista_mes = listdir("Ficheros/Tablas/"+tabla+"/"+año+"/")
            if nom_mes not in lista_mes:
                os.mkdir("Ficheros/Tablas/"+tabla+"/"+año+"/"+nom_mes+"/")
            nom_fin = nombre_unico_txt_ubi(nom,"Ficheros/Tablas/"+tabla+"/"+año+"/"+nom_mes+"/")
            os.rename("Ficheros/Tablas/"+tabla+"/"+nom,"Ficheros/Tablas/"+tabla+"/"+nom_fin)
            shutil.move("Ficheros/Tablas/"+tabla+"/"+nom_fin,"Ficheros/Tablas/"+tabla+"/"+año+"/"+nom_mes+"/")
        elif sw_año and sw_mes:
            #print(año)
            #print(mes)
            lista_tabla = listdir("Ficheros/Tablas/"+tabla+"/")
            #print(lista_tabla)
            if año not in lista_tabla:
                os.mkdir("Ficheros/Tablas/"+tabla+"/"+año+"/")
                #print("hecho")
            mes = list(mes)
            mes_Aux = []
            for m in mes:
                mes_Aux.append(int(m))
            mes = mes_Aux
            mes.sort()
            nom_mes = ""
            for kl in mes[:-1]:
                nom_mes += str(kl) + ","
            nom_mes += str(mes[-1])
            #print(nom_mes)
            lista_mes = listdir("Ficheros/Tablas/"+tabla+"/"+año+"/")
            if nom_mes not in lista_mes:
                os.mkdir("Ficheros/Tablas/"+tabla+"/"+año+"/"+nom_mes+"/")
            nom_fin = nombre_unico_txt_ubi(nom,"Ficheros/Tablas/"+tabla+"/"+año+"/"+nom_mes+"/")
            os.rename("Ficheros/Tablas/"+tabla+"/"+nom,"Ficheros/Tablas/"+tabla+"/"+nom_fin)
            shutil.move("Ficheros/Tablas/"+tabla+"/"+nom_fin,"Ficheros/Tablas/"+tabla+"/"+año+"/"+nom_mes+"/")
        else:
            messagebox.showinfo(message="No se encontro fecha o año y mes", title="Error en el excel")
        
        if sw_float_neg:
            messagebox.showinfo(message="Se encontraron valores negativos los cuales se les remplazo con cero", title="Modificacion de datos")
    messagebox.showinfo(message="Excel Guardado con Exito", title="Guardado de Excel")

def exportar_filtros(tipos, columnas):
    global filtros_form_grafico
    archivo = open("Cache/Cache_Filtros/filtros.txt",mode="w",encoding="utf-8")
    i=1
    aux = []
    #print(tipos)
    for filtro in filtros_form_grafico:
        #print(type(filtro))
        if type(filtro) == type(aux):
            archivo.write(columnas[i]+" Inicio: "+filtro[0].get()+"\n")
            archivo.write(columnas[i]+" Fin: "+filtro[1].get()+"\n")
            i+=1
        else:
            if tipos[i] == "FLOAT":
                if filtro.get() == 1:
                    archivo.write(columnas[i]+": Si\n")
                else:
                    archivo.write(columnas[i]+": No\n")
                i+=1
            else:
                archivo.write(columnas[i]+": "+str(filtro.get())+"\n")
                i+=1
    archivo.close()

def nombre_unico_txt(nombre_cache, tabla):
    sw = True
    lista_archivos=listdir("Ficheros/Tablas/"+tabla+"/")
    c=1
    numero = nombre_cache[0]
    #print(numero)
    nom_cache= nombre_cache[2:]
    nombre = nom_cache[:-4]
    while sw:
        if nom_cache in lista_archivos:
            nom_cache = nombre+" ("+str(c)+")"+".txt"
            #print(nom_cache)
            #print(lista_archivos)
            #print("Iguales")
            c+=1
            sw = True
        else:
            #print("no esta")
            sw = False
            nom_cache = str(numero)+" "+ nom_cache
            os.rename("Cache/Cache_Entrada/"+nombre_cache, "Cache/Cache_Entrada/"+nom_cache)

def nombre_unico_txt_ubi(nom_cache, dir):
    sw = True
    lista_archivos=listdir(dir)
    #print(dir)
    c=1
    nombre = nom_cache[:-4]
    while sw:
        if nom_cache in lista_archivos:
            nom_cache = nombre+" ("+str(c)+")"+".txt"
            c+=1
            sw = True
        else:
            sw = False
    #print(nom_cache)
    return nom_cache

#-- observar si es necesaria esta funcion --
def tabla_valores_unicos(tabla, archivo):
    #columnas = columnas_tabla(tabla)
    #print(tabla, archivo)
    archivo_unico = open("Ficheros/Valores Unicos/"+tabla+".txt", "w+", encoding="utf-8")

    m=[]

    for linea in archivo_unico:
        linea=linea.strip("\n")
        linea=linea.split(",")
        m.append(linea)
        #print(linea)
    archivo_unico.close()

def sacar_Dat_Uni_tabla(tabla):
    archivo_unico = open("Ficheros/Valores Unicos/"+tabla+".txt", "r", encoding="utf-8")
    columnas_unicas = []
    for linea in archivo_unico:
        linea=linea.strip("\n")
        linea=linea.split(";")
        columnas_unicas.append(linea)
    archivo_unico.close()
    return columnas_unicas

def sacar_enlaces(tabla):
    archivo_enlaces = open("Ficheros/Enlaces/"+tabla+".txt", "r", encoding="utf-8")
    columnas_enlaces = []
    for linea in archivo_enlaces:
        linea=linea.strip("\n")
        #linea=linea.split(";")
        columnas_enlaces.append(linea)
    archivo_enlaces.close()
    return columnas_enlaces

def escribir_Dat_Uni_tabla(tabla, matriz):
    archivo_unico = open("Ficheros/Valores Unicos/"+tabla+".txt", "w", encoding="utf-8")
    for fila in matriz:
        fila_aux=""
        for col in fila[:-1]:
            fila_aux+=col+";"
        fila_aux+=fila[-1]
        archivo_unico.write(fila_aux+"\n")
    archivo_unico.close()

def escribir_enlaces_tabla(tabla, matriz):
    archivo_enlace = open("Ficheros/Enlaces/"+tabla+".txt", "w", encoding="utf-8")
    #print("Enlaces")
    #cabecera = matriz[0]
    #matriz = matriz[1:].sort()
    #print(matriz)
    for col in matriz:
        archivo_enlace.write(col+"\n")
    #for fila in matriz:
    #    fila_aux=""
    #    for col in fila[:-1]:
    #        archivo_enlace.write(col+"\n")
    #    fila_aux+=fila[-1]
    #    archivo_enlace.write(fila_aux)
    #archivo_enlace.write(cabecera+"\n")
    archivo_enlace.close()

def inicio_valores_unicos():
    tablas = open("Ficheros/Datos_tablas/tablas.txt","r", encoding="utf-8")
    for linea in tablas:
        linea = linea.strip("\n")
        linea = linea.split(",")
        tipos= tipos_datos(linea)
        if tipos.count(0) > 1:
            print(linea,tipos)
        val_unico=open("Ficheros/Valores Unicos/"+linea[0]+".txt","w", encoding="utf-8")
        for columna in linea[1:-1]:
            val_unico.write(columna+'\n')
        val_unico.write(linea[-1])  
        val_unico.close()  
    tablas.close()
    
def inicio_enlaces():
    graficos = open("Ficheros/Datos_tablas/TABLA_DE_TEXTO.txt","r",encoding="utf-8")
    for linea in graficos:
        linea = linea.strip("\n")
        linea = linea.split(",")
    graf_tabl = linea
    with open("Ficheros/Datos_tablas/tablas.txt","r",encoding="utf-8") as tablas:
        for linea in tablas:
            linea = linea.strip("\n")
            linea = linea.split(",")
            #print(linea)
            if linea[0] in graf_tabl:
                tipos = tipos_datos(linea)
                #print(linea[0])
                val_unics = []
                for i in range(len(tipos)):
                    if tipos[i] == "VALORES_UNICOS":
                        val_unics.append(linea[i])
                longi = len(val_unics)
                val_unico=open("Ficheros/Enlaces/"+linea[0]+".txt","w", encoding="utf-8")
                for i in range(longi-1):
                    val_unico.write(val_unics[i]+",")
                if longi > 0:
                    val_unico.write(val_unics[-1])
                val_unico.close()
                #-- Antigua forma de crear enlaces
                #for i in range(longi-2):
                #    val_unico.write(val_unics[i]+','+val_unics[i+1]+'\n')  
                #if longi > 1:
                #    val_unico.write(val_unics[-2]+','+val_unics[-1]) 
                
    graficos.close()

def sacar_tablas():
    tablas = []
    archivo = open("Ficheros/Datos_tablas/tablas.txt", "r", encoding="utf-8")
    for linea in archivo:
        linea=linea.strip("\n")
        linea=linea.split(",")
        tablas.append(linea[0])
    archivo.close()
    return tablas

def sacar_tablas_graficos():
    tablas=[]
    archivo = open("Ficheros/Datos_tablas/TABLAS_DE_GRAFICOS.txt", "r", encoding="utf-8")
    for linea in archivo:
        linea=linea.strip("\n")
        linea=linea.split(",")
    tablas = linea
    archivo.close()
    #print(tablas)
    return tablas

def sacar_tablas_texto():
    tablas=[]
    archivo = open("Ficheros/Datos_tablas/TABLA_DE_TEXTO.txt", "r", encoding="utf-8")
    for linea in archivo:
        linea=linea.strip("\n")
        linea=linea.split(",")
    tablas = linea
    archivo.close()
    #print(tablas)
    return tablas

lista_tablas_state=[]
lista_archivos_tablas=[]    

def fecha_modificacion(filename): 
    t = os.path.getmtime(filename) 
    return datetime.datetime.fromtimestamp(t)

def buscar_txt():
    global lista_archivos_tablas
    
    #for elemento in lista_archivos_tablas:
    #    print("ELE",elemento.get())
    lista_graficos = sacar_tablas_graficos()
    sw_todo = False
    sw_graf = False
    sw_text = False

    t = lista_archivos_tablas[0].get()
    if t == "":
        sw_todo = True
        tablas = sacar_tablas()
    else: 
        tablas = t
        if t in lista_graficos:
            sw_graf = True
        else:
            sw_text = True
    
    nom_archivo = lista_archivos_tablas[1].get()
    sw_nom = False   
    #print("NOMaRCHI",nom_archivo) 
    if nom_archivo != "":
        sw_nom = True

    fecha_subida = lista_archivos_tablas[2].get()
    sw_fecha = False
    if fecha_subida != "":
        sw_fecha = True

    año = lista_archivos_tablas[3].get()
    sw_año = False
    if año != "":
        sw_año = True

    mes = lista_archivos_tablas[4].get()
    sw_mes = False
    if mes != "":
        mes = mes_a_num(mes)
        sw_mes = True
    
    #print("todo", sw_todo)
    #print("graf", sw_graf)
    #print("text", sw_text)
    #print("nom", sw_nom)
    #print("fecha", sw_fecha)
    #print("año", sw_año)
    #print("mes", sw_mes)

    res = []
    aux_nom =[]
    if sw_todo:
        tablas = sacar_tablas()
        
        
        for tabla in tablas:
            #print(tabla)
            if tabla in lista_graficos:
                aux = []
                lista_año = listdir("Ficheros/Tablas/"+tabla)
                #print(lista_año)
                if sw_año:
                    if año in lista_año:
                        año_aux = tabla+"/"+año
                        aux.append(año_aux)
                else:
                    for lis in lista_año:
                        año_aux = tabla + "/"+ lis
                        aux.append(año_aux)
                    #print(aux)
                aux_mes = []
                
                if sw_mes:
                    #print(mes)
                    for año in aux:
                        lista_mes = listdir("Ficheros/Tablas/"+año)
                        for grupo_mes in lista_mes:
                            grupo_mes_aux = grupo_mes.split(",")
                            #print(grupo_mes_aux)
                            if mes in grupo_mes_aux:
                                aux_mmm = año+"/"+grupo_mes
                                aux_mes.append(aux_mmm)
                else:
                    for año in aux:
                        lista_mes = listdir("Ficheros/Tablas/"+año)
                        for grupo_mes in lista_mes:
                            aux_mmm = año+"/"+grupo_mes
                            aux_mes.append(aux_mmm)
                #print(aux_mes)
                if sw_nom:
                    for am in aux_mes:
                        lista_mes_nom = listdir("Ficheros/Tablas/"+am)
                        for mes_nom in lista_mes_nom:
                            if nom_archivo in mes_nom:
                                res.append(am+"/"+mes_nom)
                else:
                    for am in aux_mes:
                        lista_mes_nom = listdir("Ficheros/Tablas/"+am)
                        for mes_nom in lista_mes_nom:
                            res.append(am+"/"+mes_nom)
                #print(res)
            else:
                if sw_año or sw_mes:
                    pass
                else:
                    lista_nom = listdir("Ficheros/Tablas/"+tabla)
                    #print(lista_nom)
                    if sw_nom:
                        for posi_nom in lista_nom:
                            if nom_archivo in posi_nom:
                                r = tabla+"/"+posi_nom
                                res.append(r)
                    else:
                        for posi_nom in lista_nom:
                            r = tabla + "/" +posi_nom
                            res.append(r)
    
    if sw_text:
        tabla=tablas
        lista_nom = listdir("Ficheros/Tablas/"+tabla)
        if sw_nom:
            #print(lista_nom)
            for posi_nom in lista_nom:
                if nom_archivo in posi_nom:
                    r = tabla+"/"+posi_nom
                    res.append(r)
        else:
            for posi_nom in lista_nom:
                r = tabla + "/" +posi_nom
                res.append(r)
    if sw_graf:
        aux = []
        tabla=tablas
        lista_año = listdir("Ficheros/Tablas/"+tabla)
        #print(lista_año)
        if sw_año:
            if año in lista_año:
                año_aux = tabla+"/"+año
                aux.append(año_aux)
        else:
            for lis in lista_año:
                año_aux = tabla + "/"+ lis
                aux.append(año_aux)
            #print(aux)
        aux_mes = []
        
        if sw_mes:
            #print(mes)
            for año in aux:
                lista_mes = listdir("Ficheros/Tablas/"+año)
                for grupo_mes in lista_mes:
                    grupo_mes_aux = grupo_mes.split(",")
                    #print(grupo_mes_aux)
                    if mes in grupo_mes_aux:
                        aux_mmm = año+"/"+grupo_mes
                        aux_mes.append(aux_mmm)
        else:
            for año in aux:
                lista_mes = listdir("Ficheros/Tablas/"+año)
                for grupo_mes in lista_mes:
                    aux_mmm = año+"/"+grupo_mes
                    aux_mes.append(aux_mmm)
        #print(aux_mes)
        if sw_nom:
            for am in aux_mes:
                lista_mes_nom = listdir("Ficheros/Tablas/"+am)
                for mes_nom in lista_mes_nom:
                    if nom_archivo in mes_nom:
                        res.append(am+"/"+mes_nom)
        else:
            for am in aux_mes:
                lista_mes_nom = listdir("Ficheros/Tablas/"+am)
                for mes_nom in lista_mes_nom:
                    res.append(am+"/"+mes_nom)
    #print("Aux",aux)
    #print("Aux_mes",aux_mes)
    #print("Aux_nom",aux_nom)
    #res = res + aux_nom

    #print("Res",res)
    #print(len(res))
    c = 0
    if sw_fecha:
        fecha_subida = time.strptime(fecha_subida, "%Y-%m-%d")
        res_Aux_fecha = res.copy()
        for posi_nom in res_Aux_fecha:
            fecha_aux = fecha_modificacion("Ficheros/Tablas/"+posi_nom)
            #print(posi_nom, fecha_aux, fecha_subida)
            año1 = fecha_subida.tm_year
            año2 = fecha_aux.year

            mes1 = fecha_subida.tm_mon
            mes2 = fecha_aux.month

            dia1 = fecha_subida.tm_mday
            dia2 = fecha_aux.day
           
            if año1 == año2 and mes1 == mes2 and dia1 == dia2:
                pass
                #print("No removido")
            else:
                res.remove(posi_nom)
                #print("removido")
                c+=1

    #print("Res",res)
    #print(len(res), c)
    #print(res)
    if len(res) > 0:
        ventana_res = tk.Toplevel()
        ventana_res.title("Busqueda Archivos")
        panel = tk.Canvas(ventana_res)
        panel.config(background="#F9F9F9",width="700", height="400")
        panel.pack(side="left", fill="y")

        scroll_vertical = tk.Scrollbar(ventana_res, orient='vertical', command=panel.yview)
        scroll_vertical.pack(side="left", fill="y")

        panel.configure(yscrollcommand=scroll_vertical.set)
        panel.bind("<Configure>", lambda e: panel.configure(scrollregion=panel.bbox("all")))

        seg_frame = tk.Frame(panel)
        

        panel.create_window((0,0), window=seg_frame, anchor="nw", width="700")

        seg_frame.columnconfigure(0, weight=4)
        seg_frame.columnconfigure(1, weight=1)
        seg_frame.columnconfigure(2, weight=1)

        label = tk.Label(seg_frame,text="Resultados de la Busqueda", width=40, anchor="w",font=("Helvetica", 14)).grid(column=0,row=0,pady=15, padx=10)
        
        c = 1
        for resultado in res:
            label = tk.Label(seg_frame,text=resultado, anchor="w").grid(column=0,row=c,  pady=15, padx=10)
            boton_descargar=tk.Button(seg_frame, text="Descargar", command=lambda ubicacion = resultado: descargar_archivo(ubicacion)).grid(column=1,row=c ,pady=(10,0))
            boton_enviar=tk.Button(seg_frame, text="Eliminar", command=lambda ubicacion = resultado: eliminar_archivo(ubicacion)).grid(column=2,row=c ,pady=(10,0))
            c+=1
    else:
        messagebox.showinfo(message="No se encontró archivos", title="Mensaje de Busqueda")

def eliminar_archivo(ubi):
    os.remove("Ficheros/Tablas/"+ubi)
    #print("Eliminado:" + ubi)
    messagebox.showinfo(message="Archivo Eliminado", title="Mensaje de Confirmación")

def descargar_archivo(ubi):
    #print("Descargar:" + ubi)
    directorio_archivo = f"Ficheros/Tablas/"+ubi
    ruta_destino = filedialog.askdirectory()
    if ruta_destino:
        # Copiar el archivo al directorio de destino
        shutil.copy(directorio_archivo, ruta_destino)
        #print("Archivo descargado exitosamente.")
        messagebox.showinfo(message="Archivo Descargado", title="Mensaje de Confirmación")

def mes_a_num(mes):
    l_mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    res = l_mes.index(mes)+1
    return str(res)

class Texto(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background= style.PLOMO)
        self.controller =controller
        self.graficoMode = tk.StringVar(self,value="Texto")
        self.init_widgets()

    def seleccionar_elemento2(self,lista_tablas,options_frame, event):
        seleccion = lista_tablas.get(lista_tablas.curselection())
        form_llenar2(options_frame,seleccion)

    def move_to_graficos(self):
        self.controller.show_frame(Grafico)
    def move_to_ftexto(self):
        self.controller.show_frame(Texto)
    def move_to_cargar(self):
        self.controller.show_frame(Excel)
    def move_to_agregar(self):
        self.controller.show_frame(Nuevo)
        

    def init_widgets(self):
        Frame1=tk.Frame(self)
        Frame1.configure(background=style.BACKGROUND
                               )
        Frame1.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            #expand=True,
            padx=12,
            pady=5
        )   
        tk.Button(
            Frame1,
            text="Cargar archivo",
            command=self.move_to_cargar,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )

        tk.Button(
            Frame1,
            text="Graficos",
            command=self.move_to_graficos,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Button(
            Frame1,
            text="Filtros de texto",
            command=self.move_to_ftexto,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Button(
            Frame1,
            text="Agregar/Eliminar",
            command=self.move_to_agregar,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        
        tk.Label(
            self,
            text="Filtros de texto",
            justify=tk.CENTER,
            **style.STYLE
            ).pack(
            side = tk.TOP,
            fill= tk.BOTH,
            padx= 22,
            pady= 5
            )
        optionsFrame=tk.Frame(self)
        optionsFrame.configure(background="white"
                               )
        optionsFrame.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=True,
            padx=22,
            pady=11
        )
        tk.Label(
            self,
            text="Tablas:",
            justify=tk.CENTER,
            **style.STYLE
            ).pack(
            side = tk.TOP,
            fill= tk.X,
            ipadx= 20,
            ipady= 5,
            padx= 20,
            pady= 10,
            )
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        lista_tablas=tk.Listbox(
            self,
            width=30, 
            height=20,
            yscrollcommand=scrollbar.set
            )
        lista_tablas.pack(
            side = tk.TOP,
            fill= tk.X,
            ipadx= 10,
            ipady= 5,
            padx= 20,
            pady= 10,
            )
        # Asociar la barra de desplazamiento con la lista
        scrollbar.config(command=lista_tablas.yview)
        lista=sacar_tablas_texto()

        for elemento in lista:
            lista_tablas.insert(tk.END, elemento)
        
            
        lista_tablas.bind("<<ListboxSelect>>", lambda event: self.seleccionar_elemento2(lista_tablas,optionsFrame, event))
  
class Excel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background= style.PLOMO)
        self.controller =controller
        self.graficoMode = tk.StringVar(self,value="Excel")
        self.init_widgets()
        # Anterior gestion de archivos
        #self.gestion_archivos()
        self.formulario_archivos()
        self.form_excels()
        
        # -- Inicio de valores unicos en blanco, con las columnas de cada tabla --
        #inicio_valores_unicos()
        # -- Inicio enlaces de tablas graficos
        #inicio_enlaces()
    """  
    def entry_excel(self):
        files = askopenfiles(mode="r", filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')])
        aux_fila=1
        lista_radio=[0]*len(files)
        #lista_labels=[0]*len(files)
        lista_variables=[0]*len(files)
        c=0
        for file in files:
            columnas=[]
            excel = pd.read_excel(file.name)

            for columna in excel.columns:
                if "Unnamed" in columna:
                    break
                else:
                    columnas.append(columna) 
            #print(columnas)
            tablas = detectar_tabla(columnas)

            #print(tablas)
            nombre = file.name.split("/")
            nombre = nombre[-1]
            # self.children['!labelframe2']

            label = tk.Label(self.children['!labelframe2'], text=nombre).grid(column=0, row=aux_fila)
            #lista_labels[c] = tk.Label(self.children['!labelframe2'], text=tablas[0]).grid(column=1, row=aux_fila, pady=10)
            
            if len(tablas)>1:
                lista_variables[c] = tk.StringVar(self.children['!labelframe2'], "1")
                for tabla in tablas:
                    lista_radio[c] = tk.Radiobutton(
                        self.children['!labelframe2'],
                        text=tabla, value=c, variable = lista_variables[c] , command=lambda t=tabla, v=lista_variables[c]: self.asignar_texto(t,v)
                    )
                    lista_radio[c].grid(column=2,row=aux_fila)
                    aux_fila+=1
            else:
                lab_l = tk.Label(self.children['!labelframe2'], text=tablas[0]).grid(column=1, row=aux_fila, pady=10)

            
            aux_fila+=1
            c+=1

            
              
        button = tk.Button(
                self.children['!labelframe2'],
                text="Obtener Resutlado",
                command=self.asignar_texto)
        
        button.grid(column=4, row=aux_fila+1)

    def asignar_text(self,lista):
        print(lista)

        for caja in listas_cajas:
            if caja == 0:
                pass
            else:
                indices = caja.curselection()
                for i in indices:
                    print(caja.get[i])
                print(indices)
        """

    def move_to_graficos(self):
        self.controller.show_frame(Grafico)
    def move_to_ftexto(self):
        self.controller.show_frame(Texto)
    def move_to_cargar(self):
        self.controller.show_frame(Excel)
    def move_to_agregar(self):
        self.controller.show_frame(Nuevo)

    def init_widgets(self):
        Frame1=tk.Frame(self)
        Frame1.configure(background=style.BACKGROUND
                               )
        Frame1.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            #expand=True,
            padx=12,
            pady=5
        )   
        tk.Button(
            Frame1,
            text="Cargar archivo",
            command=self.move_to_cargar,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )

        tk.Button(
            Frame1,
            text="Graficos",
            command=self.move_to_graficos,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Button(
            Frame1,
            text="Filtros de texto",
            command=self.move_to_ftexto,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Button(
            Frame1,
            text="Agregar/Eliminar",
            command=self.move_to_agregar,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Label(
            self,
            text="Cargar Archivos",
            justify=tk.CENTER,
            **style.STYLE
            ).pack(
            side = tk.TOP,
            fill= tk.BOTH,
            padx= 22,
            pady= 5
            )

    def gestion_archivos(self):
        lista_tablas=[]
        with open("Ficheros/Tablas/TABLA_DE_TEXTO.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
                linea=linea.split(",")
        lista_tablas=linea

        panel = tk.Canvas(self)
        panel.config(background="#F9F9F9", width="200")
        panel.pack(side="left", fill="y")

        scroll_vertical = tk.Scrollbar(self, orient='vertical', command=panel.yview)
        scroll_vertical.pack(side="left", fill="y")

        panel.configure(yscrollcommand=scroll_vertical.set)
        panel.bind("<Configure>", lambda e: panel.configure(scrollregion=panel.bbox("all")))

        seg_frame = tk.Frame(panel)

        panel.create_window((0,0), window=seg_frame, anchor="nw", width="200")

        for tabla in lista_tablas:
            
            label = tk.Label(seg_frame,text=tabla, width=20, anchor="w").pack(pady=(5,0), padx=10)
            L_archivo = listdir("Ficheros/Tablas/"+tabla+"/")
            archivo_aux = tk.StringVar()
            lista_archivos = ttk.Combobox(seg_frame,textvariable=archivo_aux, height="5")
            lista_archivos['values'] = L_archivo
            lista_archivos['state'] = 'readonly'
            lista_archivos.pack(pady=(5,5))
            lista_archivos_tablas.append(archivo_aux)
            but = tk.Button(seg_frame, text="Eliminar", width=20, anchor="w").pack(pady=(0,10))

        
        #bot = tk.Button(seg_frame, text=tabla, width=20, anchor="w", command=lambda texto=tabla:form_comparar(self.children['!labelframe2'],texto)).pack(pady=5, padx=10)

    def tabla_seleccionada(self, event):
        global lista_archivos_tablas, lista_tablas_state
        tabla = lista_archivos_tablas[0].get()
        #print(tabla)
        lista_graficos = sacar_tablas_graficos()
        if tabla in lista_graficos:
            #print("si")
            #aumentar_año_mes()
            lista_tablas_state[0].config(state="readonly")
            lista_tablas_state[1].config(state="readonly")
        else:
            lista_tablas_state[0].set("")
            lista_tablas_state[1].set("")
            lista_tablas_state[0].config(state=tk.DISABLED)
            lista_tablas_state[1].config(state=tk.DISABLED)

    def formulario_archivos(self):
        global lista_tablas_state, lista_archivos_tablas
        lista_tablas_state = []
        panel = tk.Canvas(self)
        panel.config(background="#F9F9F9", width="200")
        panel.pack(side="left", fill="y")

        scroll_vertical = tk.Scrollbar(self, orient='vertical', command=panel.yview)
        scroll_vertical.pack(side="left", fill="y")

        panel.configure(yscrollcommand=scroll_vertical.set)
        panel.bind("<Configure>", lambda e: panel.configure(scrollregion=panel.bbox("all")))

        seg_frame = tk.Frame(panel)

        panel.create_window((0,0), window=seg_frame, anchor="nw", width="200")
        
        label = tk.Label(seg_frame,text="Busqueda Archivos", width=40, anchor="w",font=("Helvetica", 14)).pack(pady=15, padx=10)
        tablas = sacar_tablas()
        label = tk.Label(seg_frame,text="Tabla", width=40, anchor="w").pack(pady=(0,5), padx=10)

        archivo_aux = tk.StringVar()
        lista_archivos = ttk.Combobox(seg_frame,textvariable=archivo_aux, height="10")
        lista_archivos['values'] = tablas
        lista_archivos['state'] = 'readonly'
        lista_archivos.bind("<<ComboboxSelected>>",self.tabla_seleccionada)
        lista_archivos.pack(pady=(0,5))
        lista_archivos_tablas.append(archivo_aux)

        label = tk.Label(seg_frame,text="Nombre Archivo", width=40, anchor="w").pack(pady=(0,5), padx=10)
        var_nom_Archivo = tk.StringVar()
        l_entry = tk.Entry(seg_frame,text="Nombre de Archivo",textvariable=var_nom_Archivo).pack(pady=(0,5))
        lista_archivos_tablas.append(var_nom_Archivo)

        label = tk.Label(seg_frame,text="Fecha de Subida", width=40, anchor="w").pack(pady=(0,5), padx=10)
        fecha_subida = tk.StringVar()
        l_entry = tk.Entry(seg_frame,text="Fecha Subida",textvariable=fecha_subida).pack(pady=(0,5))
        lista_archivos_tablas.append(fecha_subida)

        label = tk.Label(seg_frame,text="Año", width=40, anchor="w").pack(pady=(0,5), padx=10)

        date = datetime.date.today()
        year = date.strftime("%Y")
        l_años = list(range(int(year),1999,-1))
        archivo_aux = tk.StringVar()
        lista_archivos = ttk.Combobox(seg_frame,textvariable=archivo_aux, height="10")
        lista_tablas_state.append(lista_archivos)
        lista_archivos['values'] = l_años
        lista_archivos['state'] = 'readonly'
        lista_archivos.pack(pady=(0,5))
        lista_archivos_tablas.append(archivo_aux)

        label = tk.Label(seg_frame,text="Mes", width=40, anchor="w").pack(pady=(0,5), padx=10)

        l_mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        archivo_aux_mes = tk.StringVar()
        lista_archivos = ttk.Combobox(seg_frame,textvariable=archivo_aux_mes, height="10")
        lista_tablas_state.append(lista_archivos)
        lista_archivos['values'] = l_mes
        lista_archivos['state'] = 'readonly'
        lista_archivos.pack(pady=(0,5))
        lista_archivos_tablas.append(archivo_aux_mes)

        btn = tk.Button(seg_frame, text ='Buscar', command = lambda: buscar_txt()).pack(pady=15, padx=10)

    def form_excels(self):
        formulario = tk.LabelFrame(self)
        formulario.config(background="#D9D9D9")
        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(2, weight=1)
        formulario.columnconfigure(3, weight=1)
        formulario.columnconfigure(4, weight=1)
        formulario.columnconfigure(5, weight=1)
        formulario.columnconfigure(6, weight=1)
        formulario.columnconfigure(7, weight=1)
        formulario.pack(fill="both",expand=True)

        btn = tk.Button(formulario, text ='Seleccionar Excel', command = lambda: entry_excel(self))
        btn.grid(column=0,row=0, pady="10")

def Exportar_datos(columnas,tipos,container):
    global filtros_form_grafico
    
    print(filtros_form_grafico)
    tipos=tipos[1:]
    tabla = columnas[0]
    num_datos_para_grafico=0
    nro_columnas=len(columnas)-1
    filtro_datos = [0]*(nro_columnas)
    columnas_grafico=[]
    
    filtro_datos,lista_año,lista_mes= filtros_tablas(columnas,tipos)
    ubi_cache="Cache_Texto"
    filtrar_datos(tabla, ubi_cache, tipos, filtro_datos, nro_columnas, lista_año, lista_mes)
    
    def leer_lineas_con_nombre(nombre_archivo,nombre_tabla):
        lineas_con_nombre = []
        with open(nombre_archivo, 'r',encoding='utf-8') as archivo:
            for linea in archivo:
                # Eliminar espacios en blanco al principio y al final de la línea
                linea = linea.strip("\n")
                
                # Dividir la línea en palabras
                palabras = linea.split(",")
                
                # Comprobar si el primer elemento de la línea es igual a "nombre"
                if  palabras[0] == nombre_tabla:
                    i = 0
                    longitud = len(linea)
                    
                    while i < longitud and linea[i] != ',':
                        i += 1
                    linea_aux=linea[i+1:]  # Utilizamos lower() para ignorar mayúsculas/minúsculas
                    
                    lineas_con_nombre.append(linea_aux)
                    lineas_con_nombre=palabras[1:]
        return lineas_con_nombre

    nombre_archivo = "Ficheros/Datos_tablas/tablas.txt"  # Reemplaza "archivo.txt" con el nombre de tu archivo
    lineas_con_nombre = leer_lineas_con_nombre(nombre_archivo,tabla)
    
    print(lineas_con_nombre)

        # Nombre del archivo de destino donde se copiará el contenido
    archivo_destino = "ficheros/tabla_a_exportar/archivo_exportar.txt"  
    
    # Nombre de la carpeta que contiene los archivos txt
    carpeta = "Cache/Cache_Texto"

    with open(archivo_destino, 'w',encoding='utf-8') as archivo: 
        for index, elemento in enumerate(lineas_con_nombre):
            if index == len(lineas_con_nombre) - 1:
                    archivo.write(str(elemento) + '\n')
            else:
                    archivo.write(str(elemento) + '◘')
        
        for nombre_archivo in os.listdir(carpeta):
            ruta_archivo = os.path.join(carpeta, nombre_archivo)
            if os.path.isfile(ruta_archivo) :
                with open(ruta_archivo, 'r',encoding='utf-8') as archivo_origen:
                    contenido = archivo_origen.read()
                    contenido = contenido.strip("\n")
                    contenido = contenido.split(";;")
                    aux = ""
                    for palabra in contenido:
                        aux += palabra + "◘"
                    archivo.write(aux[:-1])

    # Set for TxtLoadOptions
    loadOptions = TxtLoadOptions()
    loadOptions.setSeparator('◘')

    # Create a Workbook object and opening the file from its path
    workbook = Workbook( "ficheros/tabla_a_exportar/archivo_exportar.txt", loadOptions)
    print("TXT file opened successfully!")

    fecha = datetime.datetime.now()

    # Formatear la fecha y hora sin microsegundos
    fechaformateada = fecha.strftime("%Y-%m-%d%H%M%S")

    # Save for check
    workbook.save(f"ficheros/tabla_a_exportar/{tabla+fechaformateada}.xlsx")

    jpype.shutdownJVM()

    def descargar_archivo(tabla,fechaformateada):
        # Directorio del archivo en tu proyecto
        directorio_archivo = f"ficheros/tabla_a_exportar/{tabla+fechaformateada}.xlsx"

        # Abrir el cuadro de diálogo para seleccionar el directorio de destino
        ruta_destino = filedialog.askdirectory()

        # Verificar si el usuario seleccionó una ruta válida
        if ruta_destino:
            # Copiar el archivo al directorio de destino
            shutil.copy(directorio_archivo, ruta_destino)
            messagebox.showinfo('Resultado', 'Se descargó su archivo con éxito')
            print("Archivo descargado exitosamente.")

        # Crear un botón para iniciar la descarga
    boton_descargar = tk.Button(container, text="Descargar Archivo", command=lambda: descargar_archivo(tabla,fechaformateada))
    boton_descargar.pack(pady=20)    

class Home(tk.Frame):

    def __init__(self,parent,controller):
        super().__init__(parent)
        self.configure(background=style.BACKGROUND, width=1000)
        self.controller = controller
        self.graficoMode = tk.StringVar(self,value="Normal")
        self.lugar = "1000.png"
        self.imagen = tk.PhotoImage(file=self.lugar)
        tk.Button(
            self,
            image=self.imagen,
            command=self.move_to_graficos
        ).pack()
    def move_to_graficos(self):
        self.controller.mode= self.graficoMode.get()
        self.controller.show_frame(Grafico)

class Nuevo(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.configure(background=style.PLOMO)
        self.controller = controller
        self.graficoMode = tk.StringVar(self,value="Normal")
        self.init_widgets()
        self.form_nuevo()
        
    
    def move_to_graficos(self):
        self.controller.show_frame(Grafico)
    def move_to_ftexto(self):
        self.controller.show_frame(Texto)
    def move_to_cargar(self):
        self.controller.show_frame(Excel)
    def move_to_agregar(self):
        self.controller.show_frame(Nuevo)

    def init_widgets(self):
        Frame1=tk.Frame(self)
        Frame1.configure(background=style.BACKGROUND)
        Frame1.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            #expand=True,
            padx=12,
            pady=5
        )   
        tk.Button(
            Frame1,
            text="Cargar archivo",
            command=self.move_to_cargar,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )

        tk.Button(
            Frame1,
            text="Graficos",
            command=self.move_to_graficos,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Button(
            Frame1,
            text="Filtros de texto",
            command=self.move_to_ftexto,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Button(
            Frame1,
            text="Agregar/Eliminar",
            command=self.move_to_agregar,
            **style.STYLE2,
            relief= tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground= style.TEXT,
        ).pack(
            side =tk.LEFT,
            fill=tk.X,
            padx=22,
            pady=11
        )
        tk.Label(
            self,
            text="Agregar o Elimnar Archivos",
            justify=tk.CENTER,
            **style.STYLE
            ).pack(
            side = tk.TOP,
            fill= tk.BOTH,
            padx= 22,
            pady= 5
            )

    def form_nuevo(self):
        Frame1=tk.Frame(self)
        Frame1.configure(background=style.BACKGROUND)
        Frame1.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            #expand=True,
            padx=12,
            pady=5
        )  
        


        nombre= tk.StringVar()

        l = tk.Label(Frame1, text="Nombre Tabla:").pack()
        en = tk.Entry(Frame1, textvariable=nombre).pack()
        columnas= tk.IntVar()
        l = tk.Label(Frame1, text="Cantidad de columnas:").pack()
        en = tk.Entry(Frame1, textvariable=columnas).pack()
        b = tk.Button(Frame1, text="Crear Tabla", command= lambda: crear_tabla(nombre,columnas)).pack()

        Frame3 = tk.Frame(self)
        Frame3.configure(background=style.BLANCO, height=200, width=400)
        tabla_eliminar= tk.StringVar()
        l = tk.Label(Frame3, text="Tabla a eliminar:").pack()
        en = tk.Entry(Frame3, textvariable=tabla_eliminar).pack()
        b = tk.Button(Frame3, text="Eliminar Tabla", command= lambda: eliminar_tabla(tabla_eliminar)).pack()

        Frame3.pack()

nuevas_columnas = []
nuevos_tipos = []
boton_columna = 0
#Tabla de graficos si o si necesita fecha

def columna_seleccionada(event):
    global nuevas_columnas, nuevos_tipos

    m = []
    with open("Ficheros/Datos_tablas/tablas.txt","r",encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip("\n")
            linea = linea.split(",")
            m.append(linea)
    
def crear_tabla(nombre, columnas):
    global nuevas_columnas, nuevos_tipos, boton_columna
    nombre = nombre.get()
    columnas = columnas.get()
    tablas = sacar_tablas()
    if nombre in tablas:
        messagebox.showerror('Error', 'Ya hay una tabla con ese nombre')
    else:
        #print("Se puede continuar")
        #print(container)
        tipos = ("FECHA","AÑO","MES","DIA","CADENAS","FLOAT","DESCRIPCIÓN","VALORES_UNICOS","HORAS")
        ventana_col = tk.Toplevel()
        ventana_col.title("Agregación de Columnas")
        panel = tk.Canvas(ventana_col)
        panel.config(background="#F9F9F9",width="700", height="400")
        panel.pack(side="left", fill="y")

        scroll_vertical = tk.Scrollbar(ventana_col, orient='vertical', command=panel.yview)
        scroll_vertical.pack(side="left", fill="y")

        panel.configure(yscrollcommand=scroll_vertical.set)
        panel.bind("<Configure>", lambda e: panel.configure(scrollregion=panel.bbox("all")))

        container = tk.Frame(panel)

        panel.create_window((0,0), window=container, anchor="nw", width="700")
        for i in range(columnas):
            nom= tk.StringVar()
            l = tk.Label(container, text="Nombre de columna "+str(i+1)+":").pack()
            en = tk.Entry(container, textvariable=nom).pack()
            nuevas_columnas.append(nom)
            l = tk.Label(container, text="Tipo de Dato "+str(i+1)+":").pack()

            archivo_aux = tk.StringVar()
            lista_archivos = ttk.Combobox(container,textvariable=archivo_aux, height="10")
            lista_tablas_state.append(lista_archivos)
            lista_archivos['values'] = tipos
            lista_archivos['state'] = 'readonly'
            #lista_archivos.bind("<<ComboboxSelected>>",columna_seleccionada)
            lista_archivos.pack(pady=(0,5))
            nuevos_tipos.append(archivo_aux)
        boton_columna = tk.Button(container, text="Crear Columnas",command=lambda: crear_columnas(nombre)).pack()

def crear_columnas(nombre):
    global nuevas_columnas, nuevos_tipos

    m = []
    with open("Ficheros/Datos_tablas/tipos_datos.txt","r",encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip("\n")
            linea = linea.split(",")
            m.append(linea)
    swCol = False
    sw = False
    contador = 0
    for c in nuevas_columnas:
        col = c.get()
        if col == "":
            sw = True
        else:
            cont_aux = 0
            for linea in m:
                a = linea[0]
                if col in linea and col!=a:
                    tipo_aux = nuevos_tipos[contador].get()
                    if tipo_aux != a:
                        swCol = True
                cont_aux += 1
        contador += 1
   
    sw1 = False
    swFloat = False
    swFecha = False
    swAño = False
    swMes = False
    swDATE = 0
    for t in nuevos_tipos:
        if t.get() == "":
            sw1 = True
        elif t.get() == "FLOAT":
            swFloat = True
        elif t.get() == "FECHA":
            swFecha = True
            swDATE = 2
        elif t.get() == "AÑO":
            swAño = True
            swDATE += 1
        elif t.get() == "MES":
            swMes = True
            swDATE += 1
    if sw1:
        messagebox.showerror('Error', 'Tiene que especificar el tipo de dato de cada columna')
    elif swCol:
        messagebox.showerror('Error', 'Columna ya existe y se quiere colocar un nuevo tipo de dato')
    elif sw:
        messagebox.showerror('Error', 'No puede haber columnas sin nombre')
    if swDATE != 2:
        if swDATE == 0:
            messagebox.showerror('Error', 'No se puede graficar sin fecha')
        elif swDATE == 1:
            messagebox.showerror('Error', 'Se necesita año y mes minimo para graficas')
        else:
            messagebox.showerror('Error', 'Error con las columnas de tipo fecha, año, mes, solo puede haber una de cada una')
    else:
        #print("Se puede crear")
        tipo = "TEXTO"
        if swFloat:
            tipo = "GRAFICO"
        
        agregar_tabla(tipo,nombre)
        agregar_val_unicos(nombre)
        agregar_tipos_datos()
        agregar_tabla_a_tablas(nombre)
        messagebox.showinfo('Creación de Tabla','Se creo la tabla con exito')

def agregar_tabla(tipo, tabla):
    lug = ""
    if tipo == "TEXTO":
        lug="TABLA_DE_TEXTO.txt"
    else:
        lug="TABLAS_DE_GRAFICOS.txt"
        lug1="TABLA_DE_TEXTO.txt"
        with open("Ficheros/Datos_tablas/"+lug1, mode="r",encoding="utf-8") as archivo:
            for linea in archivo:
                linea=linea.strip("\n")
        with open("Ficheros/Datos_tablas/"+lug1, mode="w",encoding="utf-8") as archivo:
            archivo.write(linea+","+tabla)

    with open("Ficheros/Datos_tablas/"+lug, mode="r",encoding="utf-8") as archivo:
        for linea in archivo:
            linea=linea.strip("\n")
    with open("Ficheros/Datos_tablas/"+lug, mode="w",encoding="utf-8") as archivo:
        archivo.write(linea+","+tabla)
    os.mkdir("Ficheros/Tablas/"+tabla)
    
def agregar_val_unicos(tabla):
    global nuevas_columnas, nuevos_tipos
    with open("Ficheros/Valores Unicos/"+tabla+".txt","w",encoding="utf-8") as nuevo:
        for columna in nuevas_columnas:
            nuevo.write(columna.get()+"\n")
    aux = ""
    for i in range(len(nuevos_tipos)):
        if nuevos_tipos[i].get() == "VALORES_UNICOS":
            aux = aux + nuevas_columnas[i].get()+","
    #print(aux)
    aux = aux[:-1]
    print(aux)
    with open("Ficheros/Enlaces/"+tabla+".txt","w",encoding="utf-8") as arch:
        arch.write(aux+"\n")

def agregar_tipos_datos():
    global nuevas_columnas, nuevos_tipos
    m = []
    tipos = []
    with open("Ficheros/Datos_tablas/tipos_datos.txt","r",encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip("\n")
            linea = linea.split(",")
            tipos.append(linea[0])
            m.append(linea)
    #print(tipos)
    for i in range(len(nuevos_tipos)):
        tipo = nuevos_tipos[i].get()
        j = tipos.index(tipo)
        #print(j)
        col = nuevas_columnas[i].get()
        if col not in m[j]:
            m[j].append(nuevas_columnas[i].get())
    #print(m)

    with open("Ficheros/Datos_tablas/tipos_datos.txt","w", encoding="utf-8") as archivo:
        for linea in m:
            aux = ""
            for cas in linea[:-1]:
                aux = aux+cas+ "," 
            aux+=linea[-1]
            archivo.write(aux+"\n")

def agregar_tabla_a_tablas(nombre):
    global nuevas_columnas, nuevos_tipos
    m = []
    with open("Ficheros/Datos_tablas/tablas.txt","r",encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip("\n")
            linea = linea.split(",")
            m.append(linea)
    aux = []
    aux.append(nombre)
    for col in nuevas_columnas:
        aux.append(col.get())
    m.append(aux)
    m = sorted(m,key=lambda fila: fila[0])
    #print(m)

    with open("Ficheros/Datos_tablas/tablas.txt","w", encoding="utf-8") as archivo:
        for linea in m:
            aux = ""
            for cas in linea[:-1]:
                aux = aux+cas+ "," 
            aux+=linea[-1]
            archivo.write(aux+"\n")

def eliminar_tabla(nombre):
    nombre = nombre.get()
    m = []
    col_aux=[] 
    tablas = sacar_tablas()
    if nombre in tablas:
        with open("Ficheros/Datos_tablas/tablas.txt", mode="r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip("\n")
                l_aux=linea
                linea = linea.split(",")
                if linea[0] != nombre:
                    m.append(l_aux)
                else:
                    col_aux = linea

        
        col2 = []
        #print(col_aux)
        swB=True
        conjunto = set()
        for linea in m:
            linea = linea.split(",")
            for col in linea:
                conjunto.add(col)
        #print(conjunto)

        for cole in col_aux:
            if cole in conjunto:
                pass
            else:
                col2.append(cole)
        #print(col2)
        mat_aux = []
        with open("Ficheros/Datos_tablas/tipos_datos.txt", mode="r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip("\n")
                linea=linea.split(",")
                l = ""
                for col in linea:
                    if col not in col2:
                        l += col+","
                mat_aux.append(l[:-1])
        #print(mat_aux)
        with open("Ficheros/Datos_tablas/tipos_datos.txt", mode="w", encoding="utf-8") as archivo:
            for lin in mat_aux:
                archivo.write(lin+"\n")
        with open("Ficheros/Datos_tablas/tablas.txt", mode="w", encoding="utf-8") as archivo:
            for lin in m:
                archivo.write(lin+"\n")

        os.remove("Ficheros/Valores Unicos/"+nombre+".txt")
        os.remove("Ficheros/Enlaces/"+nombre+".txt")
        shutil.rmtree("Ficheros/Tablas/"+nombre)

        with open("Ficheros/Datos_tablas/TABLA_DE_TEXTO.txt", mode="r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip("\n")
                l_aux=linea.split(",")

        l_e = ""
        for tabla in l_aux:
            if tabla != nombre:
                l_e += tabla + ","
        
        with open("Ficheros/Datos_tablas/TABLA_DE_TEXTO.txt", mode="w") as archivo:
            archivo.write(l_e[:-1])

        with open("Ficheros/Datos_tablas/TABLAS_DE_GRAFICOS.txt", mode="r") as archivo:
            for linea in archivo:
                linea = linea.strip("\n")
                l_aux=linea.split(",")

        l_e = ""
        for tabla in l_aux:
            if tabla != nombre:
                l_e += tabla + ","
        
        with open("Ficheros/Datos_tablas/TABLAS_DE_GRAFICOS.txt", mode="w") as archivo:
            archivo.write(l_e[:-1])
        messagebox.showinfo('Eliminación de Tabla','Se eliminó la tabla con exito')
    else:
        messagebox.showerror('Error', 'Tabla no encontrada')