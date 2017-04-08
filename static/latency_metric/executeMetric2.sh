#!/bin/bash

# Url para obtener nuevo token de facebook: https://developers.facebook.com/tools/explorer/145634995501895/
# Url para obtener nuevo token google: https://developers.google.com/+/web/api/rest/latest/activities/list#try-it
# (Para el caso de Google, haces una petición a la API con el explorer API, vas a networks, y coges el token que
# viene en el header Authorization: 'Bearer TOKEN')

# Antes de hacer una prueba nueva hay que hacer los siguientes pasos:
# - 	Hay que cambiar el token que está en FacebookWallLatency.html (carpeta Stable) y la variable FACEBOOK_TOKEN
# En GoogleplusLatency.html (Carpetas Accuracy, Latency, Stable) cambiar el valor de la variable access_token y la variable GOOGLE_TOKEN
FACEBOOK_TOKEN="EAACEdEose0cBAHoa37lJ0KzEXOQZA2ZBSqq2oUk4w86Vi9g0Po5u0acejfFj0u7hA0J4piZApzl0gPRUhzHq0wemwUqc8gD8C7tYoWKV3nbzbmqAvafJebhEcgVPbXccOJTblqUEOigCGQyifmbZARlNrtABqwDZC3PN0lG4rCpmJR8QxjQh8gHudvTh08ocZD"
GOOGLE_TOKEN="ya29.GmEnBIVse3WHOQEJIOfqK8BRtgrEMy0vLj-jXN10FESc9XKYWlUF8xvM9dX1RkxYB-w8xpS7xEmpRP6f3HcvDIKMtxIZRhNXk3HHPer0R2qL8HW8dbnZtnC0rB2Kr4zOJ9PA"

# Comentar esta línea si los componentes están deplegados en remoto
python -m SimpleHTTPServer >> /dev/null &
PID=`echo $!`
# echo $PID
# # Ejecutamos scripts para medir y recolectar los datos
#echo "##################################################################"
#echo "Realizando pruebas sobre el componente instagram-timeline..."
#python measureLatency.py instagram

# Esperamos un tiempo para asegurar que se recolectan los eventos de las distintas versiones
# y para intentar que las ejecuciones anteriores de componentes "no afecten" posteriores medidas
# sleep 10
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente github-events..."
# python measureLatency.py github

# sleep 10
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente facebook-wall..."
# python measureLatency.py facebook $FACEBOOK_TOKEN

# lo tengo en latency_metric_ana por falta de espacion al desplegar en app engine
# sleep 10
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente googleplus-timeline..."
# python measureLatency.py googleplus $GOOGLE_TOKEN

# sleep 10
# echo "##################################################################"
# echo "Realizando pruebas sobre el componente pinterest-timeline..."
# python measureLatency.py pinterest

# sleep 10
# echo "#################################################################"
# echo "Realizando pruebas sobre el componente finance-search..."
# python measureLatency.py finance

# sleep 10
# echo "#################################################################"
# echo "Realizando pruebas sobre el componente open-weather..."
# python measureLatency.py weather

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente traffic-incidents..."
python measureLatency.py traffic

sleep 10
echo "##################################################################"
echo "Recolectando y calculando métrica de latencia sobre los componentes probados..."
# python collectLatencyRecords.py instagram-timeline
# python collectLatencyRecords.py github-events
# python collectLatencyRecords.py facebook-wall
# python collectLatencyRecords.py googleplus-timeline
# python collectLatencyRecords.py pinterest-timeline
# python collectLatencyRecords.py finance-search
# python collectLatencyRecords.py open-weather
python collectLatencyRecords.py traffic-incidents
echo "Métricas calculadas"

# Matamos el proceso correspondiente al servidor local de componentes de python
kill -9 $PID

#twitter esta desplegado en remoto