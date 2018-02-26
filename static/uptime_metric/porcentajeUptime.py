#!/usr/bin/env python
#!/usr/bin/python

import sys
import os
import yaml
from pymongo import Connection

path = os.path.dirname(os.path.abspath(__file__))

#Accedemos a todos los datos mediante el fichero yaml de configuracion
output_file2 = os.path.join(path, "configUptime.yaml") 
configFile = open(output_file2,"r")
yaml_config = yaml.load(configFile)

con = Connection('localhost')
db = con.StatusAPIs

print "Los porcentajes de uptime de las siguientes APIs son:\n"

def calcular_porcentaje(collection):
    lineas_totales = 0
    lineas_correctas = 0
    for line in db[collection].find():
        if line['code'] == 200:
            lineas_correctas += 1
        lineas_totales += 1
    porcentaje = lineas_correctas / float(lineas_totales) * 100
    return round(porcentaje,2)

#Acceso al fichero con el uptime de cada API

print "\t-Twitter:     " + str(calcular_porcentaje('Twitter')) + "%"
print "\t-Facebook:    " + str(calcular_porcentaje('Facebook')) + "%"
print "\t-Pinterest:   " + str(calcular_porcentaje('Pinterest')) + "%"
print "\t-Traffic:     " + str(calcular_porcentaje('Traffic')) + "%"
print "\t-Weather:     " + str(calcular_porcentaje('Weather')) + "%"
print "\t-Reddit:      " + str(calcular_porcentaje('Reddit')) + "%"
print "\t-Spotify:     " + str(calcular_porcentaje('Spotify')) + "%"
print "\t-Google plus: " + str(calcular_porcentaje('Google')) + "%"
print "\t-Finance:     " + str(calcular_porcentaje('Finance')) + "%"

con.close()