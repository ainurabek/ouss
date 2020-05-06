from django.urls import path
from apps.dispatching.views import *
from . import views


app_name = 'dispatching'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('request/create/', views.request_create, name='request_create'),
    path('request/<int:request_id>/edit/', views.request_edit, name='request_edit'),
    path('request/delete/<int:pk>/', views.request_delete, name='request_delete'),
    path('status/list/', views.status_list, name='status_list'),
    path('create/', StatementCreateView.as_view(), name='statement_create'),
    path('shutdown/create/', ShutdownCreateView.as_view(), name='shutdown_create'),
    path('shutdown/list/', views.shutdown_list, name='shutdown_list'),
    path('shutdown/delete/<int:pk>/', views.shutdown_delete, name='shutdown_delete'),
    path('shutdown/update/<int:pk>/', ShutdownUpdateView.as_view(), name='shutdown_update'),
]