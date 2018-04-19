#!/bin/bash 

##############################################################################################################
#-----------------------------------------PRUEBAS DE REFRESCO----------------------------------------------
##############################################################################################################

python -m SimpleHTTPServer >> /dev/null &
PID=`echo $!`

# Ejecutamos scripts para medir y recolectar los datos

#---------#
#TWITTER
#---------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica refresco version master"
python refresh_metric.py twitter master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica refresco version latency"
python refresh_metric.py twitter latency
sleep 10

#---------#
#FACEBOOK
#---------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente facebook-wall: metrica refresco version master"
python refresh_metric.py facebook master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente facebook-wall: metrica refresco version latency"
python refresh_metric.py facebook latency
sleep 10


#---------#
#GOOGLE+
#---------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente googleplus-timeline: metrica refresco version master"
python refresh_metric.py googleplus master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente googleplus-timeline: metrica refresco version latency"
python refresh_metric.py googleplus latency
sleep 10

#-------#
#PINTEREST
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente pinterest-timeline: metrica refresco version master"
python refresh_metric.py pinterest master
sleep 10


echo "##################################################################"
echo "Realizando pruebas sobre el componente pinterest-timeline: metrica refresco version latency"
python refresh_metric.py pinterest latency
sleep 10

#-------#
#FINANCE
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente finance-search: metrica refresco version master"
python refresh_metric.py finance-search master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente finance-search: metrica refresco version latency"
python refresh_metric.py finance-search latency
sleep 10

#-------#
#WEATHER
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente open-weather: metrica refresco version master"
python refresh_metric.py open-weather master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente open-weather: metrica refresco version latency"
python refresh_metric.py open-weather latency
sleep 10

#-------#
#TRAFFIC
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente traffic-incidents: metrica refresco version master"
python refresh_metric.py traffic-incidents master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente traffic-incidents: metrica refresco version latency"
python refresh_metric.py traffic-incidents latency
sleep 10

#-------#
#REDDIT
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente reddit: metrica refresco version master"
python refresh_metric.py reddit master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente reddit: metrica refresco version latency"
python refresh_metric.py reddit latency
sleep 10

#-------#
#SPOTIFY
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente spotify: metrica refresco version master"
python refresh_metric.py spotify master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente spotify: metrica refresco version latency"
python refresh_metric.py spotify latency
sleep 10

kill -9 $PID
echo "##################################################################"
echo "##################################################################"
echo "Valores calculados para la metrica de refresco"
