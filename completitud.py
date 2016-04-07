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
lista=[]
for tweet in timeline:
    #print tweet['user']['name'], 'dice: '
    #print "--------------------------------------------------------------"
    text=tweet['text']
    #print "el tweet es: " + text
    time= tweet['created_at']
    #print "time: " + str(time)
    contador=contador+1
    lista.append(text)
print contador
#print lista
#print lista[0]
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
#print respuesta
# print type(respuesta)

# for lista in respuesta:
#     miDic=dict(lista)
#     print type(miDic)

#     print type(lista)
#     print lista
    # for k,v in lista.items():
    #     print k,v
#print zip(lista,respuesta)

# for k,v in zip(lista,respuesta):
#     #la k son los tweets obtenidos de twitter y v son los tweets obtenidos del componente
#     if cmp(k,v)==0:
#         print "son iguales, completitud OK"
#     else:
#         print "NO completitud"

# fixed_list = [x.items() for x in respuesta]
# keys,values = zip(*fixed_list)
# print keys


# a =[{"car":45845},{"house": 123}]
# print type(a)
# print type(respuesta)
# print respuesta
# for res in respuesta:
#     print type(res)
#     res1=map(dict, res)
#     print type(res1)


# list1 = [i.values()[0] for i in a] #iterate over values 
# list2=  [i.keys()[0] for i in a]   #iterate over keys
# print type(i)
# print a
# print list1
# print list2

