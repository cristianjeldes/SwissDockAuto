import time
import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swissdockautoapp.settings")
import django
django.setup()
from selenium import webdriver
from dockautoapp.models import *
import math
from collections import namedtuple
import random
basePath = "E:/Escritorio/Aplicaciones y paginas web/CeBiB BioInformatica SwissDock/SwissDockAuto/swissdockautoapp/dockingfiles/"
def cleanString(string):
	for i in xrange(0,10):
		string = string.replace("  "," ")
	return string
def averageXYZ(points):
	result = [0]*3
	for point in points:
		result[0] += point[0]
		result[1] += point[1]
		result[2] += point[2]
	result[0]/=len(points)*1.0
	result[1]/=len(points)*1.0
	result[2]/=len(points)*1.0
	return result
def preprocessPoints(points,csv):
	result = list()
	csvFile = open(csv.descripcion)
	atoms = dict()
	for linea in csvFile:
		if "ATOM" in linea:
			strings = cleanString(linea.strip()).split(" ")
			if strings[4] in points:
				if not strings[4] in atoms:
					atoms[strings[4]] = []
				atoms[strings[4]].append([float(strings[5]),float(strings[6]),float(strings[7])])
	for key in atoms:
		result.append(averageXYZ(atoms[key]))
	return result
def discardDimension(points):
	xDifference = 0
	yDifference = 0
	zDifference = 0
	memory = points[0]
	averages = averageXYZ(points)
	for point in points[1:]:
		xDifference+=abs(point[0]-memory[0])
		yDifference+=abs(point[1]-memory[1])
		zDifference+=abs(point[2]-memory[2])
	minimum = min(xDifference,yDifference,zDifference)
	keep1 = 0
	keep2 = 1
	average = 0
	if minimum==xDifference:
		average = 0
		keep1 = 1
		keep2 = 2
	elif minimum==yDifference:
		keep1 = 0
		average = 1
		keep2 = 2
	else:
		keep1 = 0
		keep2 = 1
		average = 2
	result = []
	for i in xrange(0,len(points)):
		result.append([0,0])
	counter = 0
	for point in points:
		result[counter][0] = point[keep1]
		result[counter][1] = point[keep2]
		counter+=1
	return (averages,result,[keep1,keep2,average])
def polygonCentroid(points):
	averages,pointsNew,dimensions = discardDimension(points)
	return (averages,dimensions)
	centroid = [0,0,0]
	centroid[dimensions[2]] = averages[dimensions[2]]
	signedArea = 0.0
	x0 = 0.0
	y0 = 0.0
	x1 = 0.0
	y1 = 0.0
	pSA = 0.0 #partial signed area
	for i in xrange(0,len(pointsNew)):
		x0 = pointsNew[i][0]
		y0 = pointsNew[i][1]
		x1 = pointsNew[(i+1)%len(pointsNew)][0]
		y1 = pointsNew[(i+1)%len(pointsNew)][1]
		a = x0*y1 - x1*y0
		print a
		signedArea += a
		centroid[dimensions[0]] += (x0 + x1)*a
		centroid[dimensions[1]] += (y0 + y1)*a
	signedArea *= 0.5
	centroid[dimensions[0]] /= (6.0*signedArea)
	centroid[dimensions[1]] /= (6.0*signedArea)
	return (centroid,dimensions)
def distance2points(a,b):
	return math.sqrt(math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2)+math.pow(a[2]-b[2],2))
def getDistances(points,centroid):
	distances = [0,0,0]
	pointDistanceFromCentroid = 0
	for point in points:
		temp = distance2points(point,centroid)
		pointDistanceFromCentroid+=temp
	pointDistanceFromCentroid/=len(points)*1.0
	return int(pointDistanceFromCentroid)*2.0
def calculateXYZAndDistances(points,csv):
	pointsList = preprocessPoints(points,csv)
	centroid,usedDimensions = polygonCentroid(pointsList)
	distance = getDistances(pointsList,centroid)
	return (centroid,distance,usedDimensions)
def generateJob(dockingpoints,targetObj,ligandObj,jobname,mail,job):
	#Getting centroid, distance and used dimensions
	XYZ,distance,usedDimensions  = calculateXYZAndDistances(dockingpoints,targetObj)
	#Start crawling
	try:
		browser = webdriver.Chrome()

		browser.get("http://www.swissdock.ch/docking")

		#Se revelan los campos necesarios
		browser.find_element_by_id("optionalparameterstoggle").click()
		browser.find_element_by_id("link_target_upload").click()
		browser.find_element_by_id("link_ligand_upload").click()

		time.sleep(5) #Para que no tenga problemas en cargar el html y reconozca las opciones extra

		#Acciones para el target
		target = browser.find_element_by_id("DockingTargetUpload")

		target.send_keys(targetObj.descripcion) # La ruta debe ser absoluta

		#Acciones para el ligand
		ligand = browser.find_element_by_id("DockingLigandUpload")
		ligand.send_keys(ligandObj.descripcion) # La ruta debe ser absoluta

		#Acciones para parametros
		#Centers
		xcenter = browser.find_element_by_id("DockingXcen")
		xcenter.send_keys(str(XYZ[0]))
		ycenter = browser.find_element_by_id("DockingYcen")
		ycenter.send_keys(str(XYZ[1]))
		zcenter = browser.find_element_by_id("DockingZcen")
		zcenter.send_keys(str(XYZ[2]))
		#Sizes
		xsize = browser.find_element_by_id("DockingXsize")
		xsize.send_keys(str(distance))#("0",str(distance))[int(usedDimensions[0]==0 or usedDimensions[1]==0)])
		ysize = browser.find_element_by_id("DockingYsize")
		ysize.send_keys(str(distance))#("0",str(distance))[int(usedDimensions[0]==1 or usedDimensions[1]==1)])
		zsize = browser.find_element_by_id("DockingZsize")
		zsize.send_keys(str(distance))#("0",str(distance))[int(usedDimensions[0]==2 or usedDimensions[1]==2)])

		#Acciones para reconocimiento
		job_name = browser.find_element_by_id("DockingJobName")
		job_name.send_keys(jobname.replace(" ","_"))
		email = browser.find_element_by_id("DockingEmail")
		email.send_keys(mail)

		#Acciones para opciones
		docking_type = browser.find_element_by_id("DockingDockingType")
		for option in docking_type.find_elements_by_tag_name('option'):
			if option.text == 'Fast':#'I\'m feeling lucky': #Opcion aqui
				option.click()

		flexibility = browser.find_element_by_id("DockingPassiveFlexibilityDistance")
		for option in flexibility.find_elements_by_tag_name('option'):
			if option.text == '5': #Opcion aqui
				option.click()

		#Submit
		browser.find_element_by_id("StartDockingButton").click()

		#Esperamos 5 seg para que se envien los archivos
		time.sleep(5)

		#Ahora buscamos el id del docking o el enlace para recibir los archivos
		linkToJob = browser.find_element_by_link_text('here')
		jobId = linkToJob.get_attribute("href").replace("http://www.swissdock.ch/docking/view/","")
		job.swissdockid = jobId
		job.idestado = Estadojob.objects.get(pk=3)
		job.save()
		#Se cierra el navegador
		browser.close()
	except:
		print "Problem connecting with swissdock"
		raise
def main():
	counter = 0
	jobs = Job.objects.filter(idestado=4,idtestset=testset.pk)
	for job in jobs:
		testset = job.idtestset
		#dockingpoints,targetObj,ligandObj,path,mail,job
		generateJob(job.puntosentrada.split(","),testset.idtarget,testset.idligand,testset.nombretestset+" "+str(job.ordenjob),testset.correotestset,job)
		time.sleep(600+30*random.randint(1,10))
		counter+=1
		if counter==10:
			break
if __name__=="__main__":
	main()