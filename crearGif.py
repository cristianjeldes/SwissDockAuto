#!/usr/bin/env python
# -*- coding: utf-8

import os
from PIL import Image
import imageio
def doGif(output,listFiles,duration=0.3):
	with imageio.get_writer(output, mode='I',duration=duration) as writer:
	    for filename in listFiles:
	        image = imageio.imread(filename)
	        writer.append_data(image)

#Variable para la ruta al directorio
nombreDock='TESTING'
path = './' + nombreDock +'/images'
 

#Lista vacia para incluir los ficheros
lstFiles = []
 
#Lista con todos los ficheros del directorio:
lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
 
 
#Crea una lista de los ficheros jpg que existen en el directorio y los incluye a la lista.
for root, dirs, files in lstDir:
	print root, dirs, files
	for fichero in files:
		(nombreFichero, extension) = os.path.splitext(fichero)
		if(extension == ".png"):
			lstFiles.append(path +'/'+nombreFichero+extension)
             
print(lstFiles)            
print ('LISTADO FINALIZADO')
print ("longitud de la lista = ", len(lstFiles))

filename =path+ "/my_gif.gif"
doGif(filename, lstFiles, duration=0.5)


