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
import hashlib
from random import randrange
from mixpanel import Mixpanel
#objetos Mixpanel para las distintas redes sociales
mpTwitter = Mixpanel("b5b07b32170e37ea45248bb1a5a042a1")
mpGithub=Mixpanel("6dbce2a15a7e5bbd608908e8d0ed8518")
mpInstagram=Mixpanel("59e0cb154cc5192322be22b2a035738e")
mpFacebook=Mixpanel("04ae91408ffe85bf83628993704feb15")
mpGoogle=Mixpanel("f2655b08b62cc657d6865f8af003bdd9")
import mixpanel_api

#---------------------------------------------------------------------------------------------------------------------
network_list = ["twitter","instagram", "facebook", "github", "googleplus"]
version_list = ["master","latency", "accuracy"]

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

        #objeto oauth con credenciales de usuario Deus
        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        #url para hacer peticion al timeline de twitter
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
            ids.append(id_tweet1)
        print contador
        zipPython=zip(ids,lis)
        zipPythonUser=zip(ids,users)
        #diccionario de tweets e ids
        dictPython=dict(zipPython)
        #diccionario de users e ids
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
                            True
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
                            True
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

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpTwitter.track(valores1,"Fallos master user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()                           

                    
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
                            True
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
                            True
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

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpTwitter.track(valores1,"Fallos latency user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()                           


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
                            True
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
                            True
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
        listacomp=[]
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
            if (events['type']=="PushEvent"):
                message=events['payload']['commits'][0]['message']
            elif(events['type']=="WatchEvent"):
                message=events['payload']['action']
            elif(events['type']=="CreateEvent"):
                message="Creo un repositorio/ Creo una rama"
            elif(events['type']=="PullRequestEvent"):
                message=events['payload']['pull_request']['title']
            elif(events['type']=="IssuesEvent"):
                message=events['payload']['issue']['title']
            elif(events['type']=="MemberEvent"):
                message=events['payload']['action']
            elif(events['type']=="ForkEvent"):
                message="Realizo un fork"
            else:
                message=''
            lis.append(message)
            users.append(userevents)
            ids.append(idsevents)
        print contador
        ids.sort()
        ids.reverse()
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

                #Recorro el diccionario del componente, k es el id del post y v es el user del post
                for k,v in dictCompUser.iteritems():
                     #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                         #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            print "falla en: " + str(k) 
                            print "falla en: " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)


                #Recorro el diccionario del componente, key es el id del post y value es el texto del post
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            True
                        else:
                            print "falla en: " + str(key)
                            print "falla en: " + value
                            liskey.append(key)
                            lisvalue.append(value)
                            listaFallosText=zip(liskey,lisvalue)

                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)
                #diccionario de textos erroneos con su id
                dictFallosText=dict(listaFallosText)

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpGithub.track(valores1,"Fallos master user",{"posicion":valores1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()

             
                #Cojo el diccionario de los tweets fallidos y el diccionario {ids:posiciones} y miro que ids que han fallado estan en el otro diccionario y saco su pos
                for clave, valor in dictFallosText.iteritems():
                    if(dictCompPos.has_key(clave)):
                        valores=dictCompPos.get(clave,None)
                        mpGithub.track(valores,"Fallos master text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                         


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

                #Recorro el diccionario del componente, k es el id del post y v es el user del post
                for k,v in dictCompUser.iteritems():
                     #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                         #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            print "falla en: " + str(k) 
                            print "falla en: " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)


                #Recorro el diccionario del componente, key es el id del post y value es el texto del post
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            True
                        else:
                            print "falla en: " + str(key)
                            print "falla en: " + value
                            liskey.append(key)
                            lisvalue.append(value)
                            listaFallosText=zip(liskey,lisvalue)

                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)
                #diccionario de textos erroneos con su id
                dictFallosText=dict(listaFallosText)

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpGithub.track(valores1,"Fallos latency user",{"posicion":valores1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()

             
                #Cojo el diccionario de los tweets fallidos y el diccionario {ids:posiciones} y miro que ids que han fallado estan en el otro diccionario y saco su pos
                for clave, valor in dictFallosText.iteritems():
                    if(dictCompPos.has_key(clave)):
                        valores=dictCompPos.get(clave,None)
                        mpGithub.track(valores,"Fallos latency text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                         
               

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

                 #Recorro el diccionario del componente, k es el id del post y v es el user del post
                for k,v in dictCompUser.iteritems():
                     #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                         #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            print "falla en: " + str(k) 
                            print "falla en: " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)


                #Recorro el diccionario del componente, key es el id del post y value es el texto del post
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        if cmp(valuesP,value)==0:
                            True
                        else:
                            print "falla en: " + str(key)
                            print "falla en: " + value
                            liskey.append(key)
                            lisvalue.append(value)
                            listaFallosText=zip(liskey,lisvalue)

                #diccionario de users erroneos con su id
                dictFallosUser=dict(listaFallosUser)
                #diccionario de textos erroneos con su id
                dictFallosText=dict(listaFallosText)

                for clave1, valor1 in dictFallosUser.iteritems():
                    print valor1
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        mpGithub.track(valores1,"Fallos accuracy user",{"posicion":valores1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()

             
                #Cojo el diccionario de los tweets fallidos y el diccionario {ids:posiciones} y miro que ids que han fallado estan en el otro diccionario y saco su pos
                for clave, valor in dictFallosText.iteritems():
                    if(dictCompPos.has_key(clave)):
                        valores=dictCompPos.get(clave,None)
                        mpGithub.track(valores,"Fallos accuracy text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                         



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
        listatext=[]
        listatex=[]

        #instagram devuelve un diccionario con 3 keys (pagination, meta y data) y solo quiero quedar con el contenido de data
        for k,v in timeline.iteritems():
            if(timeline.has_key('data')):
                values=timeline.get('data',None)
        #recorro todos los campos que tiene data
        for items in values:
            idsevents=items['id']
            userevents=items['user']['username']
            imageevents=items['images']['standard_resolution']['url']
            hash_object = hashlib.sha1(imageevents)
            imageevents = hash_object.hexdigest()
            if(items['caption']!=None):
                textevents=items['caption']['text']
                listatex.append(textevents)
                for itemtext in listatex:
                    itemtext=str(itemtext)
                    #necesito restringir el texto porque sino no puedo comparar con los datos de Mixpanel ya que restringe el num de caracteres
                    hash_object = hashlib.sha1(itemtext)
                    textevents = hash_object.hexdigest()
                    texts.append(textevents)
            else:
                texts.append('')

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
        zipPythonText=zip(ids,texts)
        dictPythonText=dict(zipPythonText)

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
                    idcomp=y.items()[3][1]
                    usercomp=y.items()[4][1]
                    imagencomp=y.items()[2][1]
                    poscomp=y.items()[0][1]
                    textcomp=y.items()[1][1]
                    listaid.append(idcomp)
                    listauser.append(usercomp)
                    listaimage.append(imagencomp)
                    listapos.append(poscomp)
                    listatext.append(textcomp)
        

                zipCompUser=zip(listapos,listauser)
                zipPos=zip(listapos,listaid)
                zipCompImage=zip(listapos,listaimage)
                zipCompText=zip(listapos,listatext)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, id
                dictCompPos=dict(zipPos)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
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
                    if(dictPythonImage.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            True
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



                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosText,"Fallos master text",{"posicion":listaFallosText, "version":version})

                    
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
                    idcomp=y.items()[3][1]
                    usercomp=y.items()[4][1]
                    imagencomp=y.items()[2][1]
                    poscomp=y.items()[0][1]
                    textcomp=y.items()[1][1]
                    listaid.append(idcomp)
                    listauser.append(usercomp)
                    listaimage.append(imagencomp)
                    listapos.append(poscomp)
                    listatext.append(textcomp)
        

                zipCompUser=zip(listapos,listauser)
                zipPos=zip(listapos,listaid)
                zipCompImage=zip(listapos,listaimage)
                zipCompText=zip(listapos,listatext)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, id
                dictCompPos=dict(zipPos)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
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
                    if(dictPythonImage.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            True
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

                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosText,"Fallos latency text",{"posicion":listaFallosText, "version":version})

              

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
                    idcomp=y.items()[3][1]
                    usercomp=y.items()[4][1]
                    imagencomp=y.items()[2][1]
                    poscomp=y.items()[0][1]
                    textcomp=y.items()[1][1]
                    listaid.append(idcomp)
                    listauser.append(usercomp)
                    listaimage.append(imagencomp)
                    listapos.append(poscomp)
                    listatext.append(textcomp)

                zipCompUser=zip(listapos,listauser)
                zipPos=zip(listapos,listaid)
                zipCompImage=zip(listapos,listaimage)
                zipCompText=zip(listapos,listatext)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, id
                dictCompPos=dict(zipPos)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
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
                    if(dictPythonImage.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            True
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

                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpInstagram.track(listaFallosText,"Fallos accuracy text",{"posicion":listaFallosText, "version":version})


#--------------------------------------------------
#CASO4: FACEBOOK
#--------------------------------------------------

    elif social_network == 'facebook':

#RECORDAR QUE FACE NO MUESTRA LOS POST SECUNCIALMENTE, SINO QUE LOS MUESTRA "COMO QUIERE". Por lo que, en la version de accuracy,
#cuando se miren los datos que fallan no van a coincidir con las posiciones de fallo que se guardan en mixpanel
#Facebook hace una ordenacion por ACTUALIZACION, no por creacion


        ##########################################################################################################################################
        #--------------------------------------------------------DATOS FACEBOOK API---------------------------------------------------------------
        ##########################################################################################################################################

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Master/facebook-wall/FacebookCompletitud.html")
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Latency/facebook-wall/FacebookCompletitudLatency.html")
                sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Accuracy/facebook-wall/FacebookCompletitudAccuracy.html")
                sleep(5)

         
        access_token="EAANMUmJPs2UBAHotDhenr6acOhnZC1jjNg6syL8zBcoW5A2nHbMFIOE1XWBzhsh3gZAZBmcTl9lYgh0NusE5ZAlJKAknZAYQ0C0rY5H9HEYVuZBHdZCnU6OE2GuMqCFWFUPb4ZCsZBi9HlwyBz6VgZADr8GqNoMZAIy4fBbHknedNOMAAZDZD"
        facebook_url = "https://graph.facebook.com/v2.3/me?fields=home&pretty=1&access_token=" + access_token

        #Request timeline home
        s= requests.get(facebook_url)
        print s
        muro=s.json()
        contador=0
        texto=[]
        ids=[]
        users=[]
        listacont=[]
        lista=[]
        images=[]
        listapos=[]
        listauser=[]
        listatext=[]
        listaimg=[]
        liskey=[]
        lisvalue=[]
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
             #if para ver si un description o un message
            if(items1.has_key('description')):
                text1 = items1['description']
                hash_object = hashlib.sha1(text1)
                text = hash_object.hexdigest()
            elif (items1.has_key('message')):
                text1=items1['message']
                hash_object = hashlib.sha1(text1)
                text = hash_object.hexdigest()
            else:
                text= ''


            if(items1.has_key('picture')):
                imagen1=items1['picture']
                hash_object = hashlib.sha1(imagen1)
                imagen = hash_object.hexdigest()
            else:
                imagen=''
          

            listacont.append(contador)
            contador=contador+1
            ids.append(idsevents)
            users.append(userevents)
            images.append(imagen)
            texto.append(text)

        print contador
        zipPythonUser=zip(listacont,users)
        dictPythonUser=dict(zipPythonUser)
        zipPythonTexto=zip(listacont,texto)
        dictPythonText=dict(zipPythonTexto)
        zipPythonImage=zip(listacont,images)
        dictPythonImage=dict(zipPythonImage)

        ##########################################################################################################################################
        #-------------------------------------------DATOS FACEBOOK COMPONENTE (RECOGIDOS DE MIXPANEL)---------------------------------------------
        ##########################################################################################################################################

        sleep(10)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("de21df1c2c63dff29ffce8a1a449494a","a7917928a9ba3dd88592fac7ac36e8a9")

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
                    poscomp=y.items()[0][1]
                    imagecomp=y.items()[1][1]
                    usercomp=y.items()[2][1]
                    textcomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listaimg.append(imagecomp)
                    listauser.append(usercomp)
                    listatext.append(textcomp)
                    
                zipCompUser=zip(listapos,listauser)
                zipCompImage=zip(listapos,listaimg)
                zipCompText=zip(listapos,listatext)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                    #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosUser,"Fallos master user",{"posicion":listaFallosUser, "version":"master"})

                    else:
                        print "el user que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)


                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompImage.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonImage.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "la imagen que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosImagen=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosImagen,"Fallos master imagen",{"posicion":listaFallosImagen, "version":"master"})

                    else:
                        print "la imagen que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)

                #Recorro el diccionario del componente, k es la posicion y v es el texto
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosText,"Fallos master text",{"posicion":listaFallosText, "version":"master"})  


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
                    poscomp=y.items()[0][1]
                    imagecomp=y.items()[1][1]
                    usercomp=y.items()[2][1]
                    textcomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listaimg.append(imagecomp)
                    listauser.append(usercomp)
                    listatext.append(textcomp)
                    
                zipCompUser=zip(listapos,listauser)
                zipCompImage=zip(listapos,listaimg)
                zipCompText=zip(listapos,listatext)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                    #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosUser,"Fallos latency user",{"posicion":listaFallosUser, "version":"latency"})

                    else:
                        print "el user que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)


                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompImage.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonImage.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "la imagen que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosImagen=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosImagen,"Fallos latency imagen",{"posicion":listaFallosImagen, "version":"latency"})

                    else:
                        print "la imagen que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)

                #Recorro el diccionario del componente, k es la posicion y v es el texto
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosText,"Fallos latency text",{"posicion":listaFallosText, "version":"latency"})  

            
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
                    poscomp=y.items()[0][1]
                    imagecomp=y.items()[1][1]
                    usercomp=y.items()[2][1]
                    textcomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listaimg.append(imagecomp)
                    listauser.append(usercomp)
                    listatext.append(textcomp)
                    
                zipCompUser=zip(listapos,listauser)
                zipCompImage=zip(listapos,listaimg)
                zipCompText=zip(listapos,listatext)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, imagen
                dictCompImage=dict(zipCompImage)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)

                #Recorro el diccionario del componente, k es la posicion y v es el user
                for k,v in dictCompUser.iteritems():
                #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                    #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosUser,"Fallos accuracy user",{"posicion":listaFallosUser, "version":"accuracy"})

                    else:
                        print "el user que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)


                #Recorro el diccionario del componente, k es la posicion y v es la imagen
                for k,v in dictCompImage.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonImage.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonImagen=dictPythonImage.get(k,None)
                        if cmp(vPythonImagen,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "la imagen que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosImagen=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosImagen,"Fallos accuracy imagen",{"posicion":listaFallosImagen, "version":"accuracy"})

                    else:
                        print "la imagen que no esta es: " + v
                        print "corresponde a la posicion: " + str(k)

                #Recorro el diccionario del componente, k es la posicion y v es el texto
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpFacebook.track(listaFallosText,"Fallos accuracy text",{"posicion":listaFallosText, "version":"accuracy"})  


#--------------------------------------------------
#CASO5: GOOGLE+
#--------------------------------------------------

    elif social_network == 'googleplus':

        ##########################################################################################################################################
        #--------------------------------------------------------DATOS GOOGLE+ API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Master/googleplus-timeline/demo/GooglePlusCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Latency/googleplus-timeline/demo/GooglePlusCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/accuracy_metric/Accuracy/googleplus-timeline/demo/GooglePlusCompletitudAccuracy.html")
                sleep(3)

        sleep(5)
         
        access_token=" ya29.CjkRAyYODwEOPnuYiQ09rOMs34IKMUipFaGhQX6CXCBtWgG0VQwTyyLoN3OvbgAjq0Ay4-dXyOXMUv0"
        google_url_followers="https://www.googleapis.com/plus/v1/people/me/people/visible"
        headers = {"Authorization": "Bearer " + access_token}
        
        #Request a followers de Deus
        s= requests.get(google_url_followers,headers=headers)
        muro=s.json()
        followers=[]
        if(muro.has_key('items')):
            values1=muro.get('items',None)
            for n in values1:
                id_followers=n['id']
                id_followers=int(id_followers)
                followers.append(id_followers)

        texto=[]
        users=[]
        ids=[]
        listacont=[]
        lista=[]
        images=[]
        listapos=[]
        listauser=[]
        listapub=[]
        listatext=[]
        liskey=[]
        lisvalue=[]
        publicado=[]
        contador=0
        cont=0

        #Request a timeline Deus para todos los usuarios
        for i in followers:
            #hay que poner str(i) porque sino no se puede concatenar string con un long (int)
            google_url="https://www.googleapis.com/plus/v1/people/" + str(i) + "/activities/public"
            pet= requests.get(google_url,headers=headers)
            print pet

            timeline=pet.json()
            if(timeline.has_key('items')):
                values1=timeline.get('items',None)
            for n in values1:
                users_name=n['actor']['displayName']
                text1=n['object']['content']
                hash_object = hashlib.sha1(text1)
                text = hash_object.hexdigest()
                id_user=n['id']
                published=n['published']
                #uso calendar.timegm porque me devuelve el tiempo desde el epoch time (al igual que javascript). Si utilizo time.mktime me lo devuelve como localtime
                publish=calendar.timegm(datetime.datetime.strptime(published, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())
                publish=int(float(publish))

                listacont.append(contador)
                contador=contador+1 
                ids.append(id_user)
                users.append(users_name)
                texto.append(text)
                publicado.append(publish)

        time_pub=zip(publicado,users)
        for time in time_pub:
            zipPythonUser=sorted(time_pub, reverse=True)
        zipPythonUser1=zipPythonUser[0:16]
        #diccionario de Python de usuarios ordenado por tiempo de publicacion
        dictPythonUser=dict(zipPythonUser1)


        texto_pub=zip(publicado,texto)
        for texto1 in texto_pub:
            zipPythonText=sorted(texto_pub, reverse=True)
        zipPythonTexto1=zipPythonText[0:16]
        #diccionario de Python de textos ordenado por tiempo de publicacion
        dictPythonText=dict(zipPythonTexto1)


        ##########################################################################################################################################
        #-------------------------------------------DATOS GOOGLE+ COMPONENTE (RECOGIDOS DE MIXPANEL)---------------------------------------------
        ##########################################################################################################################################

        sleep(10)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("b9eb42288e7e416028ddf3ee70ae4ca9","0c24b55a9806c9eb41cb3d5f3a7e7ef6")

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
                newlist = sorted(lista, key=lambda posicion: posicion['publish'], reverse=True)

                for y in newlist:
                    poscomp=y.items()[0][1]
                    textcomp=y.items()[1][1]
                    usercomp=y.items()[2][1]
                    publishcomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listauser.append(usercomp)
                    listatext.append(textcomp)
                    listapub.append(publishcomp)

                zipCompUser=zip(listapub,listauser)
                zipCompText=zip(listapub,listatext)
                zipCompPub=zip(listapub,listapub)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)


                #Recorro el diccionario del componente, k es el tiempo de publicacion y v es el user
                for k,v in dictCompUser.iteritems():
                #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                    #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpGoogle.track(listaFallosUser,"Fallos master user",{"posicion":listaFallosUser, "version":"master"})



                #Recorro el diccionario del componente, k es el tiempo de publicacion y v es el texto
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpGoogle.track(listaFallosText,"Fallos master text",{"posicion":listaFallosText, "version":"master"})


            elif version=="latency":
                #defino los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el tiempo de publicacion
                newlist = sorted(lista, key=lambda posicion: posicion['publish'], reverse=True)

                for y in newlist:
                    poscomp=y.items()[0][1]
                    textcomp=y.items()[1][1]
                    usercomp=y.items()[2][1]
                    publishcomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listauser.append(usercomp)
                    listatext.append(textcomp)
                    listapub.append(publishcomp)

                zipCompUser=zip(listapub,listauser)
                zipCompText=zip(listapub,listatext)
                zipCompPub=zip(listapub,listapub)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)


                #Recorro el diccionario del componente, k es el tiempo de publicacion y v es el user
                for k,v in dictCompUser.iteritems():
                #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                    #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpGoogle.track(listaFallosUser,"Fallos latency user",{"posicion":listaFallosUser, "version":"latency"})



                #Recorro el diccionario del componente, k es el tiempo de publicacion y v es el texto
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpGoogle.track(listaFallosText,"Fallos latency text",{"posicion":listaFallosText, "version":"latency"})


            elif version=="accuracy":
                #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
                newlist = sorted(lista, key=lambda posicion: posicion['publish'], reverse=True)

                for y in newlist:
                    poscomp=y.items()[0][1]
                    textcomp=y.items()[1][1]
                    usercomp=y.items()[2][1]
                    publishcomp=y.items()[3][1]
                    listapos.append(poscomp)
                    listauser.append(usercomp)
                    listatext.append(textcomp)
                    listapub.append(publishcomp)

                zipCompUser=zip(listapub,listauser)
                zipCompText=zip(listapub,listatext)
                zipCompPub=zip(listapub,listapub)
                #Diccionario posicion, user
                dictCompUser=dict(zipCompUser)
                #Diccionario posicion, imagen
                dictCompText=dict(zipCompText)


                #Recorro el diccionario del componente, k es el tiempo de publicacion y v es el user
                for k,v in dictCompUser.iteritems():
                #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonUser.has_key(k)):
                    #si es asi, cojo los values de python y del componente y los comparo
                        vPythonUser=dictPythonUser.get(k,None)
                        if cmp(vPythonUser,v)==0:
                            True
                        else:
                            #devuelvo el timestampo del que falla, pero no devuelvo la posicion porque no corresponde a lo que se muestra en el timeline, ya que Ana
                            #no ordena las fechas por hora, minutos y segundos. Solo los ordena por dia, por lo que los posts del mismo dia aparecen "como quieren"
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            mpGoogle.track(listaFallosUser,"Fallos accuracy user",{"posicion":listaFallosUser, "version":"accuracy"})



                #Recorro el diccionario del componente, k es el tiempo de publicacion y v es el texto
                for k,v in dictCompText.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPythonText.has_key(k)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        vPythonText=dictPythonText.get(k,None)
                        if cmp(vPythonText,v)==0:
                            True
                        else:
                            print "falla en posicion: " + str(k) 
                            print "el texto que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosText=zip(liskey,lisvalue)
                            mpGoogle.track(listaFallosText,"Fallos accuracy text",{"posicion":listaFallosText, "version":"accuracy"})    
    else:
        print "Wrong social network or missing param"
        # {}: Obligatorio, []: opcional
        print "Usage: completitud.py {twitter|facebook|instagram|github [facebook_access_token]"


#if __name__ == "__main__":
    #main()



