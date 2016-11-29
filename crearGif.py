#!/usr/bin/env python
# -*- coding: utf-8

import os
import images2gif as i2
from PIL import Image

#Variable para la ruta al directorio
nombreDock='DEHU_4PYP_OUT'
path = './' + nombreDock +'/images'
 

#Lista vacia para incluir los ficheros
lstFiles = []
 
#Lista con todos los ficheros del directorio:
lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
 
 
#Crea una lista de los ficheros jpg que existen en el directorio y los incluye a la lista.
 
for root, dirs, files in lstDir:
    for fichero in files:
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".jpg"):
            lstFiles.append(path +'/'+nombreFichero+extension)
            #print (nombreFichero+extension)
             
print(lstFiles)            
print ('LISTADO FINALIZADO')
print ("longitud de la lista = ", len(lstFiles))

###GENERAR GIF
#las imagenes deben ser del mismo tamaño

images = [Image.open(fn) for fn in lstFiles]

size = (1000,1000)
for im in images:
    im.thumbnail(size, Image.ANTIALIAS)

filename =path+ "/my_gif.gif"
i2.writeGif(filename, images, duration=0.4)


