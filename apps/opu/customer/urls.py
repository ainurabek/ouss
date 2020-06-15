from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.customer.views import CustomerViewSet, CustomerEditView
from . import views

app_name = 'customer'

router = routers.DefaultRouter()
router.register('', CustomerViewSet, basename='customer')


urlpatterns = [

    url(r'^edit/(?P<pk>\S+)/$', CustomerEditView.as_view(), name='customer_edit'),
    url(r'^delete/(?P<pk>\S+)/$', views.customer_delete_view, name='customer_delete'),

    path('', include(router.urls))

]