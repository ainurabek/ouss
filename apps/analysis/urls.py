from django.urls import path, include
from apps.dispatching.views import *
from . import views
from rest_framework import routers

app_name = 'analysis'

router = routers.DefaultRouter()



urlpatterns = [
    path("api/form/", views.get_report),
    path('', include(router.urls)),

]