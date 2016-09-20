
#!/usr/bin/python
# -*- coding: UTF-8 -*

import httplib
import urllib2, urllib
import hashlib
import sys
import json
import time
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
#recorro todos los eventos recogidos
for x in components:
	respuesta=json.loads(x)
	#de cada eventos cojo del campo properties el valor del componente (twitter,face,google+ y github)
	componentes=respuesta['properties']['component']
	listacomp.append(componentes)
	#de cada eventos cojo del campo properties el valor del selection(escala de 1 al 5, valor con el que el usuario ha valorado el componente)
	selections=respuesta['properties']['selection']
	listaselec.append(selections)
	#hago el match del componente con su valoracion
	zipComSel=zip(listacomp,listaselec)
print zipComSel

twitter=[]
face=[]
github=[]
google=[]
contTwitter=0
contFace=0
contGithub=0
contGoogle=0
#recorro la lista donde tengo todos los matching
#voy tratando casos segun el componente que sea; y sumando las valoraciones (los selections)
#me creo contadores por cada red social para saber el numero de ocurrencias de cada uno
for x in zipComSel:
	if (x[0]=='twitter-timeline'):
		contTwitter=contTwitter+1
		twitter.append(int(x[1]))
		valorTwitter=sum(twitter)
	elif (x[0]=='facebook-wall'):
		contFace=contFace+1
		face.append(int(x[1]))
		valorFace=sum(face)
	elif (x[0]=='googleplus-timeline'):
		contGoogle=contGoogle+1
		google.append(int(x[1]))
		valorGoogle=sum(google)
	elif (x[0]=='github-events'):
		contGithub=contGithub+1
		github.append(int(x[1]))
		valorGithub=sum(github)

#divido la suma de todas las valoraciones entre las ocurrencias que ha habido de cada componente
RepuTwitter=float(valorTwitter)/float(contTwitter)
RepuFace=float(valorFace)/float(contFace)
RepuGoogle=float(valorGoogle)/float(contGoogle)
RepuGithub=float(valorGithub)/float(contGithub)	

print RepuTwitter
print RepuFace
print RepuGoogle
print RepuGithub

#mando a mixpanel la reputacion de cada componente
mpResults.track("Reputacion", "Reputacion twitter",{"valor":RepuTwitter})
mpResults.track("Reputacion", "Reputacion facebook",{"valor":RepuFace})
mpResults.track("Reputacion", "Reputacion google+",{"valor":RepuGoogle})
mpResults.track("Reputacion", "Reputacion github",{"valor":RepuGithub})





      
