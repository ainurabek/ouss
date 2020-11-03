from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.form53 import views


app_name = 'form53'

router = routers.DefaultRouter()


urlpatterns = [

    ###API
    path("<int:pk>/create/", views.Form53CreateViewAPI.as_view()),
    path("list/", views.Form53ListAPIView.as_view()),
    path("api/regions/", views.Region53ListAPIView.as_view()),
    path("<int:pk>/edit/", views.Form53UpdateAPIView.as_view()),
    path("<int:pk>/delete/", views.Form53DeleteAPIView.as_view()),


#orderphoto
    path("api/order53photo/create/<int:pk>/", views.Order53PhotoCreateView.as_view()),
    path("api/order53photo/delete/<int:obj_pk>/<int:deleted_pk>/", views.Order53PhotoDeleteView.as_view()),

#schemaphoto
    path("api/schema53photo/create/<int:pk>/", views.Schema53PhotoCreateView.as_view()),
    path("api/schema53photo/delete/<int:obj_pk>/<int:deleted_pk>/", views.Schema53PhotoDeleteView.as_view()),

    path("history/form53/<int:pk>/", views.Form53History.as_view(), name='form53_history'),

    path('', include(router.urls))
]

