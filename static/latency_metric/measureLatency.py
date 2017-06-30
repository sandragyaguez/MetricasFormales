#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import sys
import requests
import grequests
import httplib
import urllib
import json
import ssl
import webbrowser
import mixpanel
from mixpanel_client import MixpanelQueryClient
from mixpanel import Mixpanel
import time
import base64

mp = Mixpanel("53da31965c3d047fa72de756aae43db1")
# Instantiates the Query Client
query_client = MixpanelQueryClient('582d4b303bf22dd746b5bb1b9acbff63', '8b2d351133ac2a5d4df0700afc595fb6')
CLIENT_ID_REDDIT = "RxkV7Oo-8Zid5Q"
CLIENT_SECRECT_REDDIT = "eF-kiWrj12VmIV62m-NR4YiZgJ8"
REFRESH_TOKEN_REDDIT = "65263530-S9mkAkp7M4pGHhxFPRs30qOY3fo"
def replicate_googleplus_requests(access_token, experiment_id):
	google_requests = {}
	# Endpoint where it is deployed the different versions of twitter-timeline (with the script tracker that sends events to Mixpanel!)
	# remote_base_url = "TWITTER_ENDPOINT"
	total_time = 0
	people_url = "https://people.googleapis.com/v1/people/me/connections"
	people_data = {"key":"AIzaSyAArT6pflqm1-rj9Nwppuj_4z15FFh4Kis", "access_token":access_token}
	people_data = urllib.urlencode(people_data)
	people_url += "?" + people_data

	resp = requests.get(people_url)
	time_req = resp.elapsed.total_seconds()*1000
	response = resp.json()
	print "Peticion %s: %f" % (people_url, time_req)

	total_time += time_req

	async_requests = []
	request_iniciated = []
	callback_captured = 0
	for user in response['connections']:
		if user.has_key('urls'):
			user_id = user['urls'][0]['metadata']['source']['id']
			url = "https://www.googleapis.com/plus/v1/people/" + user_id + "/activities/public"
			startTime = time.time()
			async_requests.append(grequests.get(url))
			request_iniciated.append(startTime)
	responses = grequests.map(async_requests)
	timesCalculated = [resp.elapsed.total_seconds()*1000 for resp in responses]
	total_time += reduce((lambda x, y: x+y), timesCalculated)
	async_time = ((max(timesCalculated)+request_iniciated[-1]) - request_iniciated[0])
	print "Tiempo sumado: %f" % total_time
	print "Tiempo asincrono: %f" % async_time
	mp.track("1111", 'latencyMetric', {
			'component': 'googleplus-timeline',
			'version': 'host',
			'requestDuration': async_time,
			'experiment_id': experiment_id,
		'request': google_url,
		'requestCount': requestCount,
		'event_id': experiment_id + google_url
	})
# Url para obtener nuevo token de facebook: https://developers.facebook.com/tools/explorer/145634995501895/
def main():
	network_list = ["instagram", "facebook", "github", "googleplus", "twitter", "pinterest", "traffic", "finance", "weather", "reddit"]
	server_base_url = "http://localhost:8000"
	if len(sys.argv) >= 2:
		social_network = sys.argv[1]
	else:
		social_network = ''

	if social_network in network_list:
		# We set the experiment id
		experiment_id = str(time.time())
		if social_network == 'instagram':
			# Medimos la latencia desde el host
			data = {}
			data['access_token'] = '2062815740.34af286.169a9c42e1404ae58591d066c00cb979'
			url_values = urllib.urlencode(data)	
			instagram_url = 'http://instagram-timeline.appspot.com/request/instagram'
			full_url = instagram_url + '?' + url_values
			
			req = urllib2.Request(full_url)
			# We set the start time
			startTime = time.time()
			data = urllib2.urlopen(req)
			# We set end time
			endTime = time.time()

			# Mandamos los tiempos recogidos a Mixpanel de la petición realizada desde el host
			requestTime = (endTime - startTime)*1000
			print "Request time ", requestTime

			mp.track("1111", 'latencyMetric', {
			    'component': 'instagram-timeline',
			    'version': 'host',
			    'requestDuration': requestTime,
			    'experiment': experiment_id,
			    'request': full_url
			})

			# Lanzamos una pestaña por cada versión del componente
			webbrowser.open_new(server_base_url + "/Stable/InstagramLatency.html?experiment="+ experiment_id)
			time.sleep(10)
			webbrowser.open_new(server_base_url + "/Accuracy/InstagramLatency.html?experiment="+ experiment_id)
			time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/InstagramLatency.html?experiment="+ experiment_id)
		
		elif social_network == 'github':
			# Medimos la latencia desde el host
			github_url = "https://api.github.com/users/polymer-spain/received_events"

			req = urllib2.Request(github_url)
			# We set the start time
			startTime = time.time()
			data = urllib2.urlopen(req)
			# We set end time
			endTime = time.time()

			# Mandamos los tiempos recogidos a Mixpanel de la petición realizada desde el host
			requestTime = (endTime - startTime)*1000
			print "Request time ", requestTime

			mp.track("1111", 'latencyMetric', {
			    'component': 'github-events',
			    'version': 'host',
			    'requestDuration': requestTime,
			    'experiment': experiment_id,
			    'request': github_url
			})
			# Lanzamos una pestaña por cada versión del componente
			webbrowser.open_new(server_base_url + "/Stable/GithubEventsLatency.html?experiment="+ experiment_id)
			time.sleep(10)
			webbrowser.open_new(server_base_url + "/Accuracy/GithubEventsLatency.html?experiment="+ experiment_id)
			time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/GithubEventsLatency.html?experiment="+ experiment_id)

		elif social_network == 'facebook' and len(sys.argv) >= 3:
			access_token = sys.argv[2]
			facebook_url = "https://graph.facebook.com/v2.3/me?fields=home&pretty=1&access_token=" + access_token
			# We measure the request/response latency from host

			req = urllib2.Request(facebook_url)
			# We set the start time
			startTime = time.time()
			data = urllib2.urlopen(req)
			# We set end time
			endTime = time.time()

			# Mandamos los tiempos recogidos a Mixpanel de la petición realizada desde el host
			requestTime = (endTime - startTime)*1000
			print "Request time ", requestTime

			mp.track("1111", 'latencyMetric', {
			    'component': 'facebook-wall',
			    'version': 'host',
			    'requestDuration': requestTime,
			    'experiment': experiment_id,
			    'request': facebook_url
			})
			# Lanzamos una pestaña por cada versión del componente (El componente de Facebook tiene solo una version implementada)
			webbrowser.open_new(server_base_url + "/Stable/FacebookWallLatency.html?experiment="+ experiment_id +
			 "&facebook_token=" + access_token)
			time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/FacebookWallLatency.html?experiment="+ experiment_id +
			 "&facebook_token=" + access_token)
			# time.sleep(10)
			# webbrowser.open_new(server_base_url + "/Accuracy/FacebookWallLatency.html?experiment="+ experiment_id +
			#  "&facebook_token=" + access_token)


		elif social_network == 'twitter':
			#twitter_url = "http://metricas-formales.appspot.com/oauth/twitter"
			twitter_url = "https://centauro.ls.fi.upm.es/api/aux/twitterTimeline"
			data = {'access_token': "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf",
          			'secret_token': "OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock",
          			'consumer_key': "BOySBn8XHlyYDQiGiqZ1tzllx",
          			'consumer_secret': "xeSw5utUJmNOt5vdZZy8cllLegg91vqlzRitJEMt5zT7DtRcHE",
          			'count': 200 }

			url_values = urllib.urlencode(data)	
			full_url = twitter_url + '?' + url_values
			print full_url

			# We measure the request/response latency from host
			req = urllib2.Request(full_url) #ana aqui tenia puesta la peticion a twitter_url sin pasarle los parametros
			context = ssl._create_unverified_context()
			# We set the start time
			startTime = time.time()
			data = urllib2.urlopen(req, context=context)
			# We set end time
			endTime = time.time()
			response = data.read()
			print "respuesta aqui"

			# Mandamos los tiempos recogidos a Mixpanel de la petición realizada desde el host
			requestTime = (endTime - startTime)*1000
			print "Request time ", requestTime

			mp.track("1111", 'latencyMetric', {
			    'component': 'twitter-timeline',
			    'version': 'host',
			    'requestDuration': requestTime,
				'experiment': experiment_id,
				'request': twitter_url
			})

			#We open a window for each component version
			webbrowser.open_new(server_base_url + "/Stable/TwitterTimelineLatency.html?experiment="+ experiment_id)
			time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/TwitterTimelineLatency.html?experiment="+ experiment_id)
			# time.sleep(10)
			# webbrowser.open_new(server_base_url + "/Accuracy/TwitterTimelineLatency.html?experiment="+ experiment_id)
			

		elif social_network == 'googleplus' and len(sys.argv) >= 3:
			access_token = sys.argv[2]
			# We open a window for each component version
			webbrowser.open_new(server_base_url + "/Stable/GoogleplusLatency.html?experiment=" + experiment_id)
			time.sleep(10)
			# webbrowser.open_new(server_base_url + "/Accuracy/GoogleplusLatency.html?experiment=" + experiment_id)
			# time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/GoogleplusLatency.html?experiment=" + experiment_id)
		
			# First, we obtain data generated today from stable versions

			# We replicate the request done from the client side and send the request times to Mixpanel
			replicate_googleplus_requests(access_token, experiment_id)

		elif social_network == 'pinterest':
			board_names = []
			req_limit = 60
			access_token = "AdCKtwyMSg_tKhDOvhzQ-25yrkSHFJKOjZfO6N9DaxDMLKAvZgAAAAA"
			user_url = "https://api.pinterest.com/v1/me/"
			userboards_url = "https://api.pinterest.com/v1/me/boards/"
			followingboards_url = "https://api.pinterest.com/v1/me/following/boards/"
			# Here we have to wait until having the user_id and the boards_id retrieved
			# pins:
			# url="https://api.pinterest.com/v1/boards/{{username}}/{{board}}/pins/"
			pins_url = ""
			user_data = {"access_token": access_token,
						"fields": "id, username, first_name, image"}
			user_url_values = urllib.urlencode(user_data)
			user_url_complete = user_url + '?' + user_url_values
			# We measure the request/response latency from host
			req = urllib2.Request(user_url_complete) 
			# We set the start time
			startTime = time.time()
			data = urllib2.urlopen(req)
			# We set end time
			endTime = time.time()
			time1 = (endTime - startTime)*1000
			print "Peticion %s: %f" % (user_url_complete, time1)
			response = data.read()
			resp = json.loads(response)

			username = resp["data"]["username"] # First parameter for pins request

			userboards_data = {"access_token": access_token}
			userboards_values = urllib.urlencode(userboards_data)
			userboards_url_complete = userboards_url + '?' + userboards_values
			# We are going to take measure of start and end of the request
			req2 = urllib2.Request(userboards_url_complete)
			# We set the start of the measure
			startTime = time.time()
			data = urllib2.urlopen(req2)
			# We stop measuring
			endTime = time.time()
			time2 = (endTime - startTime) * 1000
			print "Peticion %s: %f" % (userboards_url_complete, time2)
			response = data.read()
			resp = json.loads(response)

			# Now, we need to collect the names of the created boards 
			for board in resp["data"]:
				url = board["url"]
				splited_url = url.split("/")
				dict_data = {"username": splited_url[3],
							"board": splited_url[4]}
				board_names.append(dict_data)

			# Now, we make the third request, to see the boards followed by the user
			followingboards_url_complete = followingboards_url + '?' + userboards_values

			req3 = urllib2.Request(followingboards_url_complete)
			# Start the measure of time
			startTime = time.time()
			data = urllib2.urlopen(req3)
			endTime = time.time()
			# We obtain the value for this request
			time3 = (endTime - startTime) * 1000
			print "Peticion %s: %f" % (followingboards_url_complete, time3)
			response = data.read()
			resp = json.loads(response)

			# Now, we need to collect the names of the created boards 
			for board in resp["data"]:
				url = board["url"]
				splited_url = url.split("/")
				dict_data = {"username": splited_url[3],
							"board": splited_url[4]}
				board_names.append(dict_data)

			# The fourth request needs two query params: username and board name
			# Due to this, the url is composed for each request with these parameters
			pins_data = {"access_token": access_token,
						"fields": "id, url, image",
						"limit": req_limit}
			pins_values = urllib.urlencode(pins_data)
			time_pins = 0
			for obj in board_names:
				pin_url_complete = "https://api.pinterest.com/v1/boards/" + obj["username"] + "/" + obj["board"] + "/pins/?" + pins_values
				req4 = urllib2.Request(pin_url_complete)
				startTime = time.time()
				data = urllib2.urlopen(req4)
				endTime = time.time()
				print "Peticion %s: %f" % (pin_url_complete, (endTime - startTime) * 1000)
				response = data.read()

				time_pins += (endTime - startTime) * 1000
			total_request_time = time1 + time2 + time3 + time_pins
			print "Tiempo total: %f" % (total_request_time)
			mp.track("1111", 'latencyMetric', {
			    'component': 'pinterest-timeline',
			    'version': 'host',
			    'requestDuration': total_request_time,
			    'experiment': experiment_id,
			    'request': "All requests"
			})

			# We open a window for each component version
			webbrowser.open_new(server_base_url + "/Stable/PinterestTimelineLatency.html?experiment=" + experiment_id)
			time.sleep(10)
			# webbrowser.open_new(server_base_url + "/Accuracy/PinterestTimelineLatency.html?experiment=" + experiment_id)
			# time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/PinterestTimelineLatency.html?experiment=" + experiment_id)

		elif social_network == 'finance':
			# symbol = "Alphabet Inc."
			finance_url = "https://centauro.ls.fi.upm.es:4444/stock"
			finance_data = {"q": "select * from yahoo.finance.quote where symbol in (\'GOOGL\')"} 
			finance_values = urllib.urlencode(finance_data)
			finance_url_complete = finance_url + '?' + finance_values

			req = urllib2.Request(finance_url_complete)
			context = ssl._create_unverified_context()
			startTime = time.time()
			data = urllib2.urlopen(req, context=context)
			endTime = time.time()
			response = data.read()

			# We calculate the time of the made request
			time_req = (endTime - startTime) * 1000

			mp.track("1111", 'latencyMetric', {
				'component': 'finance-search',
				'version': 'host',
				'requestDuration': time_req,
				'experiment': experiment_id,
				'request': "All requests"
			})

			# We open a window for each component version
			webbrowser.open_new(server_base_url + "/Stable/FinanceSearchLatency.html?experiment=" + experiment_id)
			time.sleep(10)
			# webbrowser.open_new(server_base_url + "/Accuracy/FinanceSearchLatency.html?experiment=" + experiment_id)
			# time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/FinanceSearchLatency.html?experiment=" + experiment_id)

		elif social_network == 'weather':
			weather_url = "https://centauro.ls.fi.upm.es:4444/weather"
			weather_data = {"lat": "40.4893538421231",
							"lon": "-3.6827461557",
							"units": "metric",
							"lang": "es",
							"appId": "655f716c02b3f0aceac9e3567cfb46a8"}
			weather_values = urllib.urlencode(weather_data)
			weather_url_complete = weather_url + '?' + weather_values

			req = urllib2.Request(weather_url_complete)
			context = ssl._create_unverified_context()
			startTime = time.time()
			data = urllib2.urlopen(req, context=context)
			endTime = time.time()
			response = data.read()

			time_req = (endTime - startTime) * 1000

			mp.track("1111", 'latencyMetric', {
				'component': 'open-weather',
				'version': 'host',
				'requestDuration': time_req,
				'experiment': experiment_id,
				'request': "All requests"
				})

			# We open a window for each component version
			webbrowser.open_new(server_base_url + "/Stable/OpenWeatherLatency.html?experiment=" + experiment_id)
			time.sleep(10)
			# webbrowser.open_new(server_base_url + "/Accuracy/OpenWeatherLatency.html?experiment=" + experiment_id)
			# time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/OpenWeatherLatency.html?experiment=" + experiment_id)

		elif social_network == "traffic":
			traffic_url = "https://centauro.ls.fi.upm.es:4444/traffic"
			traffic_data = {"map": "50.6064499990991,-1.028659200900901,52.4082518009009,0.7731426009009009",
							"key": "AmWMG90vJ0J9Sh2XhCp-M3AFOXJWAKqlersRRNvTIS4GyFmd3MxxigC4-l0bdvz-"}
			traffic_values = urllib.urlencode(traffic_data)
			traffic_url_complete = traffic_url + '?' + traffic_values

			req = urllib2.Request(traffic_url_complete)
			context = ssl._create_unverified_context()
			startTime = time.time()
			data = urllib2.urlopen(req, context=context)
			endTime = time.time()
			response = data.read()

			time_req = (endTime - startTime) * 1000

			mp.track("1111", 'latencyMetric', {
				'component': 'traffic-incidents',
				'version': 'host',
				'requestDuration': time_req,
				'experiment_id': experiment_id,
				'request': "All requests"
				})

			# We open a window for each component version
			webbrowser.open_new(server_base_url + "/Stable/TrafficIncidentsLatency.html?experiment=" + experiment_id)
			time.sleep(10)
			# webbrowser.open_new(server_base_url + "/Accuracy/TrafficIncidentsLatency.html?experiment=" + experiment_id)
			# time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/TrafficIncidentsLatency.html?experiment=" + experiment_id)
		elif social_network == "reddit":
			total_time = 0
			reddit_token = "https://www.reddit.com/api/v1/access_token?grant_type=refresh_token&refresh_token=%s" % REFRESH_TOKEN_REDDIT
			rq_token = base64.b64encode("%s:%s" % (CLIENT_ID_REDDIT, CLIENT_SECRECT_REDDIT) )
			# Añadir authorization: Basic 
			headers = {
        "authorization":"Basic " + rq_token,
        "User-agent": "Mozilla/5.0"
      }
			resp = requests.post(reddit_token, headers=headers)
			total_time += resp.elapsed.total_seconds()*1000
			data = resp.json()
			access_token = data['access_token']

			# Añadir authorization: Bearer token_obtenido
			reddit_subscriber = "https://oauth.reddit.com/subreddits/mine/subscriber"
			headers = {
				"authorization":"Bearer %s" % access_token,
				"User-agent": "Mozilla/5.0"
				}

			resp = requests.get(reddit_subscriber, headers=headers)
			total_time += resp.elapsed.total_seconds()*1000
			print resp.text
			resp = resp.json()

			reddit_hot= "https://oauth.reddit.com/r/all/hot"
			req = requests.get(reddit_hot, headers=headers)
			total_time += req.elapsed.total_seconds()*1000
			print "Tiempo sumado: %f" % total_time
			mp.track("1111", 'latencyMetric', {
					'component': 'reddit-timeline',
					'version': 'host',
					'requestDuration': total_time,
					'experiment_id': experiment_id,
					'event_id': experiment_id 
			})
			webbrowser.open_new(server_base_url + "/Stable/RedditTimelineLatency.html?experiment=" + experiment_id)
			time.sleep(10)
			# webbrowser.open_new(server_base_url + "/Accuracy/TrafficIncidentsLatency.html?experiment=" + experiment_id)
			# time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/RedditTimelineLatency.html?experiment=" + experiment_id)
	else:
		print "Wrong social network or missing param"
		# {}: Obligatorio, []: opcional
		print "Usage: measureLatency.py {facebook|instagram|github|googleplus|twitter|pinterest|reddit} [googleplus_access_token|facebook_access_token]"
if __name__ == "__main__":
	main()
