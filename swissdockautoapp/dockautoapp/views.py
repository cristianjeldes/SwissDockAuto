from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate
from selenium import webdriver
import time
def preprocessPoints(points):
	result = list()
	#aqui se procesan los datos de los puntos elegidos
	#se obtienen su X, Y y Z
	return result
def calculateXYZAndDistances(points):
	pointsList = preprocessPoints(points)
	hull = convexHull(pointsList)
	centerHull = hull(centerHull)
	distances = getDistances(hull)
	return (centerHull,distances)
# Create your views here.
class IndexView(View):
	def get(self, request):
		return render(request, 'dockautoapp/index.html',{})
class CrearJobView(View):
	def get(self, request):
		return render(request, 'dockautoapp/crearJob.html',{})
	def post(self, request):
		basePath = "E:\\Escritorio\\Aplicaciones y paginas web\\CeBiB BioInformatica SwissDock\\SwissDockAuto\\input\\"
		liganFile = request.POST.get("ligandFile")
		targetFile = request.POST.get("targetFile")
		pointsXYZAndDistances  = calculateXYZAndDistances(request.POST.get("points"))
		browser = webdriver.Chrome()

		browser.get("http://www.swissdock.ch/docking")

		#Se revelan los campos necesarios
		browser.find_element_by_id("optionalparameterstoggle").click()
		browser.find_element_by_id("link_target_upload").click()
		browser.find_element_by_id("link_ligand_upload").click()

		time.sleep(5) #Para que no tenga problemas en cargar el html y reconozca las opciones extra

		#Acciones para el target
		target = browser.find_element_by_id("DockingTargetUpload")

		target.send_keys(basePath+targetFile) # La ruta debe ser absoluta

		#Acciones para el ligand
		ligand = browser.find_element_by_id("DockingLigandUpload")
		ligand.send_keys(basePath+liganFile) # La ruta debe ser absoluta

		#Acciones para parametros
		#Centers
		xcenter = browser.find_element_by_id("DockingXcen")
		xcenter.send_keys("")
		ycenter = browser.find_element_by_id("DockingYcen")
		ycenter.send_keys("")
		zcenter = browser.find_element_by_id("DockingZcen")
		zcenter.send_keys("")
		#Sizes
		xsize = browser.find_element_by_id("DockingXsize")
		xsize.send_keys("")
		ysize = browser.find_element_by_id("DockingYsize")
		ysize.send_keys("")
		zsize = browser.find_element_by_id("DockingZsize")
		zsize.send_keys("")

		#Acciones para reconocimiento
		job_name = browser.find_element_by_id("DockingJobName")
		job_name.send_keys("Test1")
		email = browser.find_element_by_id("DockingEmail")
		email.send_keys("vodcon@gmail.com")

		#Acciones para opciones
		docking_type = browser.find_element_by_id("DockingDockingType")
		for option in docking_type.find_elements_by_tag_name('option'):
			if option.text == 'I\'m feeling lucky': #Opcion aqui
				option.click()

		flexibility = browser.find_element_by_id("DockingPassiveFlexibilityDistance")
		for option in flexibility.find_elements_by_tag_name('option'):
			if option.text == '3': #Opcion aqui
				option.click()

		#Submit
		browser.find_element_by_id("StartDockingButton").click()

		#Esperamos 5 seg para que se envien los archivos
		time.sleep(5)

		#Ahora buscamos el id del docking o el enlace para recibir los archivos
		linkToJob = browser.find_element_by_link_text('here')
		jobId = linkToJob.get_attribute("href").replace("http://www.swissdock.ch/docking/view/","")
		print jobId
		#Se cierra el navegador
		browser.close()
class RevisarJobsView(View):
	def get(self, request):
		return render(request, 'dockautoapp/jobs.html',{})
class RevisarJobView(View):
	def get(self, request):
		return render(request, 'dockautoapp/job.html',{})