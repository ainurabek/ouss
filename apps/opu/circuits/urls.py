from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.circuits.views import CircuitListViewSet, CircuitEditView
from . import views

app_name = 'circuits'

router = routers.DefaultRouter()



urlpatterns = [
    path('trakt/<int:pk>/', CircuitListViewSet.as_view(), name = 'circuit_list '),
    path('edit/<int:pk>/', CircuitEditView.as_view(), name='circuit_edit'),
    path('', include(router.urls))

]