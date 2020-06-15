from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.form_customer import views


app_name = 'form_customer'

router = routers.DefaultRouter()

urlpatterns = [
    ###HTML
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
    path("customer/<int:pk>/", views.FilterFormCustView.as_view(), name="filter_form_cust"),
    path("", views.FormCustListView.as_view(), name="form_customer_list"),


    ###API


    path('', include(router.urls))
]

