#IMPORTS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab as P
from zipfile import ZipFile
import os.path
import tarfile
from subprocess import call
import os
DockName= 'TESTING' #Esto deberia estar disponible
path= os.path.join('./', DockName)
if not os.path.isdir(path):
    os.makedirs (path)

with ZipFile(DockName +'.zip') as myzip:
    myzip.extractall(path )

#CREAR ESTRUCTURA DE DIRECTORIOS
pathClusters= os.path.join(path + '/clusters')
if not os.path.isdir(pathClusters):
    os.makedirs (pathClusters)

pathComplexes= os.path.join(path + '/complexes')
if not os.path.isdir(pathComplexes):
    os.makedirs (pathComplexes)

pathImages= os.path.join(path + '/images')
if not os.path.isdir(pathImages):
    os.makedirs (pathImages)

#Descomprimir Otros Archivos
with ZipFile(path+'/clusters.zip') as myzip:
    myzip.extractall(pathClusters )

call(["7z", "e",path+"/complexes.tar.xz","-aoa"])

with tarfile.open("complexes.tar") as f:
	f.extractall(pathComplexes)

try:
    os.remove("complexes.tar")
except OSError:
    pass

archivo = open(path+ "/clusters.dock4.csv", "r")
contenido = archivo.read()
# EL PUNTERO QUEDA 
# AL FINAL DEL DOCUMENTO
archivo.seek(0)
contenido= contenido.replace(' ', ',')
archivo.close()

#ESCRIBIR EL ARCHIVO CSV
f=open(path+"/salida.csv","w")
f.write(contenido)
f.close()

#LEER CSV COMO DATA FRAME
Frame=  pd.read_csv(path +'/salida.csv')

#SELECCIONAR COLS: N CLUSTERS y DELTA G

COLS = Frame[[0, 2]]

#ESTO OTORGA MUCHOS VALORES PARA CADA CLUSTER.
#OBTENDEMOS LA MEDIA PARA CADA CLUSTER.

COLS2= COLS.groupby('Cluster').mean()

#GRAFICAR. (?)
#####NO ME SALE EL MONITO

#MEDIA POBLACIONAL y DESVIACION ESTANDAR.
MEDIA= str(float(COLS2.mean()))
ERROR= str(float(COLS2.std()))
resultado= [MEDIA, ERROR]
resultado= 'delta G: ' + MEDIA + ', error: ' + ERROR  

#ESCRIBIR EL ARCHIVO CSV
f=open(path+"/resultado.txt","w")
f.write(resultado)
f.close()


