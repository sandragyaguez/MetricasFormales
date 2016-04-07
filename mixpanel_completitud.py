import mixpanel_api, json
from mixpanel import Mixpanel
#Tienes que crear una instancia de la clase Mixpanel, con tus credenciales
x=mixpanel_api.Mixpanel("0be846115003ba87c667ee6467edb336","c282259a64f150a4ce2496a2dd73e097")


#Cuando lo tengas, defines los parametros necesarios para la peticion
params={'event':['completitud twitter'],
	'name':'text',
	'type':"general",
        'unit':"day",
        'interval':1,
        'from_date':'2016-03-09',
        'to_date':'2016-06-15'}


respuesta=x.request(['events/properties/values'], params, format='json')
print respuesta