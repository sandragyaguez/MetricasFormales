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
from twitter import *
from requests_oauthlib import OAuth1
import requests
import webbrowser
import urllib3
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import datetime
import re
import mixpanel
from mixpanel import Mixpanel
mp = Mixpanel("070bf8a01a6127ebf78325716490697a")

estado="prueba"
estado1="prueba1"
estado2="prueba2"

webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/_refresh.html" + "?" + estado)
webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/RefreshLatency.html" + "?" + estado1)
webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/RefreshAccuracy.html" + "?" + estado2)

#webbrowser.open_new("http://twitter-timeline-app.appspot.com/app/_refresh.html" + "?" + estado + "&" + estado1 + "&" + estado2)

time.sleep(5)

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

#PUBLICACION DE TWEET Y REQUEST DEL TIMELINE
oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
url = 'https://api.twitter.com/1.1/statuses/update.json'
request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"

event_master_post= "Twitter post master"
event_latency_post="Twitter post latency"
event_accuracy_post="Twitter post accuracy"

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
    mp.track(tpubl_ms, event_accuracy_post,{"time post": tpubl_ms, "tweet": estado})
    print "tiempo post en ms (1): " + str(tpubl_ms)

#Request timeline user
    s= requests.get(request_usertimeline, auth=oauth)
    timeline=s.json()
#Encontrar el texto del tweet que acabo de publicar, con el campo text que tiene cada tweet, y timestamp cuando me lo muestre en twitter (tambien se puede hacer con ID)(polling)
    for tweet in timeline:
        text=tweet['text']
        print "el tweet es: " + text
        if text==estado:
            break
#     tiguales=datetime.datetime.now()
#     tiguales_ms=int(time.time()*1000)
#     print "encontrado en Twitter: " + str(tiguales_ms)
#     dif=tiguales-tpubl
#     esta diferencia es el tiempo que tarda desde que hago un post (twitteo) hasta que Twitter me lo muestra (se encuentra en el timeline del usuario)
#     dif_ms=tiguales_ms-tpubl_ms


    
#Pruebas
#publicar(estado)
#publicar(estado1)
publicar(estado2)

