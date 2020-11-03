from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.form_customer import views


app_name = 'form_customer'

router = routers.DefaultRouter()

urlpatterns = [

    ###API
    path("api/customers/", views.CustomerFormListView.as_view()),
    path("api/list/", views.FormCustomerListAPIView.as_view()),
    path("api/circuit/<int:pk>/", views.CircuitListAPIView.as_view()),
    path("api/object/<int:pk>/", views.ObjectListAPIView.as_view()),
    path("api/circuit/create/<int:pk>/", views.FormCustomerCircCreateAPIView.as_view()),
    path("api/object/create/<int:pk>/", views.FormCustomerObjCreateAPIView.as_view()),
    path("api/update/<int:pk>/", views.FormCustomerUpdateAPIView.as_view()),
    path("api/delete/<int:pk>/", views.FormCustomerDeleteAPIView.as_view()),

#orderphoto
    path("api/ordercusphoto/create/<int:pk>/", views.OrderCusPhotoCreateView.as_view()),
    path("api/ordercusphoto/delete/<int:obj_pk>/<int:deleted_pk>/", views.OrderCusPhotoDeleteView.as_view()),

    path("history/form_customer/<int:pk>/", views.FormCustomerHistory.as_view(), name='form_customer_history'),


    path('', include(router.urls))
]

