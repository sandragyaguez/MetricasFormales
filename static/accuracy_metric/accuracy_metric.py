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
from requests_oauthlib import OAuth1
import requests
import webbrowser
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import datetime
import re
import ast
import calendar
import mixpanel
import os
import hashlib
from random import randrange
from mixpanel import Mixpanel
import datetime
import base64
from requests.auth import HTTPBasicAuth
import yaml

path = os.path.dirname(os.path.abspath(__file__))
output_file2 = os.path.join(path, "../Componentes/config.yaml") 
configFile = open(output_file2,"r")
yaml_config = yaml.load(configFile)

#objetos Mixpanel para las distintas redes sociales (token del project)
mpTwitter = Mixpanel (yaml_config['mixpanelToken']['twitter'])
mpFacebook = Mixpanel (yaml_config['mixpanelToken']['facebook'])
mpGoogle = Mixpanel (yaml_config['mixpanelToken']['google'])
mpPinterest = Mixpanel (yaml_config['mixpanelToken']['pinterest'])
mpTraffic = Mixpanel (yaml_config['mixpanelToken']['traffic'])
mpWeather = Mixpanel (yaml_config['mixpanelToken']['weather'])
mpStock = Mixpanel (yaml_config['mixpanelToken']['finance'])
mpReddit = Mixpanel (yaml_config['mixpanelToken']['reddit'])
mpSpotify = Mixpanel (yaml_config['mixpanelToken']['spotify'])

#api secret de cada project para hacer peticiones
twitterSecret = yaml_config['requestTokenAccuracy']['twitter']
facebookSecret = yaml_config['requestTokenAccuracy']['facebook']
googleSecret = yaml_config['requestTokenAccuracy']['google']
pinterestSecret = yaml_config['requestTokenAccuracy']['pinterest']
trafficSecret = yaml_config['requestTokenAccuracy']['traffic']
weatherSecret = yaml_config['requestTokenAccuracy']['weather']
financeSecret = yaml_config['requestTokenAccuracy']['finance']
redditSecret = yaml_config['requestTokenAccuracy']['reddit']
spotifySecret = yaml_config['requestTokenAccuracy']['spotify']

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

network_list = ["twitter", "facebook", "googleplus", "pinterest", "traffic-incidents", "open-weather", "finance-search", "reddit", "spotify"]
version_list = ["master","latency", "accuracy"]
url_base_local= "http://localhost:8000"

#de los comandos que ejecuto desde consola, me quedo con el segundo (posicion 1,array empieza en 0),
if len(sys.argv) >= 2:
    social_network = sys.argv[1]
else:
    social_network = ''

if len(sys.argv) >= 3:
    version= sys.argv[2]
else:
    version = ''

if social_network in network_list:

############################################
            #CASO1: TWITTER
############################################
    if social_network == 'twitter':
        
        #--DATOS API TWITTER--#
        CONSUMER_KEY = yaml_config['twitter']['consumer-key']
        CONSUMER_SECRET =  yaml_config['twitter']['consumer-secret']
        ACCESS_KEY =  yaml_config['twitter']['access-token']
        ACCESS_SECRET =  yaml_config['twitter']['secret-token']

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new( url_base_local + "/twitter-timeline/static/TwitterCompletitud.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new( url_base_local + "/Accuracy/twitter-timeline/static/TwitterCompletitudAccuracy.html")
                sleep(3)

        #objeto oauth con credenciales de usuario Deus
        oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
        #url para hacer peticion al timeline de twitter
        request_hometimeline="https://api.twitter.com/1.1/statuses/home_timeline.json?count=200"
        s= requests.get(request_hometimeline, auth=oauth)
        timeline=s.json()
        print timeline[0]

        #--DATOS TWITTER COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(30)
        lista = []; liskey = []; lisvalue = []; listaFallosText = []; listaFallosUser = []
        contadorFallos = 0
        params={'event':version,'name':'value'}
        #se le pasa el API secret
        respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(twitterSecret, '')).json()

        for x in respuesta:
            #pasar de unicode a dict
            resp = ast.literal_eval(x)
            lista.append(resp)

        newlist = sorted(lista, key=lambda id_tweet: id_tweet['id'])
        newlist.reverse()

        contador = len(newlist)
        for index, element in enumerate(newlist):
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
        mpTwitter.track(contadorFallos, "Fallos totales " + version, {"numero fallos": contadorFallos})                           

############################################
            #CASO2: FACEBOOK
############################################

    elif social_network == 'facebook':

        #--DATOS FACEBOOK API--#
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/facebook-wall/FacebookCompletitud.html")
                sleep(5)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/facebook-wall-accuracy/FacebookCompletitudAccuracy.html")
                sleep(5)

        #cambiarlo cada hora y media: https://developers.facebook.com/tools/explorer/928341650551653 (Get User Access Token, version 2.12)
        access_token= yaml_config['facebook']['access_token']
        facebook_url="https://centauro.ls.etsiinf.upm.es/api/aux/facebookTimeline?&access_token=" + access_token +"&locale=es_es"

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
          
        #--DATOS FACEBOOK COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(20)
        contadorFallos=0
        params={'event':version,'name':'value'}
        respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(facebookSecret, '')).json()

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
        mpFacebook.track(contadorFallos, "Fallos totales accuracy", {"numero fallos": contadorFallos})


############################################
            #CASO3: GOOGLE+
############################################

    elif social_network == 'googleplus':
        #--DATOS GOOGLE+ API--#
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/googleplus-timeline/demo/GooglePlusCompletitud.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/googleplus-timeline/demo/GooglePlusCompletitudAccuracy.html")
                sleep(3)

        # Url para obtener nuevo token google: https://developers.google.com/+/web/api/rest/latest/activities/list#try-it
        # (Para el caso de Google, haces una peticion a la API con el explorer API, vas a networks, y coges el token que
        # viene en el header Authorization: 'Bearer TOKEN')
        #cambiar token cada hora y media: https://developers.google.com/+/web/api/rest/latest/activities/list?authuser=1
        access_token= yaml_config['googleplus']['token']
        key = yaml_config['googleplus']['api_key']
        google_url_followers="https://people.googleapis.com/v1/people/me/connections?key=%s&access_token=%s" % (key,access_token)
        headers = {"Authorization": "Bearer " + access_token}
        
        #Request a followers de Deus
        s= requests.get(google_url_followers,headers=headers)
        muro=s.json()
        followers=[str(follower['metadata']['sources'][1]['id']) for follower in muro['connections']]

        posts=[]
        #Request a timeline Deus para todos los usuarios. Para obtener la informacion de los post, previamente he tenido que obtener los followers
        for i in followers:
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

        #--DATOS GOOGLE+ COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(10)
        contadorFallos=0
        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(googleSecret, '')).json()

            lista = []
            for x in respuesta:
                resp = ast.literal_eval(x)
                lista.append(resp)

            newlist = sorted(lista, key=lambda posicion: posicion['publish'], reverse=True)            

            for component, post_api in zip(newlist,posts):
                if component['user'] != post_api['actor']['displayName']:
                    print "falla en el usuario: %s vs %s" % (component['user'], post_api['actor']['displayName'])
                    contadorFallos += 1
                if component['text'] != post_api['hashed_text']:
                    print "falla en el usuario: %s vs %s" % (component['text'], post_api['hashed_text'])
                    contadorFallos += 1

            contadorFallos=contadorFallos / (len(newlist)*2.0)
            mpGoogle.track(contadorFallos, "Fallos totales %s" % version, {"numero fallos": contadorFallos})
            

############################################
            #CASO4: PINTEREST
############################################

    elif social_network == 'pinterest':

        #--DATOS PINTEREST API--#
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/pinterest-timeline/demo/PinterestCompletitud.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/pinterest-timeline/demo/PinterestCompletitudAccuracy.html")
                sleep(3)

        access_token= yaml_config['pinterest']['token']
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

        #de cada url separo por / para poder coger el nombre del usuario y del tablero para despues poder hacer peticion de pins
        for image in lista_img:
            new=image.split("/")
            #cojo todos los username a los que sigo para poder hacer la siguiente peticion
            new[3]=str(new[3])
            username.append(new[3])
            #cojo todos los nombres de los tableros
            new[4]=str(new[4])
            board.append(new[4])

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
                    
        getData(pets)
        
        #--DATOS PINTEREST COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(30)
        imagComp=[]
        contadorFallos=0

       #metodo que me compara la lista de imagenes obtenidas por la API con la lista de imagenes cogidas en el componente
        def comp(list1, list2):
            # variable global para que no me de el fallo "referenciado antes de asignado"
            global contadorFallos
            fallos=[]
            for val in list2:
                if not (val in list1):
                    fallos.append(val)
                    contadorFallos=contadorFallos+1        
            return fallos

        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(pinterestSecret, '')).json()        
            imagComp = [str(json.loads(res)['url']) for res in respuesta]        
            fallos=comp(imagAPI,imagComp)
            mpPinterest.track(fallos,"Fallos imagenes %s" % version,{"imagen":fallos, "version": version})
            contadorFallos=contadorFallos/float(len(imagAPI))
            mpPinterest.track(contadorFallos, "Fallos totales %s" % version, {"numero fallos": contadorFallos})


############################################
        #CASO5: TRAFFIC-INCIDENTS
############################################

    elif social_network == 'traffic-incidents':
        
        #--DATOS TRAFFIC API--#
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/traffic-incidents/demo/TrafficCompletitud.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/traffic-incidents/demo/TrafficCompletitudAccuracy.html")
                sleep(3)

        token = yaml_config['traffic-incidents']['api_key_traffic']
        request_uri= "https://centauro.etsiinf.fi.upm.es:4444/traffic?map=39.56276609909911,-4.650120900900901,41.36456790090091,-2.848319099099099&key=" + token
        
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
        dictPythonText=dict(zipPythonDesc)
        zipPythonDate=zip(listacont,lista_date)
        dictPythonDate=dict(zipPythonDate)
        zipPythonType=zip(listacont,lista_type)
        dictPythonType=dict(zipPythonType)

        #--DATOS TRAFFIC COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(30)
        params={'event':version,'name':'value'}
        respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(trafficSecret, '')).json()     
        contadorFallos=0
        lista=[]; liskey=[]; lisvalue=[]

        for x in respuesta:
            resp = ast.literal_eval(x)
            lista.append(resp)

        newlist = sorted(lista, key=lambda posicion: posicion['i'])

        for index, entry in enumerate(newlist):
          if len(dictPythonText) < index or  dictPythonText[index] != entry['descripcion']:
            print "falla en posicion: ", entry['i'] 
            liskey.append(k)
            lisvalue.append(v)
            listaFallosDate=zip(liskey,lisvalue)
            contadorFallos=contadorFallos+1
          
          if len(dictPythonText) < index or dictPythonType[index] != entry['tipo']:
            print "falla en posicion: ", entry['i'] 
            liskey.append(k)
            lisvalue.append(v)
            listaFallosDate=zip(liskey,lisvalue)
            contadorFallos=contadorFallos+1

        contadorFallos=contadorFallos/(contador*2.0)
        mpTraffic.track(contadorFallos, "Fallos totales" + version, {"numero fallos": contadorFallos})
   
############################################
        #CASO6: FINANCE-SEARCH
############################################

    elif social_network == 'finance-search':

        #--DATOS STOCK API--#
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/finance-search/demo/FinanceSearchMaster.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/finance-search-accuracy/demo/FinanceSearchAccuracy.html")
                sleep(3)
               
        symbol = "GOOGL"
        query = 'select * from yahoo.finance.quote where symbol in ("%s")' % symbol

        request_uri= "https://centauro.ls.etsiinf.upm.es:4444/stock?q=%s" % query
        headers= {"content-type":"application/x-www-form-urlencoded"}
        #verify=False para que no me de errores de SSL
        response= requests.get(request_uri, verify=False, headers=headers)
        
        data = response.json()
        data = data['query']['results']['quote'][0]

        #--DATOS STOCK COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        latency=0
        if version == 'latency':
          latency=10
        sleep(10+latency)
        params={'event':version,'name':'value'}
        respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(financeSecret, '')).json()
        respuesta = [ json.loads(res) for res in respuesta ]
        respuesta = sorted(respuesta, key=lambda x: -x['Date'])
        respuesta = respuesta[0]
        errors = 0
        analyzed = 0.0
        
        for key,value in respuesta.iteritems():
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
        #CASO6: OPEN-WEATHER
############################################

    elif social_network == 'open-weather':

        #--DATOS WEATHER API--#
        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/open-weather/demo/WeatherCompletitud.html")
            # elif(version=="accuracy"):
            #     webbrowser.open_new(url_base_local + "/Accuracy/open-weather-accuracy/demo/WeatherCompletitudAccuracy.html")
        
        contador = 0
        ppid_weather = yaml_config['open-weather']['app-id']
        request_uri= "https://centauro.ls.etsiinf.upm.es:4444/weather?lat=40.4336199&lon=-3.8134707000000003&units=metric&lang=es&appId=" + ppid_weather
        
        headers= {"content-type":"application/x-www-form-urlencoded"}
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

          hayValorespixita = True
          while hayValorespixita:
            nextdate += datetime.timedelta(days=1)
            values_next_day1=filter(lambda x: datetime.datetime.fromtimestamp(x['dt']).strftime('%d/%m/%Y') == nextdate.strftime("%d/%m/%Y"), lista_timeline)
            if len(values_next_day1) == 0:
                hayValorespixita = False
            else: 
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

        #--DATOS WEATHER COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(30)
        contadorFallos=0
        lista=[]

        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(weatherSecret, '')).json()
    
            for x in respuesta:
                resp = ast.literal_eval(x)
                lista.append(resp)                   
          
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
            mpWeather.track(contadorFallos, "Fallos totales " + version, {"numero fallos": contadorFallos})

############################################
        #CASO6: REDDIT-TIMELINE
############################################

    elif social_network == "reddit":
        experiment_id = int(time.time())
        print "ID. Experimento: %d" % experiment_id
        reddit_token = yaml_config['reddit-timeline']['token']
        
        #--DATOS REDDIT API--#
        if(version=="master"):
            webbrowser.open_new(url_base_local + "/Master/reddit-timeline/demo/RedditTimelineMaster.html?" + str(experiment_id))
        elif(version=="accuracy"):
            webbrowser.open_new(url_base_local + "/Accuracy/reddit-timeline/demo/RedditTimelineAccuracy.html?" + str(experiment_id))

        #Coger un access token valido
        request_uri = "https://oauth.reddit.com/r/all/hot"
        header = {
            "authorization": "Bearer " + reddit_token,
            'User-agent': 'Mozilla/5.0'
        }
        req = requests.get(request_uri, headers=header)

        if (req.status_code != 200):
            print "(%d) El token proporcionado no es valido o se ha superado el limite de peticiones" % req.status_code
            sys.exit(2)
        timeline = req.json()['data']['children']
        timeline = [element['data'] for element in timeline]
        
        #--DATOS REDDIT COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(15)
        params={'event':version,'name':'value'}
        respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(redditSecret, '')).json()
        respuesta = [json.loads(data) for data in respuesta]
        respuesta = filter(lambda el: el['experiment'] == str(experiment_id), respuesta)
        respuesta = sorted(respuesta, key=lambda element: element['i'])

        if len(respuesta) != len(timeline):
            print "Las longitudes de las dos listas recibidas no son iguales. Comprueba que se mandan todos los datos bien"
            print "mixpanel: %d  vs  componente: %d" % (len(respuesta), len(timeline))
            sys.exit(3)
        
        errores_encontrados = 0
        CAMPOS_COMPROBADOS = 4.0

        errores_maximos = len(respuesta) * CAMPOS_COMPROBADOS
        for component_data, timeline_data  in zip(respuesta, timeline):
            if component_data['author'] != timeline_data['author']:
                print "Error en el campo author"
                print "%s != %s" % (component_data['author'], timeline_data['author'])
                errores_encontrados += 1
            
            hashed_title = hashlib.sha1(timeline_data['title']).hexdigest()
            if component_data['title'] != hashed_title:
                print "Error en el campo title"
                print "%s != %s" % (component_data['title'], hashed_title)
                errores_encontrados += 1

            if component_data['subreddit'] != timeline_data['subreddit']:
                print "Error en el campo subreddit"
                print "%s != %s" % (component_data['subreddit'], timeline_data['subreddit'])
                errores_encontrados += 1
            
            hashed_text = hashed_title = hashlib.sha1(timeline_data['selftext']).hexdigest()
            if component_data['text'] != hashed_text:
                print "Error en el campo text"
                print "%s != %s" % (component_data['text'], hashed_text)
                errores_encontrados += 1
        completitud = errores_encontrados/errores_maximos
        print "Completitud del experimento %d: %f" %(experiment_id, completitud)
        mpReddit.track(completitud, "Fallos totales " + version, {"numero fallos": completitud})


############################################
        #CASO7: SPOTIFY
############################################

    elif social_network == "spotify":
        
        #--DATOS SPOTIFY API--#
         
        #eliminar datos de mixpanel
        #request = requests.get('https://mixpanel.com/api/2.0/engage',  auth=HTTPBasicAuth('c21511e177f3b64c983228d922e0d1f6', '')).json()
        #requests.delete('https://mixpanel.com/api/2.0/annotations/delete/', params, auth=HTTPBasicAuth('c21511e177f3b64c983228d922e0d1f6', ''))

        if version in version_list:
            if(version=="master"):
                webbrowser.open_new(url_base_local + "/Master/spotify-component/spotifyCompletitudMaster.html")
                sleep(3)
            elif(version=="accuracy"):
                webbrowser.open_new(url_base_local + "/Accuracy/spotify-component/spotifyCompletitudAccuracy.html")
                sleep(3)

        #token:te vas al componente y haces polymer serve -o -p 8080. Se despliega, en consola de navegador haces $(componente).token
        access_token= yaml_config['spotify']['token']

        spotify_getTimeline = "https://api.spotify.com/v1/me/playlists" 
        headers = {"Authorization": "Bearer " + access_token}
        pet_timeline_spoti= requests.get(spotify_getTimeline,headers=headers)   
        timeline_spoti = byteify(pet_timeline_spoti.json())

        imagesList=[]; namePlaylist=[]; createdByList=[]; listaCanciones=[]; listSpotify=[]
        numTracksArtists=0
    
        for k,v in timeline_spoti.iteritems():
            if 'items' in timeline_spoti:
                itemsSpoti=timeline_spoti.get('items',None)
        for playlist in itemsSpoti:
            numPlayList=len(itemsSpoti)
            namePlaylist.append(playlist['name'])
            createdByList.append(playlist['owner']['id'])
            hashed_image= hashlib.sha1(playlist['images'][0]['url']).hexdigest()
            imagesList.append(hashed_image)
            numImages=len(imagesList)
            listaCanciones.append(playlist['tracks']['href'])
            listSpotify.append({"id": playlist['id'],"owner": playlist['owner']['id'], "image": hashlib.sha1(playlist['images'][0]['url']).hexdigest(), "playList": playlist['name'], "songs": {}})
        
        #peticion para obtener los tracks (lista de canciones)
        for i, listaTracks in enumerate(listaCanciones):
            spotify_getTracks = listaTracks
            headers = {"Authorization": "Bearer " + access_token}
            pet_tracks= requests.get(spotify_getTracks,headers=headers)
            tracks_spoti= byteify(pet_tracks.json())
            for canciones in tracks_spoti['items']:
                numTracksArtists+=1
                listSpotify[i]['songs'].update({canciones['track']['id']: [canciones['track']['name'], canciones['track']['artists'][0]['name']]})

        datosEstudiados= numPlayList+numImages+(numTracksArtists*2)
        
        #---DATOS SPOTIFY COMPONENTE (RECOGIDOS DE MIXPANEL)--#
        sleep(10)
        contadorFallos=0
        listaComp=[]; liscompararAPI=[]; liscompararComp=[]
        if version in version_list:
            params={'event':version,'name':'value'}
            respuesta = requests.get('https://mixpanel.com/api/2.0/events/properties/values', params,  auth=HTTPBasicAuth(spotifySecret, '')).json()
        
        aux = []
        for datosComp in respuesta:
            resp = ast.literal_eval(datosComp)
            if "owner" in resp and "image" in resp and "id" in resp and "playList" in resp and "song" in resp and "idSong" in resp and "artist" in resp: 
                key = resp["idSong"]
                if key in aux: # ya esta de antes
                    listaComp[aux.index(key)]['songs'].update({resp['idSong']: [resp['song'], resp['artist']]})
                else:
                    listaComp.append({"id": resp["id"], "owner": resp['owner'], "image": resp['image'], "playList": resp['playList'], "songs": {resp['idSong']: [resp['song'], resp['artist']]}})
                    aux.append(key)

        def search(key, list):
            return next((item for item in list if item['id']==key), False)
        
        #contadorFallos += abs(len(listSpotify) - len(listaComp))
        for datosAPI in listSpotify:
            datosComponente = search(datosAPI['id'], listaComp)
            if datosComponente:
                if datosAPI['owner'] != datosComponente['owner']:
                    contadorFallos += 1
                if datosAPI['playList'] != datosComponente['playList']:
                    contadorFallos += 1

                #contadorFallos += abs(len(datosAPI['songs']) - len(datosComponente['songs']))
                for key in datosAPI['songs']:
                    for i in listaComp:
                        if key == i['songs'].keys()[0]:
                            if datosAPI['songs'][key][0] != i['songs'][key][0]: 
                                contadorFallos += 1
                            if datosAPI['songs'][key][1] != i['songs'][key][1]:
                                contadorFallos += 1
                
            listaComp.remove(datosComponente)

        fallosInterpolados = float(contadorFallos)/datosEstudiados
        mpSpotify.track(contadorFallos, "Fallos totales " + version, {"numero fallos": fallosInterpolados})


    else:
        print "Wrong social network or missing param"
        # {}: Obligatorio, []: opcional
        print "Usage: completitud.py {twitter|facebook|instagram|github [facebook_access_token]"

# if __name__ == "__main__":
#     app.run(port=9000)
