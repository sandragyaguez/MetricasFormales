#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import httplib
import urllib2, urllib
import json
import time
from twitter import *
from requests_oauthlib import OAuth1
import requests
import webbrowser
import urllib3
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import datetime
import re
import ast
import calendar
import mixpanel
from mixpanel import Mixpanel
mp = Mixpanel("10b73632200abfbd592a5567ae99f065")


webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/_completitud.html")

time.sleep(10)

#CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
#CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
#ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
#ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret

CONSUMER_KEY= "7pBOCbidtVpQfTpPpwvQBL31o"
CONSUMER_SECRET = "0M3o2TTQQQi4fqXx03XRkfUIOXZBa3sIN0w5q7culXPnVv3enb"
ACCESS_KEY = "249717000-nG3UUpnfHkhIkyhnA8KpClgVKK0Uc2kl33qTrBdP"
ACCESS_SECRET = "erdkRUxv9eKGjfNHSkpzxi0kUYGAlOvI7ESOdPuxEv4OA"


##########################################################################################################################################
##########################################################################################################################################
#--------------------------------------------------------------COMPLETITUD----------------------------------------------------------------
##########################################################################################################################################
##########################################################################################################################################


oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
#url = 'https://api.twitter.com/1.1/statuses/update.json'
request_hometimeline="https://api.twitter.com/1.1/statuses/home_timeline.json?count=200"


#Request timeline home
s= requests.get(request_hometimeline, auth=oauth)
timeline=s.json()
contador=0
lis=[]
tiempo=[]
for tweet in timeline:
    #print tweet['user']['name'], 'dice: '
    #print "--------------------------------------------------------------"
    #if para ver si el tweet es un retweet
    if(tweet.has_key('retweeted_status')):
        text = tweet['retweeted_status']['text']
        #print "text: " + str(text)
    else:
        text=tweet['text']
    #print "el tweet es: " + text
    t= tweet['created_at']
    stamp=calendar.timegm(time.strptime(t,"%a %b %d %H:%M:%S +0000 %Y"))
    stamp=int(stamp)
    stamp=stamp*1000
    contador=contador+1
    lis.append(text)
    tiempo.append(stamp)
print contador
tiempo=sorted(tiempo)
tiempo.reverse()

print "--------------------------------------------------------------"
#quitar RT @usuario:   pero si el tweet empieza asi (sin ser un retweet) lo quita igualmente y esta mal
#listaT=[]
#for listT in lis:
    #listT = re.sub(r'RT[^:]*: ','',listT)
    #listaT.append(listT)

##########################################################################################################################################
##########################################################################################################################################
#------------------------------------------------------PETICION A MIXPANEL----------------------------------------------------------------
##########################################################################################################################################
##########################################################################################################################################

import mixpanel_api, json
from mixpanel import Mixpanel
#Tienes que crear una instancia de la clase Mixpanel, con tus credenciales
x=mixpanel_api.Mixpanel("0be846115003ba87c667ee6467edb336","c282259a64f150a4ce2496a2dd73e097")


event_master="completitud twitter master"
event_latency= "completitud twitter latency"
event_accuracy="completitud twitter accuracy"

#Cuando lo tengas, defines los parametros necesarios para la peticion
params={'event':[event_master],
        'name':'value',
        'type':"general",
        'unit':"day",
        'interval':1}

respuesta=x.request(['events/properties/values'], params, format='json')

lista=[]
for x in respuesta:
    #pasar de unicode a dict
    resp = ast.literal_eval(x)
    lista.append(resp)

#ordeno la lista de diccionarios por el tiempo
newlist = sorted(lista, key=lambda created_at: created_at['time_created'])
newlist.reverse()

listacomp=[]
listatiempo=[]
for y in newlist:
    #la k son los text y el tme_created y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
    textocomp=y.items()[0][1]
    tiempocomp=y.items()[1][1]
    listacomp.append(textocomp)
    listatiempo.append(tiempocomp)


#comparar timestamp de twitter con el del componente
contador=0
for k,v in zip(tiempo,listatiempo):
    #la k son los timestamps obtenidos de twitter y v son los timestamps obtenidos del componente
    if cmp(k,v)==0:
        contador+=1
        #print contador
        #print "tiempos iguales" 
    #else:
        #print "NO son iguales"
        #print "falla en: " + k

print "-------------------------------------------------------------"
cont=1
for k,v in zip(lis,listacomp):
    #la k son los tweets obtenidos de twitter y v son los tweets obtenidos del componente
    if cmp(k,v)==0:
        cont+=1
        #print cont
        #print "son iguales, completitud OK"       
    else:
        print "-----------------------------------------------------"
        print "-----------------------------------------------------"
        print "NO completitud"
        cont+=1
        print "falla en el numero: " + str(cont)
        print "python: " + k
        print "componente: " + v











#Miguel funcion de ordenacion
#def sort(item):
    #return -item.items()[1][1]
#fastList = sorted(respuesta,key=sort)
