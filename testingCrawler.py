from selenium import webdriver
import time

browser = webdriver.Chrome()

browser.get("http://127.0.0.1:8000/")

time.sleep(2)

#Ahora buscamos el id del docking o el enlace para recibir los archivos
linkToJob = browser.find_element_by_link_text('Crear Docking')
print linkToJob
jobId = linkToJob.get_attribute("href").replace("/docking/view/","")
print jobId
#Se cierra el navegador
browser.close()