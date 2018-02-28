#!/usr/bin/env python
#!/usr/bin/python

import matplotlib.pyplot as plt
import time
import os
import sys
from sys import argv
from pymongo import Connection
import matplotlib.dates as md
import datetime as dt

path = os.path.dirname(os.path.abspath(__file__))
con = Connection('localhost')
db = con.StatusAPIs

script, app, medida = argv

tuplas = []

horaActual = time.time()

if medida == "horas":
    segundosARestar = 3600
    rango = range(24)
    formato = '%H:%M'
    caracter = 'a'

elif medida == "dias":
    segundosARestar = 86400
    rango = range(30)
    formato = '%D'
    caracter = 'o'

elif medida == "meses":
    segundosARestar = 2592000
    rango = range(12)
    formato = '%m:%Y'
    caracter = 'o'
else:
    print "La medida para medir no es correcta."
    con.close()
    sys.exit()

for i in rango:
    lineas_totales = 0
    lineas_correctas = 0
    for element in db[app].find({ "time": { "$gt": horaActual-segundosARestar, "$lt": horaActual } } ):
        if element['code'] == 200:
            lineas_correctas += 1
        lineas_totales += 1
    if lineas_totales == 0:
        porcentaje = 0.0
    else:
        porcentaje = lineas_correctas / float(lineas_totales) * 100
    horaActual = horaActual-segundosARestar
    tuplas.insert(0, (dt.datetime.fromtimestamp(int(horaActual)),porcentaje))

plt.xlabel(medida)
plt.ylabel('Porcentaje')
plt.title('Uptime de l' + caracter + 's ultim' + caracter + 's ' + str(i+1) + ' ' + medida + ' de \"' + app + '\"')
ax=plt.gca()
xfmt = md.DateFormatter(formato)
ax.xaxis.set_major_formatter(xfmt)

plt.plot(*zip(*tuplas))
plt.show()
con.close()