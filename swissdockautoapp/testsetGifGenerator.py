import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swissdockautoapp.settings")
import django
django.setup()
from dockautoapp.models import *
from glob import glob
import imageio
basePath = "E:/Escritorio/Aplicaciones y paginas web/CeBiB BioInformatica SwissDock/SwissDockAuto/swissdockautoapp/dockingfiles/"
staticPath = "E:/Escritorio/Aplicaciones y paginas web/CeBiB BioInformatica SwissDock/SwissDockAuto/swissdockautoapp/static/img/"

# No es un cambio radical, pero al menos asi funca bien respecto a que no quede tan pesado.
#El 30 habra que cambiarlo segun la cantidad media de jobs que se estime que hagan.
def doGif(output,listFiles,duration=0.3):
	i = 0
	with imageio.get_writer(output, mode='I',duration=duration) as writer:
	    for filename in listFiles:
			if len(listFiles)<=30:
				image = imageio.imread(filename)
				writer.append_data(image)
			else:
				if i%2==0:
					image = imageio.imread(filename)
					writer.append_data(image)
					i += 1
				else:
					i += 1
def generateFinalGif(listDirsImg,testset):
	listDirsImg.sort()
	# A diferencia del otro script se tienen que hacer los nombres y la lista 
	#vacia antes de iniciar los for 
	gifName = str(testset.pk)+testset.nombretestset+"(Terminado)"+str(testset.pk)+".gif"
	filename = basePath+testset.nombretestset+"/"+gifName
	staticgif = staticPath+"/"+gifName
	lstFiles = []
	for directory in listDirsImg:
		lstDir = os.walk(directory)   #os.walk()Lista directorios y ficheros
			#Crea una lista de los ficheros jpg que existen en el directorio y los incluye a la lista.
		for root, dirs, files in lstDir:
			for fichero in files:
				(nombreFichero, extension) = os.path.splitext(fichero)
				if(extension == ".png"):
					lstFiles.append(directory+nombreFichero+extension)

	doGif(filename, lstFiles, duration=0.5)
	doGif(staticgif, lstFiles, duration=0.5)
def main():
	testsets = Testset.objects.all()
	for testset in testsets:
		if not "(Terminado)" in testset.nombretestset:
			jobs = Job.objects.filter(idtestset=testset.pk)
			aux = True
			dirlist = []
			for job in jobs:
				dirlist.append(basePath+testset.nombretestset+"/"+str(job.ordenjob)+"/resultados/images/")
				if job.idestado.pk!=2:
					aux = False
					break
			if aux:
				generateFinalGif(dirlist,testset)
				testset.nombretestset = testset.nombretestset+"(Terminado)"
				testset.save()
			else:
				print "Para el testset",testset.nombretestset,"todavia no terminan sus jobs"
		else:
			print testset.nombretestset,"esta terminado"
if __name__=="__main__":
	main()