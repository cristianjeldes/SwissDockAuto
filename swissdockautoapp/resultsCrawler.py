# -*- coding: utf-8 -*-
import os
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swissdockautoapp.settings")
import django
django.setup()
from dockautoapp.models import *
from selenium import webdriver
import requests
from PIL import Image
import imageio
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab as P
from zipfile import ZipFile
import os.path
import tarfile
import datetime
from django.utils import timezone
import subprocess
import __main__
from time import sleep
__main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
import pymol
pymol.finish_launching()
global basePath
global staticPath


basePath = "E:/Escritorio/Aplicaciones y paginas web/CeBiB BioInformatica SwissDock/SwissDockAuto/swissdockautoapp/dockingfiles/"
staticPath = "E:/Escritorio/Aplicaciones y paginas web/CeBiB BioInformatica SwissDock/SwissDockAuto/swissdockautoapp/static/img/"
def checkmkdir(path):
	if not os.path.isdir(path):
	    os.makedirs (path)
def generarArchivosNecesarios(path,swissdockid):
	checkmkdir(path)

	with ZipFile(path+"/"+swissdockid +'.zip') as myzip:
	    myzip.extractall(path )

	#CREAR ESTRUCTURA DE DIRECTORIOS
	pathClusters= os.path.join(path + '/clusters')
	checkmkdir(pathClusters)

	pathComplexes= os.path.join(path + '/complexes')
	checkmkdir(pathComplexes)

	pathImages= os.path.join(path + '/images')
	checkmkdir(pathImages)

	#Descomprimir Otros Archivos
	with ZipFile(path+'/clusters.zip') as myzip:
	    myzip.extractall(pathClusters )
	pathToComplexestarxz = path+"/complexes.tar.xz"
	z7 = ["7z","e",pathToComplexestarxz.replace("/","\\"),"-aoa"]
	print z7
	return_code = subprocess.call(z7, shell=True) 
	print "Decompressing ended with code:",return_code
	with tarfile.open("complexes.tar") as f:
		f.extractall(pathComplexes)
	print pathToComplexestarxz[:-3]
	try:
	    os.remove(pathToComplexestarxz[:-3])
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
	print "Reading data"
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
	COLS2 = COLS2.sort(['deltaG'])
	COLS2 = COLS2[:10]
	print COLS2
	#MEDIA POBLACIONAL y DESVIACION ESTANDAR.
	MEDIA= str(float(COLS2.mean()))
	ERROR= str(float(COLS2.std()))
	resultado= [MEDIA, ERROR]
	resultado= 'delta G: ' + MEDIA + ', error: ' + ERROR  
	print "El resultado es:",resultado
	#ESCRIBIR EL ARCHIVO CSV
	f=open(path+"/resultado.txt","w")
	f.write(resultado)
	f.close()
	return (MEDIA,ERROR)

def generarImagenes(directorio):
	directorio_clusters=directorio+'/clusters'
	directorio_complexes=directorio+'/complexes'
	directorio_imagenes=directorio+'/images'
	delta_g = []
	for file in os.listdir(directorio_clusters):
		f = open(directorio_clusters+'/'+file, 'r')
		for line in f:
			if line.startswith("* deltaG: "):
				delta_g.append([file,line[10:][:-1]])
				break
		f.close()
	delta_g = sorted(delta_g, key=lambda delta_g: delta_g[1], reverse=True)
	
	indice=0

	for dg in delta_g:
		f = open(directorio_clusters+'/'+dg[0], 'r')
		cluster=''
		cluster_rank=''
		for line in f:
			if line.startswith("* Cluster: "):
				cluster=line[11:][:-1]
			if line.startswith("* ClusterRank: "):
				cluster_rank=line[15:][:-1]
		f.close()
		pdb_file=directorio_complexes+'/complex.'+cluster+'_'+cluster_rank+'.pdb'
		# Load Structures
		pymol.cmd.reinitialize()
		pymol.cmd.load(pdb_file)
		pymol.cmd.bg_color('white')
		## EDITAR ROTACIONES
		pymol.cmd.rotate('x','90')
		pymol.cmd.rotate('y','90')
		pymol.cmd.rotate('z','0')
		pymol.cmd.show_as('ribbon','complex.'+cluster+'_'+cluster_rank)
		pymol.cmd.color('red','complex.'+cluster+'_'+cluster_rank)
		pymol.cmd.show_as('spheres', 'resn LIG')
		pymol.cmd.color('blue','resn LIG')
		print('Imprimiendo imagen '+str(indice+1))
		fileImage = directorio_imagenes+'/imagen_'+str(indice+1)+'.png'
		print fileImage
		pymol.cmd.png(fileImage.replace("/","/"))
		sleep(0.5) # (in seconds)
		indice+=1
		## EDITAR NUMERO DE IMAGENES QUE RENDEREA
		if indice==10:
			break
	

def generarGif(path,swissdockid):
	global staticPath
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
	filename = path+"/"+swissdockid+".gif"
	staticgif = staticPath+"/"+swissdockid+".gif"
	doGif(filename, lstFiles, duration=0.5)
	doGif(staticgif, lstFiles, duration=0.5)

def doGif(output,listFiles,duration=0.3):
	with imageio.get_writer(output, mode='I',duration=duration) as writer:
	    for filename in listFiles:
	        image = imageio.imread(filename)
	        writer.append_data(image)

def download_file(url,name,relativePath):
	global basePath
	newDir = basePath+"/"+relativePath
	checkmkdir(newDir)
	local_filename = basePath+"/"+relativePath+"/"+name+".zip"
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True, allow_redirects=False)
	if r.status_code==404 or r.status_code=="404":
		return False
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=2048): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	return True
def checkJobs():
	global basePath
	estado = Estadojob.objects.get(pk=3)
	for job in Job.objects.filter(idestado=estado):
		pathJob = job.idtestset.nombretestset+"/"+str(job.ordenjob)+"/resultados"
		print pathJob
		if download_file("http://www.swissdock.ch/files/tmp/"+job.swissdockid+".zip",
		job.swissdockid,pathJob):
			pathJob = basePath+pathJob
			try:
				(media,error) = generarArchivosNecesarios(pathJob,job.swissdockid)
				generarImagenes(pathJob)
				generarGif(pathJob+"/images",job.swissdockid)
				job.idestado = Estadojob.objects.get(pk=2)
				job.fechahoratermino = timezone.now()
				job.errorresultado = error
				job.deltagpromedio = media
				job.save()
			except:
				raise
		else:
			print "Resultado para",pathJob,"no se encuentra disponible"
def main():
	print "Start checking jobs"
	checkJobs()
	pymol.cmd.quit()
if __name__ == '__main__':
    main()