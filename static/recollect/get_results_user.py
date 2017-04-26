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
mp_user = Mixpanel("d3bef513d72a99cc1e8bd3ca133e0f69")
query_client = MixpanelQueryClient("c2c6f5c021a293bf6e850746540a82ed", "cb2011ee8d19c4e6dcf68c1cca1b151a")

# Boundary dates for retrieving data
START_DATE = "2017-04-21"
END_DATE = time.strftime("%Y-%m-%d")

# Query to get data from Mixpanel
resp = query_client.get_export(START_DATE, END_DATE, result_key="timestamp")

for key in resp.keys():
	print resp[key]["user"]
	print resp[key]["component"]
	print resp[key]["version"]
	print resp[key]["timestamp"]
	print resp[key]["question"]
	print "-------------------------------"