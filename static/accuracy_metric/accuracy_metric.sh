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
python accuracy_metric.py twitter master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version accuracy"
python accuracy_metric.py twitter accuracy
sleep 10

#---------#
#FACEBOOK
#---------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente facebook-wall: metrica completitud version master"
python accuracy_metric.py facebook master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente facebook-wall: metrica completitud version accuracy"
python accuracy_metric.py facebook accuracy
sleep 10


#---------#
#GOOGLE+
#---------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente googleplus-timeline: metrica completitud version master"
python accuracy_metric.py googleplus master
sleep 10
# pkill chrome

echo "##################################################################"
echo "Realizando pruebas sobre el componente googleplus-timeline: metrica completitud version accuracy"
python accuracy_metric.py googleplus accuracy
sleep 10

#-------#
#PINTEREST
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente pinterest-timeline: metrica completitud version master"
python accuracy_metric.py pinterest master
sleep 10


echo "##################################################################"
echo "Realizando pruebas sobre el componente pinterest-timeline: metrica completitud version accuracy"
python accuracy_metric.py pinterest accuracy
sleep 10

#-------#
#FINANCE
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente finance-search: metrica completitud version master"
python accuracy_metric.py finance-search master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente finance-search: metrica completitud version accuracy"
python accuracy_metric.py finance-search accuracy
sleep 10

#-------#
#WEATHER
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente open-weather: metrica completitud version master"
python accuracy_metric.py open-weather master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente open-weather: metrica completitud version accuracy"
python accuracy_metric.py open-weather accuracy
sleep 10

#-------#
#TRAFFIC
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente traffic-incidents: metrica completitud version master"
python accuracy_metric.py traffic-incidents master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente traffic-incidents: metrica completitud version accuracy"
python accuracy_metric.py traffic-incidents accuracy
sleep 10

#-------#
#REDDIT
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente reddit: metrica completitud version master"
python accuracy_metric.py reddit master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente reddit: metrica completitud version accuracy"
python accuracy_metric.py reddit accuracy
sleep 10

#-------#
#SPOTIFY
#-------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente spotify: metrica completitud version master"
python accuracy_metric.py spotify master
sleep 10

echo "##################################################################"
echo "Realizando pruebas sobre el componente spotify: metrica completitud version accuracy"
python accuracy_metric.py spotify accuracy
sleep 10

kill -9 $PID
echo "##################################################################"
echo "##################################################################"
echo "Valores calculados para la metrica de completitud"
