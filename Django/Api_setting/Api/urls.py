from django.urls import path

from . import views

urlpatterns =[
path("",views.home,name='home'),
path("request/",views.json_reqest,name='json_request')
]