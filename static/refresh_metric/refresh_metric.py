#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*

import warnings
warnings.filterwarnings("ignore")
import httplib
import urllib2, urllib
from random import getrandbits
from hashlib import sha1
import json
import hmac
import base64
import time
from time import sleep
from requests_oauthlib import OAuth1
import requests
import webbrowser
import urllib3
requests.packages.urllib3.disable_warnings()
import datetime
import re
import sys
import facebook
import urlparse
import random
import string
import operator
import hashlib
import ast
import mixpanel
import mixpanel_api, json
from mixpanel import Mixpanel
from postGoogle import post as postGoogle
from requests.auth import HTTPBasicAuth
import yaml
import os

path = os.path.dirname(os.path.abspath(__file__))
output_file2 = os.path.join(path, "../config.yaml") 
configFile = open(output_file2,"r")
yaml_config = yaml.load(configFile)

#objetos Mixpanel para las distintas redes sociales (token del project)
mpTwitter = Mixpanel (yaml_config['mixpanel']['twitter'])
mpFacebook = Mixpanel (yaml_config['mixpanel']['facebook'])
mpGoogle = Mixpanel (yaml_config['mixpanel']['google'])
mpPinterest = Mixpanel (yaml_config['mixpanel']['pinterest'])
mpTraffic = Mixpanel (yaml_config['mixpanel']['traffic'])
mpWeather = Mixpanel (yaml_config['mixpanel']['weather'])
mpStock = Mixpanel (yaml_config['mixpanel']['finance'])
mpReddit = Mixpanel (yaml_config['mixpanel']['reddit'])
mpSpotify = Mixpanel (yaml_config['mixpanel']['spotify'])

network_list = ["twitter", "facebook","googleplus", "pinterest", "traffic-incidents", "open-weather", "finance-search", "reddit", "spotify"]
version_list = ["master","latency", "accuracy"]
url_base_local= "http://localhost:8000"

#de los comandos que ejecuto desde consola, me quedo con el segundo (posicion 1,array empieza en 0),consola: python refresco.py twitter coge la "variable" twitter
if len(sys.argv) >= 2:
    social_network = sys.argv[1]
else:
    social_network = ''

if len(sys.argv) >= 3:
    version= sys.argv[2]
else:
    version = ''

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

if social_network in network_list:


############################################
            #CASO1: TWITTER
############################################

    if social_network == 'twitter':

        #--DATOS TWITTER API--#
        CONSUMER_KEY = yaml_config['twitter']['consumer_key']  
        CONSUMER_SECRET =  yaml_config['twitter']['consumer_key']
        ACCESS_KEY =  yaml_config['twitter']['access-token']
        ACCESS_SECRET =  yaml_config['twitter']['secret-token']

        listestado=[]; listtpubl_ms=[]

        estado=randomword(10)
        #PUBLICACION DE TWEET Y REQUEST DEL TIMELINE
        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/twitter-timeline-stable/static/TwitterRefresco.html" + "?" + estado)
                sleep(10)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/twitter-timeline-latency/static/TwitterRefrescoLatency.html"  + "?" + estado)
                sleep(10)
   
        #Request publicar tweet
        def publicar(estado):
            if estado == '':
                return 1
            #CODIGO DE ERROR SI EL TWEET YA ESTABA PUBLICADO (ERROR CODE STATUS 187). CUANDO RESPONSE ==403
            r = requests.post(url=url,data={"status":estado},auth=oauth)
            if r.status_code == 403:
                print "Tweet duplicado"
                return 1
            print "Respuesta: " + str(r)
            tpubl_ms=int(time.time()*1000)
            print "tiempo post en ms: " + str(tpubl_ms)
            listestado.append(estado)
            listtpubl_ms.append(tpubl_ms)

            #Request timeline user   
            s= requests.get(request_usertimeline, auth=oauth)
            timeline=s.json()
            #Encontrar el texto del tweet que acabo de publicar, con el campo text que tiene cada tweet, y timestamp cuando me lo muestre en twitter
            for tweet in timeline:
                text=tweet['text']
                if text==estado:
                    break
        publicar(estado)
        #zip con todos los post y sus correspondientes tiempos de publicacion
        zipPython=zip(listestado,listtpubl_ms)
        dictPython=dict(zipPython)

        #--DATOS TWITTER COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        #pongo 70 segundos porque tengo que esperar a que se produzca el refresco automatico del componente y mande los datos a mixpanel
        sleep(100)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        
        x=mixpanel_api.Mixpanel("c10939e3faf2e34b4abb4f0f1594deaa","4a3b46218b0d3865511bc546384b8928")
        lista=[]; listacomp=[]; listatime=[]

        #se le pasa el API secret

        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth('', '')).json()

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
                listacomp.append(textocomp)
                listatime.append(timecomp)

            zipComp=zip(listacomp,listatime)
            #Diccionario tweet, time
            dictComp=dict(zipComp)

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
                    mpTwitter.track(final_time, "Final time " + version,{"time final": final_time, "post": key, "version":version})

############################################
            #CASO2: FACEBOOK
############################################
    elif social_network == 'facebook':

        #--DATOS FACEBOOK API--#
        message=randomword(10)

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/facebook-wall/FacebookRefresco.html" + "?" + message)
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/facebook-wall/FacebookRefrescoLatency.html" + "?" + message)
                sleep(5)

        #Url para obtener nuevo token de facebook: https://developers.facebook.com/tools/explorer/928341650551653/
        
        #cambiarlo cada hora y media: https://developers.facebook.com/tools/explorer/928341650551653 (Get User Access Token, version 2.3)
        access_token= yaml_config['facebook']['access_token']
        listestado=[]; listtpubl_ms=[]

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
        dictPython=dict(zipPython)
        print dictPython

        #--DATOS FACEBOOK COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(70)
        lista=[]; listacomp=[]; listatime=[]

        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth('', '')).json()

            for x in respuesta:
                resp = ast.literal_eval(x)
                lista.append(resp)

            newlist = sorted(lista, key=lambda post: post['post'])
            for y in newlist:
                textocomp=y.items()[0][1]
                timecomp=y.items()[1][1]
                listacomp.append(textocomp)
                listatime.append(timecomp)

            zipComp=zip(listacomp,listatime)
            dictComp=dict(zipComp)

            for key,value in dictComp.iteritems():
                if(dictPython.has_key(key)):
                    valuesP=dictPython.get(key,None)
                    final_time=float(value)-float(valuesP)
                    print "final_time: " + str(final_time)
                    mpFacebook.track(final_time, "Final time " + version,{"time final": final_time, "post": key, "version":version})
        

############################################
            #CASO3: GOOGLE+
############################################
    elif social_network == 'googleplus':

        #--DATOS GOOGLE+ API--#

        # Url para obtener nuevo token google: https://developers.google.com/+/web/api/rest/latest/activities/list#try-it
        # (Para el caso de Google, haces una peticion a la API con el explorer API, vas a networks, y coges el token que
        # viene en el header Authorization: 'Bearer TOKEN')
        randomtext = randomword(20)
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/googleplus-timeline-stable/demo/GoogleplusRefresco.html?" + randomtext)
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/googleplus-timeline-latency/demo/GoogleplusRefrescoLatency.html?" + randomtext)
                sleep(5)

       #--DATOS GOOGLE+ COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        postTime = postGoogle.publish(randomtext)
        latency=0
        if (version=="latency"):
            latency=10
        #request mixpanel response
        sleep(70+latency)
        params={'event':version,'name':'value'}
        respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth('', '')).json()
        
        # remove unicode
        respuesta = [ ast.literal_eval(data) for data in respuesta ]
        correct_post = [post for post in respuesta if post['post'] == randomtext][0]

        final_time = correct_post['time']/1000 - postTime
        mpGoogle.track(final_time, "Final time "+ version,{"time final": final_time, "post": correct_post['post'], "version":version})
        print "Tiempo final: ", final_time
        print "Version: ", version
        print "Post: ", correct_post['post']     
        

############################################
            #CASO4: PINTEREST
############################################

    elif social_network == 'pinterest':

        #--DATOS PINTEREST API--#
        image_url="http://www.mundoperro.net/wp-content/uploads/Perro-Carlino-485x300.jpg"

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/pinterest-timeline/demo/PinterestRefresco.html" + "?" + image_url)
                sleep(10)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/pinterest-timeline/demo/PinterestRefrescoLatency.html" + "?" + image_url)
                sleep(10)
  
        access_token= yaml_config['pinterest']['token']
        post_my_board= "https://api.pinterest.com/v1/me/pins/?access_token=" + access_token
        note="Take a look"
        link="https://www.google.es/search?q=perros&espv=2&biw=1855&bih=966&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjchq_cz8vRAhXCzxQKHQ4DCWMQ_AUIBigB#imgrc=BqLqaxHeCHP0ZM%3A"
        board="829295787572730316"

        listimags=[]; listtpubl_ms=[]

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
        dictPython=dict(zipPython)

        #--DATOS PINTEREST COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(100)
        lista=[]; listacomp=[]; listatime=[]

        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth('', '')).json()

            for x in respuesta:
                resp = ast.literal_eval(x)
                lista.append(resp)

            newlist = sorted(lista, key=lambda post: post['post'])
            for y in newlist:
                urlcomp=y.items()[0][1]
                timecomp=y.items()[1][1]
                listacomp.append(urlcomp)
                listatime.append(timecomp)

            zipComp=zip(listacomp,listatime)
            dictComp=dict(zipComp)

            for key,value in dictComp.iteritems():
                if(dictPython.has_key(key)):
                    valuesP=dictPython.get(key,None)
                    final_time=float(value)-float(valuesP)
                    print "final_time: " + str(final_time)
                    mpPinterest.track(final_time, "Final time " + version,{"time final": final_time, "post": key, "version":version})

############################################
         #CASO5: TRAFFIC-INCIDENTS
############################################

    elif social_network == 'traffic-incidents':

        #--DATOS TRAFFIC API--#
        description=randomword(10)

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/traffic-incidents/demo/TrafficRefresco.html" + "?" + description)
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/traffic-incidents/demo/TrafficRefrescoLatency.html" + "?" + description)
                sleep(3)

        listpost=[]; listtpubl_ms=[]
        
        datos = {"description": description}
        url = "https://centauro.ls.fi.upm.es:4444/traffic"
        response = requests.post(url, data=datos, verify=False)
        tpubl_ms=int(time.time())
        listpost.append(description)
        listtpubl_ms.append(tpubl_ms)

        zipPython=zip(listpost,listtpubl_ms)
        dictPython=dict(zipPython)

        #--DATOS TRAFFIC COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(70)
        #limpio la cache antes de coger datos del componente
        url = "https://centauro.ls.fi.upm.es:4444/fakes/traffic/clean"
        response = requests.get(url, verify=False)

        lista=[]; listacomp=[]; listatime=[]

        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth('', '')).json()

            for x in respuesta:
                resp = ast.literal_eval(x)
                lista.append(resp)

            newlist = sorted(lista, key=lambda post: post['post'])
            for y in newlist:
                postcomp=y.items()[0][1]
                timecomp=y.items()[1][1]
                listacomp.append(postcomp)
                listatime.append(timecomp)

            zipComp=zip(listacomp,listatime)
            dictComp=dict(zipComp)

            for key,value in dictComp.iteritems():
                if(dictPython.has_key(key)):
                    valuesP=dictPython.get(key,None)
                    final_time=float(value)-float(valuesP)
                    print "final_time: " + str(final_time)
                    mpTraffic.track(final_time, "Final time " + version,{"time final": final_time, "post": key, "version":version})

        
############################################
           #CASO6: OPEN-WEATHER
############################################

    elif social_network == 'open-weather':

        #--DATOS WEATHER API--#

        #cojo el tiempo para saber que hora es y conocer a partir de que hora tengo que publicar
        #tengo un array con 8 tiempos a publicar porque corresponde a las horas 0 3 6 9 12 15 18 21
        tiempo=time.strftime("%H")
        #resto uno al tiempo porque cuando le pregunto al componente las horas me las da como GTM+1 y python lo tiene en GTM+0
        #entonces el componente tiene las horas 1 4 7 10 13 19 22 en GTM+1 
        tiempo=int(tiempo)-1

        #cuando divido entres 3 conozco el intervalo en el que estoy y a partir de que elemento tengo que coger en el array par apublicar
        #si por ejemplo tiempo=12. Divido 12/3=4 y se que tengo que publicar desde la posicion 4 de mi array datos
        
        intervalo=tiempo/int(3)
        #pongo datos random para que cada post sea unico
        datos = [{"temp": random.randint(0,100), "min": 1, "max": 40, "icon": "wi-day-sunny"}, {"temp": random.randint(0,100), "min": 1, "max": 40, "icon": "wi-day-sunny"},{"temp": random.randint(0,100), "min": 1, "max": 40, "icon": "wi-day-sunny"},{"temp": random.randint(0,100), "min": 1, "max": 40, "icon": "wi-day-sunny"},{"temp": random.randint(0,100), "min": 1, "max": 40, "icon": "wi-day-sunny"},{"temp": random.randint(0,100), "min": 1, "max": 40, "icon": "wi-day-sunny"},{"temp": random.randint(0,100), "min": 1, "max": 40, "icon": "wi-day-sunny"},{"temp": random.randint(0,100), "min": 1, "max": 40, "icon": "wi-day-sunny"}]
        
        datos1=datos[intervalo+1:]
        datos1=str(datos1)
        datos2 = urllib.quote(datos1)

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/open-weather-stable/demo/WeatherRefresco.html" + "?" + datos2)
                sleep(10)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/open-weather-latency/demo/WeatherRefrescoLatency.html" + "?" + datos2)
                sleep(10)

        listpost=[]; listtpubl_ms=[]
        
        #en la llamada tengo que mandar todos los datos, los este publicando en ese momento o no
        #codificar datos porque la peticion hay que hacerla en ese formato
        datos = str(datos)
        datos = "data= " + urllib.quote(datos)

        headers= {
            "content-type":"application/x-www-form-urlencoded"
        }
        url = "https://centauro.ls.fi.upm.es:4444/weather"
        response = requests.post(url, data=datos, verify=False, headers=headers)        

        tpubl_ms=int(time.time())
        
        #hasheo los datos para evitar problema de limitacion de mixpanel
        hash_object = hashlib.sha1(datos1)
        text = hash_object.hexdigest()
        listpost.append(text)
        listtpubl_ms.append(tpubl_ms)

        zipPython=zip(listpost,listtpubl_ms)
        #diccionario con los mensajes publicados y su tiempo de publicacion
        dictPython=dict(zipPython)

       #--DATOS WEATHER COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(100)
        url = "https://centauro.ls.fi.upm.es:4444/fakes/weather/clean"
        response = requests.get(url, verify=False)

        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales (API KEY y API SECRET)
        lista=[]; listacomp=[]; listatime=[]; listacomp1=[]; listacomp2=[] 

        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth('', '')).json()

            for x in respuesta:
                resp = ast.literal_eval(x)
                lista.append(resp)

            newlist = sorted(lista, key=lambda post: post['post'])
            for y in newlist:
                postcomp=y.items()[0][1]
                timecomp=y.items()[1][1]
                listacomp.append(postcomp)
                listatime.append(timecomp)

            zipComp=zip(listacomp,listatime)
            dictComp=dict(zipComp)

            for key,value in dictComp.iteritems():
                if(dictPython.has_key(key)):
                    valuesP=dictPython.get(key,None)
                    final_time=float(value)-float(valuesP)
                    print "final_time: " + str(final_time)
                    mpWeather.track(final_time, "Final time " + version,{"time final": final_time, "post": key, "version":version})


############################################
            #CASO7: FINANCE
############################################

    elif social_network == 'finance-search':

        #--DATOS FINANCE API--#
        data = {"Symbol": "GOOGL", "Change": 10, "DaysLow": 10, "DaysHigh": 10, "YearLow": 10, "YearHigh": 10, "Volume": 10, "LastTradePriceOnly": 10, "Name":"Alphabet Inc."}
        data_text = urllib.urlencode(data)
        random_id = random.randint(0,1000000)
        data_text = data_text + "&id=%d" % random_id
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/finance-search-stable/demo/FinanceSearchRefresco.html?" + data_text)
                sleep(8)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/finance-search-latency/demo/FinanceSearchRefrescoLatency.html?" + data_text)
                sleep(8)
     
        datos = "data= " + urllib.quote(str(data))
        headers= {
            "content-type":"application/x-www-form-urlencoded"
        }
        url = "https://centauro.ls.fi.upm.es:4444/stock"
        response = requests.post(url, data=data, verify=False, headers=headers)
        print response, response.json()      
        postTime=time.time()
        
        latency=0
        if (version=="latency"):
            latency=10
        
        #--DATOS FINANCE COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        ## request mixpanel response
        sleep(70+latency)
         params={'event':version,'name':'value'}
        respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth('', '')).json()

        # remove unicode
        respuesta = [ ast.literal_eval(data) for data in respuesta ]
        correct_post = [ post for post in respuesta if post['id'] == str(random_id) ]
        
        if len(correct_post) == 1:
          correct_post = correct_post[0]
        else:
          print "No se encontro el evento relacionado con el id: %f" % random_id
          # Clean data
          headers= {
            "content-type":"application/x-www-form-urlencoded"
          }
          url = "https://centauro.ls.fi.upm.es:4444/fakes/stock/clean"
          response = requests.get(url, verify=False, headers=headers)

        final_time = correct_post['time']/1000 - postTime
        mpStock.track(final_time, "Final time "+ version,{"time final": final_time, "id": correct_post['id'], "version":version})
        print "Tiempo final: ", final_time
        print "Version:", version
        print "Post id: ", correct_post['id']

        # Clean data
        headers= {
          "content-type":"application/x-www-form-urlencoded"
        }
        url = "https://centauro.ls.fi.upm.es:4444/fakes/stock/clean"
        response = requests.get(url, verify=False, headers=headers)
    
    elif social_network == "reddit":
        publish_text = str(time.time())
        data = {"title":"Test post", "author":"test", "selftext":publish_text,"subreddit":"test" }

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/reddit-timeline/demo/RedditTimelineRefresh.html?" + publish_text)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/reddit-timeline/demo/RedditTimelineRefresh.html?" + publish_text)
        
        sleep(10)
        print "Publicando datos"
        headers= {
          "content-type":"application/x-www-form-urlencoded"
        }
        url = "https://centauro.ls.fi.upm.es:4444/reddit"
        response = requests.post(url, data=data, verify=False, headers=headers)
        print "Respuesta de publicar: %d" % response.status_code
        print "======================="
        print "Esperando a encontrar modificaciones"
        sleep(80)
        print "Recolectando datos"
        panel = mixpanel_api.Mixpanel("a9e682c78c1c951e7ebf76794223e850","ffe6ada8738ed520e54aaf7e8b7c0cec")
        params={'event':version,'name':'value','type':"general",'unit':"day",'interval':1}
        respuesta=panel.request(['events/properties/values'], params, format='json')

        respuesta = [json.loads(resp) for resp in respuesta]
        
        data = filter(lambda el: el['published_text'] == publish_text, respuesta)
        requests.get("https://centauro.ls.fi.upm.es:4444/fakes/reddit/clean", verify=False)
        if len(data) == 0:
            print "No se registraron datos en mixpanel. Espere mas tiempo o compruebe que se esta mandando correctamente"
            sys.exit(2)
        final_time = float(data[0]['time']) / 1000
        print "(%s) Latencia de %s: %f" % (version,social_network, final_time)

        mpReddit.track(final_time, "Final time "+ version,{"time final": final_time, "version":version})

############################################
            #CASO8: SPOTIFY
############################################

    elif social_network == 'spotify':
    
        #--DATOS SPOTIFY API--#
        datos = {'name' : randomword(8)}
        playListSend = datos['name']
        newTracks = {'uris': ["spotify:track:6rqhFgbbKwnb9MLmUQDhG6","spotify:track:1qfYG2JrchEyJiqKnkE7YQ"]}
        track = newTracks['uris']
        dataSend = playListSend
        for i in track:
            dataSend += i
    
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/spotify-component/spotifyRefrescoMaster.html" + "?" + dataSend)
                sleep(5)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/spotify-component/spotifyRefrescoLatency.html" + "?" + dataSend)
                sleep(5)
    
        listtpubl_ms=[]; listpost=[]; listestado=[]
        #este token hay que cogerlo de la API, no puedo coger el token del componente porque el componente no permite crear playList, solo mostrarlas
        #https://developer.spotify.com/web-api/console/post-playlists/
        access_token= yaml_config['spotify']['token']

        url_newPlayList = "https://api.spotify.com/v1/users/deusconwet/playlists"
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
            }

        response= requests.post(url_newPlayList, json.dumps(datos) ,headers=headers)
        idNewPlayList = response.json()['id']
        url_postTracks= "https://api.spotify.com/v1/users/deusconwet/playlists/" + idNewPlayList + "/tracks"
        res= requests.post(url_postTracks, json.dumps(newTracks) ,headers=headers)

        tpubl_ms=int(time.time())
       
        #--DATOS SPOTIFY COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep (70)
        lista=[]; listacomp=[]; listatime=[]
        if version in version_list:
            params={'event':version,'name':'value'}
            #a la peticion se le mete el api secret
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth('e1437fb0cc27d32cad87bd94bcb95bc7', '')).json()

            for x in respuesta:
                #pasar de unicode a dict
                resp = ast.literal_eval(x)
                lista.append(resp)

            for i in lista:
                if(i['post']==dataSend):
                    final_time=float(i['time'])-float(tpubl_ms)
                    print "final_time: " + str(final_time)
                    mpSpotify.track(final_time, "Final time " + version,{"time final": final_time, "post": dataSend, "version":version})

