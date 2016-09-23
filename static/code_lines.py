
import sys

##########################################################################################################################################
##########################################################################################################################################
#----------------------------------------------------METRICA LINEAS DE CODIGO-------------------------------------------------------------
##########################################################################################################################################
##########################################################################################################################################

network_list = ["twitter", "facebook", "github","googleplus","instagram"]
version_list = ["master","latency", "accuracy"]

#consola: python code_lines.py component version
if len(sys.argv) >= 2:
    social_network = sys.argv[1]
else:
    social_network = ''

if len(sys.argv) >= 3:
    version= sys.argv[2]
else:
    version = ''

#CASOS:
if social_network in network_list:

#--------------------------------------------------
#CASO1: TWITTER
#--------------------------------------------------

	if social_network == 'twitter':
		if version in version_list:
			if(version=="master"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/twitter-timeline/static/twitter-timeline.html", "r")
			elif(version=="latency"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/twitter-timeline/static/twitter-timeline.html", "r")
			elif(version=="accuracy"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/twitter-timeline/static/twitter-timeline.html", "r")


#--------------------------------------------------
#CASO2: FACEBOOK
#-------------------------------------------------

	elif social_network == 'facebook':
		if version in version_list:
			if(version=="master"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/facebook-wall/facebook-wall.html", "r")
			elif(version=="latency"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/facebook-wall/facebook-wall.html", "r")
			elif(version=="accuracy"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/facebook-wall/facebook-wall.html", "r")

#--------------------------------------------------
#CASO3: GITHUB
#-------------------------------------------------

	elif social_network == 'github':
		if version in version_list:
			if(version=="master"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/github-events/github-events.html", "r")
			elif(version=="latency"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/github-events/github-events.html", "r")
			elif(version=="accuracy"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/github-events/github-events.html", "r")


#--------------------------------------------------
#CASO4: GOOGLEPLUS
#-------------------------------------------------

	elif social_network == 'googleplus':
		print version
		if version in version_list:

			if(version=="master"):
				fichero = open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Master/googleplus-timeline/googleplus-timeline.html", "r")
			elif(version=="latency"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Latency/googleplus-timeline/googleplus-timeline.html", "r")
			elif(version=="accuracy"):
				fichero=open("/home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Accuracy/googleplus-timeline/googleplus-timeline.html", "r")

	else:
		print "algo va mal"

	text = fichero.read()
	non_blank_lines=0
	blank_lines=0

	for line in text.splitlines():
		if line.strip():
			non_blank_lines+=1
		else:
			blank_lines+=1

	print 'lineas NO vacias %d' % non_blank_lines
	print 'lineas vacias %d' % blank_lines
	total_lines=non_blank_lines+blank_lines
	print 'lineas totales %d' % total_lines