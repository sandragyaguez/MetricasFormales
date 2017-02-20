
#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*

import httplib
import urllib2, urllib
from random import getrandbits
from hashlib import sha1
import json
import hmac
import base64
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
import sys
import facebook
import urlparse
import random
import string
import ast
import mixpanel
import mixpanel_api, json
from mixpanel import Mixpanel
mpTwitter = Mixpanel("070bf8a01a6127ebf78325716490697a")
mpFacebook=Mixpanel("f9177cf864c2778e099d5ec71113d0bf")
mpPinterest=Mixpanel("98b144c253b549db5cdeb812a9323ca3")
mpTraffic=Mixpanel("d47fab64a1be9d41d8b1e8850df74754")
mpWeather=Mixpanel("1a7d93449a9b07f9d00e86e03a1a7d6a")


network_list = ["twitter", "facebook","googleplus", "pinterest", "traffic-incidents", "open-weather"]
version_list = ["master","latency", "accuracy"]
url_base_remote= "http://metricas-formales.appspot.com/app/refresh_metric"
url_base_local= "http://localhost:8080/refresh_metric"

#de los comandos que ejecuto desde consola, me quedo con el segundo (posicion 1,array empieza en 0),consola: python refresco.py twitter coge la "variable" twitter
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

        #Las credenciales no cambian, a no ser que se quieran hacer peticiones con un usuarios que no sea Deus
        CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
        CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
        ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
        ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret

        listestado=[]
        listtpubl_ms=[]

        #funcion random para crear tweets aleatorios
        def randomword(length):
            return ''.join(random.choice(string.lowercase) for i in range(length))

        estado=randomword(10)
        #PUBLICACION DE TWEET Y REQUEST DEL TIMELINE
        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_remote + "/Master/twitter-timeline/static/TwitterRefresco.html" + "?" + estado)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_remote + "/Latency/twitter-timeline/static/TwitterRefrescoLatency.html"  + "?" + estado)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_remote + "/Accuracy/twitter-timeline/static/TwitterRefrescoAccuracy.html" + "?" + estado)
                sleep(3)

   
        #Request publicar tweet
        def publicar(estado):
            if estado == '':
                return 1
            print "--------------------------------------------------------------"
            #CODIGO DE ERROR SI EL TWEET YA ESTABA PUBLICADO (ERROR CODE STATUS 187). CUANDO RESPONSE ==403
            r = requests.post(url=url,data={"status":estado},auth=oauth)
            if r.status_code == 403:
                print "Tweet duplicado"
                return 1
            print "Respuesta: " + str(r)
            tpubl=datetime.datetime.now()
            tpubl_ms=int(time.time()*1000)
            print "tiempo post en ms: " + str(tpubl_ms)
            listestado.append(estado)
            listtpubl_ms.append(tpubl_ms)

            #Request timeline user   
            s= requests.get(request_usertimeline, auth=oauth)
            timeline=s.json()
            #Encontrar el texto del tweet que acabo de publicar, con el campo text que tiene cada tweet, y timestamp cuando me lo muestre en twitter (tambien se puede hacer con ID)(polling)
            for tweet in timeline:
                text=tweet['text']
                if text==estado:
                    break

        #Pruebas
        publicar(estado)

        #zip con todos los post y sus correspondientes tiempos de publicacion
        zipPython=zip(listestado,listtpubl_ms)
        dictPython=dict(zipPython)

        ##########################################################################################################################################
        #-----------------------------------------DATOS TWITTER COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(70)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("c10939e3faf2e34b4abb4f0f1594deaa","4a3b46218b0d3865511bc546384b8928")
        lista=[]
        listacomp=[]
        listatime=[]

        if version in version_list:
            if version=="master":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el tweet
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    #obtengo el texto de cada post recogido del componente
                    textocomp=y.items()[0][1]
                    #obtengo el tiempo de cada post recogido del componente
                    timecomp=y.items()[1][1]
                    #voy guardando ambos datos en dos listas diferentes
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario tweet, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto del tweet y el value son los times de refresco en el componente
                #en la siguiente prueba, aunque en el dict de Python haya dos keys con sus values, dictComp solo tiene una key y un value porque
                #es el nuevo evento. Y busco la key del componente (del nuevo evento) en el dict de Python por lo que siempre va a restar bien los tiempos
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        #resto el tiempo obtenido del componente menos el tiempo que me devuelve directamente la api al postear
                        final_time=float(value)-float(valuesP)
                        print "final_time: " + str(final_time)
                        #mando a Mixpanel el tiempo final obtenido de la resta, el post al que pertenece esa diferencia de tiempo y la version que estamos tratando
                        mpTwitter.track(final_time, "Final time master",{"time final": final_time, "post": key, "version":version})

            elif version=="latency":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el tweet
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario tweet, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto del tweet y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        final_time=float(value)-float(valuesP)
                        print "final_time: " + str(final_time)
                        mpTwitter.track(final_time, "Final time latency",{"time final": final_time, "post": key, "version":version})

            elif version=="accuracy":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el tweet
                newlist = sorted(lista, key=lambda tweet: tweet['tweet'])

                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario tweet, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto del tweet y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        final_time=float(value)-float(valuesP)
                        print "final_time: " + str(final_time)
                        mpTwitter.track(final_time, "Final time accuracy",{"time final": final_time, "post": key, "version":"master"})



#--------------------------------------------------
#CASO2: FACEBOOK
#--------------------------------------------------
    elif social_network == 'facebook':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS FACEBOOK API--------------------------------------------------------------
        ##########################################################################################################################################
        
        #funcion random para crear publicaciones aleatorias
        def randomword(length):
            return ''.join(random.choice(string.lowercase) for i in range(length))

        message=randomword(10)

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/facebook-wall/FacebookRefresco.html" + "?" + message)
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/facebook-wall/FacebookRefrescoLatency.html" + "?" + message)
                sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/facebook-wall/FacebookRefrescoAccuracy.html" + "?" + message)
                sleep(5)

        #es necesario cambiar el token cada hora y media: https://developers.facebook.com/tools/explorer/928341650551653 (Get User Access Token, version 2.3)
        access_token='EAANMUmJPs2UBAMhsmC2RmpMyUZCaY8qcB7hnNbCvVhOvcTZB6cPmfyAHNiSP90UoZChLeoAWrHwgZCtaGOubUW3GEZBZBSP5qlqvPrMZBhzmXJtPCDaE5VcPIYA2cZCmZACY3PZAZApfMZCQEHMoyxXGs90vK05L81vDMOTICNuntJLhuwZDZD'

        listestado=[]
        listtpubl_ms=[]

        #uso la API de facebook pasandole como parametro el access token y la version de la api que utilizamos
        graph = facebook.GraphAPI(access_token=access_token, version='2.3')

        #POST EN FACEBOOK
        attachment =  {}
        graph.put_wall_post(message=message, attachment=attachment)
        tpubl=datetime.datetime.now()
        tpubl_ms=int(time.time()*1000)
        print "tiempo post en ms: " + str(tpubl_ms)
        listestado.append(message)
        listtpubl_ms.append(tpubl_ms)

        zipPython=zip(listestado,listtpubl_ms)
        #diccionario con los mensajes publicados y su tiempo de publicacion
        dictPython=dict(zipPython)
        print dictPython

        ##########################################################################################################################################
        #----------------------------------------DATOS FACEBOOK COMPONENTE (RECOGIDOS DE MIXPANEL)-----------------------------------------------
        ##########################################################################################################################################
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(70)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("1c480cfa1d4cbaaeadc5c102a9ff50ea","b1308de232be2c6edf329081831eba52")
        lista=[]
        listacomp=[]
        listatime=[]

        if version in version_list:
            if version=="master":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpFacebook.track(final_time, "Final time master",{"time final": final_time, "post": key, "version":version})


            elif version=="latency":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpFacebook.track(final_time, "Final time latency",{"time final": final_time, "post": key, "version":version})


            elif version=="accuracy":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    textocomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(textocomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)
                print dictComp

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpFacebook.track(final_time, "Final time accuracy",{"time final": final_time, "post": key, "version":version})

   


#--------------------------------------------------
#CASO3: GOOGLEPLUS
#--------------------------------------------------
    elif social_network == 'googleplus':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS FACEBOOK API--------------------------------------------------------------
        ##########################################################################################################################################
        
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/googleplus-timeline/demo/GoogleplusRefresco.html")
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/googleplus-timeline/demo/GoogleplusRefrescoLatency.html")
                sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/googleplus-timeline/demo/GoogleplusRefrescoAccuracy.html")
                sleep(5)


             

#--------------------------------------------------
#CASO4: PINTEREST
#--------------------------------------------------

    elif social_network == 'pinterest':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS PINTEREST API---------------------------------------------------------------
        ##########################################################################################################################################
        
        image_url="http://www.mundoperro.net/wp-content/uploads/Perro-Carlino-485x300.jpg"

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/pinterest-timeline/demo/PinterestRefresco.html" + "?" + image_url)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/pinterest-timeline/demo/PinterestRefrescoLatency.html" + "?" + image_url)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/pinterest-timeline/demo/PinterestRefrescoAccuracy.html" + "?" + image_url)
                sleep(3)

        access_token="AXh-Xld9fy7jeDuI23ovntIthRVjFI6N-kmb11xDmW-C0gBCfwAAAAA"
        post_my_board= "https://api.pinterest.com/v1/me/pins/?access_token=" + access_token
        note="Take a look"
        link="https://www.google.es/search?q=perros&espv=2&biw=1855&bih=966&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjchq_cz8vRAhXCzxQKHQ4DCWMQ_AUIBigB#imgrc=BqLqaxHeCHP0ZM%3A"
        board="829295787572730316"

        listimags=[]
        listtpubl_ms=[]

        def post_pin(access_token, board, note, link, image_url):
            response = urllib.urlopen(
                'https://api.pinterest.com/v1/pins/',
                data=urllib.urlencode(dict(
                    access_token=access_token,
                    board=board,
                    note=note,
                    link=link,
                    image_url=image_url
                )))

            response_data = json.load(response)
            tpubl_ms=int(time.time())
            print "tiempo post en ms: " + str(tpubl_ms)
            listimags.append(image_url)
            listtpubl_ms.append(tpubl_ms)

        sleep(2)
        post_pin(access_token, board, note, link, image_url)


        zipPython=zip(listimags,listtpubl_ms)
        #diccionario con los mensajes publicados y su tiempo de publicacion
        dictPython=dict(zipPython)
        print dictPython


        ##########################################################################################################################################
        #----------------------------------------DATOS PINTEREST COMPONENTE (RECOGIDOS DE MIXPANEL)-----------------------------------------------
        ##########################################################################################################################################
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(70)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales (API KEY y API SECRET)
        x=mixpanel_api.Mixpanel("c6a5d1682613e89df94c6eceb3859be6","17a38edfdff693b56b50f332ae8f8e9e")
        lista=[]
        listacomp=[]
        listatime=[]

        if version in version_list:
            if version=="master":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    urlcomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(urlcomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpPinterest.track(final_time, "Final time master",{"time final": final_time, "post": key, "version":version})


            elif version=="latency":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    urlcomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(urlcomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpPinterest.track(final_time, "Final time latency",{"time final": final_time, "post": key, "version":version})


            
            elif version=="accuracy":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    urlcomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(urlcomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpPinterest.track(final_time, "Final time accuracy",{"time final": final_time, "post": key, "version":version})




#--------------------------------------------------
#CASO4: TRAFFIC INCIDENTS
#--------------------------------------------------

    elif social_network == 'traffic-incidents':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS TRAFFIC API---------------------------------------------------------------
        ##########################################################################################################################################
        
        def randomword(length):
            return ''.join(random.choice(string.lowercase) for i in range(length))

        description=randomword(10)

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/traffic-incidents/demo/TrafficRefresco.html" + "?" + description)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/traffic-incidents/demo/TrafficRefrescoLatency.html" + "?" + description)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/traffic-incidents/demo/TrafficRefrescoAccuracy.html" + "?" + description)
                sleep(3)

        listpost=[]
        listtpubl_ms=[]
        
        datos = {"description": description}
        url = "https://centauro.ls.fi.upm.es:4444/traffic"
        response = requests.post(url, data=datos, verify=False)
        tpubl_ms=int(time.time())
        listpost.append(description)
        listtpubl_ms.append(tpubl_ms)

        zipPython=zip(listpost,listtpubl_ms)
        #diccionario con los mensajes publicados y su tiempo de publicacion
        dictPython=dict(zipPython)
        print dictPython


        ##########################################################################################################################################
        #----------------------------------------DATOS TRAFFIC COMPONENTE (RECOGIDOS DE MIXPANEL)-----------------------------------------------
        ##########################################################################################################################################
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(70)
        #limpio la cache antes de coger datos del componente
        url = "https://centauro.ls.fi.upm.es:4444/fakes/traffic/clean"
        response = requests.get(url, verify=False)


        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales (API KEY y API SECRET)
        x=mixpanel_api.Mixpanel("f84c5fe9d8cacb4271819b9e0f06f5e5","4b7abff36fb44e36332e12ff744d36c5")
        lista=[]
        listacomp=[]
        listatime=[]

        if version in version_list:
            if version=="master":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    postcomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(postcomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpTraffic.track(final_time, "Final time master",{"time final": final_time, "post": key, "version":version})



            elif version=="latency":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    postcomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(postcomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpTraffic.track(final_time, "Final time latency",{"time final": final_time, "post": key, "version":version})


            elif version=="accuracy":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    postcomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(postcomp)
                    listatime.append(timecomp)

                zipComp=zip(listacomp,listatime)
                #Diccionario post, time
                dictComp=dict(zipComp)

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpTraffic.track(final_time, "Final time accuracy",{"time final": final_time, "post": key, "version":version})



#--------------------------------------------------
#CASO5: OPEN WEATHER
#--------------------------------------------------

    elif social_network == 'open-weather':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS TRAFFIC API---------------------------------------------------------------
        ##########################################################################################################################################
        
        #cojo el tiempo para saber que hora es y conocer a partir de que hora tengo que publicar
        #tengo un array con 8 tiempos a publicar porque corresponde a las horas 0 3 6 9 12 15 18 21
        tiempo=time.strftime("%H")
        print tiempo
        datos1=[]
        #cuando divido entres 3 conozco el intervalo en el que estoy y a partir de que elemento tengo que coger en el array par apublicar
        #si por ejemplo tiempo=12. Divido 12/3=4 y se que tengo que publicar desde la posicion 4 de mi array datos
        intervalo=int(tiempo)/int(3)
        print intervalo
        datos = [{"temp": 1, "min": 1, "max": 20, "icon": "wi-day-sunny"}, {"temp": 2, "min": 1, "max": 20, "icon": "wi-day-sunny"},{"temp": 3, "min": 1, "max": 20, "icon": "wi-day-sunny"},{"temp": 4, "min": 1, "max": 20, "icon": "wi-day-sunny"},{"temp": 5, "min": 1, "max": 20, "icon": "wi-day-sunny"},{"temp": 6, "min": 1, "max": 20, "icon": "wi-day-sunny"},{"temp": 7, "min": 1, "max": 20, "icon": "wi-day-sunny"},{"temp": 8, "min": 1, "max": 20, "icon": "wi-day-sunny"}]
        
        #creo que lo correcto seria datos1=datos[intervalo+1:] pero hay problemas con la franja horaria. REVISAR
        datos1=datos[intervalo:]
        datos1= str(datos1)

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/open-weather/demo/WeatherRefresco.html" + "?" + datos1)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/open-weather/demo/WeatherRefrescoLatency.html" + "?" + datos1)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/open-weather/demo/WeatherRefrescoAccuracy.html" + "?" + datos1)
                sleep(3)


        listpost=[]
        listtpubl_ms=[]
        
        #codificar datos porque la peticion hay que hacerla en ese formato
        datos = str(datos)
        datos = 'data='+ urllib.quote(datos)


        headers= {
            "content-type":"application/x-www-form-urlencoded"
        }
        url = "https://centauro.ls.fi.upm.es:4444/weather"
        response = requests.post(url, data=datos, verify=False, headers=headers)
        print response
        tpubl_ms=int(time.time())
        print tpubl_ms
        listpost.append(datos1)
        listtpubl_ms.append(tpubl_ms)


        zipPython=zip(listpost,listtpubl_ms)
        #diccionario con los mensajes publicados y su tiempo de publicacion
        dictPython=dict(zipPython)
        print dictPython

        ##########################################################################################################################################
        #----------------------------------------DATOS WEATHER COMPONENTE (RECOGIDOS DE MIXPANEL)-----------------------------------------------
        ##########################################################################################################################################
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(70)
        #limpio la cache antes de coger datos del componente
        url = "https://centauro.ls.fi.upm.es:4444/fakes/weather/clean"
        response = requests.get(url, verify=False)


        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales (API KEY y API SECRET)
        x=mixpanel_api.Mixpanel("c8fcf17a2d3201de0c409c902d8f4a08","60375710344595c8d8a05b18a9574adb")
        lista=[]
        listacomp=[]
        listatime=[]

        if version in version_list:
            if version=="master":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el post
                newlist = sorted(lista, key=lambda post: post['post'])
                for y in newlist:
                    postcomp=y.items()[0][1]
                    timecomp=y.items()[1][1]
                    listacomp.append(postcomp)
                    listatime.append(timecomp)

                print listacomp
                print "********************************************"
                print listatime
                zipComp=zip(listacomp,listatime)
                print "********************************************"
                print "********************************************"
                print zipComp
                #Diccionario post, time
                dictComp=dict(zipComp)

                #la key es el texto de la publicacion y el value son los times de refresco en el componente
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                            valuesP=dictPython.get(key,None)
                            final_time=float(value)-float(valuesP)
                            print "final_time: " + str(final_time)
                            mpTraffic.track(final_time, "Final time master",{"time final": final_time, "post": key, "version":version})

