#!/bin/bash

# Copyright 2017 Luis Ruiz Ruiz

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

echo "###############################################"
echo "Recogiendo valores de latencia"
python get_results_latency.py

sleep 5
echo "###############################################"
echo "Recogiendo valores de complejidad ciclomatica"
python get_results_complexity.py

sleep 5
echo "###############################################"
echo "Recogiendo valores de complejidad estructural"
python get_results_structural.py

sleep 5
echo "###############################################"
echo "Recogiendo valores de mantenibilidad"
python get_results_maintenance.py

# sleep 5
# echo "################################################"
# echo "Recogiendo valores de completitud"
# python get_results_accuracy.py

# sleep 5
# echo "###############################################"
# echo "Recogiendo valores de refresco"
# python get_results_refresh.py

echo "Todas las metricas recogidas"