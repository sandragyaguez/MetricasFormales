
#guardar datos de mixpanel
import mixpanel_api, json
from mixpanel import Mixpanel
mp = Mixpanel("070bf8a01a6127ebf78325716490697a")

#Tienes que crear una instancia de la clase Mixpanel, con tus credenciales
x=mixpanel_api.Mixpanel("c10939e3faf2e34b4abb4f0f1594deaa","4a3b46218b0d3865511bc546384b8928")

version="master"
event_master="Twitter refresh master"
event_latency= "Twitter refresh latency"
event_accuracy="Twitter refresh accuracy"

################################################################################################
#----------------------------------------------REFRESH-----------------------------------------#
################################################################################################

#Cuando lo tengas, defines los parametros necesarios para la peticion
params={'event':[event_master],
	'name':'time_refresh',
	'type':"general",
        'unit':"day",
        'interval':1,
        'from_date':'2016-03-09',
        'to_date':'2016-06-15'}

params_refresh={'event':[event_master],
	'name':'tweet',
	'type':"general",
        'unit':"day",
        'interval':1,
        'from_date':'2016-03-09',
        'to_date':'2016-06-15'}


respuesta_refresh=x.request(['events/properties/values'], params, format='json')
respuesta_refresh_sort=sorted(respuesta_refresh)

# respuesta1=x.request(['events/properties/values'], params1, format='json')
# res=map(int, respuesta1)
# res=sorted(res)


respuesta_refresh1=x.request(['events/properties/values'], params_refresh, format='json')
respuesta_refresh_sort1=sorted(respuesta_refresh1)

listarefresh=zip(respuesta_refresh_sort1,respuesta_refresh_sort)
miDiccionario=dict(listarefresh)

print "---------------------------------------------------------------------------------------------------------"
print "diccionario refresh: " + str(miDiccionario)

################################################################################################
#--------------------------------------------------POST----------------------------------------#
################################################################################################

event_master_post= "Twitter post master"
event_latency_post="Twitter post latency"
event_accuracy_post="Twitter post accuracy"

params1={'event':[event_master_post], 
	'name':'time post',
        'type':"general",
        'from_date':'2016-03-09',
        'to_date':'2016-06-15',
        'unit':"day", 
        'interval':1}


params1_post={'event':[event_master_post], 
	'name':'tweet',
        'type':"general",
        'from_date':'2016-03-09',
        'to_date':'2016-06-15',
        'unit':"day", 
        'interval':1}


respuesta_post=x.request(['events/properties/values'], params1, format='json')
respuesta_post_sort=sorted(respuesta_post)

respuesta_post1=x.request(['events/properties/values'], params1_post, format='json')
respuesta_post_sort1=sorted(respuesta_post1)

listapost=zip(respuesta_post_sort1,respuesta_post_sort)
miDiccionario1=dict(listapost)

print "---------------------------------------------------------------------------------------------------------"
print "diccionario post: " + str(miDiccionario1)

################################################################################################
#----------------------------------------------VERSION1----------------------------------------#
################################################################################################

#version en las que ordeno los tiempos y hago la resta de ambas listas, dando por hecho que esas listas estan bien ordendas, es decir
#que el tiempo del refresh de un tweet coindice con el tiempo del post del mismo tweet para hacer la resta. No comprueba si el campo tweet es el mismo

# i = 0
# for timerefresh, timepost in zip(respuesta_refresh_sort, respuesta_post_sort):
#         final_time=int(timerefresh)-int(timepost)
#         texto=list(respuesta_refresh_sort1)
#         print "final_time: " + texto[i] + " " +  str(final_time)
#         i+=1

################################################################################################
#----------------------------------------------VERSION2----------------------------------------#
################################################################################################

#version en la que las listas las paso a diccionario para poder comparar el tweet de forma mas sencilla y ver si realmente estoy restando los tiempos
#correspondientes al mismo tweet  

#la k corresponde al diccionario de refresco, y la v al diccionario de post. No va por clave, valor de una lista! (para dudas: imprimir y ver que devuelve)
for k,v in zip(miDiccionario.items(),miDiccionario1.items()):
        if cmp(k[0],v[0])==0:
                print "-------------"
                print k[0]
                final_time=int(k[1])-int(v[1])
                print "final_time diccionarios: " + str(final_time)
                mp.track(final_time, "Final time master",{"time final": final_time, "tweet": k[0], "version":version})