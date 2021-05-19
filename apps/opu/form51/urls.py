from django.urls import path, include
from rest_framework import routers
from apps.opu.form51 import views


app_name = 'form51'

router = routers.DefaultRouter()

urlpatterns = [
    path("list/", views.FormListAPIView.as_view()),
    path("api/update/<int:pk>/", views.Form51UpdateAPIView.as_view()),
    path("history/form51/<int:pk>/", views.Form51History.as_view(), name='form51_history'),
    path('', include(router.urls))
]

