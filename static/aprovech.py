from requests_oauthlib import OAuth1
import requests
import pprint
import sys
import codecs
import re
import urllib
import unicodedata
from bs4 import BeautifulSoup


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

		access_token="EAANMUmJPs2UBAHL47dg0mZAX04ifmK2FlZC4OoUa9UyY6l2fmXKmKhrzA7c9j8aRPyVCZC7wFAJZALBb4BJ45qgtZButZBAGq8cAKPuduSkDv6pkZA1w4v73ZCJKRIDuOJFEXOupmvUIQIREyxDlMZCijshil8Kf6zCZCKR69SK0iSxgZDZD"
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
		print timeline

		if version in version_list:
			if(version=="master"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/github-events/github-events.html"))
			elif(version=="latency"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/github-events/github-events.html"))
			elif(version=="accuracy"):
				soup = BeautifulSoup(open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/github-events/github-events.html"))

	elif social_network == 'googleplus':

		access_token="ya29.CjmQA_vaigup3T7ViOcvuFYQuMyOP7cr4XFyrkK4-IA6NnXdeavy7YbLAGVBrFr8aRAFOrdaz06QrHo"
		google_url_followers="https://www.googleapis.com/plus/v1/people/me/people/visible"
		headers = {"Authorization": "Bearer " + access_token}

		s= requests.get(google_url_followers,headers=headers)
		timeline=s.json()
		print timeline
		#para acceder a los recursos de googleplus
		if(timeline.has_key('items')):
			timeline=timeline.get('items',None)

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

print "he encontrado:", matching