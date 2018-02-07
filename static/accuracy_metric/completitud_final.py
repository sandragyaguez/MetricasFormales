#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*

import sys
import pprint
pp = pprint.PrettyPrinter(indent=2)
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
import datetime
import base64
#objetos Mixpanel para las distintas redes sociales (token del project)
mpTwitter = Mixpanel("b5b07b32170e37ea45248bb1a5a042a1")
mpFacebook = Mixpanel("04ae91408ffe85bf83628993704feb15")
mpGoogle = Mixpanel("f2655b08b62cc657d6865f8af003bdd9")
mpPinterest = Mixpanel("6ceb3a37029277deb7f530ac7d65d7d4")
mpTraffic = Mixpanel("85519859ef8995bfe213dfe822e72ab3")
mpWeather = Mixpanel("19ecdb19541d1e7b61dce3d4d5fa485b")
mpStock = Mixpanel("f2703d11ce4b2e6fed5d95f400306e48")

#---------------------------------------------------------------------------------------------------------------------
network_list = ["twitter", "facebook", "googleplus", "pinterest", "traffic-incidents", "open-weather", "finance-search", "reddit", "spotify"]
version_list = ["master","latency", "accuracy"]
# url_base_remote= "http://metricas-formales.appspot.com/app/accuracy_metric"
url_base_local= "http://localhost:8000"

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
        CONSUMER_KEY = 'BOySBn8XHlyYDQiGiqZ1tzllx' #Consumer key
        CONSUMER_SECRET = 'xeSw5utUJmNOt5vdZZy8cllLegg91vqlzRitJEMt5zT7DtRcHE' #Consumer secret
        ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
        ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret


        #Lanzamos una pestana por cada version del componente
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new( url_base_local + "/Master/twitter-timeline-stable/static/TwitterCompletitud.html")
                sleep(3)
            # elif(version=="latency"):
            #     webbrowser.open_new( url_base_remote + "/Latency/twitter-timeline/static/TwitterCompletitudLatency.html")
            #     sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new( url_base_local + "/Accuracy/twitter-timeline-accuracy/static/TwitterCompletitudAccuracy.html")
                sleep(3)

        #objeto oauth con credenciales de usuario Deus
        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        #url para hacer peticion al timeline de twitter
        request_hometimeline="https://api.twitter.com/1.1/statuses/home_timeline.json?count=200"
        #Request timeline home
        s= requests.get(request_hometimeline, auth=oauth)
        timeline=s.json()

        ##########################################################################################################################################
        #-----------------------------------------DATOS TWITTER COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        sleep(30)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("70d459a2d5e96864f6eacdcb1a1fcd50","4dd2fff92abd81af8f06950f419f066a")
        lista = []; listaid = []; liskey = []; lisvalue = []; listaFallosText = []; listaFallosUser = []
        contadorFallos = 0


        #defino los parametros necesarios para la peticion
        params={'event':version,'name':'value','type':"general",'unit':"day",'interval':1}
        respuesta=x.request(['events/properties/values'], params, format='json')           

        for x in respuesta:
            #pasar de unicode a dict
            resp = ast.literal_eval(x)
            lista.append(resp)

        #ordeno la lista de diccionarios por el id
        newlist = sorted(lista, key=lambda id_tweet: id_tweet['id'])
        newlist.reverse()

        #Recorro el diccionario del componente
        contador = len(newlist)
        for index, element in enumerate(newlist):
            #Comparamos los valores
            if str(element['text']) != str(timeline[index]['text']):
              print "Falla el texto con valor %s" % element['text']
              liskey.append('text')
              lisvalue.append(element['text'])
              contadorFallos=contadorFallos+1
              listaFallosText=zip(liskey,lisvalue)
            if str(element['user']) != str(timeline[index]['user']['name']):
              print "Falla el usuario con valor %s" % element['user']
              liskey.append('user')
              lisvalue.append(element['user'])
              contadorFallos=contadorFallos+1
              listaFallosUser=zip(liskey,lisvalue)

        contadorFallos=contadorFallos/(contador * 2.0)
        print contadorFallos
        mpTwitter.track(contadorFallos, "Fallos totales " + version, {"numero fallos": contadorFallos})                           

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
                webbrowser.open_new(url_base_local + "/Master/facebook-wall-stable/FacebookCompletitud.html")
                sleep(5)
            # elif(version=="latency"):
            #     webbrowser.open_new(url_base_remote + "/Latency/facebook-wall/FacebookCompletitudLatency.html")
            #     sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/facebook-wall-accuracy/FacebookCompletitudAccuracy.html")
                sleep(5)
        # Url para obtener nuevo token de facebook: https://developers.facebook.com/tools/explorer/928341650551653/
        #es necesario cambiar el token cada hora y media: https://developers.facebook.com/tools/explorer/928341650551653 (Get User Access Token, version 2.3)
        access_token="EAANMUmJPs2UBAHQGTF7m8XnJWBw7wjuVVZCh7isrZARoXU5sZCkOrv2wqytW66urZALhjujJX8GZBIBbQJbLBaNqMAod89avZBqG71LgI0CBU1yUjrg4UaTHzuVRZA2M5EDhUA2ZBIf4FUdz8BXiTm9sUIvHzWZBl5CwTlJUeabqfQIorqkOsDOws5r7xpUPhLo8ZD"
        facebook_url = "https://graph.facebook.com/v2.3/me?fields=home&pretty=1&access_token=" + access_token

        #Request timeline home
        s= requests.get(facebook_url)
        muro=s.json()
        

        #facebook devuelve un diccionario con 2 keys (home, id) y solo me quiero quedar con los values del home
        if not muro.has_key('home') or not muro['home'].has_key('data'):
          print "La api de facebook devuelve error. Comprobar token."
          sys.exit(-1)
        muro = muro['home']['data']
        for element in muro:
          text = ""
          picture = ""

          if(element.has_key('description')):
              text1 = element['description']
              hash_object = hashlib.sha1(text1)
              text = hash_object.hexdigest()
          elif (element.has_key('message')):
              text1=element['message']
              hash_object = hashlib.sha1(text1)
              text = hash_object.hexdigest()
          
          if(element.has_key('picture')):
              text1 = element['picture']
              hash_object = hashlib.sha1(text1)
              picture = hash_object.hexdigest()

          element['_text'] = text
          element['_picture'] = picture
          
        ##########################################################################################################################################
        #-------------------------------------------DATOS FACEBOOK COMPONENTE (RECOGIDOS DE MIXPANEL)---------------------------------------------
        ##########################################################################################################################################

        sleep(20)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("de21df1c2c63dff29ffce8a1a449494a","a7917928a9ba3dd88592fac7ac36e8a9")
        contadorFallos=0

        #defino los parametros necesarios para la peticion
        params={'event':version,'name':'value','type':"general",'unit':"day",'interval':1}
        respuesta=x.request(['events/properties/values'], params, format='json')
        respuesta = [json.loads(str(post)) for post in respuesta]
        respuesta = sorted(respuesta, key=lambda posicion: posicion['i'])
        
        for index, element in enumerate(respuesta):

          if str(element['user']) != str(muro[index]['from']['name']):
            print "falla en la posicion %d" % index
            print "El usuario %s deberia ser %s" % (element['user'], muro[index]['from']['name'])
            contadorFallos+=1
          
          if 'picture' in muro[index] and 'image' in element and str(element['image']) != str(muro[index]['_picture']):
            print "falla en la posicion %d" % index
            print "La imagen %s deberia ser %s" % (element['image'], muro[index]['_picture'])
            contadorFallos+=1
          if str(element['texto']) != str(muro[index]['_text']):
            print "falla en la posicion %d" % index
            print "El texto %s deberia ser %s" % (element['texto'], str(muro[index]['_text']))
            contadorFallos+=1            

        contadorFallos=contadorFallos/(len(respuesta)*3.0)
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
                webbrowser.open_new(url_base_local + "/Master/googleplus-timeline-stable/demo/GooglePlusCompletitud.html")
                sleep(3)
            # elif(version=="latency"):
            #     webbrowser.open_new(url_base_remote + "/Latency/googleplus-timeline/demo/GooglePlusCompletitudLatency.html")
            #     sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/googleplus-timeline-accuracy/demo/GooglePlusCompletitudAccuracy.html")
                sleep(3)

        sleep(5)
        # Url para obtener nuevo token google: https://developers.google.com/+/web/api/rest/latest/activities/list#try-it
        # (Para el caso de Google, haces una peticion a la API con el explorer API, vas a networks, y coges el token que
        # viene en el header Authorization: 'Bearer TOKEN')
        #cambiar token cada hora y media: https://developers.google.com/+/web/api/rest/latest/activities/list?authuser=1
        access_token="ya29.Gl1oBMPNI8iI22G0j2AEj8JdssVrW90t7fg7xABbT8rydEPsxTn-XHfZGsIxhu0P_AUA8Oj-dYJcrVUN7Mujm-Te-M13X29a2_cYhuk0ZoCdFAXDGQXS3gVTLA0jycI"
        key = "AIzaSyAArT6pflqm1-rj9Nwppuj_4z15FFh4Kis"
        google_url_followers="https://people.googleapis.com/v1/people/me/connections?key=%s&access_token=%s" % (key,access_token)
        headers = {"Authorization": "Bearer " + access_token}
        
        #Request a followers de Deus
        s= requests.get(google_url_followers,headers=headers)
        muro=s.json()
        followers=[str(follower['metadata']['sources'][1]['id']) for follower in muro['connections']]

        posts=[]
        #Request a timeline Deus para todos los usuarios. Para obtener la informacion de los post, previamente he tenido que obtener los followers
        for i in followers:
            #hay que poner str(i) porque sino no se puede concatenar string con un long (int)
            google_url="https://www.googleapis.com/plus/v1/people/" + str(i) + "/activities/public"
            pet= requests.get(google_url,headers=headers)

            timeline=pet.json()
            if(timeline.has_key('items')):
                posts += timeline['items']
        
        for post in posts:
            hash_object = hashlib.sha1(post['object']['content'])
            post['hashed_text'] = hash_object.hexdigest()
            post['date_published'] = int(calendar.timegm(datetime.datetime.strptime(post['published'], "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()))
        
        posts = sorted(posts,key=lambda post: post['date_published'], reverse=True)

        ##########################################################################################################################################
        #-------------------------------------------DATOS GOOGLE+ COMPONENTE (RECOGIDOS DE MIXPANEL)---------------------------------------------
        ##########################################################################################################################################

        sleep(10)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("b9eb42288e7e416028ddf3ee70ae4ca9","0c24b55a9806c9eb41cb3d5f3a7e7ef6")
        contadorFallos=0

        if version in version_list:
            params={'event':version,'name':'value','type':"general",'unit':"day",'interval':1}
            respuesta=x.request(['events/properties/values'], params, format='json')

            lista = []
            for x in respuesta:
                #pasar de unicode a dict
                resp = ast.literal_eval(x)
                lista.append(resp)

            #ordeno la lista de diccionarios por el id
            newlist = sorted(lista, key=lambda posicion: posicion['publish'], reverse=True)            

            for component, post_api in zip(newlist,posts):
                if component['user'] != post_api['actor']['displayName']:
                    print "falla en el usuario: %s vs %s" % (component['user'], post_api['actor']['displayName'])
                    contadorFallos += 1
                if component['text'] != post_api['hashed_text']:
                    print "falla en el usuario: %s vs %s" % (component['text'], post_api['hashed_text'])
                    contadorFallos += 1

       
            contadorFallos=contadorFallos / (len(newlist)*2.0)
            print contadorFallos
            mpGoogle.track(contadorFallos, "Fallos totales %s" % version, {"numero fallos": contadorFallos})

            
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
            # elif(version=="latency"):
            #     webbrowser.open_new(url_base_local + "/Latency/pinterest-timeline/demo/PinterestCompletitudLatency.html")
            #     sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/pinterest-timeline/demo/PinterestCompletitudAccuracy.html")
                sleep(3)

        access_token="AYzOkS8gPFoFyhU56X9RjekH8IQFFI3y549FYk9DmW-C0gBCfwAAAAA"
        request_my_board= "https://api.pinterest.com/v1/me/pins/?access_token=" + access_token  + "&limit=60"
        request_others= "https://api.pinterest.com/v1/me/following/boards/?access_token=" + access_token

        #tengo que hacer una primera peticion a los boards de a los que sigo para poder pedir sus pins (imagenes)
        s= requests.get(request_others)
        timeline=s.json()

        lista_img=[]; username=[]; board=[]; pets=[]; imagAPI=[]
    
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
            contador=0
            for pet in pets:
                request=makeRequest(pet)
                data= request.get('data',None)
                for urls in data:
                    url=urls.get('url', None)
                    imagAPI.append(url)
                    
        getData(pets)
       
        ##########################################################################################################################################
        #------------------------------------------DATOS PINTEREST COMPONENTE (RECOGIDOS DE MIXPANEL)---------------------------------------------
        ##########################################################################################################################################

        sleep(30)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("55736dc621aade0a3e80ea2f7f28f42b","5d34c88bc7f29c166e56484966b1c85b")

        imagComp=[]
        contadorFallos=0

       #metodo que me compara la lista de imagenes obtenidas por la API con la lista de imagenes cogidas en el componente
        def comp(list1, list2):
            # variable global para que no me de el fallo "referenciado antes de asignado"
            global contadorFallos
            fallos=[]
            # if len(list1) != len(list2):
            #     print "no tienen la misma longitud"
            #     return False
            for val in list2:
                if not (val in list1):
                    fallos.append(val)
                    contadorFallos=contadorFallos+1        
            return fallos

        if version in version_list:
            if version=="master":
            #defino los parametros necesarios para la peticion
                params={'event':"master",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')
                imagComp = [str(json.loads(res)['url']) for res in respuesta]        

                fallos=comp(imagAPI,imagComp)

                mpPinterest.track(fallos,"Fallos master imagenes",{"imagen":fallos, "version":"master"})
                contadorFallos=contadorFallos/float(len(imagAPI))
                print contadorFallos
                mpPinterest.track(contadorFallos, "Fallos totales master", {"numero fallos": contadorFallos})
 

            elif version=="latency":
                #defino los parametros necesarios para la peticion
                params={'event':"latency",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')

                imagComp = [str(json.loads(res)['url']) for res in respuesta]        
                #print len(imagComp)
         
                fallos=comp(imagAPI,imagComp)

                mpPinterest.track(fallos,"Fallos latency imagenes",{"imagen":fallos, "version":"latency"})
                contadorFallos=contadorFallos/float(len(imagAPI))
                print contadorFallos
                mpPinterest.track(contadorFallos, "Fallos totales latency", {"numero fallos": contadorFallos})
 

            elif version=="accuracy":
                #defino los parametros necesarios para la peticion
                params={'event':"accuracy",'name':'value','type':"general",'unit':"day",'interval':1}
                respuesta=x.request(['events/properties/values'], params, format='json')
                imagComp = [str(json.loads(res)['url']) for res in respuesta]         
                fallos=comp(imagAPI,imagComp)

                mpPinterest.track(fallos,"Fallos accuracy imagenes",{"imagen":fallos, "version":"accuracy"})
                contadorFallos=contadorFallos/float(len(imagComp))
                print contadorFallos
                mpPinterest.track(contadorFallos, "Fallos totales accuracy", {"numero fallos": contadorFallos})


############################################
############################################
        #CASO5: TRAFFIC-INCIDENTS
############################################
############################################

    elif social_network == 'traffic-incidents':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS TRAFFIC API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/traffic-incidents/demo/TrafficCompletitud.html")
                sleep(3)
            # elif(version=="latency"):
            #     webbrowser.open_new(url_base_local + "/Latency/traffic-incidents/demo/TrafficCompletitudLatency.html")
            #     sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/traffic-incidents/demo/TrafficCompletitudAccuracy.html")
                sleep(3)
               
        request_uri= "https://centauro.ls.fi.upm.es:4444/traffic?map=39.56276609909911,-4.650120900900901,41.36456790090091,-2.848319099099099&key=AmWMG90vJ0J9Sh2XhCp-M3AFOXJWAKqlersRRNvTIS4GyFmd3MxxigC4-l0bdvz-"
        
        headers= {"content-type":"application/x-www-form-urlencoded"}
        #verify=False para que no me de errores de SSL
        s= requests.get(request_uri, verify=False, headers=headers)
        timeline=s.json()
        lista_descrip=[]; lista_date=[]; lista_type=[]; listacont=[]
        contador=0

        #los tres for que hago a continuacion es para conseguir llegar al dato 'description'. La api devuelve los datos en diccionarios dentro de listas dentro de diccionarios
        for k,v in timeline.iteritems():
            if(timeline.has_key('resourceSets')):
                values1=timeline.get('resourceSets',None)

        for m in values1:
            if(m.has_key('resources')):
                values2=m.get('resources',None)
                
        for n in values2:
            #descipcion de la incidencia
            if(n.has_key('description')):
                values3=n.get('description')
                hash_object = hashlib.sha1(values3)
                values3 = hash_object.hexdigest()
            lista_descrip.append(values3)
            #fecha de la publicacion de la incidencia
            if(n.has_key('lastModified')):
                values4=n.get('lastModified')
            lista_date.append(values4)
            #el type es el grado de gravedad de la incidencia. El usuario lo ve porque dependiendo del numero el icono cambia
            if(n.has_key('type')):
                values5=n.get('type')
            lista_type.append(values5)

            #la lista de contador la hago para poder identificar cada descripcion con su type de imagen y su date
            listacont.append(contador)
            contador=contador+1

        zipPythonDesc=zip(listacont,lista_descrip)
        #diccionario contador y usuarios
        dictPythonText=dict(zipPythonDesc)
        zipPythonDate=zip(listacont,lista_date)
        #diccionario contador y textos
        dictPythonDate=dict(zipPythonDate)
        zipPythonType=zip(listacont,lista_type)
        #diccionario contador e imagenes
        dictPythonType=dict(zipPythonType)

        ##########################################################################################################################################
        #----------------------------------------DATOS TRAFFIC COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        sleep(30)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("f9048e936929679df4e14859ebd1dd98","0795378c7f94b5b1f4170deb0221ec59")
        contadorFallos=0
        lista=[]; images=[]; listapos=[]; listadate=[]; listatext=[]; listatype=[]; liskey=[]; lisvalue=[]
        params={'event':version,'name':'value','type':"general",'unit':"day",'interval':1}
        respuesta=x.request(['events/properties/values'], params, format='json')

        for x in respuesta:
            #pasar de unicode a dict
            resp = ast.literal_eval(x)
            lista.append(resp)

        #ordeno la lista de diccionarios por la posicion (va de 0 a x)
        newlist = sorted(lista, key=lambda posicion: posicion['i'])

        for index, entry in enumerate(newlist):
          if len(dictPythonText) < index or  dictPythonText[index] != entry['descripcion']:
            print "falla en posicion: ", entry['i'] 
            print "el date que falla es : descripcion"
            liskey.append(k)
            lisvalue.append(v)
            listaFallosDate=zip(liskey,lisvalue)
            contadorFallos=contadorFallos+1
          
          if len(dictPythonText) < index or dictPythonType[index] != entry['tipo']:
            print "falla en posicion: ", entry['i'] 
            print "el date que falla es : type" 
            liskey.append(k)
            lisvalue.append(v)
            listaFallosDate=zip(liskey,lisvalue)
            contadorFallos=contadorFallos+1

        contadorFallos=contadorFallos/(contador*2.0)
        print contadorFallos
        
        mpTraffic.track(contadorFallos, "Fallos totales" + version, {"numero fallos": contadorFallos})
    elif social_network == 'finance-search':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS STOCK API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/finance-search-stable/demo/FinanceSearchMaster.html")
                sleep(3)
            # elif(version=="latency"):
            #     webbrowser.open_new(url_base_local + "/Latency/finance-search/demo/FinanceSearchLatency.html")
            #     sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/finance-search-accuracy/demo/FinanceSearchAccuracy.html")
                sleep(3)
               
        symbol = "GOOGL"
        query = 'select * from yahoo.finance.quote where symbol in ("%s")' % symbol

        request_uri= "https://centauro.ls.fi.upm.es:4444/stock?q=%s" % query
        headers= {"content-type":"application/x-www-form-urlencoded"}
        #verify=False para que no me de errores de SSL
        response= requests.get(request_uri, verify=False, headers=headers)
        
        data = response.json()
        data = data['query']['results']['quote'][0]

        ##########################################################################################################################################
        #----------------------------------------DATOS STOCK COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        latency=0
        if version == 'latency':
          latency=10
        sleep(10+latency)
        panel = mixpanel_api.Mixpanel('67699e9fba765cebbbe98621271db4ba','fbb422f045419447722e54b70690c638')
        params={'event':version,'name':'value','type':"general",'unit':"day",'interval':1}
        response=panel.request(['events/properties/values'], params, format='json')
        response = [ json.loads(res) for res in response ]
        response = sorted(response, key=lambda x: -x['Date'])
        response = response[0]
        errors = 0
        analyzed = 0.0
        
        for key,value in response.iteritems():
          key = str(key)
          value = str(value)
          if key != 'Date':
            analyzed += 1
            if data[key] != value:
              print "El campo %s no es igual en ambos lados: %s vs %s" % (key, value, data[key])
              errors+=1
        contadorFallos = errors/analyzed
        print "% fallos " + version, ' :', contadorFallos
        mpStock.track(contadorFallos, "Fallos totales %s" % version, {"numero fallos": contadorFallos})


############################################
############################################
        #CASO6: OPEN-WEATHER
############################################
############################################

    elif social_network == 'open-weather':

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS WEATHER API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/open-weather-stable/demo/WeatherCompletitud.html")
            # elif(version=="latency"):
            #     webbrowser.open_new(url_base_local + "/Latency/open-weather/demo/WeatherCompletitudLatency.html")
            #     sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/open-weather-accuracy/demo/WeatherCompletitudAccuracy.html")
        
        #pasar parametros de weather   
        contador = 0
        request_uri= "https://centauro.ls.fi.upm.es:4444/weather?lat=40.4336199&lon=-3.8134707000000003&units=metric&lang=es&appId=655f716c02b3f0aceac9e3567cfb46a8"
        
        headers= {"content-type":"application/x-www-form-urlencoded"}
        #verify=False para que no me de errores de SSL
        s= requests.get(request_uri, verify=False, headers=headers)
        timeline=s.json()

        if(timeline.has_key('city')):
            city=timeline['city']
        if (timeline.has_key('list')):
            values3=timeline['list']
               
        if(city.has_key('name')):
          lista_city=city['name']

        iconMapping={
            "01d": "wi-day-sunny",
            "01n": "wi-night-clear",
            "02d": "wi-day-cloudy",
            "02n": "wi-night-cloudy",
            "03d": "wi-cloudy",
            "03n": "wi-cloudy",
            "04d": "wi-cloudy",
            "04n": "wi-cloudy",
            "09d": "wi-showers",
            "09n": "wi-showers",
            "10d": "wi-day-rain",
            "10n": "wi-night-rain",
            "11d": "wi-thunderstorm",
            "11n": "wi-thunderstorm",
            "13d": "wi-snow",
            "13n": "wi-snow",
            "50d": "wi-fog",
            "50n": "wi-fog"
        }

        def list_temp_min_max(lista_timeline):
          days = []
          days.append(filter(lambda x: datetime.datetime.fromtimestamp(x['dt']).strftime('%d/%m/%Y') == time.strftime("%d/%m/%Y"), lista_timeline))
          nextdate=datetime.datetime.now().date()
          
          for i in range(4): 
            nextdate += datetime.timedelta(days=1)
            values_next_day1=filter(lambda x: datetime.datetime.fromtimestamp(x['dt']).strftime('%d/%m/%Y') == nextdate.strftime("%d/%m/%Y"), lista_timeline)
            days.append(values_next_day1)
          
          mins = []
          maxs = []
          for day in days:
            min_day = min([weather['temp_min'] for weather in day])
            max_day = max([weather['temp_max'] for weather in day])
            mins += [min_day]*len(day)
            maxs += [max_day]*len(day)
          
          for index, weather in enumerate(lista_timeline):
            weather['temp_min'] = mins[index]
            weather['temp_max'] = maxs[index]
          
          return lista_timeline
        def recorrer_timeline(lista_timeline):
          pretty = []          
          for entry in lista_timeline:
            information = {}
            information['dt'] = entry['dt']
            information["city"] = str(lista_city)
            information["icon"] = iconMapping[entry['weather'][0]['icon']]
            information["temp"] = int(round(entry['main']['temp']))
            information["temp_max"] = int(round(entry['main']['temp_max']))
            information["temp_min"] = int(round(entry['main']['temp_min']))

            pretty.append(information)
          return pretty
       
        api_response = recorrer_timeline(timeline['list'])
        api_response = list_temp_min_max(api_response)

        ##########################################################################################################################################
        #----------------------------------------DATOS WEATHER COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        sleep(30)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales
        x=mixpanel_api.Mixpanel("aab0e30bdb1ec923fe2d85fb95e051ec","a019aa23c38827f307f0d5eff0d0d6f5")
        contadorFallos=0
        lista=[]

        if version in version_list:
          params={'event':version,'name':'value','type':"general",'unit':"day",'interval':1}
          respuesta=x.request(['events/properties/values'], params, format='json')
          
          #pasar de unicode a dict
          for x in respuesta:
            resp = ast.literal_eval(x)
            lista.append(resp)                   
          
          #ordeno la lista de diccionarios por la posicion (va de 0 a x)
          newlist = sorted(lista, key=lambda posicion: posicion['i'])

          for index, weather in enumerate(newlist):
            if api_response[index]['icon'] != weather['icon']:
              print index, " falla en posicion icon: ", api_response[index]['icon'], weather['icon']
              contadorFallos+=1
            if api_response[index]['temp'] != weather['temp']:
              print index, " falla en posicion temp: ", api_response[index]['temp'], weather['temp']
              contadorFallos+=1
            if api_response[index]['temp_min'] != weather['temp_min']:
              print index, " falla en posicion temp_min: ", api_response[index]['temp_min'], weather['temp_min']
              contadorFallos+=1
            if api_response[index]['temp_max'] != weather['temp_max']:
              print index, " falla en posicion temp_max: ", api_response[index]['temp_max'], weather['temp_max']
              contadorFallos+=1                            
          
  
          contadorFallos=contadorFallos / (len(newlist)*4.0)
          print contadorFallos
          mpWeather.track(contadorFallos, "Fallos totales " + version, {"numero fallos": contadorFallos})

############################################
############################################
        #CASO6: REDDIT-TIMELINE
############################################
############################################

    elif social_network == "reddit":
        experiment_id = int(time.time())
        print "ID. Experimento: %d" % experiment_id
        print "===================================="
        reddit_token = "bHluEetl5RSZIi7wH_NwnEu4YhI"
        if(version=="master"):
            webbrowser.open_new(url_base_local + "/Master/reddit-timeline/demo/RedditTimelineMaster.html?" + str(experiment_id))
        # elif(version=="latency"):
        #     webbrowser.open_new(url_base_local + "/Latency/open-weather/demo/WeatherCompletitudLatency.html?" + str(experiment_id))
        #     sleep(3)
        elif(version=="accuracy"):
            webbrowser.open_new(url_base_local + "/Accuracy/reddit-timeline/demo/RedditTimelineAccuracy.html?" + str(experiment_id))

        # Coger un access token valido
        request_uri = "https://oauth.reddit.com/r/all/hot"
        header = {
            "authorization": "Bearer " + reddit_token,
            'User-agent': 'Mozilla/5.0'
        }
        req = requests.get(request_uri, headers=header)

        if (req.status_code != 200):
            print "(%d) El token proporcionado no es valido o se ha superado el limite de peticiones" % req.status_code
            print req.text
            sys.exit(2)
        timeline = req.json()['data']['children']
        timeline = [element['data'] for element in timeline]
        
        sleep(15)

        mixpanel_redit = mixpanel_api.Mixpanel("b3b33d92ce26bc2171dcd4efa907794e","7bc71232ea359bf84f9abe6c6e06726b")
        params = {'event':version, 'name':'value','type':'general', 'unit':'day','interval':1}
        mixpanel_data = mixpanel_redit.request(['events/properties/values'], params, format='json')

        mixpanel_data = [json.loads(data) for data in mixpanel_data]
        mixpanel_data = filter(lambda el: el['experiment'] == str(experiment_id), mixpanel_data)
        mixpanel_data = sorted(mixpanel_data, key=lambda element: element['i'])

        if len(mixpanel_data) != len(timeline):
            print "Las longitudes de las dos listas recibidas no son iguales. Comprueba que se mandan todos los datos bien"
            print "mixpanel: %d  vs  componente: %d" % (len(mixpanel_data), len(timeline))
            sys.exit(3)
        
        errores_encontrados = 0
        CAMPOS_COMPROBADOS = 4.0

        errores_maximos = len(mixpanel_data) * CAMPOS_COMPROBADOS
        for component_data, timeline_data  in zip(mixpanel_data, timeline):
            if component_data['author'] != timeline_data['author']:
                print "Error en el campo author"
                print "%s != %s" % (component_data['author'], timeline_data['author'])
                errores_encontrados += 1
            
            hashed_title = hashlib.sha1(timeline_data['title']).hexdigest()
            if component_data['title'] != hashed_title:
                print "Error en el campo title"
                print "%s != %s" % (component_data['title'], hashed_title)
                errores_encontrados += 1
            
            # if component_data['score'] != timeline_data['score']:
            #     print "Error en el campo score"
            #     print "%s != %s" % (component_data['score'], timeline_data['score'])
            #     errores_encontrados += 1

            # if component_data['num_comments'] != timeline_data['num_comments']:
            #     print "Error en el campo num_comments"
            #     print "%s != %s" % (component_data['num_comments'], timeline_data['num_comments'])
            #     errores_encontrados += 1

            if component_data['subreddit'] != timeline_data['subreddit']:
                print "Error en el campo subreddit"
                print "%s != %s" % (component_data['subreddit'], timeline_data['subreddit'])
                errores_encontrados += 1
            
            hashed_text = hashed_title = hashlib.sha1(timeline_data['selftext']).hexdigest()
            if component_data['text'] != hashed_text:
                print "Error en el campo text"
                print "%s != %s" % (component_data['text'], hashed_text)
                errores_encontrados += 1
            print "--------------------------------------"
        completitud = errores_encontrados/errores_maximos
        print "Completitud del experimento %d: %f" %(experiment_id, completitud)
        mpFacebook.track(completitud, "Fallos totales " + version, {"numero fallos": completitud})


############################################
############################################
        #CASO7: SPOTIFY
############################################
############################################

    elif social_network == "spotify":

        ##########################################################################################################################################
        #-------------------------------------------------------DATOS SPOTIFY API---------------------------------------------------------------
        ##########################################################################################################################################
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/spotify-component/spotifyCompletitudMaster.html")
                sleep(3)
            elif(version=="latency"):
                webbrowser.open_new(url_base_local + "/Latency/spotify-component/spotifyCompletitudLatency.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/spotify-component/spotifyCompletitudAccuracy.html")
                sleep(3)

        #token:te vas al componente y haces polymer serve -o -p 8080. Se despliega, en consola de navegador haces $(componente).token
        access_token= "BQDz3rTqpaTzqD0A-qz6-okvAjmVXAVVF_3OM5RBpR0oBlR4Sr9D5N8jq7h4qENj0q_yL8y1IwwpHT0gry2FLfw9SRJhiYXCeqnJi7E_Pm6xnbN3IjVv-H06JL-FQ05Tcyb3d66oM1grxIXu1kmMddmYwCYIgyiX"

        spotify_getTimeline = "https://api.spotify.com/v1/me/playlists" 
        headers = {"Authorization": "Bearer " + access_token}
        pet_timeline_spoti= requests.get(spotify_getTimeline,headers=headers)
        #aqui tengo todos los objetos de spotify (cada playlist)
        timeline_spoti=pet_timeline_spoti.json()

        imagesList=[]; namePlaylist=[]; createdByList=[]; songsList=[]; artistList=[]; listaCanciones=[]; tracks=[]; idList=[]; songArtistList=[]
    
        #recorro el timeline y cojo de la clave 'data' sus valores y dentro de sus valores la url de cada tablero
        for k,v in timeline_spoti.iteritems():
            if(timeline_spoti.has_key('items')):
                itemsSpoti=timeline_spoti.get('items',None)
        for playlist in itemsSpoti:
            namePlaylist.append(playlist['name'])
            createdByList.append(playlist['owner']['id'])
            imagesList.append(playlist['images'][0]['url'])
            listaCanciones.append(playlist['tracks']['href'])
        
        #peticion para obtener los tracks (lista de canciones)
        for listaTracks in listaCanciones:
            spotify_getTracks = listaTracks
            headers = {"Authorization": "Bearer " + access_token}
            pet_tracks= requests.get(spotify_getTracks,headers=headers)
            tracks_spoti= pet_tracks.json()
            tracks.append(tracks_spoti)

        #recorro para coger el nombre del artista y el nombre de la cancion
        #tracks son los 6 albumes que tiene esta cuenta
        for canciones in tracks:
            songsArray = canciones['items']
            for songs in songsArray:
                songsList.append(songs['track']['name'])
                idList.append(songs['track']['id'])
                songsIdZip=zip (idList,songsList)
                #lista de los nombres de los artistas de una cancion
                artistList.append(songs['track']['artists'][0].get('name'))
                artistIdZip=zip(idList,artistList)
                dictSongs = dict(songsIdZip)
                dictArtists = dict(artistIdZip)
                songArtistList = [(k, dictSongs[k], dictArtists[k]) for k in sorted(dictSongs)]
                songArtistList = [(k, v, dictArtists[k]) for k, v in songsIdZip]

        ##########################################################################################################################################
        #----------------------------------------DATOS SPOTIFY COMPONENTE (RECOGIDOS DE MIXPANEL)------------------------------------------------
        ##########################################################################################################################################
        sleep(30)
        # Hay que crear una instancia de la clase Mixpanel, con tus credenciales (API KEY y API SECRET)
        x=mixpanel_api.Mixpanel("dfe97ec9423e91ce01a6f223288bfb91","c21511e177f3b64c983228d922e0d1f6")
        contadorFallos=0
        lista=[]
        if version in version_list:
            params={'event':version,'name':'value','type':"general",'unit':"day",'interval':1}
            print type(params)
            respuesta=x.request(['events/properties/values'], params, format='json')
            print type(respuesta)
          #pasar de unicode a dict
          #for x in respuesta:
            #resp = ast.literal_eval(x)
            #lista.append(resp)                   
        
          #ordeno la lista de diccionarios por la posicion (va de 0 a x)
          #newlist = sorted(lista, key=lambda posicion: posicion['i'])


    

    else:
        print "Wrong social network or missing param"
        # {}: Obligatorio, []: opcional
        print "Usage: completitud.py {twitter|facebook|instagram|github [facebook_access_token]"




#if __name__ == "__main__":
    #main()



