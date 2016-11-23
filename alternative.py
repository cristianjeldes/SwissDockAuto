from selenium import webdriver
import time

browser = webdriver.Chrome()

browser.get("http://www.swissdock.ch/docking")

#Se revelan los campos necesarios
browser.find_element_by_id("optionalparameterstoggle").click()
browser.find_element_by_id("link_target_upload").click()
browser.find_element_by_id("link_ligand_upload").click()

time.sleep(5) #Para que no tenga problemas en cargar el html y reconozca las opciones extra

#Acciones para el target
target = browser.find_element_by_id("DockingTargetUpload")
#target.send_keys('/home/gabriel/Desktop/BioInfo/input/GAT-1.pdb') # La ruta debe ser absoluta

#Acciones para el ligand
ligand = browser.find_element_by_id("DockingLigandUpload")
#ligand.send_keys('/home/gabriel/Desktop/BioInfo/input/DEHU.mol2') # La ruta debe ser absoluta

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
email.send_keys("gg@cebib.cl")

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

#Se cierra el navegador
browser.close()
