
import sys
import json
import subprocess
from mixpanel import Mixpanel


mpResults = Mixpanel("f9ce3b0a5f0c588c7219f4624085db0e")

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
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/twitter-timeline/static/twitter-timeline.html"], stdout=subprocess.PIPE, shell=True)
			elif(version=="latency"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/twitter-timeline/static/twitter-timeline.html"], stdout=subprocess.PIPE, shell=True)
			elif(version=="accuracy"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/twitter-timeline/static/twitter-timeline.html"], stdout=subprocess.PIPE, shell=True)


#--------------------------------------------------
#CASO2: FACEBOOK
#-------------------------------------------------

	elif social_network == 'facebook':
		if version in version_list:
			if(version=="master"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/facebook-wall/facebook-wall.html"], stdout=subprocess.PIPE, shell=True)
			elif(version=="latency"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/facebook-wall/facebook-wall.html"], stdout=subprocess.PIPE, shell=True)
			elif(version=="accuracy"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/facebook-wall/facebook-wall.html"], stdout=subprocess.PIPE, shell=True)

#--------------------------------------------------
#CASO3: GITHUB
#-------------------------------------------------

	elif social_network == 'github':
		if version in version_list:
			if(version=="master"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/github-events/github-events.html"], stdout=subprocess.PIPE, shell=True)
			elif(version=="latency"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Latency/github-events/github-events.html"], stdout=subprocess.PIPE, shell=True)
			elif(version=="accuracy"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Accuracy/github-events/github-events.html"], stdout=subprocess.PIPE, shell=True)


#--------------------------------------------------
#CASO4: GOOGLEPLUS
#-------------------------------------------------

	elif social_network == 'googleplus':
		if version in version_list:
			if(version=="master"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Master/googleplus-timeline/googleplus-timeline.html"], stdout=subprocess.PIPE, shell=True)
			elif(version=="latency"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Latency/googleplus-timeline/googleplus-timeline.html"], stdout=subprocess.PIPE, shell=True)
			elif(version=="accuracy"):
				proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/accuracy_metric/Accuracy/googleplus-timeline/googleplus-timeline.html"], stdout=subprocess.PIPE, shell=True)

	else:
		print "algo va mal"

	#cloc solo cuenta las lineas de codigo reales
	#con esto consigo ejecutar una llamada del sistema y almacenar su valor
	#Popen: execute a child program in a new process
	#stdout=subprocess.PIPE : Special value that can be used as the stdin, stdout or stderr argument to Popen and indicates that a pipe to the standard stream should be opened.
	#proc = subprocess.Popen(["cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/twitter-timeline/static/twitter-timeline.html"], stdout=subprocess.PIPE, shell=True)
	#communicate: Send data to stdin
	(out,err)= proc.communicate()
	print out
	data=json.loads(out)
	code= data['SUM']['code']
	print code
	mpResults.track("Code lines", social_network,{"lineas":code,"componente":social_network,"version":version})



#---------------------------------------------------------------------------

#este codigo se traga los comentarios y si defino lineas de codigo no validas, las cuenta como una mas
	# text = fichero.read()
	# non_blank_lines=0
	# blank_lines=0

	# for line in text.splitlines():
	# 	if line.strip():
	# 		non_blank_lines+=1
	# 	else:
	# 		blank_lines+=1

	# print 'lineas NO vacias %d' % non_blank_lines
	# print 'lineas vacias %d' % blank_lines
	# total_lines=non_blank_lines+blank_lines
	# print 'lineas totales %d' % total_lines


#------------------------------------------------------------------------------

#Otra forma de hacer lo mismo
#Run command with arguments and return its output as a byte string.
# batcmd="cloc --json /home/sandra/Documentos/Labo/MetricasFormales/static/refresh_metric/Master/twitter-timeline/static/twitter-timeline.html"
# result = subprocess.check_output(batcmd, shell=True)
# #print result
# print type(result)
