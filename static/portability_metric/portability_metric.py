# -*- coding: utf-8 -*-
import csv
import re
from sys import argv
import pymongo
from pymongo import Connection
from os import path


def getErrors(diccsErrores, comps_Name):
	
	arrResult = []    
	for k in comps_Name:
		arrResult.append({k:[[],[],[]]})
	for dicc in diccsErrores:
		coErr=dicc['Component']
		if comps_Name.count(coErr) != 0:
			for p in arrResult:
				if p.has_key(coErr):
					p[coErr][0].append(dicc['Browser'])
					p[coErr][1].append(dicc['Browser Version'])
					p[coErr][2].append(dicc)
	return arrResult


def getComponents(cfile):
	file = open(cfile,'r')
	ref = ""
	comment = 0
	components = []
	res = []
	resFinal = []
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
	for c in components:
		c_aux = path.basename(c)
		c_aux2 = c_aux.replace(".html","")
		res.append(c_aux2)
	resFinal.append(res)
	resFinal.append(components)
	return resFinal

def abrirBD():
	conex = Connection('localhost',27017)
	return conex.portabilidad

def insertInDB(datos,db,fname,compNames):
	global contadorErroresTotales
	contadorErroresTotales+=1
	fname = fname.replace("-","")
	fname = fname.replace(".","")
	Errores = fname + "Errores"
	EstadisticaBuscadores = fname + "EstadBuscadores"
	EstadVersionBuscadores = fname + "EstadVersionBuscadores"

	for componente in datos:
		clave = componente.keys()
		if (len(componente[clave[0]][0]) != 0):
			for diccErr in componente[clave[0]][2]:
				db[Errores].insert(diccErr)
			diccBuscadores = {}
			diccVersiones = {}
			buscadores = componente[clave[0]][0]
			versBuscadores = componente[clave[0]][1]
			diccBuscadores['Component'] = clave[0]
			diccVersiones['Component'] = clave[0]
			

			if len(buscadores)!=0:
				for buscador in buscadores:
					if diccBuscadores.keys().count(buscador) == 0: 
						diccBuscadores[buscador] = str(buscadores.count(buscador))

			if len(versBuscadores)!=0:
				for versBus in versBuscadores:
					if diccVersiones.keys().count(versBus) == 0:
						diccVersiones[versBus] = str(versBuscadores.count(versBus))
						
			db[EstadisticaBuscadores].insert(diccBuscadores)
			db[EstadVersionBuscadores].insert(diccVersiones)

def mainFun (componentFile,diccionarios,rutaBase):
	
	arr_Fallos = []
	nombreFichero = path.basename(componentFile)
	nomFichRes = nombreFichero
	nomFichRes = nomFichRes.replace(".html","")
	componentFile = rutaBase + '/' +nombreFichero
	#print componentFile
	c_Name = getComponents(componentFile)
	c_NameCompl = c_Name[1]
	c_NameAbr = c_Name[0]
	arr_Fallos = getErrors(diccionarios,c_NameAbr)
	bd = abrirBD()
	insertInDB(arr_Fallos,bd,nombreFichero,c_NameAbr)
	return c_Name
	
def funcionRecursiva(c_N,dicc,rutaBase,cRevisados):
	for c in c_N[1]:
		rutaComp = path.dirname(c)
		rutaComp = rutaComp.replace("..","bower_components")
		nombreC = path.basename(c)
		if rutaComp == "" and cRevisados.count(nombreC)==0:
			cRecur = mainFun(c,dicc,rutaBase)
			cRevisados.append(nombreC)
			funcionRecursiva(cRecur,dicc,rutaBase,cRevisados)
		elif cRevisados.count(nombreC)==0:
			cRecur = mainFun(c,dicc,rutaComp)
			cRevisados.append(nombreC)
			funcionRecursiva(cRecur,dicc,rutaComp,cRevisados)


def getGrade(fallos,name,straux):
    csvfile = open( "nota" + straux + ".csv" ,"w")
    spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if (straux == "noRec"):
    	spamwriter.writerow( str(10 - (fallos*0.25)))
    else:
		spamwriter.writerow( str(10 - (fallos*0.1)))
    csvfile.close()

script, bbdd, fEntrada = argv
with open(bbdd, 'r') as csvfile:
	lineas = csvfile.read().splitlines()        
	lineas.pop(0)                               
	arr_dicc = []
	for l in lineas:
		linea = l.split(',')
		linea3 = linea[3].replace(",","")
		linea5 = linea[5].replace(",","")
		arr_dicc.append({'Component':linea[0],'Browser':linea[1],'Browser Version':linea[2],
			'Error':linea3,'Operating System': linea[4],'Description': linea5})
	contadorErroresTotales = 0
	contadorErroresNoRec = 0
	listC = mainFun(fEntrada,arr_dicc,".")
	global contadorErroresNoRec
	contadorErroresNoRec+=len(listC[0])
	cRev = []
	funcionRecursiva(listC,arr_dicc,".",cRev)
	getGrade(contadorErroresTotales,path.basename(fEntrada),"Rec")
	getGrade(contadorErroresNoRec,path.basename,"noRec")