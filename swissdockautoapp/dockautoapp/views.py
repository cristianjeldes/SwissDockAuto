from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate
from selenium import webdriver
from django.utils import timezone
import time
import requests
import os
from dockautoapp.models import *
import math
from collections import namedtuple
global basePath
basePath = "E:\\Escritorio\\Aplicaciones y paginas web\\CeBiB BioInformatica SwissDock\\SwissDockAuto\\swissdockautoapp\\dockingfiles\\"
def mkdir(path):
	if not os.path.isdir(path):
		os.makedirs (path)

def handleUploadedFile(jobname,f):
	global basePath
	path = basePath+jobname+"\\"
	mkdir(path)
	path = path+f.name
	destination = open(path,'wb')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()


# Create your views here.
def downloadFile(url):
    localFilename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(localFilename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return localFilename
class IndexView(View):
	def get(self, request):
		Proyectont = namedtuple("Proyectont",["proyecto","testsets"])
		Testsetnt = namedtuple("Testsetnt",["testset","jobs"])
		proyectos = Proyectojob.objects.all()
		listaProyectos = []
		for proyecto in proyectos:
			testsets = Testset.objects.filter(idproyecto = proyecto.pk)
			listaTestset = []
			for testset in testsets:
				jobs = Job.objects.filter(idtestset = testset.pk)
				listaTestset.append(Testsetnt(testset,jobs))
			listaProyectos.append(Proyectont(proyecto,listaTestset))
		return render(request, 'dockautoapp/verProyectos.html',{'proyectos':listaProyectos})
class CrearProyectoView(View):
	def get(self, request):
		return render(request, 'dockautoapp/crearProyecto.html',{})
	def post(self,request):
		projectname = request.POST.get('projectname')
		projectdescription = request.POST.get('projectdescription')
		if projectname and projectdescription:
			proyecto = Proyectojob(None,projectname,projectdescription,timezone.now())
			proyecto.save()
			return redirect("/crearTestset")
		else:
			return redirect("/crearProyecto")
class RevisarTestsetView(View):
	def get(self,request,id):
		testset = Testset.objects.get(pk=id)
		jobs = Job.objects.filter(idtestset=testset.pk)
		xChart = []
		deltagChart = []
		errorChart = []
		for job in jobs:
			xChart.append(int(job.ordenjob))
			deltagChart.append(job.deltagpromedio)
			errorChart.append(job.errorresultado)
		context = {"jobs":jobs,"testset":testset,"xChart":xChart,"deltagChart":deltagChart,"errorChart":errorChart}
		return render(request, 'dockautoapp/verTestset.html',context)
class CrearTestsetView(View):
	def get(self,request):
		proyectos = Proyectojob.objects.all()
		return render(request, 'dockautoapp/crearTestset.html',{'proyectos':proyectos})
	def post(self,request):
		global basePath
		#Receiving parameters
		ligandFile = request.FILES.get("ligandfile")
		targetFile = request.FILES.get("targetfile")
		dockingpoints = request.POST.getlist("dockingpoints[]")
		nametestset = request.POST.get("nametestset")
		projectid = request.POST.get("projectid")
		correotestset = request.POST.get("correotestset")
		print request.POST
		print request.FILES
		#Managing parameters and saving it to database
		handleUploadedFile(nametestset,ligandFile)
		handleUploadedFile(nametestset,targetFile)
		ligandObj = Ligand(None,ligandFile.name,basePath+nametestset+"\\"+ligandFile.name)
		ligandObj.save()
		targetObj = Target(None,targetFile.name,basePath+nametestset+"\\"+targetFile.name)
		targetObj.save()
		project = Proyectojob.objects.get(pk=int(projectid))
		testset = Testset(ligandObj.pk,targetObj.pk,None,project.pk,nametestset,correotestset)
		testset.save()
		estado = Estadojob.objects.get(pk=4)
		contador = 0
		for points in dockingpoints:
			mkdir(basePath+nametestset+"\\"+str(contador))
			job = Job(None,estado.pk,testset.pk,nametestset+str(contador),
				basePath+nametestset+"\\"+str(contador)+"\\resultados\\",0,0,contador,
				timezone.now(),None,points)
			job.save()
			contador+=1
		print dockingpoints
		return redirect("/verProyectos")
class RevisarProyectosView(View):
	def get(self,request):
		Proyectont = namedtuple("Proyectont",["proyecto","testsets"])
		Testsetnt = namedtuple("Testsetnt",["testset","jobs"])
		proyectos = Proyectojob.objects.all()
		listaProyectos = []
		for proyecto in proyectos:
			testsets = Testset.objects.filter(idproyecto = proyecto.pk)
			listaTestset = []
			for testset in testsets:
				jobs = Job.objects.filter(idtestset = testset.pk)
				listaTestset.append(Testsetnt(testset,jobs))
			listaProyectos.append(Proyectont(proyecto,listaTestset))
		return render(request, 'dockautoapp/verProyectos.html',{'proyectos':listaProyectos})
class RevisarJobsView(View):
	def get(self, request):
		jobs = Job.objects.all()
		return render(request, 'dockautoapp/jobs.html',{"jobs":jobs})
class RevisarJobView(View):
	def get(self, request,id):
		job = Job.objects.filter(swissdockid=id)
		if(len(job)==0):
			return redirect("/revisarjobs")
		job = job[0]
		comentarios = Comentario.objects.filter(id=job.pk)
		return render(request, 'dockautoapp/job.html',{'job':job,'comentarios':comentarios})
	def post(self,request,id):
		autor = request.POST.get("autor")
		descripcion = request.POST.get("descripcion")
		jobid = request.POST.get("jobid")
		job = Job.objects.get(pk=jobid)
		comentario = Comentario(None,job.pk,descripcion,autor,timezone.now())
		comentario.save()
		comentarios = Comentario.objects.filter(id=job.pk)
		return redirect("/verjob/"+job.swissdockid)