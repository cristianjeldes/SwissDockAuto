from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^crearjob$', CrearJobView.as_view()),
    url(r'^revisarjobs$', RevisarJobsView.as_view()),
    url(r'^revisarjob$', RevisarJobsView.as_view()),
]