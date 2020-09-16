from django.urls import path, include
from rest_framework import routers
from apps.opu.circuits.views import CircuitListViewSet, CircuitEditView
from . import views

app_name = 'circuits'

router = routers.DefaultRouter()
router.register('measure', views.MeasureAPIView, basename='measure')
router.register('mode', views.ModeAPIView, basename='mode')
router.register('type-com', views.TypeComAPIView, basename='type_com')
router.register('speed', views.SpeedAPIView, basename='speed')


urlpatterns = [
    path('trakt/<int:pk>/', CircuitListViewSet.as_view(), name = 'circuit_list '),
    path('edit/<int:pk>/', CircuitEditView.as_view(), name='circuit_edit'),

    path('', include(router.urls))

]