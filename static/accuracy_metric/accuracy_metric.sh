#!/bin/bash 


##############################################################################################################
#-----------------------------------------PRUEBAS DE COMPLETITUD----------------------------------------------
##############################################################################################################

python -m SimpleHTTPServer >> /dev/null &
PID=`echo $!`

# Ejecutamos scripts para medir y recolectar los datos

#---------#
#TWITTER
#---------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version master"
python completitud_final.py twitter master
sleep 10
# pkill chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version accuracy"
python completitud_final.py twitter accuracy
sleep 10

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version latency"
# python completitud_final.py twitter latency
# sleep 10
# pkill chrome

#---------#
#GITHUB
#---------#

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente github-events: metrica completitud version master"
# python completitud.py github master
# sleep 10
# pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente github-events: metrica completitud version latency"
# python completitud.py github latency
# sleep 10
# pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente github-events: metrica completitud version accuracy"
# python completitud.py github accuracy
# sleep 10
# pkill chrome


#---------#
#INSTAGRAM
#---------#

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version master"
# python completitud.py instagram master
# sleep 10
# pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version latency"
# python completitud.py instagram latency
# sleep 10
# pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version accuracy"
# python completitud.py instagram accuracy
# sleep 10
# pkill chrome


#---------#
#FACEBOOK
#---------#

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente facebook-wall: metrica completitud version master"
# python completitud_final.py facebook master
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente facebook-wall: metrica completitud version accuracy"
# python completitud_final.py facebook accuracy
# sleep 10

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente facebook-wall: metrica completitud version latency"
# python completitud_final.py facebook latency
# sleep 10
# pkill chrome


#---------#
#GOOGLE+
#---------#

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente googleplus-timeline: metrica completitud version master"
# python completitud_final.py googleplus master
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente googleplus-timeline: metrica completitud version accuracy"
# python completitud_final.py googleplus accuracy
# sleep 10

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente googleplus-timeline: metrica completitud version latency"
# python completitud_final.py googleplus latency
# sleep 10
# pkill chrome

#-------#
# PINTEREST
#-------#

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente pinterest-timeline: metrica completitud version master"
# python completitud_final.py pinterest master
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente pinterest-timeline: metrica completitud version accuracy"
# python completitud_final.py pinterest accuracy
# sleep 10

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente pinterest-timeline: metrica completitud version latency"
# python completitud_final.py pinterest latency
# sleep 10
# # pkill chrome


##############################
########### STOCK ############
##############################

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente finance-search: metrica completitud version master"
# python completitud_final.py finance-search master
# sleep 10
# # pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente finance-search: metrica completitud version accuracy"
# python completitud_final.py finance-search accuracy
# sleep 10
# pkill chrome

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente finance-search: metrica completitud version latency"
# python completitud_final.py finance-search latency
# sleep 10
# pkill chrome


#############################
######## WEATHER ############
#############################

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente open-weather: metrica completitud version master"
# python completitud_final.py open-weather master
# sleep 10

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente open-weather: metrica completitud version accuracy"
# python completitud_final.py open-weather accuracy
# sleep 10

#############################
######## TRAFFIC ############
#############################

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente traffic-incidents: metrica completitud version master"
# python completitud_final.py traffic-incidents master
# sleep 10

# echo "##################################################################"
# echo "Realizando pruebas sobre el componente traffic-incidents: metrica completitud version accuracy"
# python completitud_final.py traffic-incidents accuracy
# sleep 10

kill -9 $PID
echo "##################################################################"
echo "##################################################################"
echo "Valores calculados para la metrica de completitud"
