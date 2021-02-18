# coding: utf-8

from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import LPCreateView, LPEditView, IPCreateView, ObjectCreateView, ObjectEditView, ObjectListView, \
          ObjectDetailView,  MainLineTypeList
from .trassa import SelectObjectView, SaveTrassaView, DeleteTrassaView, CreateLeftTrassaView, CreateRightTrassaView,\
    SelectCircuitView, CreateLeftCircuitTrassaView, CreateRightCircuitTrassaView, SaveCircuitTrassaView, \
    DeleteCircuitTrassaView, PointListTrassa, ObjectList, SelectPointView, CircuitListTrassa,  \
    PGCircuitListView, CreateLeftReserveTrassaView, CreateRightReserveTrassaView, SaveReserveTrassaView, DeleteReserveTrassaView

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
#ds,jh
    path('trakt/select-lp/<int:pk>/', SelectObjectView.as_view(), name='select_lp'),
    path('trakt/point-list/', PointListTrassa.as_view(), name='point_list'),
    path('trakt/select-point/<int:pk>/', SelectPointView.as_view(), name='select_point'),
    path('trakt/select-object/<int:pk>/', ObjectList.as_view(), name='select_obj'),
    #основная трасса
    path('trakt/left-trassa/<int:main_pk>/<int:pk>/', CreateLeftTrassaView.as_view(), name='left_trassa'),
    path('trakt/right-trassa/<int:main_pk>/<int:pk>/', CreateRightTrassaView.as_view(), name='right_trassa'),
    path('trakt/save-trassa/<int:pk>/', SaveTrassaView.as_view(), name='save_trassa'),
    path('trakt/delete-trass/<int:main_pk>/<int:pk>/', DeleteTrassaView.as_view(), name='delete_trassa'),
    #резервная трасса
    path('reserve/left-trassa/<int:main_pk>/<int:pk>/', CreateLeftReserveTrassaView.as_view(), name='reserve_left_trassa'),
    path('reserve/right-trassa/<int:main_pk>/<int:pk>/', CreateRightReserveTrassaView.as_view(), name='reserve_right_trassa'),
    path('reserve/save-trassa/<int:pk>/', SaveReserveTrassaView.as_view(), name='save_reserve_trassa'),
    path('reserve/delete-trass/<int:main_pk>/<int:pk>/', DeleteReserveTrassaView.as_view(), name='delete_reserve_trassa'),

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
    path('cir_trassa/left-trassa/<int:main_pk>/<int:pk>/', CreateLeftCircuitTrassaView.as_view(), name='left_trassa_circuit'),
    path('cir_trassa/right-trassa/<int:main_pk>/<int:pk>/', CreateRightCircuitTrassaView.as_view(), name='right_trassa_circuit'),
    path('cir_trassa/save-trassa/<int:pk>/', SaveCircuitTrassaView.as_view(), name='save_trassa_circ'),
    path('cir_trassa/delete-trass/<int:main_pk>/<int:pk>/', DeleteCircuitTrassaView.as_view(), name='delete_trassa_circ'),

    path('main-line-type/list/', MainLineTypeList.as_view(), name='line_type'),

    path('', include(router.urls))

]