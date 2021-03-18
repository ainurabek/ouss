from django.urls import path, include
from apps.dispatching.views import *
from . import views
from rest_framework import routers

from .views import OutfitWorkerAPIView

app_name = 'dispatching'

router = routers.DefaultRouter()


router.register('comment', views.CommentModelViewSet, basename='comment')
router.register('type_journal', views.TypeJournalModelViewSet, basename='type_journal')
router.register('reason', views.ReasonModelViewSet, basename='reason')
router.register('index', views.IndexModelViewSet, basename='index')


urlpatterns = [

    #api
    path('api/list/', views.EventListAPIView.as_view({'get': 'list'}), name="api_list_event"),
    path('api/detail/<int:pk>/', views.EventListAPIView.as_view({'get': 'retrieve'}), name="api_detail_event"),
    # path('api/list/', views.event_list, name="api_list_event"),
    path('api/detail/<int:pk>/', views.EventDetailAPIView.as_view(), name="api_detail_event"),
    path("api/event/edit/<int:pk>/", views.EventUpdateAPIView.as_view()),
    path("api/event/delete/<int:pk>/", views.EventDeleteAPIView.as_view()),

    #if IPS
    path("api/event/ips/create/<int:pk>/", views.EventIPCreateViewAPI.as_view()),

    #if circuits
    path("api/event/circuits/create/<int:pk>/", views.EventCircuitCreateViewAPI.as_view()),

    #if objects

    path("api/event/objects/create/<int:pk>/", views.EventObjectCreateViewAPI.as_view()),

    #outfit_worker
    path("api/outfit_worker/", views.OutfitWorkerAPIView.as_view()),
    path("api/outfit_worker/create/", views.OutfitWorkerCreateView.as_view()),
    path("api/outfit_worker/edit/<int:pk>/", views.OutfitWorkerEditView.as_view()),
    path("api/outfit_worker/delete/<int:pk>/", views.OutfitWorkerDeleteAPIView.as_view()),

    #передавать сотрудникв предприятий - Айнур
    path("api/outfit_worker/<int:pk>/", views.OutfitWorkerGet.as_view()),


    #статистика за месяц-неделю-сегодня
    path("api/event/week/", views.get_dates_and_counts_week),
    path("api/event/month/", views.get_dates_and_counts_month),
    path("api/event/today/", views.get_dates_and_counts_today),

    #статистика событий по предприятиям за день-сегодня-месяц
    path("api/event/out-month/", views.get_outfit_statistics_for_a_month),
    path("api/event/out-week/", views.get_outfit_statistics_for_a_week),
    path("api/event/out-today/", views.get_outfit_statistics_for_a_day),
    #статистика завершенных событий по определнной дате
    path("api/event/completed-list/", views.CompletedEvents.as_view()),
    #статистика незавершенных событий
    path("api/event/uncompleted-list/", views.UncompletedEventList.as_view()),

    #фильтры для отчета
    path("api/reports/", views.get_report_object),
    #второй звонок
    path("api/event/calls/create/<int:pk>/", views.EventCallsCreateViewAPI.as_view()),

    path("api/unknown/event/create/", views.EventUnknownCreateViewAPI.as_view()),


    path('', include(router.urls)),

]