#!/usr/bin/env python
#!/usr/bin/python

import matplotlib.pyplot as plt
import time
import os
from sys import argv
from pymongo import Connection
import matplotlib.dates as md
import datetime as dt

path = os.path.dirname(os.path.abspath(__file__))
con = Connection('localhost')
db = con.StatusAPIs

script, app = argv

t = time.time()

####################################     BUSQUEDA POR LAS ULTIMAS 24 HORAS      #################################

tuplas = []

for i in range(24):
    lineas_totales = 0
    lineas_correctas = 0
    for element in db[app].find({ "time": { "$gt": t-3600, "$lt": t } } ):
        if element['code'] == 200:
            lineas_correctas += 1
        lineas_totales += 1
    if lineas_totales == 0:
        porcentaje = 0.0
    else:
        porcentaje = lineas_correctas / float(lineas_totales) * 100
    t = t-3600
    tuplas.insert(0, (dt.datetime.fromtimestamp(int(t)),porcentaje))

ax=plt.gca()
xfmt = md.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(*zip(*tuplas))

plt.xlabel('Horas')
plt.ylabel('Porcentaje')
plt.title('Uptime de las ultimas 24 horas de \"' + app + '\"')
plt.show()
con.close()