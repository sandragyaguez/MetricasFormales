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
import mixpanel_api

#objetos Mixpanel para las distintas redes sociales
mpTwitter = Mixpanel("b5b07b32170e37ea45248bb1a5a042a1")
mpFacebook=Mixpanel("04ae91408ffe85bf83628993704feb15")
mpGoogle=Mixpanel("f2655b08b62cc657d6865f8af003bdd9")
mpPinterest=Mixpanel("6ceb3a37029277deb7f530ac7d65d7d4")

#---------------------------------------------------------------------------------------------------------------------
network_list = ["twitter", "facebook", "googleplus", "pinterest"]
version_list = ["master","latency", "accuracy"]
url_base_remote= "http://metricas-formales.appspot.com/app/accuracy_metric"
url_base_local= "http://localhost:8080/accuracy_metric"

#de los comandos que ejecuto desde consola, me quedo con el segundo (posicion 1,array empieza en 0),
#consola: python completitud.py twitter coge la "variable" twitter
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


############################################
############################################
            #CASO1: TWITTER
############################################
############################################


    if social_network == 'twitter':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS TWITTER API---------------------------------------------------------------
        ##########################################################################################################################################

        #Las credenciales no cambian, a no ser que se quieran hacer peticiones con un usuarios que no sea Deus
        CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
        CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
        ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
        ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret


        #Lanzamos una pestana por cada version del componente
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new( url_base_remote + "/Master/twitter-timeline/static/TwitterCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new( url_base_remote + "/Latency/twitter-timeline/static/TwitterCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new( url_base_remote + "/Accuracy/twitter-timeline/static/TwitterCompletitudAccuracy.html")
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
                #guardo texto del tweet
                text=tweet['text']
            #guardo id del tweet
            id_tweet1=tweet['id_str']
            id_tweet1=int(id_tweet1)
            #guardo el usuario que ha publicado el tweet
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
        contadorFallos=0

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
                    #la k son la i,text,id,user(en ese orden) y las v son los valores de cada uno. [0][1] del texto cojo su valor (posicion 0 que es el texto y posicion 1 que es el valor)
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
                        #si coinciden devuelvo true, sino muestro que tweet es el que ha fallado
                        if cmp(valuesP,value)==0:
                            True
                        else:
                            print "falla en: " + str(key)
                            print "falla en: " + value
                            liskey.append(key)
                            lisvalue.append(value)
                            contadorFallos=contadorFallos+1
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
                            contadorFallos=contadorFallos+1
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
                        #mpTwitter.track(valores,"Fallos master text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        #mpTwitter.track(valores1,"Fallos master user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()

                contadorFallos=contadorFallos/float(contador)
                mpTwitter.track(contadorFallos, "Fallos totales master", {"numero fallos": contadorFallos})                           

                    
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
                            contadorFallos=contadorFallos+1
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
                            contadorFallos=contadorFallos+1
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
                        #mpTwitter.track(valores,"Fallos latency text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        #mpTwitter.track(valores1,"Fallos latency user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort() 

                contadorFallos=contadorFallos/float(contador)
                mpTwitter.track(contadorFallos, "Fallos totales latency", {"numero fallos": contadorFallos})                            


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
                            contadorFallos=contadorFallos+1
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
                            contadorFallos=contadorFallos+1
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
                        #mpTwitter.track(valores,"Fallos accuracy text",{"posicion":valores ,"tweet": valor, "version":version})
                    listavalores.append(valores)
                listavalores.sort()
                print listavalores

                for clave1, valor1 in dictFallosUser.iteritems():
                    if(dictCompPos.has_key(clave1)):
                        valores1=dictCompPos.get(clave1,None)
                        #mpTwitter.track(valores1,"Fallos accuracy user",{"posicion":valores1 ,"tweet": valor1, "version":version})
                    listavalores1.append(valores1)
                listavalores1.sort()
                print listavalores1

                fallosTotales=contadorFallos/float(contador)
                print fallosTotales
                mpTwitter.track(contadorFallos, "Fallos totales latency", {"numero fallos": contadorFallos})
                           

############################################
############################################
            #CASO2: FACEBOOK
############################################
############################################

    elif social_network == 'facebook':

#RECORDAR QUE FACE NO MUESTRA LOS POST SECUNCIALMENTE, SINO QUE LOS MUESTRA "COMO QUIERE". Por lo que, en la version de accuracy,
#cuando se miren los datos que fallan no van a coincidir con las posiciones de fallo que se guardan en mixpanel
#Facebook hace una ordenacion por ACTUALIZACION, no por creacion


        ##########################################################################################################################################
        #--------------------------------------------------------DATOS FACEBOOK API---------------------------------------------------------------
        ##########################################################################################################################################

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_remote + "/Master/facebook-wall/FacebookCompletitud.html")
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new(url_base_remote + "/Latency/facebook-wall/FacebookCompletitudLatency.html")
                sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_remote + "/Accuracy/facebook-wall/FacebookCompletitudAccuracy.html")
                sleep(5)

        #es necesario cambiar el token cada hora y media: https://developers.facebook.com/tools/explorer/928341650551653 (Get User Access Token, version 2.3)
        access_token="EAANMUmJPs2UBADlumZA4z9ZBJPAFczLhPliTS0SepEXUGd9DsPEl6bVsM953ja4WfXRj10ouLT3OuhZBltXR5yBjLB82DLYA1SQmYiNPeSEnsZAvO1cV2KcWiw6J040OO6ImHE0worFkJIt841HVsCvWRDgU6gy8wos0gMCZB8AZDZD"
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
            #guardo el id de la publicacion
            idsevents=items1['id']
            #guardo el usuario de la publicacion
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

            #en casa de haber una imagen, la guardo
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
        #diccionario contador y usuarios
        dictPythonUser=dict(zipPythonUser)
        zipPythonTexto=zip(listacont,texto)
        #diccionario contador y textos
        dictPythonText=dict(zipPythonTexto)
        zipPythonImage=zip(listacont,images)
        #diccionario contador e imagenes
        dictPythonImage=dict(zipPythonImage)

        ##########################################################################################################################################
        #-------------------------------------------DATOS FACEBOOK COMPONENTE (RECOGIDOS DE MIXPANEL)---------------------------------------------
        ##########################################################################################################################################

        sleep(10)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("de21df1c2c63dff29ffce8a1a449494a","a7917928a9ba3dd88592fac7ac36e8a9")
        contadorFallos=0

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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosUser,"Fallos master user",{"posicion":listaFallosUser, "version":"master"})

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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosImagen,"Fallos master imagen",{"posicion":listaFallosImagen, "version":"master"})

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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosText,"Fallos master text",{"posicion":listaFallosText, "version":"master"})  

                contadorFallos=contadorFallos/float(contador)
                print contadorFallos
                mpFacebook.track(contadorFallos, "Fallos totales master", {"numero fallos": contadorFallos})

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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosUser,"Fallos latency user",{"posicion":listaFallosUser, "version":"latency"})

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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosImagen,"Fallos latency imagen",{"posicion":listaFallosImagen, "version":"latency"})

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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosText,"Fallos latency text",{"posicion":listaFallosText, "version":"latency"})  

                contadorFallos=contadorFallos/float(contador)
                print contadorFallos
                mpFacebook.track(contadorFallos, "Fallos totales latency", {"numero fallos": contadorFallos})
            
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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosUser,"Fallos accuracy user",{"posicion":listaFallosUser, "version":"accuracy"})

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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosImagen,"Fallos accuracy imagen",{"posicion":listaFallosImagen, "version":"accuracy"})

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
                            contadorFallos=contadorFallos+1
                            #mpFacebook.track(listaFallosText,"Fallos accuracy text",{"posicion":listaFallosText, "version":"accuracy"})  

                contadorFallos=contadorFallos/float(contador)
                print contadorFallos
                mpFacebook.track(contadorFallos, "Fallos totales accuracy", {"numero fallos": contadorFallos})

############################################
############################################
            #CASO3: GOOGLE+
############################################
############################################

    elif social_network == 'googleplus':

        ##########################################################################################################################################
        #--------------------------------------------------------DATOS GOOGLE+ API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_remote + "/Master/googleplus-timeline/demo/GooglePlusCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_remote + "/Latency/googleplus-timeline/demo/GooglePlusCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_remote + "/Accuracy/googleplus-timeline/demo/GooglePlusCompletitudAccuracy.html")
                sleep(3)

        sleep(5)
        
        #cambiar token cada hora y media: https://developers.google.com/+/web/api/rest/latest/activities/list?authuser=1
        access_token=" ya29.CjlYA4BhZvIJllOAI0BJHEQ2dbmX-CTolwmV1OrqGq30pfdKhu1fZKr288pBAZMPBaWzisCONy5fKeM"
        google_url_followers="https://www.googleapis.com/plus/v1/people/me/people/visible"
        headers = {"Authorization": "Bearer " + access_token}
        
        #Request a followers de Deus
        s= requests.get(google_url_followers,headers=headers)
        muro=s.json()
        followers=[]
        if(muro.has_key('items')):
            values1=muro.get('items',None)
            for n in values1:
                #guardo el id del follower
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

        #Request a timeline Deus para todos los usuarios. Para obtener la informacion de los post, previamente he tenido que obtener los followers
        for i in followers:
            #hay que poner str(i) porque sino no se puede concatenar string con un long (int)
            google_url="https://www.googleapis.com/plus/v1/people/" + str(i) + "/activities/public"
            pet= requests.get(google_url,headers=headers)
            print pet

            timeline=pet.json()
            if(timeline.has_key('items')):
                values1=timeline.get('items',None)
            for n in values1:
                #guardo el usuario del post
                users_name=n['actor']['displayName']
                #guardo el contenido del post
                text1=n['object']['content']
                #hash para "comprimir" el texto
                hash_object = hashlib.sha1(text1)
                text = hash_object.hexdigest()
                #guardo el id del post
                id_user=n['id']
                #guardo el tiempo de publicacion
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
        contadorFallos=0

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
                            contadorFallos=contadorFallos+1
                            #mpGoogle.track(listaFallosUser,"Fallos master user",{"posicion":listaFallosUser, "version":"master"})


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
                            contadorFallos=contadorFallos+1
                            #mpGoogle.track(listaFallosText,"Fallos master text",{"posicion":listaFallosText, "version":"master"})

                contadorFallos=contadorFallos/float(contador)
                print contadorFallos
                mpGoogle.track(contadorFallos, "Fallos totales master", {"numero fallos": contadorFallos})

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
                            contadorFallos=contadorFallos+1
                            #mpGoogle.track(listaFallosUser,"Fallos latency user",{"posicion":listaFallosUser, "version":"latency"})


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
                            contadorFallos=contadorFallos+1
                            #mpGoogle.track(listaFallosText,"Fallos latency text",{"posicion":listaFallosText, "version":"latency"})

                contadorFallos=contadorFallos/float(contador)
                print contadorFallos
                mpGoogle.track(contadorFallos, "Fallos totales latency", {"numero fallos": contadorFallos})


            elif version=="accuracy":
                #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
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
                            #devuelvo el timestamp del que falla, pero no devuelvo la posicion porque no corresponde a lo que se muestra en el timeline, ya que Ana
                            #no ordena las fechas por hora, minutos y segundos. Solo los ordena por dia, por lo que los posts del mismo dia aparecen "como quieren"
                            print "falla en posicion: " + str(k) 
                            print "el usuario que falla es : " + v
                            liskey.append(k)
                            lisvalue.append(v)
                            listaFallosUser=zip(liskey,lisvalue)
                            contadorFallos=contadorFallos+1
                            #mpGoogle.track(listaFallosUser,"Fallos accuracy user",{"posicion":listaFallosUser, "version":"accuracy"})


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
                            contadorFallos=contadorFallos+1
                            #mpGoogle.track(listaFallosText,"Fallos accuracy text",{"posicion":listaFallosText, "version":"accuracy"}) 

                contadorFallos=contadorFallos/float(contador)
                print contadorFallos
                mpGoogle.track(contadorFallos, "Fallos totales accuracy", {"numero fallos": contadorFallos})

############################################
############################################
            #CASO4: PINTEREST
############################################
############################################

    elif social_network == 'pinterest':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS PINTEREST API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/pinterest-timeline/demo/PinterestCompletitud.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/pinterest-timeline/demo/PinterestCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/pinterest-timeline/demo/PinterestCompletitudAccuracy.html")
                sleep(3)

        access_token="AYzOkS8gPFoFyhU56X9RjekH8IQFFI3y549FYk9DmW-C0gBCfwAAAAA"
        request_my_board= "https://api.pinterest.com/v1/me/pins/?access_token=" + access_token  + "&limit=60"
        request_others= "https://api.pinterest.com/v1/me/following/boards/?access_token=" + access_token

        #tengo que hacer una primera peticion a los boards de a los que sigo para poder pedir sus pins (imagenes)
        s= requests.get(request_others)
        timeline=s.json()

        lista_img=[]
        username=[]
        board=[]
        pets=[]
        imagAPI=[]

        #recorro el timeline y cojo de la clave data sus valores y dentro de sus valores la url de cada tablero
        for k,v in timeline.iteritems():
            if(timeline.has_key('data')):
                values1=timeline.get('data',None)
        for m in values1:
            if(m.has_key('url')):
                values3=m.get('url',None)
            lista_img.append(values3)

        # de cada url separo por / para poder coger el nombre del usuario y del tablero para despues poder hacer peticion de pins
        for image in lista_img:
            new=image.split("/")
            #cojo todos los username a los que sigo para poder hacer la siguiente peticion
            new[3]=str(new[3])
            username.append(new[3])
            #cojo todos los nombres de los tableros
            new[4]=str(new[4])
            board.append(new[4])

        #junto cada usuario con su tablero
        zipUserBoard=zip(username,board)
        
        #voy a crear todas las urls a las que tengo que hacer peticion con su usuario y tablero correspondiente
        #los anido todos en una lista y finalmente le anado la url de my board (cuidado si tengo mas de un board creado, que pasa?)
        for user,tablero in zipUserBoard:
            pet="https://api.pinterest.com/v1/boards/" + user + "/" + tablero + "/pins/?access_token=" + access_token + "&limit=60"
            pets.append(pet)
        pets.append(request_my_board)

        #metodo que hace todas las peticiones pasandole la lista de urls
        def makeRequest(url):
            pet= requests.get(url)
            return pet.json()
            
        #metodo que coge las urls de las imagenes (60 como maximo por cada tablero)
        def getData(pets):
            for pet in pets:
                request=makeRequest(pet)
                data= request.get('data',None)
                for urls in data:
                    url=urls.get('url', None)
                    imagAPI.append(url) 

                # hacer las siguiente 60 peticiones          
                # siguiente=request.get('page',None).get('next',None)
                # while(siguiente):
                #     request=makeRequest(siguiente)
                #     for urls in data:
                #         url=urls.get('url', None)
                #         imagAPI.append(url)
                #     siguiente=request.get('page',None).get('next',None)
                    
        getData(pets)
        print len(imagAPI)
        

        ##########################################################################################################################################
        #------------------------------------------DATOS PINTEREST COMPONENTE (RECOGIDOS DE MIXPANEL)---------------------------------------------
        ##########################################################################################################################################

        sleep(10)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("55736dc621aade0a3e80ea2f7f28f42b","5d34c88bc7f29c166e56484966b1c85b")

        imagComp=[]
        contadorFallos=0


       #metodo que me compara la lista de imagenes obtenidas por la API con la lista de imagenes cogidas en el componente
        def comp(list1, list2):
            fallos=[]
            if len(list1) != len(list2):
                print "no tienen la misma longitud"
                return False
            for val in list1:
                if not (val in list2):
                    fallos.append(val)
                    contadorFallos=contadorFallos+1        
            return fallos   


        if version in version_list:
            if version=="master":
            #defino los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    resp=str(x)
                    imagComp.append(resp)
                print len(imagComp)

                fallos=comp(imagAPI,imagComp)
                print fallos

                mpPinterest.track(fallos,"Fallos master imagenes",{"imagen":fallos, "version":"master"})
                contadorFallos=contadorFallos/float(contador)
                mpPinterest.track(contadorFallos, "Fallos totales master", {"numero fallos": contadorFallos})
 

            elif version=="latency":
                #defino los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    resp=str(x)
                    imagComp.append(resp)
                print len(imagComp)
         
                fallos=comp(imagAPI,imagComp)
                print fallos

                mpPinterest.track(fallos,"Fallos latency imagenes",{"imagen":fallos, "version":"latency"})
                ontadorFallos=contadorFallos/float(contador)
                mpPinterest.track(contadorFallos, "Fallos totales latency", {"numero fallos": contadorFallos})
 

            elif version=="accuracy":
                #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    resp=str(x)
                    imagComp.append(resp)
                print len(imagComp)
            
                fallos=comp(imagAPI,imagComp)
                print fallos

                mpPinterest.track(fallos,"Fallos accuracy imagenes",{"imagen":fallos, "version":"accuracy"})
                ontadorFallos=contadorFallos/float(contador)
                mpPinterest.track(contadorFallos, "Fallos totales accuracy", {"numero fallos": contadorFallos})
 

                



    else:
        print "Wrong social network or missing param"
        # {}: Obligatorio, []: opcional
        print "Usage: completitud.py {twitter|facebook|instagram|github [facebook_access_token]"


#if __name__ == "__main__":
    #main()



