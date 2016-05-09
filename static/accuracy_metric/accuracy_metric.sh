


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
echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version latency"
python completitud.py twitter latency

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline: metrica completitud version accuracy"
python completitud.py twitter accuracy
	

#---------#
#GITHUB
#---------#

# Ejecutamos scripts para medir y recolectar los datos
echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica completitud version master"
python completitud.py github master

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica completitud version latency"
python completitud.py github latency

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente github-events: metrica completitud version accuracy"
python completitud.py github accuracy



#---------#
#INSTAGRAM
#---------#

# Ejecutamos scripts para medir y recolectar los datos
echo "##################################################################"
echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version master"
python completitud.py instagram master

# Esperamos un tiempo para asegurar que se recolectan los eventos de las distintas versiones
# y para intentar que las ejecuciones anteriores de componentes "no afecten" posteriores medidas
sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version latency"
python completitud.py instagram latency

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente instagram-timeline: metrica completitud version accuracy"
python completitud.py instagram accuracy



echo "Métricas calculadas"