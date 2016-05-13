#!/bin/bash 



##############################################################################################################
#-----------------------------------------PRUEBAS DE COMPLETITUD----------------------------------------------
##############################################################################################################


#---------#
#TWITTER
#---------#

# Ejecutamos scripts para medir y recolectar los datos
echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version master"
python completitud.py twitter master
sleep 10
pkill chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version latency"
python completitud.py twitter latency
sleep 10
pkill chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version accuracy"
python completitud.py twitter accuracy
sleep 10
pkill chrome

#---------#
#GITHUB
#---------#

# Ejecutamos scripts para medir y recolectar los datos
echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica completitud version master"
python completitud.py github master
sleep 10
pkill chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica completitud version latency"
python completitud.py github latency
sleep 10
pkill chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica completitud version accuracy"
python completitud.py github accuracy
sleep 10
pkill chrome


#---------#
#INSTAGRAM
#---------#

# Ejecutamos scripts para medir y recolectar los datos
echo "##################################################################"
echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version master"
python completitud.py instagram master
sleep 10
pkill chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version latency"
python completitud.py instagram latency
sleep 10
pkill chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version accuracy"
python completitud.py instagram accuracy
sleep 10
pkill chrome


echo "##################################################################"
echo "##################################################################"
echo "Valores calculados para la metrica de completitud"