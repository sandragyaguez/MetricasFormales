- Tienes que instalar el paquete mixpanel-query (es una dependencia del módulo mixpanel_client, que utilizamos para hacer las peticiones a la API de Export de Mixpanel):
	sudo pip install mixpanel-query-py

- Para ejecutar las pruebas sobre los componentes, tienes que actualizar los tokens de Google y Facebook, pegarlos en los ficheros (Las instrucciones vienen en executeMetric.sh):
	- executeMetric.sh
	- Stable/GoogleplusLatency.html, Latency/GoogleplusLatency.html, Accuracy/GoogleplusLatency.html
	- Stable/FacebookWallLatency.html 

- Para cada componente ejecutado, se abren las pestañas para recoger los tiempos y se miden los tiempos desde python (measureLatency), y se recolectan las métricas de cada componente para el día actual (collectLatencyRecords). Si no quieres probar alguno de los componentes, comenta su línea de measureLatency y collectLatencyRecords. En cada fichero viene al final un pequeño mensaje de qué parámetros acepta cada script. 

- Para el caso de Twitter, hay que arreglar la llamada que se hace al endpoint de nuestro proxy para que no devuelva un error de autenticación (215), a partir de la línea 172 de measureLateny. Después habría que descomentar la parte de abajo del caso de Twitter, y asegurarte que la url con la que abres el componente es donde el componente está desplegado en remoto.

- Si decides desplegar los componentes en remoto, tendrás que cambiar la variable server_base_url (si mantienes la estructura de directorios cuando subes todo esto a App Engine).

- Los tiempos desde el cliente se miden gracias a la API de resource timing de Javascript:
	- Nos basamos en este artículo. Los tiempos que se envían a Mixpanel son algunos de los que aparecen desglosados en el diagrama de tiempos (enviamos a Mixpanel todos los campos de tiempo que podemos obtener para recursos externos https://www.w3.org/TR/2016/WD-resource-timing-20160225/
	- Aquí hay ejemplos de implementación: https://developer.mozilla.org/en-US/docs/Web/API/Resource_Timing_API/Using_the_Resource_Timing_API
	- Sería interesante que comentases que se han tenido que hacer unos pequeños campos en los componentes, ya que hemos tenido que añadir el header "Allow-timing-Origin" para poder trackear los tiempos de petición a dominios externos a la página. Esos cambios se pueden ver en las distintas versiones de los componentes en este directorio y en la página de Github de cada componente. En el artículo de la W3C lo explican aquí: https://www.w3.org/TR/2016/WD-resource-timing-20160225/#timing-allow-origin 
