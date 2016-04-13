#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*

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
import mixpanel
from mixpanel import Mixpanel
mp = Mixpanel("10b73632200abfbd592a5567ae99f065")


#webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/_completitud.html")

#time.sleep(5)

CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret


##########################################################################################################################################
##########################################################################################################################################
#--------------------------------------------------------------COMPLETITUD----------------------------------------------------------------
##########################################################################################################################################
##########################################################################################################################################


oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key="3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf",resource_owner_secret="OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock")
url = 'https://api.twitter.com/1.1/statuses/update.json'
request_usertimeline="https://api.twitter.com/1.1/statuses/home_timeline.json?count=300"

#Request timeline home
s= requests.get(request_usertimeline, auth=oauth)
timeline=s.json()
contador=0
lis=[]
for tweet in timeline:
    #print tweet['user']['name'], 'dice: '
    #print "--------------------------------------------------------------"
    text=tweet['text']
    #print "el tweet es: " + text
    t= tweet['created_at']
    #print "t: " + str(t)
    #stamp=time.mktime(time.strptime(t,"%a %b %d %H:%M:%S +0000 %Y"))
    #print stamp
    contador=contador+1
    lis.append(text)
print contador
#print lis
#print lis[0]
print "--------------------------------------------------------------"

import mixpanel_api, json
from mixpanel import Mixpanel
#Tienes que crear una instancia de la clase Mixpanel, con tus credenciales
x=mixpanel_api.Mixpanel("0be846115003ba87c667ee6467edb336","c282259a64f150a4ce2496a2dd73e097")


#Cuando lo tengas, defines los parametros necesarios para la peticion
params={'event':['completitud twitter'],
        'name':'value',
        'type':"general",
        'unit':"day",
        'interval':1}

respuesta=x.request(['events/properties/values'], params, format='json')

lista=[]
import ast
for x in respuesta:
    #pasar de unicode a dict
    resp = ast.literal_eval(x)
    lista.append(resp)


#ordeno la lista de diccionarios por el tiempo
newlist = sorted(lista, key=lambda created_at: created_at['time_created'])
newlist.reverse()
print newlist

#def sort(item):
    #return -item.items()[1][1]

#fastList = sorted(respuesta,key=sort)


#COGER SOLO LOS TEXT DE NEWLIST Y COMPARAR CON LIST

#imprimir solo los timestamp
#for y in newlist:
#    print y['time_created']



#for k,v in zip(lis,newlist):
    #print k,v
#     #la k son los tweets obtenidos de twitter y v son los tweets obtenidos del componente
    #if cmp(k,v)==0:
        #print "son iguales, completitud OK"
    #else:
        #print "NO completitud"
