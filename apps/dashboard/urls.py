# DASHBOARD APP LEVEL

from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^dashboard$', views.home),
    url(r'^dashboard/add$', views.add),
    url(r'^dashboard/(?P<id>\d+)/delete$', views.delete),
    url(r'^dashboard/(?P<appntmnt_id>\d+)/edit$', views.edit),
    url(r'^(?P<appntmnt_id>\d+)/update$', views.update),
    
]
