from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import LPListView, LPCreateView, LPEditView, TPOCreateView, \
    TPOEditView, OutfitCreateView, OutfitEditView, PointCreateView, PointEditView, IPCreateView,\
    ObjectCreateView, ObjectEditView, ObjectListView, \
    SelectObjectView, SaveTrassaView, DeleteTrassaView, PointListTrassa, ObjectList, CreateLeftTrassaView, \
    CreateRightTrassaView, SelectPointView, ObjectDetailView

app_name = 'objects'

router = routers.DefaultRouter()
router.register('tpo', views.TPOListView, basename='tpo_list')
router.register('outfit', views.OutfitsListView, basename='outfit_list')
router.register('point', views.PointListView, basename='point_list')
router.register('lp', views.LPListView, basename='lp_list')
router.register('objects', views.ObjectAllView, basename='all_objects')
router.register('line-type', views.LineTypeAPIVIew, basename='line_type')
router.register('category', views.CategoryAPIVIew, basename='category')
router.register('order', views.OrderAPIVIew, basename='order')
router.register('type-of-location', views.TypeOfLocationAPIVIew, basename='type_of_location')
router.register('in-out', views.InOutAPIVIew, basename='in_out')







urlpatterns = [

    path('tpo/create/', TPOCreateView.as_view(), name='tpo_create'),
    url(r'^tpo/edit/(?P<pk>\S+)/$', TPOEditView.as_view()),
    # url(r'^tpo/delete/(?P<tpo_id>\S+)/$', views.TPODeleteView.as_view(), name='tpo_delete'),

    path('outfit/create/', OutfitCreateView.as_view(), name='outfit_create'),
    url(r'^outfit/edit/(?P<pk>\S+)/$', OutfitEditView.as_view()),
    # url(r'^outfit/delete/(?P<outfit_id>\S+)/$', views.OutfitDeleteView.as_view(), name='outfit_delete'),

    path('point/create/', PointCreateView.as_view(), name='point_create'),
    url(r'^point/edit/(?P<pk>\S+)/$', PointEditView.as_view()),
    # url(r'^point/delete/(?P<pk>\S+)/$', views.PointDeleteView.as_view(), name='point_delete'),

    url(r'^ip/$', views.IPListView().as_view(), name='ip_list'),
    url(r'^ip/create/(?P<pk>\S+)/$', IPCreateView.as_view()),
    url(r'^ip/delete/(?P<pk>\S+)/$', views.IPDeleteView().as_view(), name='ip_delete'),

    path('lp/create/', LPCreateView.as_view(), name='lp_create'),
    url(r'^lp/edit/(?P<pk>\S+)/$', LPEditView.as_view(), name='lp_edit'),
    # url(r'^lp/delete/(?P<pk>\S+)/$', views.LPDeleteView.as_view(), name='lp_delete'),

    path('trakt/<int:pk>/', ObjectListView.as_view(), name='trakt_list'),
    path('trakt/object-create/<int:pk>/',  ObjectCreateView.as_view(), name='object_create'),
    path('trakt/object-edit/<int:pk>/', ObjectEditView.as_view(), name='object_edit'),
    path('trakt/object-detail/<int:pk>/', ObjectDetailView.as_view(), name='object_delete'),

    path('trakt/select-lp/<int:pk>/', SelectObjectView.as_view(), name='select_lp'),
    path('trakt/point-list/', PointListTrassa.as_view(), name='point_list'),
    path('trakt/select-point/<int:pk>/', SelectPointView.as_view(), name='select_point'),
    path('trakt/select-object/<int:pk>/', ObjectList.as_view(), name='select_obj'),
    path('trakt/left-trassa/<int:main_pk>/<int:pk>/', CreateLeftTrassaView.as_view(), name='left_trassa'),
    path('trakt/right-trassa/<int:main_pk>/<int:pk>/', CreateRightTrassaView.as_view(), name='right_trassa'),
    path('trakt/save-trassa/<int:pk>/', SaveTrassaView.as_view(), name='save_trassa'),
    path('trakt/delete-trass/<int:main_pk>/<int:pk>/', DeleteTrassaView.as_view(), name='delete_trassa'),
    path('filter-object/', views.FilterObjectList.as_view(), name='filter_object'),

    path("amount_channel/list/", views.AmountChannelListAPIView.as_view(), name="amount_channel_list"),

#orderphoto
    path("orderphoto/create/<int:pk>/", views.ObjectOrderPhotoCreateView.as_view()),
    path("orderphoto/delete/<int:obj_pk>/<int:deleted_pk>/", views.ObjectOrderPhotoDeleteView.as_view()),

#schemaphoto
    path("schemaphoto/create/<int:pk>/", views.ObjectSchemaPhotoCreateView.as_view()),
    path("schemaphoto/delete/<int:obj_pk>/<int:deleted_pk>/", views.ObjectSchemaPhotoDeleteView.as_view()),

    path("history/obj/<int:pk>/", views.ObjectHistory.as_view(), name='object_history'),
    path("history/ip/<int:pk>/", views.IPHistory.as_view(), name='ip_history'),
    path("history/order/<int:pk>/", views.OrderHistory.as_view(), name='order_history'),
    path("history/point/<int:pk>/", views.PointHistory.as_view(), name='point_history'),
    path("history/outfit/<int:pk>/", views.OutfitHistory.as_view(), name='outfit_history'),

    path('', include(router.urls))

]