#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import sys
import httplib
import urllib
import json
import webbrowser
import mixpanel
from mixpanel_client import MixpanelQueryClient
from mixpanel import Mixpanel
import time
mp = Mixpanel("53da31965c3d047fa72de756aae43db1")
# Instantiates the Query Client
query_client = MixpanelQueryClient('582d4b303bf22dd746b5bb1b9acbff63', '8b2d351133ac2a5d4df0700afc595fb6')

def replicate_googleplus_requests(access_token, experiment_id, experiment_list):
	google_requests = {}
	# Endpoint where it is deployed the different versions of twitter-timeline (with the script tracker that sends events to Mixpanel!)
	remote_base_url = "TWITTER_ENDPOINT"
	for key, experiment in experiment_list.iteritems():
		google_url = experiment['request']
		print ">>> Endpoint: " + google_url
		if experiment['requestCount'] >= 2:
			options_requestTime = 0
			# Si replicamos un experimento cliente en el que se han realizado dos llamadas,
			# haremos primero una petición de tipo OPTIONS y luego una de tipo GET
			# if experiment['requestCount'] == 2:
			# 	# Hacemos una petición options
			# 	req = urllib2.Request(google_url)
			# 	req.add_header('authorization', 'Bearer ' + access_token)
			# 	req.get_method = lambda: 'OPTIONS'
			# 	# We set the start time
			# 	startTime = time.time()
			# 	data = urllib2.urlopen(req)
			# 	# We set end time
			# 	endTime = time.time()
				
			# 	# Mandamos los tiempos recogidos a Mixpanel de la petición realizada desde el host
			# 	options_requestTime = (endTime - startTime)*1000

			# Hacemos una petición GET
			req = urllib2.Request(google_url)
			req.add_header('authorization', 'Bearer ' + access_token)
			# We set the start time
			startTime = time.time()
			data = urllib2.urlopen(req)
			# We set end time
			endTime = time.time()
			get_requestTime =  (endTime - startTime)*1000
			# Calculamos el tiempo total
			total_request_time = options_requestTime + get_requestTime 
			requestCount = 2 if not options_requestTime == 0 else 1
			print ">>> Request time: ", total_request_time
			print ">>> Request count: ", requestCount
			
			# Mandamos el evento a mixpanel		
			mp.track("1111", 'latencyMetric', {
			    'component': 'googleplus-timeline',
			    'version': 'host',
			    'requestDuration': total_request_time,
			    'experiment_id': experiment_id,
				'request': google_url,
				'requestCount': requestCount,
				'event_id': experiment_id + google_url
			})


# Url para obtener nuevo token de facebook: https://developers.facebook.com/tools/explorer/145634995501895/
def main():
	network_list = ["instagram", "facebook", "github", "googleplus", "twitter"]
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
			    'experiment_id': experiment_id,
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
			    'experiment_id': experiment_id,
			    'request': github_url
			})
			# Lanzamos una pestaña por cada versión del componente
			webbrowser.open_new("http://metricas-formales.appspot.com/app/latency_metric/Stable/GithubEventsLatency.html?experiment="+ experiment_id)
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
			    'component': 'facebooks-wall',
			    'version': 'host',
			    'requestDuration': requestTime,
			    'experiment_id': experiment_id,
			    'request': facebook_url
			})
			# Lanzamos una pestaña por cada versión del componente (El componente de Facebook tiene solo una version implementada)
			webbrowser.open_new(server_base_url + "/Stable/FacebookWallLatency.html?experiment="+ experiment_id +
			 "&facebook_token=" + access_token)

		elif social_network == 'twitter':
			#twitter_url = "http://metricas-formales.appspot.com/oauth/twitter"
			twitter_url = "http://metricas-formales.appspot.com/oauth/twitter"
			data = {'access_token': "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf",
          			'secret_token': "OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock",
          			'consumer_key': "J4bjMZmJ6hh7r0wlG9H90cgEe",
          			'consumer_secret': "8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf",
          			'count': 200 }

			url_values = urllib.urlencode(data)	
			full_url = twitter_url + '?' + url_values
			print full_url

			# We measure the request/response latency from host
			req = urllib2.Request(full_url) #ana aqui tenia puesta la peticion a twitter_url sin pasarle los parametros
			# We set the start time
			startTime = time.time()
			data = urllib2.urlopen(req)
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
			webbrowser.open_new("http://metricas-formales.appspot.com/app/latency_metric/Stable/TwitterTimelineLatency.html?experiment="+ experiment_id)
			time.sleep(10)
			webbrowser.open_new("http://metricas-formales.appspot.com/app/latency_metric/Latency/TwitterTimelineLatency.html?experiment="+ experiment_id)
			time.sleep(10)
			webbrowser.open_new("http://metricas-formales.appspot.com/app/latency_metric/Accuracy/TwitterTimelineLatency.html?experiment="+ experiment_id)
			

		elif social_network == 'googleplus' and len(sys.argv) >= 3:
			access_token = sys.argv[2]
			# We open a window for each component version
			webbrowser.open_new(server_base_url + "/Stable/GoogleplusLatency.html?experiment=" + experiment_id)
			time.sleep(10)
			webbrowser.open_new(server_base_url + "/Accuracy/GoogleplusLatency.html?experiment=" + experiment_id)
			time.sleep(10)
			webbrowser.open_new(server_base_url + "/Latency/GoogleplusLatency.html?experiment=" + experiment_id)
		
			# First, we obtain data generated today from stable versions
			query = 'properties["experiment_id"]==\"' + experiment_id + '\" and properties["version"]=="stable" and properties["component"]=="googleplus-timeline"'
			experiment_dict = query_client.get_export(time.strftime("%Y-%m-%d"), time.strftime("%Y-%m-%d"), "latencyMetric", where=query, result_key='request')

			# We replicate the request done from the client side and send the request times to Mixpanel
			replicate_googleplus_requests(access_token, experiment_id, experiment_dict)
	
	else:
		print "Wrong social network or missing param"
		# {}: Obligatorio, []: opcional
		print "Usage: measureLatency.py {facebook|instagram|github|googleplus|twitter} [googleplus_access_token|facebook_access_token]"
if __name__ == "__main__":
	main()
