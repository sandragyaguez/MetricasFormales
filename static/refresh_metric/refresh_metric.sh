


##############################################################################################################
#--------------------------------------------PRUEBAS DE REFRESCO----------------------------------------------
##############################################################################################################


#---------#
#TWITTER
#---------#

# Ejecutamos scripts para medir y recolectar los datos
echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica refresco version master"
python refresco.py twitter master


sleep 10
killall chrome
echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica refresco version latency"
python refresco.py twitter latency

sleep 10
pkill chrome
echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica refresco version accuracy"
python refresco.py twitter accuracy
	

#---------#
#FACEBOOK
#---------#

echo "##################################################################"
echo "Realizando pruebas sobre el componente facebook-wall: metrica refresco version master"
python refresco.py facebook master


#---------#
#GITHUB
#---------#

# Ejecutamos scripts para medir y recolectar los datos
echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica refresco version master"
python refresco.py github master

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica refresco version latency"
python refresco.py github latency

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica refresco version accuracy"
python refresco.py github accuracy



echo "##################################################################"
echo "##################################################################"
echo "Valores calculados para la metrica de refresco"