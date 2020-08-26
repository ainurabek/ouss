from django.urls import path, include
from apps.dispatching.views import *
from . import views
from rest_framework import routers

from .views import OutfitWorkerAPIView

app_name = 'dispatching'

router = routers.DefaultRouter()


router.register('comment', views.CommentModelViewSet, basename='comment')


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

    #outfit_worker
    path("api/outfit_worker/", views.OutfitWorkerAPIView.as_view()),
    path("api/outfit_worker/create/", views.OutfitWorkerCreateView.as_view()),
    path("api/outfit_worker/edit/<int:pk>/", views.OutfitWorkerEditView.as_view()),
    path("api/outfit_worker/delete/<int:pk>/", views.OutfitWorkerDeleteAPIView.as_view()),

    #передавать сотрудникв предприятий
    path("api/outfit_worker/<int:pk>/", views.OutfitWorkerGet.as_view()),

    #unknown events
    path("api/event/unknown/", views.UnknownEventListAPIView.as_view()),
    path("api/event/unknown/create/", views.EventUnknownCreateViewAPI.as_view()),


    #статистика за месяц-неедлю-сегодня
    path("api/event/week/", views.get_dates_and_counts_week),
    path("api/event/month/", views.get_dates_and_counts_month),
    path("api/event/today/", views.get_dates_and_counts_today),
    path("api/event/precent-month/", views.get_outfit_statistics_for_a_month),
    path("api/event/precent-week/", views.get_outfit_statistics_for_a_week),
    path("api/event/precent-day/", views.get_outfit_statistics_for_a_day),
    path("api/event/completed-list/", views.CompletedEvents.as_view()),
    #статистика незавершенных событий
    path("api/uncompleted/event/", views.UncompletedEventList.as_view()),

    #comments
    path('', include(router.urls)),

]