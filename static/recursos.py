


from requests_oauthlib import OAuth1
import requests



#Las credenciales no cambian, a no ser que se quieran hacer peticiones con un usuarios que no sea Deus
CONSUMER_KEY = 'J4bjMZmJ6hh7r0wlG9H90cgEe' #Consumer key
CONSUMER_SECRET = '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf' #Consumer secret
ACCESS_KEY = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf' #Access token
ACCESS_SECRET = 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock'   #Access token secret


oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=ACCESS_KEY,resource_owner_secret=ACCESS_SECRET)
request_usertimeline="https://api.twitter.com/1.1/statuses/user_timeline.json"


s= requests.get(request_usertimeline, auth=oauth)
timeline=s.json()
print timeline[0]