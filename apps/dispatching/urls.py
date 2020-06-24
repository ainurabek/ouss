from django.urls import path
from apps.dispatching.views import *
from . import views


app_name = 'dispatching'

urlpatterns = [
    path('', views.JournalList.as_view(), name='types_journals'),
    path('journal/<int:journal_pk>/', views.event_list, name='event_list'),
    path('event/create/<int:pk>/', views.EventCreateView.as_view(), name='event_create'),
    path('event/detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('event/delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('api/list/', views.EventListAPIView.as_view()),


]