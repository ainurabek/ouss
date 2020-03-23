from django.urls import path
from django.urls import include

from apps.management.views import tpo_list, outfit_list, point_list, lp_list, trakt_list,\
   lp_create, trakt_create, trakt_delete, lp_delete, trakt_edit, lp_edit



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

]
