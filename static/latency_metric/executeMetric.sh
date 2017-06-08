#!/bin/bash

python -m SimpleHTTPServer >> /dev/null &
PID=`echo $!`

sleep 10
echo "##################################################################"
echo "Realizando pruebas sobre el componente twitter-timeline..."
python measureLatency.py pinterest

sleep 10
echo "##################################################################"
echo "Recolectando y calculando métrica de latencia sobre los componentes probados..."
python collectLatencyRecords.py pinterest-timeline
echo "Métricas calculadas"

kill -9 $PID
