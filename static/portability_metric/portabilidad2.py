# -*- coding: utf-8 -*-
import csv
import re
from sys import argv

def compara_componente(inFile, diccsErrores):
    comps = obten_componentes(inFile)
    

    arrResult = []    
    for k in comps_Name:
        arrResult.append()
    
    """
    Buscar en el diccionario los componentes del archivo de entrada
    e imprimir los errores del estilo: *Nombre del Componente* da errores en 
    los siguientes navegadores: *Nombre nav 1*
                                ...
                                *Nombre nav n*
    
    """
    for dicc in diccsErrores:
        if (dicc['Componente'])





def obten_componentes(cfile):
    file = open(cfile,'r')
    ref = ""
    comment = 0
    components = []
    for line in file.readlines():
        arr_line = line.split()
        for word in arr_line:
            if word== "<!--":
                comment = 1
            elif word =="-->" and comment==1:
                comment = 0
            elif comment == 0:
                match = re.search('<link rel="import" +href="(.+?)" *>', line)
                if match != None:
                    components.append(match.group(1))
                    break
                else:
                    break
    file.close()
    comps_Name = []
    for c in components:
        c = c.split('/')
        c_aux = c[len(c)-1]
        c_aux2 = c_aux.split('.')
        comps_Name.append(c_aux2[0])
    return comps_Name


script, bbdd, fEntrada = argv
comps = obten_componentes(fEntrada)
with open(bbdd, 'r') as csvfile:
    lineas = csvfile.read().splitlines()        #Separo archivo en lineas
    lineas.pop(0)                               #Saco el título (componente, navegador..)
    arr_dicc = []
    for l in lineas:
        linea = l.split(',')
        if comps.count(linea[0])!=0:
            arr_dicc_res.append({})
        arr_dicc.append({'Component':linea[0],'Browser':linea[1],'Browser Version':linea[2],'Error':linea[3],'Operating System': linea[4],'Description': linea[5]})
    compara_componente(fEntrada,arr_dicc)
    



