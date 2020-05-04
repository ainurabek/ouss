from django.urls import path
from apps.alarm_log.views import *

app_name = 'alarm_log'

urlpatterns = [
    path('create/', StatementCreateView.as_view(), name='statement_create'),
    path('shutdown/create/', ShutdownCreateView.as_view(), name='shutdown_create'),
    path('shutdown/list/', shutdown_list, name='shutdown_list'),
    path('shutdown/delete/<int:pk>/', shutdown_delete, name='shutdown_delete'),
    path('shutdown/update/<int:pk>/', ShutdownUpdateView.as_view(), name='shutdown_update'),
]