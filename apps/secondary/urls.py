from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'secondary'

router = routers.DefaultRouter()
router.register('type_station', views.TypeStationModelViewSet, basename='type_station')





urlpatterns = [




    path('', include(router.urls)),

]