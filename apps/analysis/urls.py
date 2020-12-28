from django.urls import path, include
from apps.dispatching.views import *
from . import views
from rest_framework import routers

app_name = 'analysis'

router = routers.DefaultRouter()
router.register('form', views.FormAnalysisAPIViewSet, basename='index')

urlpatterns = [


    path("api/form/", views.get_report),
    path("history/<int:pk>/", views.DispEventHistory.as_view(), name='history'),
    path("form/<int:pk>/edit/", views.FormAnalysisUpdateAPIView.as_view(), name='update_form'),
    path("form/create/<int:pk>/", views.FormAnalysisCreateAPIView.as_view()),
    path("punkt5/list/<int:pk>/", views.Punkt5ListAPIView.as_view()),
    path("punkt5/update/<int:pk>/", views.Punkt5UpdateAPIView.as_view()),
    path("punkt5/delete/<int:pk>/", views.Punkt5DeleteAPIVIew.as_view()),
    path("punkt7/update/<int:pk>/", views.Punkt7UpdateAPIView.as_view()),
    path("punkt7/delete/<int:pk>/", views.Punkt7DeleteAPIView.as_view()),
    path("punkt7/list/<int:pk>/", views.Punkt7ListAPIView.as_view()),
    path("report/od/oa/", views.ReportOaAndOdApiView.as_view()),
    path("winners/report/", views.WinnerReportAPIView.as_view()),

    path("disp/report/", views.get_report_analysis),
    path('', include(router.urls)),

]