from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.form51 import views


app_name = 'form51'

router = routers.DefaultRouter()

urlpatterns = [

    path("list/", views.FormListAPIView.as_view()),
    path("api/update/<int:pk>/", views.Form51UpdateAPIView.as_view()),
    path("api/detail/<int:pk>/", views.Form51DetailAPIView.as_view()),
    # path("api/reserve/<int:pk>/", views.ReserveDetailAPIView.as_view()),

    # path("api/reserve/delete/<int:form_pk>/<int:reserve_pk>/", views.ReserveDelete.as_view()),
#orderphoto
    path("api/orderphoto/create/<int:pk>/", views.OrderPhotoCreateView.as_view()),
    path("api/orderphoto/delete/<int:obj_pk>/<int:deleted_pk>/", views.OrderPhotoDeleteView.as_view()),

#schemaphoto
    path("api/schemaphoto/create/<int:pk>/", views.SchemaPhotoCreateView.as_view()),
    path("api/schemaphoto/delete/<int:obj_pk>/<int:deleted_pk>/", views.SchemaPhotoDeleteView.as_view()),

    path("history/form51/<int:pk>/", views.Form51History.as_view(), name='form51_history'),


    path('', include(router.urls))
]

