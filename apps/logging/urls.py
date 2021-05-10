from django.urls import path, include
from apps.logging.views import *
from . import views
from rest_framework import routers


app_name = 'logging'

router = routers.DefaultRouter()



urlpatterns = [

    path('list/', views.ActivityLogAPIVIew.as_view(), name = 'logging_list '),

    path('', include(router.urls)),

]