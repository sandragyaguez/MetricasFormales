#!/bin/bash

python -m SimpleHTTPServer >> /dev/null &
PID=`echo $!`

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente reddit-timeline..."
python measureLatency.py spotify


 sleep 20
 echo "##################################################################"
 echo "Recolectando y calculando métrica de latencia sobre los componentes probados..."
 python collectLatencyRecords.py spotify
 echo "Métricas calculadas"

kill -9 $PID
