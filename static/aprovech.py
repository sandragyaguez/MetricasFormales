from requests_oauthlib import OAuth1
import requests
import pprint
import sys

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
		for x in timeline:
			True
		print x.keys()

		if version in version_list:
			if(version=="master"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/twitter-timeline/static/twitter-timeline.html", "r")
			elif(version=="latency"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/twitter-timeline/static/twitter-timeline.html", "r")
			elif(version=="accuracy"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/twitter-timeline/static/twitter-timeline.html", "r")



	elif social_network == 'facebook':

		access_token="EAANMUmJPs2UBAMA7fAnfIcVd2lWTlDTVVPn625MYduZBxlxR2ggMEmD5ba0RllQ9jAMRYWy2evhUkRfeIGDLWZAfJq98DVaXYcN0MvhLsudaUdLi3LpBFZC8m84NLtyMfZAo0JDJt5VbAFg7xV0Sopo3AZA9cZCAx6YazmhcnGjAZDZD"
		facebook_url = "https://graph.facebook.com/v2.3/me?fields=home&pretty=1&access_token=" + access_token
		s= requests.get(facebook_url)
		muro=s.json()

		if version in version_list:
			if(version=="master"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/facebook-wall/facebook-wall.html","r")
			elif(version=="latency"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/facebook-wall/facebook-wall.html","r")
			elif(version=="accuracy"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/facebook-wall/facebook-wall.html","r")


	elif social_network == 'github':

		github_url = "https://api.github.com/users/mortega5/received_events?per_page=50"
		peticion= requests.get(github_url)
		muro_git=peticion.json()

		if version in version_list:
			if(version=="master"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/github-events/github-events.html","r")
			elif(version=="latency"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/github-events/github-events.html","r")
			elif(version=="accuracy"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/github-events/github-events.html","r")

	elif social_network == 'googleplus':

		access_token="ya29.CjluA4DscVkoppxgwGiWdK87q8Wf0E3YMG14VsSfEsxHhhltQj94NFC1ATbX0kkBXYQQxcEp3Pgqkak"
		google_url_followers="https://www.googleapis.com/plus/v1/people/me/people/visible"
		headers = {"Authorization": "Bearer " + access_token}

		s= requests.get(google_url_followers,headers=headers)
		muro_google=s.json()

		if version in version_list:
			if(version=="master"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Master/googleplus-timeline/googleplus-timeline.html","r")
			elif(version=="latency"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Latency/googleplus-timeline/googleplus-timeline.html","r")
			elif(version=="accuracy"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Accuracy/googleplus-timeline/googleplus-timeline.html","r")


text=fichero.read()
