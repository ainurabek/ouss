from django.urls import path, include
from rest_framework import routers
from apps.opu.customer.views import CustomerViewSet
from . import views

app_name = 'customer'

router = routers.DefaultRouter()
router.register('', CustomerViewSet, basename='customer')


urlpatterns = [
    path("history/customer/<int:pk>/", views.CustomerHistory.as_view(), name='customer_history'),
    path('', include(router.urls))

]