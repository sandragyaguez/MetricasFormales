#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from requests_oauthlib import OAuth1
import requests
import time
import os
import yaml
import urllib
import urllib3
from pymongo import Connection

#Deshabilita los warnings que salen por defecto
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

path = os.path.dirname(os.path.abspath(__file__))

# Accedemos a todos los datos(urls, claves de tokens y ficheros) mediante el fichero yaml de configuracion
output_file2 = os.path.join(path, "configUptime.yaml") 
configFile = open(output_file2,"r")
yaml_config = yaml.load(configFile)

#Inicio de la conexion con la base de datos

con = Connection('localhost')
db = con.StatusAPIs

#Funcion que inserta el estado de la api en la base de datos de mongo

def updateFile(request, app):
    if request == 200:
        answer = 'Correct'
    else:
        answer = 'Wrong'
    status = {'code':request, 'date': time.strftime("%x"), 'time': time.strftime("%X"), 'answer':answer}
    store = db[app]
    store.insert(status)

# #######################################     TWITTER     ###########################################

# Credenciales de twitter
CONSUMER_KEY =  yaml_config['twitter_credentials']['consumer_key']                       
CONSUMER_SECRET = yaml_config['twitter_credentials']['consumer_secret']                  
ACCESS_KEY = yaml_config['twitter_credentials']['access_token']                          
ACCESS_SECRET = yaml_config['twitter_credentials']['access_token_secret']    

# Autentificacion de los credenciales de Twitter
oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
request_hometimeline = yaml_config['url_Twitter']
status = requests.get(request_hometimeline, auth=oauth)
#Actualizacion del fichero con el estado de twitter
updateFile(status.status_code,'Twitter')


# #######################################     FACEBOOK    ###########################################

status = requests.get(yaml_config['url_Facebook'])
updateFile(status.status_code,'Facebook')


# #######################################     GOOGLEPLUS      #######################################
        
#Request a followers de Deus
status = requests.get(yaml_config['url_Google'])
updateFile(status.status_code,'Google')

# #######################################     PINTEREST    ##########################################

access_token = yaml_config['pinterest_credentials']['access_token']

#tengo que hacer una primera peticion a los boards de a los que sigo para poder pedir sus pins (imagenes)
status = requests.get(yaml_config['url_Pinterest'] + access_token)
updateFile(status.status_code,'Pinterest')


#######################################     TRAFFIC     ###########################################
request_uri= yaml_config['url_Traffic']
headers= {"content-type":"application/x-www-form-urlencoded"}
status = requests.get(request_uri, verify=False, headers=headers)
updateFile(status.status_code,'Traffic')


# #######################################     OPEN-WEATHER    #######################################

request_uri= yaml_config['url_Weather']
headers= {"content-type":"application/x-www-form-urlencoded"}
#verify=False para que no me de errores de SSL
status = requests.get(request_uri, verify=False, headers=headers)
updateFile(status.status_code,'Weather')


# #######################################     REDDIT      ###########################################

request_uri = yaml_config['url_Reddit']
header = {
    'User-agent': 'Mozilla/5.0'
}
status = requests.get(request_uri, headers=header) 
updateFile(status.status_code,'Reddit')


# #######################################     SPOTIFY     ###########################################

client_id = yaml_config['spotify_credentials']['client_id']
client_secret = yaml_config['spotify_credentials']['client_secret']
grant_type = 'client_credentials'
body_params = {'grant_type' : grant_type}
url=yaml_config['url_Spotify']
status = requests.post(url, data=body_params, auth = (client_id, client_secret)) 
updateFile(status.status_code,'Spotify')


#######################################     FINANCE     ###########################################

status = requests.get(yaml_config['url_Finance'])
updateFile(status.status_code,'Finance')

# Se cierra la conexion con la base de datos
con.close()