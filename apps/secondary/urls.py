from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'secondary'

router = routers.DefaultRouter()
router.register('type_station', views.TypeStationModelViewSet, basename='type_station')
router.register('base', views.BaseModelView, basename='secondary_base')
router.register('ambul_num_base', views.AmbulBaseUpdateDelete, basename='ambul_num_base')

urlpatterns = [
    path("list/", views.get_report_secondary),
    path("118/list/", views.get_report_118),

    path('', include(router.urls)),

]