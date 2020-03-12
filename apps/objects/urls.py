from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import ObjectsLPListView, TraktListView, LPCreateView, LPEditView, TPOCreateView, \
    TPOEditView, OutfitCreateView, OutfitEditView

app_name = 'objects'

router = routers.DefaultRouter()
router.register('tpo', views.TPOListView, basename='tpo_list')
router.register('outfit', views.OutfitsListView, basename='outfit_list')




urlpatterns = [

    path('tpo/create/', TPOCreateView.as_view(), name='tpo_create'),
    url(r'^tpo/edit/(?P<pk>\S+)/$', TPOEditView.as_view()),
    url(r'^tpo/delete/(?P<tpo_id>\S+)/$', views.tpo_delete_view, name='tpo_delete'),

    path('outfit/create/', OutfitCreateView.as_view(), name='outfit_create'),
    url(r'^outfit/edit/(?P<pk>\S+)/$', OutfitEditView.as_view()),
    url(r'^outfit/delete/(?P<outfit_id>\S+)/$', views.outfit_delete_view, name='outfit_delete'),

    url(r'collect_trassa/$', views.trassa, name='trassa'),
    path('lp/', ObjectsLPListView.as_view({'get': 'list'}), name='objects_lp'),
    path('lp/<int:pk>/', TraktListView.as_view(), name='objects_trakts'),
    path('lp/create/', LPCreateView.as_view(), name='lp_create'),
    url(r'^lp/edit/(?P<pk>\S+)/$', LPEditView.as_view(), name='lp_edit'),

    # path('lp/trakt/<int:pk>/', views.get_pg, name='objects_pg'),
    # path('lp/trakt/vg/<int:pk>/', views.get_vg, name='objects_vg'),

    path('', include(router.urls))

]