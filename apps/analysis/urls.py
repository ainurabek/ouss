from django.urls import path, include
from apps.dispatching.views import *
from . import views
from rest_framework import routers

app_name = 'analysis'

router = routers.DefaultRouter()
router.register('form', views.FormAnalysisAPIViewSet, basename='index')

urlpatterns = [

    path('disp/report/', views.DispEvent1ListAPIView.as_view({'get': 'list'}), name="disp_list_event"),

    path("api/form/", views.get_report),
    path("history/<int:pk>/", views.DispEventHistory.as_view(), name='history'),
    path("form/create/<int:pk>/", views.FormAnalysisCreateAPIViewItem5.as_view()),
    path("item5/outfit/list/<int:pk>/", views.OutfitItem5ListAPIView.as_view()),
    path("item5/update/<int:pk>/", views.Item5UpdateAPIView.as_view()),
    path("item5/create/<int:pk>/", views.Item5CreateAPIView.as_view()),
    path("item5/delete/<int:pk>/", views.Item5DeleteAPIVIew.as_view()),
    path("item7/create/<int:pk>/", views.Item7CreateAPIView.as_view()),
    path("item7/update/<int:pk>/", views.Item7UpdateAPIView.as_view()),
    path("item7/delete/<int:pk>/", views.Item7DeleteAPIView.as_view()),
    path('', include(router.urls)),
]