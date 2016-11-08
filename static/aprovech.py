from requests_oauthlib import OAuth1
import requests
import pprint
import sys
import codecs
import re
import urllib
import unicodedata
from bs4 import BeautifulSoup
from mixpanel import Mixpanel

mpResults = Mixpanel("6656474c876da699f51ccc6f480a0d6c")


network_list = ["twitter","facebook","github","googleplus","instagram"]
version_list = ["master","latency","accuracy"]

#consola: python code_lines.py component version
if len(sys.argv) >= 2:
    social_network = sys.argv[1]
else:
    social_network = ''

if len(sys.argv) >= 3:
    version= sys.argv[2]
else:
    version = ''

print social_network
print version


if social_network in network_list:

	if social_network == 'twitter':

		CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
		CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
		ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
		ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret

		oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
		request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"
		s= requests.get(request_usertimeline, auth=oauth)
		timeline=s.json()
		

		if version in version_list:
			if(version=="master"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/twitter-timeline/static/twitter-timeline.html"))
			elif(version=="latency"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/twitter-timeline/static/twitter-timeline.html"))
			elif(version=="accuracy"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/twitter-timeline/static/twitter-timeline.html"))



	elif social_network == 'facebook':

		access_token="EAANMUmJPs2UBAB8LIgErCGXNR4DgN9kZCkh52J23OjxVzPVZBAiULkOVll6RIaFgQa3mf1Edq7Kl2ZB6kLrFPg1DlswToZCqb3T1Ge7bNBGdmIOCZCf7l3ddZCOxTyzDdOagf1VLcG6VZCv70QoMYcSwRnuIfr4ZAcYlZCtX8o51SyAZDZD"
		facebook_url = "https://graph.facebook.com/v2.3/me?fields=home&pretty=1&access_token=" + access_token
		s= requests.get(facebook_url)
		timeline=s.json()
		#para acceder a los recursos de facebook hay que acceder al diccionario home y luego al data
		for k,v in timeline.iteritems():
			if (timeline.has_key('home')):
				values=timeline.get('home',None)
		for items in values:
			if(values.has_key('data')):
				timeline=values.get('data',None)

		if version in version_list:
			if(version=="master"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/facebook-wall/facebook-wall.html"))
			elif(version=="latency"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/facebook-wall/facebook-wall.html"))
			elif(version=="accuracy"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/facebook-wall/facebook-wall.html"))


	elif social_network == 'github':

		github_url = "https://api.github.com/users/mortega5/received_events?per_page=50"
		peticion= requests.get(github_url)
		timeline=peticion.json()

		if version in version_list:
			if(version=="master"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/github-events/github-events.html"))
			elif(version=="latency"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/github-events/github-events.html"))
			elif(version=="accuracy"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/github-events/github-events.html"))

	elif social_network == 'googleplus':

		access_token="ya29.CjmQA3LcCsuY1E6e7zcYwxze_b7O75YGepaeG_n-7NbhDhjBh0yUg6_NlRLMSSHjJyb6-2PvjzTT7TE"
		google_url_followers="https://www.googleapis.com/plus/v1/people/me/people/visible"
		headers = {"Authorization": "Bearer " + access_token}

		s= requests.get(google_url_followers,headers=headers)
		timeline=s.json()
		followers=[]
		#para acceder a los recursos de googleplus
		if(timeline.has_key('items')):
			values=timeline.get('items',None)
			for n in values:
			#guardo el id del follower
				id_followers=n['id']
                id_followers=int(id_followers)
                followers.append(id_followers)
               
        #Request a timeline Deus para todos los usuarios. Para obtener la informacion de los post, previamente he tenido que obtener los followers
        for i in followers:
            #hay que poner str(i) porque sino no se puede concatenar string con un long (int)
            google_url="https://www.googleapis.com/plus/v1/people/" + str(i) + "/activities/public"
            pet= requests.get(google_url,headers=headers)
            timeline1=pet.json()
            if(timeline1.has_key('items')):
                timeline=timeline1.get('items',None)

		if version in version_list:
			if(version=="master"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Master/googleplus-timeline/googleplus-timeline.html"))
			elif(version=="latency"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Latency/googleplus-timeline/googleplus-timeline.html"))
			elif(version=="accuracy"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Accuracy/googleplus-timeline/googleplus-timeline.html"))



#cojo las claves de cada timeline, que son los recursos que tiene cada event
for x in timeline:
	True
claves=x.keys()
print "claves: " + str(claves)
print ""


#------------------------ NO VALE-----------------------
# lista=[]
# lista2=[]
# lista3=[]

# for clave in claves:
# 	lista.append( '["' + str(clave) + '"]')
# #barra invertida para que no me lo coja todo como un string
# for clave in claves:
# 	lista2.append( '[\'' + str(clave) + '\']')

# for clave in claves:
# 	lista3.append( '.' + str(clave))

#------------------------ NO VALE-----------------------

# lista['hola']
# lista["hola"]
#este caso aun no esta contemplado:
# a = 'hola'
# lista[a]




matching=[]
#cojo todo el texto dentro de la etiqueta template
entradas = soup.find('template').prettify()
#unicode to str
html=unicodedata.normalize('NFKD', entradas).encode('ascii','ignore')
#separo palabras por espacios
html= re.split("", html)

for recursos in html:
	#busco dentro cualquier cosa que sea item.recurso
	recu=re.findall(("item*\.[A-z]*"), recursos) 

for clave in claves:
	for word in recu:
		#busco si la clave se encuentra en el html
		coind=word.find(clave)
		#si se encuentra y no estaba ya incluida, la anado
 		if (coind>=0 and clave not in matching):
 			matching.append(clave)

print "recursos encontrados:", matching

nclaves=float(len(claves))
nmatching=float(len(matching))
aprov=(nmatching/nclaves)*100
print aprov

mpResults.track("Aprovechamiento de recursos", social_network,{"aprov %":aprov,"componente":social_network,"version":version})
