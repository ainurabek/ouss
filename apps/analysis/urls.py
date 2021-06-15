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
router.register('type_equipment', views.TypeEquipmentViewSet, basename='type_equipment')


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
    path("form61/kls/update/<int:pk>/", views.Form61KLSUpdateAPIView.as_view()),
    path("form61/kls/delete/<int:pk>/", views.Form61KLSDeleteAPIView.as_view()),
    path("form61/kls/distance/<int:pk1>/<int:pk2>/", views.get_distance_length_kls),
    path("form61/kls/report/", views.get_report_form61_kls),
    path("form61/kls/order_kls_photo/create/<int:pk>/", views.OrderKLSPhotoCreateView.as_view()),
    path("form61/kls/order_kls_photo/delete/<int:obj_pk>/<int:deleted_pk>/", views.OrderKLSPhotoDeleteView.as_view()),

    path("form61/rrl/create/", views.Form61RRLCreateView.as_view()),
    path("form61/rrl/update/<int:pk>/", views.Form61RRLUpdateAPIView.as_view()),
    path("form61/rrl/delete/<int:pk>/", views.Form61RRLDeleteAPIView.as_view()),
    path("form61/rrl/report/", views.get_report_form61_rrl),
    path("form61/rrl/order_rrl_photo/create/<int:pk>/", views.OrderRRLPhotoCreateView.as_view()),
    path("form61/rrl/order_rrl_photo/delete/<int:obj_pk>/<int:deleted_pk>/", views.OrderRRLPhotoDeleteView.as_view()),
    path("detail/report/od/oa/", views.DetailOaAndOdApiView.as_view()),

    path('', include(router.urls)),

]
