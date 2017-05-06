#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2017 Luis Ruiz Ruiz

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

###############################################################################
#   This script get the results stored in Mixpanel and saves them in a file   #
###############################################################################

# First, we made the necessary imports to run the script
import json, csv, time
import mixpanel
from mixpanel_client import MixpanelQueryClient
from mixpanel import Mixpanel

# We need the tokens for Mixpanel projects to get the results
mp_latency = Mixpanel("53da31965c3d047fa72de756aae43db1") # events sender
query_client = MixpanelQueryClient('582d4b303bf22dd746b5bb1b9acbff63', '8b2d351133ac2a5d4df0700afc595fb6') # query client

# Initial and final date
START_DATE = "2017-04-04"
END_DATE = time.strftime("%Y-%m-%d")

# Query to get data of the all Results events
resp = query_client.get_export(START_DATE, END_DATE, 'latencyResult', result_key='result_id')

# Resp is a dict, access to fields
for key in resp.keys():
	# Time to show the information stored
	print "#########################################################"
	print "Componente: " + resp[key]["component"]
	print "Version evaluada: " + resp[key]["tag"]
	print "Valor de metrica: " + str(resp[key]["latency"])
	print "Id de experimento: " + str(resp[key]["experiment_id"])
	print "#########################################################"
	print "------------------------------------------------------------"