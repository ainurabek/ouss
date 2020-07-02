from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.form_customer import views


app_name = 'form_customer'

router = routers.DefaultRouter()

urlpatterns = [
    ###HTML
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
    path("menu/<int:pk>/", views.MenuCustView.as_view(), name="menu_form_cust"),
    path("customer/circ/<int:pk>/", views.FilterCircuitView.as_view(), name="filter_form_circuit"),
    path("customer/<int:pk>/", views.FilterFormCustView.as_view(), name="filter_form_cust"),
    path("create/<int:pk>/", views.FormCustCircCreateView.as_view(), name="filter_form_cust_create"),
    path('edit/<int:pk>/', views.form_cust_edit, name='form_cust_edit'),
    path("delete/<int:pk>/", views.form_cust_delete, name="form_cust_delete"),

    ###API
    path("api/customers/", views.CustomerFormListView.as_view()),
    path("api/list/", views.FormCustomerListAPIView.as_view()),
    path("api/circuit/<int:pk>/", views.CircuitListAPIView.as_view()),
    path("api/object/<int:pk>/", views.ObjectListAPIView.as_view()),
    path("api/circuit/create/<int:pk>/", views.FormCustomerCircCreateAPIView.as_view()),
    path("api/object/create/<int:pk>/", views.FormCustomerObjCreateAPIView.as_view()),
    path("api/update/<int:pk>/", views.FormCustomerUpdateAPIView.as_view()),
    path("api/delete/<int:pk>/", views.FormCustomerDeleteAPIView.as_view()),


    path('', include(router.urls))
]

