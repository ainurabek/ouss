from django.urls import path, include
from apps.dispatching.views import *
from . import views
from rest_framework import routers

app_name = 'analysis'

router = routers.DefaultRouter()



urlpatterns = [

    path('disp/report/', views.DispEvent1ListAPIView.as_view({'get': 'list'}), name="disp_list_event"),

    path("api/form/", views.get_report),
    path("history/<int:pk>/", views.DispEventHistory.as_view(), name = 'history'),
    path("punkt5/", views.punkt5, name = 'punkt5'),

    path("<int:pk>/create/", views.Punkt5CreateViewAPI.as_view()),
    path("list/", views.Punkt5ListAPIView.as_view()),
    path('', include(router.urls)),

]