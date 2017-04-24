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
mp_maintenance = Mixpanel("c693798b11075795d9e72c784b2d0864") # events sender
query_client = MixpanelQueryClient("eb4d6565391f79168f8b0482528d5eb1", "354211d103b349b2d4c0b138afe25371") # query client

# Boundary dates for retrieving data of maintenance
START_DATE = "2017-04-04"
END_DATE = time.strftime("%Y-%m-%d")

# Query for retrieving the results
resp = query_client.get_export(START_DATE, END_DATE, result_key='component')

# Resp is a dict.
for key in resp.keys():
	# Time to print the important info about the metric
	print "#########################################################"
	print "Componente: " + resp[key]["component"]
	print "Valor de metrica: " + str(resp[key]["maintainability"])
	# print "Id de ejecucion: " + resp[key]["Time"]
	print "#########################################################"