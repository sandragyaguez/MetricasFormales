#!/bin/bash 

##############################################################################################################
#--------------------------------------------PRUEBAS DE REFRESCO----------------------------------------------
##############################################################################################################

python -m SimpleHTTPServer >> /dev/null &
PID=`echo $!`

#---------#
#TWITTER
#---------#

# Ejecutamos scripts para medir y recolectar los datos
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente twitter-timeline: metrica refresco version master"
# python refresco_final.py twitter master
# sleep 10
# # killall chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente twitter-timeline: metrica refresco version latency"
# python refresco_final.py twitter latency
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente twitter-timeline: metrica refresco version accuracy"
# python refresco_final.py twitter accuracy
# sleep 10
# # pkill chrome


#---------#
#FACEBOOK
#---------#

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente facebook-wall: metrica refresco version master"
# python refresco_final.py facebook master
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente facebook-wall: metrica refresco version latency"
# python refresco_final.py facebook latency
# sleep 10
# pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente facebook-wall: metrica refresco version accuracy"
# python refresco_final.py facebook accuracy
# sleep 10
# pkill chrome


#---------#
#PINTEREST
#---------#

# Ejecutamos scripts para medir y recolectar los datos
echo "##################################################################"
echo "Realizando pruebas sobre el componente pinterest-timeline: metrica refresco version master"
python refresco_final.py pinterest master
sleep 10
# killall chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente pinterest-timeline: metrica refresco version latency"
python refresco_final.py pinterest latency
sleep 10
# pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente pinterest-timeline: metrica refresco version accuracy"
# python refresco_final.py pinterest accuracy
# sleep 10
# pkill chrome

#---------#
#TRAFFIC
#---------#

# Ejecutamos scripts para medir y recolectar los datos
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente traffic-incidents: metrica refresco version master"
# python refresco_final.py traffic-incidents master
# sleep 10
# # killall chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente traffic-incidents: metrica refresco version latency"
# python refresco_final.py traffic-incidents latency
# sleep 10
# pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente traffic-incidents: metrica refresco version accuracy"
# python refresco_final.py traffic-incidents accuracy
# sleep 10
# pkill chrome

#---------#
#WEATHER
#---------#

# Ejecutamos scripts para medir y recolectar los datos
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente open-weather: metrica refresco version master"
# python refresco_final.py open-weather master
# sleep 10
# # killall chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente open-weather: metrica refresco version latency"
# python refresco_final.py open-weather latency
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente open-weather: metrica refresco version accuracy"
# python refresco_final.py open-weather accuracy
# sleep 10
# pkill chrome


#---------#
# STOCK
#---------#

# Ejecutamos scripts para medir y recolectar los datos
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente finance-search: metrica refresco version master"
# python refresco_final.py finance-search master
# sleep 10
# # killall chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente finance-search: metrica refresco version latency"
# python refresco_final.py finance-search latency
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente finance-search: metrica refresco version accuracy"
# python refresco_final.py finance-search accuracy
# sleep 10
# pkill chrome

#---------#
#GOOGLEPLUS
#---------#

# Ejecutamos scripts para medir y recolectar los datos
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente googleplus: metrica refresco version master"
# python refresco_final.py googleplus master
# sleep 10
# # killall chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente googleplus: metrica refresco version latency"
# python refresco_final.py googleplus latency
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente googleplus: metrica refresco version accuracy"
# python refresco_final.py googleplus accuracy
# sleep 10
# pkill chrome

kill -9 $PID
echo "##################################################################"
echo "##################################################################"
echo "Valores calculados para la metrica de refresco"