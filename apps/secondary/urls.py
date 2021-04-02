from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'secondary'

router = routers.DefaultRouter()
router.register('type_station', views.TypeStationModelViewSet, basename='type_station')

urlpatterns = [

    path('points/<int:pk>/', views.PointsByOutfittView.as_view(), name='points_list'),
    path('base/list/', views.SecondaryBaseList.as_view(), name='base_list'),
    path('', include(router.urls)),

]