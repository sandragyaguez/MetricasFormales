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

#Deshabilita los warnings que salen por defecto
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

path = os.path.dirname(os.path.abspath(__file__))

# Accedemos a todos los datos(urls, claves de tokens y ficheros) mediante el fichero yaml de configuracion
output_file2 = os.path.join(path, "configUptime.yaml") 
configFile = open(output_file2,"r")
yaml_config = yaml.load(configFile)

# Funcion que se va a utilizar para todas las APIs, tiene como parametros la respuesta de la API
# y el fichero donde queremos ir guardando esas respuestas

def updateFile(request, oldFile):
    output_file = os.path.join(path,oldFile)
    resFile = open(output_file, "a")
    if request == 200:
        resFile.write(str(request) +  " ----------- " + time.strftime("%c") + "\n")
    else:
        resFile.write(str(request) +  " ----------- " + time.strftime("%c") + " --------FALLO--------\n")
    resFile.close()


#######################################     TWITTER     ###########################################

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
updateFile(status.status_code,yaml_config['file_data_Twitter'])


#######################################     FACEBOOK    ###########################################

status = requests.get(yaml_config['url_Facebook'])
updateFile(status.status_code,yaml_config['file_data_Facebook'])


#######################################     GOOGLEPLUS      #######################################
        
#Request a followers de Deus
status = requests.get(yaml_config['url_Google'])
updateFile(status.status_code,yaml_config['file_data_Google'])

#######################################     PINTEREST    ##########################################

access_token = yaml_config['pinterest_credentials']['access_token']

#tengo que hacer una primera peticion a los boards de a los que sigo para poder pedir sus pins (imagenes)
status = requests.get(yaml_config['url_Pinterest'] + access_token)
updateFile(status.status_code,yaml_config['file_data_Pinterest'])


#######################################     TRAFFIC     ###########################################

request_uri= yaml_config['url_Traffic']
headers= {"content-type":"application/x-www-form-urlencoded"}

status = requests.get(request_uri, verify=False, headers=headers)
updateFile(status.status_code,yaml_config['file_data_Traffic'])


#######################################     OPEN-WEATHER    #######################################

request_uri= yaml_config['url_Weather']
headers= {"content-type":"application/x-www-form-urlencoded"}
#verify=False para que no me de errores de SSL
status = requests.get(request_uri, verify=False, headers=headers)
updateFile(status.status_code,yaml_config['file_data_Weather'])
if status.status_code == 500:
    print status.text

#######################################     REDDIT      ###########################################

request_uri = yaml_config['url_Reddit']
header = {
    'User-agent': 'Mozilla/5.0'
}
status = requests.get(request_uri, headers=header) 
updateFile(status.status_code,yaml_config['file_data_Reddit'])


#######################################     SPOTIFY     ###########################################

client_id = yaml_config['spotify_credentials']['client_id']
client_secret = yaml_config['spotify_credentials']['client_secret']
grant_type = 'client_credentials'
body_params = {'grant_type' : grant_type}
url=yaml_config['url_Spotify']
status = requests.post(url, data=body_params, auth = (client_id, client_secret)) 
updateFile(status.status_code,yaml_config['file_data_Spotify'])


#######################################     FINANCE     ###########################################

#verify=False para que no me de errores de SSL
status = requests.get(yaml_config['url_Finance'])
updateFile(status.status_code,yaml_config['file_data_Finance'])