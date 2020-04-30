from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.customer.views import CustomerViewSet

app_name = 'customer'

router = routers.DefaultRouter()
router.register('', CustomerViewSet, basename='customer')


urlpatterns = [

    path('', include(router.urls))

]