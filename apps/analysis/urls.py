from django.urls import path, include
from apps.dispatching.views import *
from . import views
from rest_framework import routers

app_name = 'analysis'

router = routers.DefaultRouter()
router.register('form', views.FormAnalysisAPIViewSet, basename='index')
router.register('type_cable', views.TypeCableViewSet, basename='type_cable')
router.register('method_laying', views.MethodLayingViewSet, basename='method_laying')
router.register('type_connection', views.TypeConnectionViewSet, basename='type_connection')

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
    path("update/amount_channels/<int:pk>/", views.AmountChannelsObjectKLSRRLAPIView.as_view()),

    path("form61/kls/create/", views.Form61KLSCreateView.as_view()),
    # path("form61/kls/list/", views.Form61KLSList.as_view()),
    path("form61/kls/update/<int:pk>/", views.Form61KLSUpdateAPIView.as_view()),
    # path("form61/kls/report/", views.get_report_form61_kls),
    path("form61/kls/distance/<int:pk1>/<int:pk2>/", views.get_distance_length_kls),

    path("form61/kls/report/", views.Form61KLSList.as_view()),

    path('', include(router.urls)),

]