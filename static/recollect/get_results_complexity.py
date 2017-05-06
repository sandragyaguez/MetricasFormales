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
mp_comp = Mixpanel("a31e7a032cce99482d8b407d768f9c04")
query_client = MixpanelQueryClient("3b1ffdd0d5ad8637f954b3a3febaf3f3", "6b789a89178408fa8f0b51e6b2cd93e9")

#Boundary dates for retrieving data
START_DATE = "2017-04-04"
END_DATE = time.strftime("%Y-%m-%d")

# Query to retrieve the results
resp = query_client.get_export(START_DATE, END_DATE, result_key='component')

# Go through the response to print the values
for key in resp.keys():
	print "#########################################################"
	print "Componente: " + resp[key]["component"]
	print "Valor de metrica: " + str(resp[key]["complexity"])
	# print "Id de ejecucion: " + resp[key]["Time"]
	print "#########################################################"