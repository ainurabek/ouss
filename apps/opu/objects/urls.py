# coding: utf-8

from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import LPCreateView, LPEditView, IPCreateView, ObjectCreateView, ObjectEditView, ObjectListView, \
          ObjectDetailView,  MainLineTypeList
from .trassa import SelectCircuitView, PointListTrassa, ObjectList, SelectPointView, CircuitListTrassa, \
    PGCircuitListView, TransitCreateAPIView, RetrieveUpdateDelete, TransitListAPIView

app_name = 'objects'

router = routers.DefaultRouter()
router.register('tpo', views.TPOListView, basename='tpo_list')
router.register('outfit', views.OutfitsListView, basename='outfit_list')
router.register('point', views.PointListView, basename='point_list')
router.register('lp', views.LPListView, basename='lp_list')
router.register('line-type', views.LineTypeAPIVIew, basename='line_type')
router.register('category', views.CategoryAPIVIew, basename='category')
router.register('type_trakt', views.TypeTraktListView, basename='type_of_trakt')
router.register('type-of-location', views.TypeOfLocationAPIVIew, basename='type_of_location')
router.register('consumer', views.ConsumerModelViewSet, basename='consumer')
router.register('amount_channels', views.AmountChannelListAPIView, basename='amount_channels')
router.register('bug', views.BugModelViewSet, basename='bug')


urlpatterns = [
    path('objects/', views.ObjectAllView.as_view(), name='object_list'),
    url(r'^ip/create/(?P<pk>\S+)/$', IPCreateView.as_view()),
    url(r'^ip/delete/(?P<pk>\S+)/$', views.IPDeleteView().as_view(), name='ip_delete'),

    path('lp/create/', LPCreateView.as_view(), name='lp_create'),
    url(r'^lp/edit/(?P<pk>\S+)/$', LPEditView.as_view(), name='lp_edit'),
    # url(r'^lp/delete/(?P<pk>\S+)/$', views.LPDeleteView.as_view(), name='lp_delete'),

    path('trakt/<int:pk>/', ObjectListView.as_view(), name='trakt_list'),
    path('trakt/object-create/<int:pk>/',  ObjectCreateView.as_view(), name='object_create'),
    path('trakt/object-edit/<int:pk>/', ObjectEditView.as_view(), name='object_edit'),
    path('trakt/object-detail/<int:pk>/', ObjectDetailView.as_view(), name='object_delete'),

    path('trakt/point-list/', PointListTrassa.as_view(), name='point_list'),
    path('trakt/select-point/<int:pk>/', SelectPointView.as_view(), name='select_point'),
    path('trakt/select-object/<int:pk>/', ObjectList.as_view(), name='select_obj'),

    path('filter-object/', views.FilterObjectList.as_view(), name='filter_object'),

    path("history/obj/<int:pk>/", views.ObjectHistory.as_view(), name='object_history'),
    path("history/ip/<int:pk>/", views.IPHistory.as_view(), name='ip_history'),
    path("history/point/<int:pk>/", views.PointHistory.as_view(), name='point_history'),
    path("history/outfit/<int:pk>/", views.OutfitHistory.as_view(), name='outfit_history'),

    path("order/<int:pk>/", views.OrderFileUploader.as_view(), name='order_object'),
    path("order/delete/<int:obj_pk>/<int:deleted_pk>/", views.OrderObjectFileDeleteView.as_view(), name='order_object_delete'),

    path("pg/list/", views.PGObjectView.as_view(), name='pg_object_list'),

    #statistics
    path("tpo_amount/", views.get_tpo_amount, name='tpo_amount'),
    path("points_amount/", views.get_points_amount, name='points_amount'),
    path("outfits_amount/", views.get_outfits_amount, name='outfits_amount'),
    path("customers_amount/", views.get_customers_amount, name='customers_amount'),

    #trassa for circuits
    path('cir_trassa/pg_list/<int:pk>/', PGCircuitListView.as_view(), name='cir_pg_list'),
    path('cir_trassa/select-circuit/<int:pk>/', SelectCircuitView.as_view(), name='select_circuit'),
    path('cir_trassa/circuit_list/', CircuitListTrassa.as_view(), name='circuit_list'),

    path('main-line-type/list/', MainLineTypeList.as_view(), name='line_type'),

    path('GOZ/', views.GOZListView.as_view(), name='goz_list'),
    path("GOZ/update/<int:pk>/", views.GOZUpdateAPIView.as_view()),

    path('transit/list/<int:pk>/', TransitListAPIView.as_view()),
    path("transit/create/", TransitCreateAPIView.as_view()),
    path("transit/<int:pk>/", RetrieveUpdateDelete.as_view()),


    path('', include(router.urls))

]