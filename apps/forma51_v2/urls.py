from apps.forma51_v2.views import *
from django.urls import path, include
from rest_framework import routers

app_name = 'forma51_v2'

router = routers.DefaultRouter()


urlpatterns = [
	path('region/', region_list, name='list_region'),
	path('list/<str:slug>/', form51_list, name='form51_list'),
	path('form-create/<int:pk>/', create_form51, name='create_form51'),
	path('', include(router.urls))
] 