#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib2, urllib
import json
import time
from time import sleep
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
import mixpanel_api

#JFS
#CONSUMER_KEY= "7pBOCbidtVpQfTpPpwvQBL31o"
#CONSUMER_SECRET = "0M3o2TTQQQi4fqXx03XRkfUIOXZBa3sIN0w5q7culXPnVv3enb"
#ACCESS_KEY = "249717000-nG3UUpnfHkhIkyhnA8KpClgVKK0Uc2kl33qTrBdP"
#ACCESS_SECRET = "erdkRUxv9eKGjfNHSkpzxi0kUYGAlOvI7ESOdPuxEv4OA"

#---------------------------------------------------------------------------------------------------------------------
#def main():
network_list = ["twitter","instagram", "facebook", "github"]
server_base_url = "http://localhost:8000"

#de los comandos que ejecuto desde consola, me quedo con el segundo (posicion 1,array empieza en 0),consola: python completitud.py twitter coge la "variable" twitter
if len(sys.argv) >= 2:
    social_network = sys.argv[1]
else:
    social_network = ''


#CASOS:
if social_network in network_list:
    if social_network == 'twitter':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS TWITTER API---------------------------------------------------------------
        ##########################################################################################################################################

        CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
        CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
        ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
        ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret
        # Lanzamos una pestana por cada version del componente
        webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/TwitterCompletitud.html")
        sleep(2)
        #webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/TwitterCompletitudLatency.html")
        #sleep(2)
        #webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/TwitterCompletitudAccuracy.html")
        #sleep(10)

        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        request_hometimeline="https://api.twitter.com/1.1/statuses/home_timeline.json?count=200"
        #Request timeline home
        s= requests.get(request_hometimeline, auth=oauth)
        timeline=s.json()
        contador=0
        lis=[]
        ids=[]
        for tweet in timeline:
            #if para ver si el tweet es un retweet
            if(tweet.has_key('retweeted_status')):
                text = tweet['retweeted_status']['text']
            else:
                text=tweet['text']
            id_tweet1=tweet['id_str']
            id_tweet1=int(id_tweet1)
            contador=contador+1
            lis.append(text)
            #Twitter devuelve los id de los tweets cronologicamente (comprobado)
            ids.append(id_tweet1)
        print contador

        ##########################################################################################################################################
        #-----------------------------------------DATOS TWITTER COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################

        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("0be846115003ba87c667ee6467edb336","c282259a64f150a4ce2496a2dd73e097")
        version_list = ["master","latency", "accuracy"]
        lista=[]
        listacomp=[]
        listaid=[]
        cont=0

        if len(sys.argv) >= 3:
            version= sys.argv[2]
        else:
            version = ''

        for version in version_list:
            print version
            if(version=="master"):
            #defino los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda id_tweet: id_tweet['id'])
                newlist.reverse()
                
                for y in newlist:
                #la k son los text y el id y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    textocomp=y.items()[0][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)

                for k,v in zip(lis,listacomp):
                #la k son los tweets obtenidos de twitter y v son los tweets obtenidos del componente
                    if cmp(k,v)==0:
                        cont+=1       
                    else:
                        print "-----------------------------------------------------"
                        print "NO completitud"
                        cont+=1
                        print "falla en el numero: " + str(cont)
                        #con listacom.index(v) mando a mixpanel la posicion en la que esta el tweet que fall en el componente
                        mp.track(cont,"Fallos master",{"posicion": listacomp.index(v)+1 , "tweet": v, "version":version})

            elif(version=="latency"):
                     #defino los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda id_tweet: id_tweet['id'])
                newlist.reverse()

                for y in newlist:
                #la k son los text y el id y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    textocomp=y.items()[0][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)

                for k,v in zip(lis,listacomp):
                #la k son los tweets obtenidos de twitter y v son los tweets obtenidos del componente
                    if cmp(k,v)==0:
                        cont+=1
                    else:
                        print "NO completitud"
                        cont+=1
                        print "falla en el numero: " + str(cont)
                        #con listacom.index(v) mando a mixpanel la posicion en la que esta el tweet que fall en el componente
                        mp.track(cont,"Fallos latency",{"posicion": listacomp.index(v)+1 , "tweet": v, "version":version})

            elif(version=="accuracy"):
                     #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda id_tweet: id_tweet['id'])
                newlist.reverse()

                for y in newlist:
                #la k son los text y el id y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    textocomp=y.items()[0][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)

                for k,v in zip(lis,listacomp):
                #la k son los tweets obtenidos de twitter y v son los tweets obtenidos del componente
                    if cmp(k,v)==0:
                        cont+=1
                    else:
                        print "NO completitud"
                        cont+=1
                        print "falla en el numero: " + str(cont)
                        #con listacom.index(v) mando a mixpanel la posicion en la que esta el tweet que fall en el componente
                        mp.track(cont,"Fallos accuracy",{"posicion": listacomp.index(v)+1 , "tweet": v, "version":version})

        # elif social_network == 'github':

        #     webbrowser.open_new(server_base_url + "/Stable/GithubEventsLatency.html?experiment="+ experiment_id)
        #     time.sleep(10)
        #     webbrowser.open_new(server_base_url + "/Accuracy/GithubEventsLatency.html?experiment="+ experiment_id)
        #     time.sleep(10)
        #     webbrowser.open_new(server_base_url + "/Latency/GithubEventsLatency.html?experiment="+ experiment_id)

        # elif social_network == 'facebook' and len(sys.argv) >= 3:
        #     access_token = sys.argv[2]
            
    
    else:
        print "Wrong social network or missing param"
        # {}: Obligatorio, []: opcional
        print "Usage: completitud.py {twitter|facebook|instagram|github [facebook_access_token]"


#if __name__ == "__main__":
    #main()



