from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import LPListView, LPCreateView, LPEditView, TPOCreateView, \
    TPOEditView, OutfitCreateView, OutfitEditView, PointCreateView, PointEditView, IPCreateView, IPEditView, \
    ObjectDeleteView, ObjectCreateView, ObjectEditView, ObjectListView, select_lp, \
    select_object, left_trassa, right_trassa, save_trassa


app_name = 'objects'

router = routers.DefaultRouter()
router.register('tpo', views.TPOListView, basename='tpo_list')
router.register('outfit', views.OutfitsListView, basename='outfit_list')
router.register('point', views.PointListView, basename='point_list')
router.register('ip', views.IPListView, basename='ip_list')
router.register('lp', views.LPListView, basename='lp_list')






urlpatterns = [

    path('tpo/create/', TPOCreateView.as_view(), name='tpo_create'),
    url(r'^tpo/edit/(?P<pk>\S+)/$', TPOEditView.as_view()),
    url(r'^tpo/delete/(?P<tpo_id>\S+)/$', views.tpo_delete_view, name='tpo_delete'),

    path('outfit/create/', OutfitCreateView.as_view(), name='outfit_create'),
    url(r'^outfit/edit/(?P<pk>\S+)/$', OutfitEditView.as_view()),
    url(r'^outfit/delete/(?P<outfit_id>\S+)/$', views.outfit_delete_view, name='outfit_delete'),

    path('point/create/', PointCreateView.as_view(), name='point_create'),
    url(r'^point/edit/(?P<pk>\S+)/$', PointEditView.as_view()),
    url(r'^point/delete/(?P<pk>\S+)/$', views.point_delete_view, name='point_delete'),

    path('ip/create/', IPCreateView.as_view(), name='ip_create'),
    url(r'^ip/edit/(?P<pk>\S+)/$', IPEditView.as_view()),
    url(r'^ip/delete/(?P<pk>\S+)/$', views.ip_delete_view, name='ip_delete'),

    path('lp/create/', LPCreateView.as_view(), name='lp_create'),
    url(r'^lp/edit/(?P<pk>\S+)/$', LPEditView.as_view(), name='lp_edit'),
    url(r'^lp/delete/(?P<pk>\S+)/$', views.lp_delete_view, name='lp_delete'),

    path('trakt/<int:pk>/', ObjectListView.as_view(), name='trakt_list'),
    path('trakt/object-create/<int:pk>/',  ObjectCreateView.as_view(), name='object_create'),
    path('trakt/object-edit/<int:pk>/', ObjectEditView.as_view(), name='object_edit'),
    path('trakt/object-delete/<int:pk>/', ObjectDeleteView.as_view(), name='object_delete'),

    path('trakt/select-lp/<int:main_pk>/', select_lp, name='select_lp'),
    path('trakt/select-object/<int:lp_pk>/', select_object, name='select_obj'),
    path('trakt/left-trassa/<int:pk>/<int:id>/', left_trassa, name='left_trassa'),
    path('trakt/right-trassa/<int:pk>/<int:id>/', right_trassa, name='right_trassa'),
    path('trakt/save-trassa/<int:pk>/', save_trassa, name='save_trassa'),


    url(r'collect_trassa/$', views.trassa, name='trassa'),

    path('', include(router.urls))

]