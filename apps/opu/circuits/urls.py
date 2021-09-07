from django.urls import path, include
from rest_framework import routers
from apps.opu.circuits.views import CircuitListViewSet, CircuitEditView, CircuitDetailView, UpdateCircuitAPIView, \
    CircuitHistory, AddCircuitTrassa, DeleteCircuitTrassa

app_name = 'circuits'

router = routers.DefaultRouter()

urlpatterns = [
    path('trakt/<int:pk>/', CircuitListViewSet.as_view(), name = 'circuit_list '),
    path('edit/<int:pk>/', CircuitEditView.as_view(), name='circuit_edit'),
    path('detail/<int:pk>/', CircuitDetailView.as_view(), name='circuit_detail'),
    path("history/circuit/<int:pk>/", CircuitHistory.as_view(), name='circuit_history'),
    path("trassa/update/<int:pk>/", UpdateCircuitAPIView.as_view()),
    path("trassa/add/<int:circuit_pk>/<int:transit_pk>/", AddCircuitTrassa.as_view()),
    path("trassa/delete/<int:circuit_pk>/<int:transit_pk>/", DeleteCircuitTrassa.as_view()),
    path('', include(router.urls))

]