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
mpGithub=Mixpanel("870ae6fd08343fcfb154ad6ed5227c47")


##########################################################################################################################################
##########################################################################################################################################
#----------------------------------------------------------------OAUTH 1.0----------------------------------------------------------------
##########################################################################################################################################
##########################################################################################################################################

CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret

class OauthTwitter():

  def __init__(self, consumer_key, consumer_secret, access_key, access_secret):

    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.access_key = access_key
    self.access_secret = access_secret
    self.request_url ="https://api.twitter.com/oauth/request_token"
    self.authenticate_url = "https://api.twitter.com/oauth/authenticate"
    self.request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"

  def get_auth_token(self):

    #Crear todos los parametros que se necesitan y meterlos en la cabecera. Los parametros viene especificados por la API de Twitter
    HEADER_TITLE = "Authorization"
    #Consumer key
    HEADER = 'OAuth oauth_consumer_key="' + self.consumer_key + '", '
    #Nonce
    nonce= str(getrandbits(64))
    HEADER += 'oauth_nonce="' + nonce +'", '
    #Timestamp
    timestamp= str(int(time.time()))
    #Signature
    key= urllib2.quote(self.consumer_secret) + "&" + urllib2.quote (self.access_secret)

    # Join all of the params together
    #params_str = "&".join(["%s=%s" % (encode(k), encode(HEADER[k])) for k in sorted(HEADER)])

    base_string = 'GET&' + urllib2.quote(self.request_url, safe="") + '&' + urllib2.quote("oauth_consumer_key=" + self.consumer_key + "&oauth_nonce=" + nonce +
        "&oauth_signature_method=HMAC-SHA1&oauth_timestamp=" + timestamp + "&oauth_token=" + self.access_key +"&oauth_version=1.0",safe="")

    #md5.digest()
    signature= hmac.new(key,base_string, sha1).digest()
    #para pasar a ascii necesito un codificador (base64)
    signature = base64.standard_b64encode (signature).decode('ascii')
    HEADER += 'oauth_signature="' + urllib2.quote(signature, safe="") + '", '

    #Signature Method
    HEADER += 'oauth_signature_method="HMAC-SHA1", '
    #Timestamp
    HEADER += 'oauth_timestamp="' + timestamp + '", '
    #TOKEn
    HEADER += 'oauth_token="' + self.access_key + '", '
    #Version
    HEADER += 'oauth_version="1.0"'

    #Peticion de token, devuelve oauth_token,oauth_token_secret y oauth_callback_confirmed
    req= urllib2.Request(self.request_url)
    req.add_header(HEADER_TITLE, HEADER)
    response = urllib2.urlopen(req).read()
    response = [k.split("=") for k in response.split("&")]
    #response_json = {}
    #for k in response:
      #response_json[k[0]] = k[1]

    tokens=[]
    for v in response:
        token1=v[1]
        tokens.append(token1)
    oauth_token=tokens[0]
    oauth_token_secret=tokens[1]
    oauth_verifier1=tokens[2]

#-------------------------------------------------------------------------------------------------------------------
#Get Authorization URL. Request para permitir autorizacion
    # authoriza= "https://api.twitter.com/oauth/authorize?oauth_token=%s" % oauth_token
    # req1=urllib2.Request(authoriza)
    # response1 = urllib2.urlopen(req1).read()
    # webbrowser.open(authoriza)
    # time.sleep(3)

    # oauth_verifier="TnEti5JqFtKcQqVxFtcLMrcpyPrRyuuy"
    # access_token_url= "https://api.twitter.com/oauth/access_token?oauth_verifier=%s" % oauth_verifier

#Request token y token secret finales
    # req5= urllib2.Request(access_token_url)
    # req5.add_header(HEADER_TITLE, HEADER)
    # response5 = urllib2.urlopen(req5).read()

#     oauth = OAuth1Session(self.consumer_key,self.consumer_secret,oauth_token,oauth_token_secret,oauth_verifier)
#     oauth_tokens = oauth.fetch_access_token(self.access_token_url)
#     resource_owner_key = oauth_tokens.get('oauth_token')
#     resource_owner_secret = oauth_tokens.get('oauth_token_secret')

#---------------------------------------
#Get Authentication URL.
    #authorize_url1 = self.authenticate_url +'?'+"oauth_token=" + oauth_token
    #authent = "https://api.twitter.com/oauth/authenticate?oauth_token=%s" % oauth_token
    #req2=urllib2.Request(authent)
    #response2=urllib2.urlopen(req2).read()
   #mirar como sacar los parametros de la url al hacer esta peticion. O ver donde me devuelve el oauth_token y el oauth_verifier
    #webbrowser.open(authent)
#-----------------------------------------

#PRUEBAS
objeto = OauthTwitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
respuesta = objeto.get_auth_token()




##########################################################################################################################################
##########################################################################################################################################
#----------------------------------------------------------------REFRESCO----------------------------------------------------------------
##########################################################################################################################################
##########################################################################################################################################


network_list = ["twitter","instagram", "facebook", "github"]
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

        listestado=[]
        listtpubl_ms=[]

        #digits = "".join( [random.choice(string.digits) for i in xrange(8)] )
        #chars = "".join( [random.choice(string.letters) for i in xrange(15)] )
        #print digits + chars

        def randomword(length):
            return ''.join(random.choice(string.lowercase) for i in range(length))

        estado=randomword(10)
        #PUBLICACION DE TWEET Y REQUEST DEL TIMELINE
        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Master/twitter-timeline/static/TwitterRefresco.html" + "?" + estado)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Latency/twitter-timeline/static/TwitterRefrescoLatency.html"  + "?" + estado)
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Accuracy/twitter-timeline/static/TwitterRefrescoAccuracy.html" + "?" + estado)
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

                #ordeno la lista de diccionarios por el id
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
                #en la siguiente prueba, aunque en el dict de Python haya dos keys con sus values, dictComp solo tiene una key y un value porque
                #es el nuevo evento. Y busco la key del componente (del nuevo evento) en el dict de Python por lo que siempre va a restar bien los tiempos
                for key,value in dictComp.iteritems():
                    #compruebo que el diccionario de Python contiene todas las claves del diccionario del componente
                    if(dictPython.has_key(key)):
                        #si es asi, cojo los values de python y del componente y los comparo
                        valuesP=dictPython.get(key,None)
                        #if cmp(valuesP,value)==0:
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        mpTwitter.track(final_time, "Final time master",{"time final": final_time, "tweet": key, "version":version})

            elif version=="latency":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
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
                        #if cmp(valuesP,value)==0:
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        mpTwitter.track(final_time, "Final time latency",{"time final": final_time, "tweet": key, "version":version})

            elif version=="accuracy":
                #Cuando lo tengas, defines los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                for x in respuesta:
                    #pasar de unicode a dict
                    resp = ast.literal_eval(x)
                    lista.append(resp)

                #ordeno la lista de diccionarios por el id
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
                        #if cmp(valuesP,value)==0:
                        final_time=int(value)-int(valuesP)
                        print "final_time: " + str(final_time)
                        mpTwitter.track(final_time, "Final time accuracy",{"time final": final_time, "tweet": key, "version":version})

    elif social_network == 'facebook':

        ##########################################################################################################################################
        #---------------------------------------------------------DATOS FACEBOOK API--------------------------------------------------------------
        ##########################################################################################################################################
        
        message='Prueba1'
        webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Master/facebook-wall/FacebookRefresco.html" + "?" + message)
        sleep(3)


        access_token='EAANMUmJPs2UBACBjqjpeZC7T4zpEsKprs6S34yGbywqqe0UXwHjVO09g24NAjh4mPuG33FjJoZBkLINgI7x9RzNpkdUxFOMyOEDsebMu5F2UeydTXkNR7xQZCbpdf2btzpEKOXNUxI1brijIpq2LwPiFnMtVtYl0TUp6FEPBAZDZD'

        listestado=[]
        listtpubl_ms=[]

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

        #Cuando lo tengas, defines los parametros necesarios para la peticion
        params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
        respuesta=x.request(['events/properties/values'], params, format='json')

        for x in respuesta:
            #pasar de unicode a dict
            resp = ast.literal_eval(x)
            lista.append(resp)

        #ordeno la lista de diccionarios por el id
        newlist = sorted(lista, key=lambda post: post['post'])
        print newlist

        # for y in newlist:
        #     textocomp=y.items()[0][1]
        #     timecomp=y.items()[1][1]
        #     listacomp.append(textocomp)
        #     listatime.append(timecomp)

        # zipComp=zip(listacomp,listatime)
        # #Diccionario tweet, time
        # dictComp=dict(zipComp)
        # print dictComp

    elif social_network == 'github':

        ##########################################################################################################################################
        #----------------------------------------------------------DATOS GITHUB API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Master/github-events/GithubRefresco.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Latency/github-events/GithubRefrescoLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new("http://metricas-formales.appspot.com/app/refresh_metric/Accuracy/github-events/GithubRefrescoAccuracy.html")
                sleep(3)