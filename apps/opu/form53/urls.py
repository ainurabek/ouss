from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.form53 import views


app_name = 'form53'

router = routers.DefaultRouter()

urlpatterns = [


    path('', include(router.urls))
]

