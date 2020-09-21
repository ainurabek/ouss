from django.urls import path, include
from apps.dispatching.views import *
from . import views
from rest_framework import routers

app_name = 'analysis'

router = routers.DefaultRouter()



urlpatterns = [

    path('disp/report/', views.DispEvent1ListAPIView.as_view({'get': 'list'}), name="disp_list_event"),

    path("api/form/", views.get_report),
    path('', include(router.urls)),

]