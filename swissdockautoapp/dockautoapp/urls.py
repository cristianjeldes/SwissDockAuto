from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^crearTestset$', CrearTestsetView.as_view()),
    url(r'^verProyectos$', RevisarProyectosView.as_view()),
    url(r'^verTestset/(?P<id>[0-9]+)$', RevisarTestsetView.as_view()),
    url(r'^crearProyecto$',CrearProyectoView.as_view()),
    url(r'^verjob/(?P<id>[a-zA-Z0-9\_]*)$', RevisarJobView.as_view()),
]