from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from knox import views as knox_views
from . import views

from .views import LoginAPI, UserViewSet, Register, LogoutView, ProfileListAPIView, CreateProfileAPIView, DepartmentKTAPIView
app_name = 'accounts'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profile_list', ProfileListAPIView)
router.register('departments', DepartmentKTAPIView)



urlpatterns = [
    url(r'^register/$', Register.as_view()),
    url(r'^login/$', LoginAPI.as_view()),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile_create/$', CreateProfileAPIView.as_view(), name='create_profile'),
    url(r'^departments/(?P<department_id>\S+)/$', views.department_view, name='department_view'),
    path('', include(router.urls))

]