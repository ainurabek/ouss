from django.urls import path
from django.urls import include
from django.conf.urls import url
from apps.management import views

from apps.management.views import tpo_list, outfit_list, point_list, lp_list, trakt_list,\
   lp_create, trakt_create, trakt_delete, lp_delete, trakt_edit, lp_edit, select_obj,\
   save_trassa, left_trassa, right_trassa, region_list, form51_delete



app_name = 'management'

urlpatterns = [
    path('', lp_list, name='lp'),
    path('create/', lp_create, name='lp_create'),
    path('lp/delete/<int:pk>/', lp_delete, name='lp_delete'),
    path('lp/<int:pk>/edit/', lp_edit, name='lp_edit'),
    path('tpo/', tpo_list, name='tpo'),
    path('outfits/', outfit_list, name='outfit'),
    path('points/', point_list, name='point'),

    path('trakt/<int:lp_id>/', trakt_list, name='trakt'),
    path('trakt/create/<int:lp_id>/', trakt_create, name='trakt_create'),
    path('trakt/<int:pk>/edit/', trakt_edit, name='trakt_edit'),
    path('trakt/delete/<int:pk>/', trakt_delete, name='trakt_delete'),

    path('select-object/<int:pk>/', select_obj, name='select_obj'),
    path('create-trassa/<int:pk>/<int:id>/', left_trassa, name='left_trassa'),
    path('trassa/<int:pk>/<int:id>/', right_trassa, name='right_trassa'),
    path('save-trassa/<int:pk>/', save_trassa, name='save_trassa'),

    path('region', region_list, name='region_list'),
    url(r'^(?P<slug>\S+)/list/$', views.form51_list, name='form51'),
    url(r'^(?P<slug>\S+)/form51/create/$', views.form51_create, name='form51_create'),
    url(r'^(?P<slug>\S+)/form51/edit/(?P<pk>\d+)/$', views.form51_edit, name='form51_edit'),
    path('form51/delete/<int:pk>/', form51_delete, name='form51_delete'),

]
