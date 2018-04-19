import csv
from sys import argv



def comparaNota(sinFallos,conFallos,nombreComponente):
    with open(sinFallos,"r") as csvSinFallos:
        spamreader = csv.reader(csvSinFallos)
        for row in spamreader:
            erroresSinFallos = row[0]
    csvSinFallos.close()

    with open(conFallos,"r") as csvConFallos:
        spamreader = csv.reader(csvConFallos)
        for row in spamreader:
            erroresConFallos = row[0]
    csvConFallos.close()
 
    with open("notasComponentes.csv","wb") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(nombreComponente)
        spamwriter.writerow("Correcto")
        spamwriter.writerow([str(erroresSinFallos)])
        spamwriter.writerow("Defectuoso")
        spamwriter.writerow([str(erroresConFallos)])
    csvfile.close()


script, notaCompSinFallos, notaCompConFallos, nombreComponente = argv
comparaNota(notaCompSinFallos,notaCompConFallos,nombreComponente)