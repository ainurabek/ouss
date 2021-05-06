from django.urls import path, include
from rest_framework import routers
from apps.opu.circuits.views import CircuitListViewSet, CircuitEditView, CircuitDetailView, UpdateCircuitAPIView
from . import views

app_name = 'circuits'

router = routers.DefaultRouter()

urlpatterns = [
    path('trakt/<int:pk>/', CircuitListViewSet.as_view(), name = 'circuit_list '),
    path('edit/<int:pk>/', CircuitEditView.as_view(), name='circuit_edit'),
    path('detail/<int:pk>/', CircuitDetailView.as_view(), name='circuit_detail'),
    path("history/circuit/<int:pk>/", views.CircuitHistory.as_view(), name='circuit_history'),
    path("trassa/update/<int:pk>/", UpdateCircuitAPIView.as_view()),
    path('', include(router.urls))

]