from django.urls import path
from apps.dispatching.views import *
from . import views



app_name = 'dispatching'



urlpatterns = [
    path('', views.JournalList.as_view(), name='types_journals'),
    # path('journal/<int:journal_pk>/', views.event_list, name='event_list'),
    # path('event/create/<int:pk>/', views.EventCreateView.as_view(), name='event_create'),
    path('event/detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('event/delete/<int:pk>/', views.event_delete, name='event_delete'),


    #api
    path('api/list/', views.EventListAPIView.as_view({'get': 'list'}), name="api_list_event"),
    path('api/detail/<int:pk>/', views.EventListAPIView.as_view({'get': 'retrieve'}), name="api_detail_event"),
    path("api/event/edit/<int:pk>/", views.EventUpdateAPIView.as_view()),
    path("api/event/delete/<int:pk>/", views.EventDeleteAPIView.as_view()),

    #if IPS
    path("api/event/ips/", views.IPEventListAPIView.as_view()),
    path("api/event/ips/create/<int:pk>/", views.EventIPCreateViewAPI.as_view()),

    #if circuits
    path("api/event/circuits/", views.CircuitEventListAPIView.as_view()),
    path("api/event/circuits/create/<int:pk>/", views.EventCircuitCreateViewAPI.as_view()),

    #if objects
    path("api/event/objects/", views.ObjectEventListAPIView.as_view()),
    path("api/event/objects/create/<int:pk>/", views.EventObjectCreateViewAPI.as_view()),




]