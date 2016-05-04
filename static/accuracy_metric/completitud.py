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
mpTwitter = Mixpanel("b5b07b32170e37ea45248bb1a5a042a1")
mpGithub=Mixpanel("6dbce2a15a7e5bbd608908e8d0ed8518")
mpInstagram=Mixpanel("59e0cb154cc5192322be22b2a035738e")
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
                        mpTwitter.track(valores,"Fallos master text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                print listavalores

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpTwitter.track(valores1,"Fallos master user",{"posicion":valores1 ,"tweet": valor1, "version":version})
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
                        mpTwitter.track(valores,"Fallos latency text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                print listavalores

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpTwitter.track(valores1,"Fallos latency user",{"posicion":valores1 ,"tweet": valor1, "version":version})
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

                #Recorro el diccionario del componente, k es el id del tweet y v es el user del tweet
                for k,v in dictCompUser.iteritems():
                     #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                         #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            print "OK"
                        else:
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
                        mpTwitter.track(valores,"Fallos accuracy text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                print listavalores

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpTwitter.track(valores1,"Fallos accuracy user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()
                print listavalores1
                           



#--------------------------------------------------
#CASO2: GITHUB
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
        lista=[]
        listapos=[]
        listaid=[]
        listauser=[]
        liskey=[]
        lisvalue=[]
        listavalores=[]
        listavalores1=[]
        listaFallosText=[]
        listaFallosUser=[]

        github_url = "https://api.github.com/users/mortega5/received_events?per_page=50"
        peticion= requests.get(github_url)
        print peticion
        muro=peticion.json()
        for events in muro:
            idsevents=events['id']
            idsevents=int(idsevents)
            userevents=events['actor']['login']
            contador=contador+1
            #lis.append(message)
            users.append(userevents)
            ids.append(idsevents)
        print contador
        ids.sort()
        ids.reverse()
        #zipPython=zip(ids,lis)
        zipPythonUser=zip(ids,users)
        #dictPython=dict(zipPython)
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

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda id_event: id_event['id'])
                newlist.reverse()

                for y in newlist:
                    #la k son los la i,text,id,user(en ese orden) y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    poscomp=y.items()[0][1]
                    #textocomp=y.items()[1][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    usercomp=y.items()[2][1]
                    listapos.append(poscomp)
                    #listacomp.append(textocomp)
                    listaid.append(idcomp)
                    listauser.append(usercomp)

                #zipComp=zip(listaid,listacomp)
                zipCompUser=zip(listaid,listauser)
                zipPos=zip(listaid,listapos)
                #Diccionario id, text
                #dictComp=dict(zipComp)
                #Diccionario id, user
                dictCompUser=dict(zipCompUser)
                #Diccionario id, posicion
                dictCompPos=dict(zipPos)

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
                        print "corresponde al id: " + str(k)

                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpGithub.track(valores1,"Fallos master user",{"posicion":valores1, "version":version})
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
                newlist = sorted(lista, key=lambda id_event: id_event['id'])
                newlist.reverse()

                for y in newlist:
                    #la k son los la i,text,id,user(en ese orden) y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    poscomp=y.items()[0][1]
                    #textocomp=y.items()[1][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    usercomp=y.items()[2][1]
                    listapos.append(poscomp)
                    #listacomp.append(textocomp)
                    listaid.append(idcomp)
                    listauser.append(usercomp)

                #zipComp=zip(listaid,listacomp)
                zipCompUser=zip(listaid,listauser)
                zipPos=zip(listaid,listapos)
                #Diccionario id, text
                #dictComp=dict(zipComp)
                #Diccionario id, user
                dictCompUser=dict(zipCompUser)
                #Diccionario id, posicion
                dictCompPos=dict(zipPos)

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
                        print "corresponde al id: " + str(k)

                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpGithub.track(valores1,"Fallos latency user",{"posicion":valores1, "version":version})
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
                newlist = sorted(lista, key=lambda id_event: id_event['id'])
                newlist.reverse()

                for y in newlist:
                    #la k son los la i,text,id,user(en ese orden) y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
                    poscomp=y.items()[0][1]
                    #textocomp=y.items()[1][1]
                    idcomp=y.items()[1][1]
                    idcomp=int(idcomp)
                    usercomp=y.items()[2][1]
                    listapos.append(poscomp)
                    #listacomp.append(textocomp)
                    listaid.append(idcomp)
                    listauser.append(usercomp)

                #zipComp=zip(listaid,listacomp)
                zipCompUser=zip(listaid,listauser)
                zipPos=zip(listaid,listapos)
                #Diccionario id, text
                #dictComp=dict(zipComp)
                #Diccionario id, user
                dictCompUser=dict(zipCompUser)
                #Diccionario id, posicion
                dictCompPos=dict(zipPos)

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
                        print "corresponde al id: " + str(k)

                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpGithub.track(valores1,"Fallos accuracy user",{"posicion":valores1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()
                print listavalores1



#--------------------------------------------------
#CASO3: INSTAGRAM
#--------------------------------------------------

    elif social_network == 'instagram':

            ##########################################################################################################################################
            #-------------------------------------------------------DATOS INSTAGRAM API---------------------------------------------------------------
            ##########################################################################################################################################

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Master/instagram-timeline/static/InstagramCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Latency/instagram-timeline/static/InstagramCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Accuracy/instagram-timeline/static/InstagramCompletitudAccuracy.html")
                sleep(3)

 

        insta_url="https://api.instagram.com/v1/users/self/feed?access_token=2062815740.34af286.169a9c42e1404ae58591d066c00cb979"
        pet= requests.get(insta_url)
        print pet
        timeline=pet.json()

        contador=0
        listacont=[]
        texts=[]
        ids=[]
        users=[]
        images=[]
        lista=[]
        listapos=[]
        listaid=[]
        listaimage=[]
        listauser=[]
        liskey=[]
        lisvalue=[]
        listavalores=[]
        listavalores1=[]
        listaFallosText=[]
        listaFallosUser=[]

        #instagram devuelve un diccionario con 3 keys (pagination, meta y data) y solo quiero quedar con el contenido de data
        for k,v in timeline.iteritems():
            if(timeline.has_key('data')):
                values=timeline.get('data',None)
        #recorro todos los campos que tiene data
        for items in values:
            idsevents=items['id']
            userevents=items['user']['username']
            imageevents=items['images']['standard_resolution']['url']
            #if(items['caption']!=None):
                #textevents=items['caption']['text']
                #texts.append(textevents)
            #else:
                #texts.append("")
            listacont.append(contador)
            contador=contador+1
            ids.append(idsevents)
            users.append(userevents)
            images.append(imageevents)
        print contador
        zipPythonUser=zip(listacont,users)
        dictPythonUser=dict(zipPythonUser)
        zipPythonImage=zip(listacont,images)
        dictPythonImage=dict(zipPythonImage)
        #zipPythonText=zip(ids,texts)
        #dictPythonText=dict(zipPythonText)


        ##########################################################################################################################################
        #-----------------------------------------DATOS INSTAGRAM COMPONENTE (RECOGIDOS DE MIXPANEL)----------------------------------------------
        ##########################################################################################################################################
        sleep(10)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("26904a5a94b675f2360d75af0ccbf0b6","2af7a58160fd737d242e81d9055a02c3")

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
                newlist = sorted(lista, key=lambda posicion: posicion['i'])

                for y in newlist:
                #la k son los la id,user,i(en ese orden) y las v son los valores de cada uno
                    idcomp=y.items()[2][1]
                    usercomp=y.items()[3][1]
                    imagencomp=y.items()[1][1]
                    poscomp=y.items()[0][1]
                    listaid.append(idcomp)
                    listauser.append(usercomp)
                    listaimage.append(imagencomp)
                    listapos.append(poscomp)
        

                zipCompUser=zip(listapos,listauser)
                zipPos=zip(listapos,listaid)
                zipCompImage=zip(listapos,listaimage)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, id
                dictCompPos=dict(zipPos)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            print "OK"
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosUser,"Fallos master user",{"posicion":listaFallosUser, "version":version})

                    else:
                        print "el user que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)


                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompImage.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            print "OK"
                        else:
                            print "falla en posicion: " + str(k) 
                            print "la imagen que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosImagen=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosImagen,"Fallos master imagen",{"posicion":listaFallosImagen, "version":version})

                    else:
                        print "la imagen que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)

                    
            elif version=="latency":
                #defino los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda posicion: posicion['i'])

                for y in newlist:
                #la k son los la id,user,i(en ese orden) y las v son los valores de cada uno
                    idcomp=y.items()[2][1]
                    usercomp=y.items()[3][1]
                    imagencomp=y.items()[1][1]
                    poscomp=y.items()[0][1]
                    listaid.append(idcomp)
                    listauser.append(usercomp)
                    listaimage.append(imagencomp)
                    listapos.append(poscomp)
        

                zipCompUser=zip(listapos,listauser)
                zipPos=zip(listapos,listaid)
                zipCompImage=zip(listapos,listaimage)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, id
                dictCompPos=dict(zipPos)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            print "OK"
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosUser,"Fallos latency user",{"posicion":listaFallosUser, "version":version})

                    else:
                        print "el user que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)


                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompImage.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            print "OK"
                        else:
                            print "falla en posicion: " + str(k) 
                            print "la imagen que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosImagen=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosImagen,"Fallos latency imagen",{"posicion":listaFallosImagen, "version":version})

                    else:
                        print "la imagen que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)

              

            elif version=="accuracy":
                #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda posicion: posicion['i'])

                for y in newlist:
                #la k son los la id,user,i(en ese orden) y las v son los valores de cada uno
                    idcomp=y.items()[2][1]
                    usercomp=y.items()[3][1]
                    imagencomp=y.items()[1][1]
                    poscomp=y.items()[0][1]
                    listaid.append(idcomp)
                    listauser.append(usercomp)
                    listaimage.append(imagencomp)
                    listapos.append(poscomp)
        

                zipCompUser=zip(listapos,listauser)
                zipPos=zip(listapos,listaid)
                zipCompImage=zip(listapos,listaimage)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, id
                dictCompPos=dict(zipPos)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            print "OK"
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosUser,"Fallos accuracy user",{"posicion":listaFallosUser, "version":version})

                    else:
                        print "el user que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)


                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompImage.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            print "OK"
                        else:
                            print "falla en posicion: " + str(k) 
                            print "la imagen que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosImagen=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosImagen,"Fallos accuracy imagen",{"posicion":listaFallosImagen, "version":version})

                    else:
                        print "la imagen que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)



    elif social_network == 'facebook':

        ##########################################################################################################################################
        #--------------------------------------------------------DATOS FACEBOOK API---------------------------------------------------------------
        ##########################################################################################################################################

        webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Master/facebook-wall/FacebookCompletitud.html")
        sleep(3)
         
        access_token="EAACEdEose0cBAJUSvIw0P1tfiFFGZBynfWsiJi7DG7md9QxV5SKreLvNn66ZBNRubvLfboXOZCfqpBOdj8EZCx08kfN3OUyyFsZCneiKNjo24rzDmxZBUAkvLHztZBu3L1mVxjECsDnCUiiQ3OoXI1O4tsZCuT0y8zSbHGhKvi12rwZDZD"
        facebook_url = "https://graph.facebook.com/v2.3/me?fields=home&pretty=1&access_token=" + access_token

        #Request timeline home
        s= requests.get(facebook_url)
        print s
        muro=s.json()
        contador=0
        lis=[]
        ids=[]
        users=[]
        listacont=[]
        lista=[]
        listapos=[]
        listauser=[]
        #facebook devuelve un diccionario con 2 keys (home, id) y solo me quiero quedar con los values del home
        for k,v in muro.iteritems():
            if(muro.has_key('home')):
                values=muro.get('home',None)

        #recorro todos los campos que tiene data
        for items in values:
            if(values.has_key('data')):
                values1=values.get('data',None)

        for items1 in values1:
            idsevents=items1['id']
            userevents=items1['from']['name']
            print userevents

            listacont.append(contador)
            contador=contador+1
            ids.append(idsevents)
            #users.append(userevents)
        
        print contador
        #zipPythonUser=zip(listacont,users)
        #dictPythonUser=dict(zipPythonUser)
        #zipPythonImage=zip(listacont,images)
        #dictPythonImage=dict(zipPythonImage)

        ##########################################################################################################################################
        #-------------------------------------------DATOS FACEBOOK COMPONENTE (RECOGIDOS DE MIXPANEL)---------------------------------------------
        ##########################################################################################################################################

        sleep(10)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("de21df1c2c63dff29ffce8a1a449494a","a7917928a9ba3dd88592fac7ac36e8a9")

        #defino los parametros necesarios para la peticion
        params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
        respuesta=x.request(['events/properties/values'], params, format='json')

        for x in respuesta:
            #pasar de unicode a dict
            resp = ast.literal_eval(x)
            lista.append(resp)

        #ordeno la lista de diccionarios por el id
        newlist = sorted(lista, key=lambda posicion: posicion['i'])

        for y in newlist:
            #la k son los la id,user,i(en ese orden) y las v son los valores de cada uno
            poscomp=y.items()[0][1]
            usercomp=y.items()[1][1]
            listapos.append(poscomp)
            listauser.append(usercomp)
            
        zipCompUser=zip(listapos,listauser)
        #Diccionario posicion, user
        dictCompUser=dict(zipCompUser)
        print dictCompUser


    #elif social_network == 'facebook' and len(sys.argv) >= 3:
        #     access_token = sys.argv[2]
            
    
    #else:
        #print "Wrong social network or missing param"
        # {}: Obligatorio, []: opcional
        #print "Usage: completitud.py {twitter|facebook|instagram|github [facebook_access_token]"


#if __name__ == "__main__":
    #main()



