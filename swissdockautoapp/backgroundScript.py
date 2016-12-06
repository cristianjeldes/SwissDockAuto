# -*- coding: utf-8 -*-
import os
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swissdockautoapp.settings")
import django
from selenium import webdriver
django.setup()
from dockautoapp.models import *

def checkJobs():
    estado = Estadojob.objects.get(pk=3)
    for job in Job.objects.filter(idestado=estado):
        print job.swissdockid
def main():
    print "Start checking jobs"
    checkJobs()

if __name__ == '__main__':
    main()