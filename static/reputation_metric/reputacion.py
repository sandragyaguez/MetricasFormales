
#!/usr/bin/python
# -*- coding: UTF-8 -*

import httplib
import urllib2, urllib
import hashlib
import sys
import json
import time
import pprint
import mixpanel
import requests
import mixpanel_api, json
from mixpanel import Mixpanel

#objeto mixpanel para mandar los resultados
mpResults = Mixpanel("538a819ae81a787ae2beff8f3dfd3473")
#me creo un objeto mixpanel de la clase Mixpanel del script mixpanel_api
x=mixpanel_api.Mixpanel("c2c6f5c021a293bf6e850746540a82ed","cb2011ee8d19c4e6dcf68c1cca1b151a")


#PREGUNTA OBLIGATORIA
#obtengo los datos de la primera pregunta del cuestionario recogidos en mixpanel
#en to_date tengo que poner la fecha actual (del dia que se esta ejecutando), asi que para no tener que cambiarlo a mano cada dia
#utilizo esa funcion que me devuelve la fecha actual
params={'from_date':'2016-09-10','to_date':time.strftime("%Y-%m-%d"),'event':'["initialQuestion"]'}
components=x.request(['export'],params, format='json')

listacomp=[]
listaselec=[]
listavers=[]
#recorro todos los eventos recogidos
for x in components:
	respuesta=json.loads(x)
	#de cada evento cojo del campo properties el valor del componente (twitter,face,google+ y github)
	componentes=respuesta['properties']['component']
	listacomp.append(componentes)
	#de cada evento cojo del campo properties el valor del selection(escala de 1 al 5, valor con el que el usuario ha valorado el componente)
	selections=respuesta['properties']['selection']
	listaselec.append(selections)
	#de cada evento cojo la version del componente
	versions=respuesta['properties']['version']
	listavers.append(versions)
	#hago el match del componente con su valoracion
	zipComSel=zip(listacomp,listaselec)
	#zip del zip que contenia la lista de componentes y la de las valoraciones; junto a las versiones de los componentes
	zipFinal=zip(zipComSel,listavers)

#datos falsos hasta que el round robin funcione
# zipFinal=[((u'github-events', u'2'), u'stable'), ((u'twitter-timeline', u'5'), u'stable'), 
#  ((u'facebook-wall', u'3'), u'latency'), ((u'twitter-timeline', u'4'), u'accuracy'), ((u'googleplus-timeline', u'1'), u'stable'), 
#  ((u'googleplus-timeline', u'4'), u'stable'), ((u'github-events', u'1'), u'latency'), ((u'facebook-wall', u'4'), u'latency'),
#   ((u'github-events', u'3'), u'stable')]

diccionario={}
#recorro la lista donde tengo todos los matching
#voy tratando casos segun el componente que sea y dentro de cada caso filtro por version; y sumo las valoraciones (los selections)
for x in zipFinal:
	#al haber hecho un zip de un zip, la forma en la que estan los datos son:((component,selection),version)
	#por lo que para de acceder a los campos que quiero es x[0][0] (con x[0] accedo a (component,selection) y con x[0][0] accedo al component)
	component=x[0][0]
	selection=x[0][1]
	version=x[1]
	
	#organizo todos los datos en una estructura de datos. La estructura va a ser: diccionario={component:{version:{cont:x, selection:[]}}}
	#primero compruebo que el diccionario tenga el componente, sino lo creo como diccionario
	if (not diccionario.has_key(component)):
		diccionario[component]={}
	#una vez creado ese diccionario o si ya existia compruebo si existe la version, sino existe creo el diccionario con lo que quiero que
	#contenga que en este caso es el contador de ocurrencias y las valoraciones (selections)
	if (not diccionario[component].has_key(version)):
		diccionario[component][version]={'cont':0,'selection':[]}

	#aumento el contador cuando encuentro una ocurrencia de cada version de cada componente y en el campo selection anado la valoracion
	diccionario[component][version]['cont']=diccionario[component][version]['cont']+1
	selections=diccionario[component][version]['selection']
	selections.append(int(selection))

#recorro el diccionario que me he creado para llegar hasta los valores que quiero sumar para luego dividir entre el contador
#key son los componentes y value el diccionario de version que contiene contador y selection
for key,value in diccionario.iteritems():
	#recorro el diccionario de la version para llegar a las valoraciones y al contador
	for clave, valor in value.iteritems():
		#sumo todos los selections de cada version
		suma=sum(valor['selection'])
		#divido entre el numero de ocurrencias (cont)
		valorFinal=suma/float(valor['cont'])
		#en el diccionario tengo que ir guardando que valor pertenece a que version y a que componente
		#por eso cojo el componente (key) y la version(clave) y le anado una nueva entrada que es valor total
		diccionario[key][clave]['total']=valorFinal
		#mando a mixpanel todos los valores
		mpResults.track("Reputacion", key,{"valor":valorFinal,"componente":key,"version":clave})

#libreria para pintar bonito los diccionarios por consola
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(diccionario)