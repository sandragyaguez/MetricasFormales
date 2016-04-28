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
import os
from mixpanel import Mixpanel
mp = Mixpanel("b5b07b32170e37ea45248bb1a5a042a1")
mpGithub=Mixpanel("6dbce2a15a7e5bbd608908e8d0ed8518")
import mixpanel_api

#---------------------------------------------------------------------------------------------------------------------
network_list = ["twitter","instagram", "facebook", "github"]
version_list = ["master","latency", "accuracy"]
server_base_url = "http://localhost:8000"

#de los comandos que ejecuto desde consola, me quedo con el segundo (posicion 1,array empieza en 0),consola: python completitud.py twitter coge la "variable" twitter
if len(sys.argv) >= 2:
    social_network = sys.argv[1]
else:
    social_network = ''

if len(sys.argv) >= 3:
    version= sys.argv[2]
else:
    version = ''

#CASOS:
if social_network in network_list:

#--------------------------------------------------
#CASO1: TWITTER
#--------------------------------------------------

    if social_network == 'twitter':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS TWITTER API---------------------------------------------------------------
        ##########################################################################################################################################

        CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
        CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
        ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
        ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret
        # Lanzamos una pestana por cada version del componente

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Master/twitter-timeline/static/TwitterCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Latency/twitter-timeline/static/TwitterCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Accuracy/twitter-timeline/static/TwitterCompletitudAccuracy.html")
                sleep(3)

        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        request_hometimeline="https://api.twitter.com/1.1/statuses/home_timeline.json?count=200"
        #Request timeline home
        s= requests.get(request_hometimeline, auth=oauth)
        timeline=s.json()
        contador=0
        lis=[]
        ids=[]
        users=[]
        for tweet in timeline:
            #if para ver si el tweet es un retweet
            if(tweet.has_key('retweeted_status')):
                text = tweet['retweeted_status']['text']
            else:
                text=tweet['text']

            id_tweet1=tweet['id_str']
            id_tweet1=int(id_tweet1)
            user=tweet['user']['name']
            contador=contador+1
            lis.append(text)
            users.append(user)
            #Twitter devuelve los id de los tweets cronologicamente (comprobado)
            ids.append(id_tweet1)
        print contador
        zipPython=zip(ids,lis)
        zipPythonUser=zip(ids,users)
        dictPython=dict(zipPython)
        dictPythonUser=dict(zipPythonUser)

        ##########################################################################################################################################
        #-----------------------------------------DATOS TWITTER COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        sleep(10)
                # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("70d459a2d5e96864f6eacdcb1a1fcd50","4dd2fff92abd81af8f06950f419f066a")
        lista=[]
        listacomp=[]
        listaid=[]
        listauser=[]
        listapos=[]
        liskey=[]
        lisvalue=[]
        listavalores=[]
        listavalores1=[]
        listaFallosText=[]
        listaFallosUser=[]

        if version in version_list:
            if version=="master":
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
                    #la k son los la i,text,id,user(en ese orden) y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    poscomp=y.items()[0][1]
                    textocomp=y.items()[1][1]
                    idcomp=y.items()[2][1]
                    idcomp=int(idcomp)
                    usercomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)
                    listauser.append(usercomp)

                zipComp=zip(listaid,listacomp)
                zipCompUser=zip(listaid,listauser)
                zipPos=zip(listaid,listapos)
                #Diccionario id, text
                dictComp=dict(zipComp)
                #Diccionario id, user
                dictCompUser=dict(zipCompUser)
                #Diccionario id, posicion
                dictCompPos=dict(zipPos)

                #Recorro el diccionario del componente, key es el id del tweet y value es el texto del tweet
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            print "OK"
                        else:
                            print "falla en: " + str(key)
                            print "falla en: " + value
                            liskey.append(key)
                            lisvalue.append(value)
                            listaFallosText=zip(liskey,lisvalue)

                    else:
                        print "el tweet que no esta en API twitter es: " + value
                        #mp.track(cont,"Fallos accuracy text",{"posicion": cont, "tweet": value, "version":version})

                #Recorro el diccionario del componente, k es el id del tweet y v es el user del tweet
                for k,v in dictCompUser.iteritems():
                     #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                         #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            print "OK"
                        else:
                            print "falla en: " + str(k) 
                            print "falla en: " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)

                    else:
                        print "el user que no esta es: " + v

                #diccionario de textos erroneos con su id
                dictFallosText=dict(listaFallosText)
                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)

                #Cojo el diccionario de los tweets fallidos y el diccionario {ids:posiciones} y miro que ids que han fallado estan en el otro diccionario y saco su pos
                for clave, valor in dictFallosText.iteritems():
                    if(dictCompPos.has_key(clave)):
                        valores=dictCompPos.get(clave,None)
                        mp.track(valores,"Fallos master text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                print listavalores

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mp.track(valores1,"Fallos master user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()
                print listavalores1
                           

                    
            elif version=="latency":
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
                    #la k son los la i,text,id,user(en ese orden) y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    poscomp=y.items()[0][1]
                    textocomp=y.items()[1][1]
                    idcomp=y.items()[2][1]
                    idcomp=int(idcomp)
                    usercomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)
                    listauser.append(usercomp)

                zipComp=zip(listaid,listacomp)
                zipCompUser=zip(listaid,listauser)
                zipPos=zip(listaid,listapos)
                #Diccionario id, text
                dictComp=dict(zipComp)
                #Diccionario id, user
                dictCompUser=dict(zipCompUser)
                #Diccionario id, posicion
                dictCompPos=dict(zipPos)

                #Recorro el diccionario del componente, key es el id del tweet y value es el texto del tweet
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            print "OK"
                        else:
                            print "falla en: " + str(key)
                            print "falla en: " + value
                            liskey.append(key)
                            lisvalue.append(value)
                            listaFallosText=zip(liskey,lisvalue)

                    else:
                        print "el tweet que no esta en API twitter es: " + value
                        #mp.track(cont,"Fallos accuracy text",{"posicion": cont, "tweet": value, "version":version})

                #Recorro el diccionario del componente, k es el id del tweet y v es el user del tweet
                for k,v in dictCompUser.iteritems():
                     #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                         #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            print "OK"
                        else:
                            print "falla en: " + str(k) 
                            print "falla en: " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)

                    else:
                        print "el user que no esta es: " + v

                #diccionario de textos erroneos con su id
                dictFallosText=dict(listaFallosText)
                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)

                #Cojo el diccionario de los tweets fallidos y el diccionario {ids:posiciones} y miro que ids que han fallado estan en el otro diccionario y saco su pos
                for clave, valor in dictFallosText.iteritems():
                    if(dictCompPos.has_key(clave)):
                        valores=dictCompPos.get(clave,None)
                        mp.track(valores,"Fallos latency text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                print listavalores

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mp.track(valores1,"Fallos latency user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()
                print listavalores1
                           


            elif version=="accuracy":
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
                    #la k son los la i,text,id,user(en ese orden) y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    poscomp=y.items()[0][1]
                    textocomp=y.items()[1][1]
                    idcomp=y.items()[2][1]
                    idcomp=int(idcomp)
                    usercomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listacomp.append(textocomp)
                    listaid.append(idcomp)
                    listauser.append(usercomp)

                zipComp=zip(listaid,listacomp)
                zipCompUser=zip(listaid,listauser)
                zipPos=zip(listaid,listapos)
                #Diccionario id, text
                dictComp=dict(zipComp)
                #Diccionario id, user
                dictCompUser=dict(zipCompUser)
                #Diccionario id, posicion
                dictCompPos=dict(zipPos)

                #Recorro el diccionario del componente, key es el id del tweet y value es el texto del tweet
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            print "OK"
                        else:
                            print "falla en: " + str(key)
                            print "falla en: " + value
                            liskey.append(key)
                            lisvalue.append(value)
                            listaFallosText=zip(liskey,lisvalue)

                    else:
                        print "el tweet que no esta en API twitter es: " + value
                        #mp.track(cont,"Fallos accuracy text",{"posicion": cont, "tweet": value, "version":version})

                #Recorro el diccionario del componente, k es el id del tweet y v es el user del tweet
                for k,v in dictCompUser.iteritems():
                     #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                         #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            print "OK"
                        else:
                            print "falla en: " + str(k) 
                            print "falla en: " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)

                    else:
                        print "el user que no esta es: " + v

                #diccionario de textos erroneos con su id
                dictFallosText=dict(listaFallosText)
                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)

                #Cojo el diccionario de los tweets fallidos y el diccionario {ids:posiciones} y miro que ids que han fallado estan en el otro diccionario y saco su pos
                for clave, valor in dictFallosText.iteritems():
                    if(dictCompPos.has_key(clave)):
                        valores=dictCompPos.get(clave,None)
                        mp.track(valores,"Fallos accuracy text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                print listavalores

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mp.track(valores1,"Fallos accuracy user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()
                print listavalores1
                           



#--------------------------------------------------
#CASO1: GITHUB
#--------------------------------------------------
                
    elif social_network == 'github':

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Master/GithubCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Latency/GithubCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Accuracy/GithubCompletitudAccuracy.html")
                sleep(3)


        ##########################################################################################################################################
        #----------------------------------------------------------DATOS GITHUB API---------------------------------------------------------------
        ##########################################################################################################################################

        contador=0
        lis=[]
        ids=[]
        users=[]
        github_url = "https://api.github.com/users/mortega5/received_events"
        peticion= requests.get(github_url)
        print peticion
        muro=peticion.json()
        for events in muro:
            print events
            idsevents=events['id']
            userevents=events['actor']['login']
            print idsevents
            print userevents
            print "------------------------------------------------------------------"
            contador=contador+1
            #lis.append(message)
            users.append(userevents)
            ids.append(idsevents)

            #SOLO IMPRIME 30, MIRAR POR QUE
        print contador
        zipPython=zip(ids,lis)
        zipPythonUser=zip(ids,users)
        dictPython=dict(zipPython)
        dictPythonUser=dict(zipPythonUser)


        ##########################################################################################################################################
        #------------------------------------------DATOS GITHUB COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        sleep(10)
                # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("1119893e7fea6aad13e030ad514595be","bf69f1d1620ca5a5bb2b116c3e3a9944")

        if version in version_list:
            if version=="master":
                #defino los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')               
                    
            elif version=="latency":
                        #defino los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')
                

            elif version=="accuracy":
                             #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

    
    #elif social_network == 'facebook' and len(sys.argv) >= 3:
        #     access_token = sys.argv[2]
            
    
    #else:
        #print "Wrong social network or missing param"
        # {}: Obligatorio, []: opcional
        #print "Usage: completitud.py {twitter|facebook|instagram|github [facebook_access_token]"


#if __name__ == "__main__":
    #main()



