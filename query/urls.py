from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.name_input),
    url(r'^thanks/$', views.thanks),
    ]
