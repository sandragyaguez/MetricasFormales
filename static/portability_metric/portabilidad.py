# -*- coding: utf-8 -*-
import csv
import re
from sys import argv
import pymongo
from pymongo import Connection

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
		c = c.split('/')
		c_aux = c[len(c)-1]
		c_aux2 = c_aux.split('.')
		res.append(c_aux2[0])
	return res

def imprimeResultado(arrRes,c_Name):
	print arrRes
	print "El archivo introducido posee componentes que pueden dar errores\n"
	print "en diferentes navegadores, los componentes y navegadores son:\n"
	cont = 0
	for i in arrRes:
		print "Componente: " + c_Name[cont] + "\n"
		impresos = []
		vers_imp = []
		buscadores = i[c_Name[cont]][0]
		versBuscadores = i[c_Name[cont]][1]
		if len(buscadores)!=0:
			for buscador in buscadores:
				if impresos.count(buscador) == 0:
					print buscador + ": " + str(buscadores.count(buscador)) + " errores\n"
					impresos.append(buscador)
		
		if len(versBuscadores)!=0:
			print "Versiones:\n " 
			for versBus in versBuscadores:
				if vers_imp.count(versBus) == 0:
					print versBus + ": " + str(versBuscadores.count(versBus)) + " errores\n"
					vers_imp.append(versBus)
		cont += 1            
	print "------------------------------------------------------------------\n"

def getName(file):
	arch = file.split('/')
	aLen = len(arch)
	arch = arch[aLen-1]
	return arch

def insertInDB(datos):
	conex = Connection('localhost')
	db = conex.portabilidad
	colErrores = db.Errores
	colEstadBuscadores = db.EstadisticaBuscadores
	colEstadVerBuscadoresVer = db.EstadVersionBuscadores

	"""
	convertir de string a variable: 
	https://stackoverflow.com/questions/19122345/to-convert-string-to-variable-name
	
	"""

	colErrores.insert({})
	colEstadBuscadores.insert({})
	colEstadBuscadores.insert({})

	colErrores.update()
	colEstadBuscadores.update()
	colEstadBuscadores.update()

def mainFun (componentFile,diccionarios):
	
	arr_Fallos = []
	nombreFichero = getName(componentFile)
	c_Name = getComponents(componentFile)
	arr_Fallos = getErrors(diccionarios,c_Name)
	insertInDB(arrRes)
	#imprimeResultado(arr_Fallos,c_Name)


script, bbdd, fEntrada = argv
with open(bbdd, 'r') as csvfile:
	lineas = csvfile.read().splitlines()        #Separo archivo en lineas
	lineas.pop(0)                               #Saco el título (componente, navegador..)
	arr_dicc = []
	for l in lineas:
		linea = l.split(',')
		arr_dicc.append({'Component':linea[0],'Browser':linea[1],'Browser Version':linea[2],
			'Error':linea[3],'Operating System': linea[4],'Description': linea[5]})
	
	mainFun(fEntrada,arr_dicc)
	
	



	



