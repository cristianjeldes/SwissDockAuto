from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^crearjob$', CrearJobView.as_view()),
    url(r'^revisarjobs$', RevisarJobsView.as_view()),
    url(r'^verjob/(?P<id>[a-zA-Z0-9\_]*)$', RevisarJobView.as_view()),
]