#!/usr/bin/env python
#!/usr/bin/python

import sys
import os
import yaml

path = os.path.dirname(os.path.abspath(__file__))

#Accedemos a todos los datos mediante el fichero yaml de configuracion
output_file2 = os.path.join(path, "configUptime.yaml") 
configFile = open(output_file2,"r")
yaml_config = yaml.load(configFile)

print "Los porcentajes de uptime de las siguientes APIs son:\n"

def calcular_porcentaje(files):
    lineas_totales = 0
    lineas_correctas = 0
    for line in files:
        if line[0:3] == "200":
            lineas_correctas += 1
        lineas_totales += 1
    porcentaje = lineas_correctas / float(lineas_totales) * 100
    return round(porcentaje,2)

#Acceso al fichero con el uptime de cada API
file_Twitter = open(os.path.join(path,yaml_config['file_data_Twitter']), "r")
file_Facebook = open(os.path.join(path,yaml_config['file_data_Facebook']), "r")
file_Pinterest = open(os.path.join(path,yaml_config['file_data_Pinterest']), "r")
file_Traffic = open(os.path.join(path,yaml_config['file_data_Traffic']), "r")
file_Weather = open(os.path.join(path,yaml_config['file_data_Weather']), "r")
file_Reddit = open(os.path.join(path,yaml_config['file_data_Reddit']), "r")
file_Spotify = open(os.path.join(path,yaml_config['file_data_Spotify']), "r")
file_Google = open(os.path.join(path,yaml_config['file_data_Google']), "r")
file_Finance = open(os.path.join(path,yaml_config['file_data_Finance']), "r")

print "\t-Twitter:     " + str(calcular_porcentaje(file_Twitter)) + "%"
print "\t-Facebook:    " + str(calcular_porcentaje(file_Facebook)) + "%"
print "\t-Pinterest:   " + str(calcular_porcentaje(file_Pinterest)) + "%"
print "\t-Traffic:     " + str(calcular_porcentaje(file_Traffic)) + "%"
print "\t-Weather:     " + str(calcular_porcentaje(file_Weather)) + "%"
print "\t-Reddit:      " + str(calcular_porcentaje(file_Reddit)) + "%"
print "\t-Spotify:     " + str(calcular_porcentaje(file_Spotify)) + "%"
print "\t-Google plus: " + str(calcular_porcentaje(file_Google)) + "%"
print "\t-Finance:     " + str(calcular_porcentaje(file_Finance)) + "%"