from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.form51 import views


app_name = 'form51'

router = routers.DefaultRouter()

urlpatterns = [
    path("", views.Form51ListView.as_view(), name="form_list"),
    path("regions/", views.RegionListView.as_view(), name="region_list"),
    path("reserve/<int:pk>/", views.ReserveDetailView.as_view(), name="reserve_detail"),
    path("region/<slug:slug>/", views.FilterForm51View.as_view(), name="filter_form51"),
    path("update/<int:pk>/", views.Form51UpdateView.as_view(), name="form_update"),
    path("create/<int:pk>/", views.Form51CreateView.as_view(), name="form_create"),
    path("delete/<int:pk>/", views.form51_delete, name="form_delete"),
    path("api/", views.FormListAPIView.as_view()),
    path("api/regions/", views.RegionListAPIView.as_view()),
    path("api/update/<int:pk>/", views.Form51UpdateAPIView.as_view()),
    path("api/delete/<int:pk>/", views.Form51DeleteAPIView.as_view()),
    path("api/create/<int:pk>/", views.FormCreateViewAPI.as_view()),
    path("api/reserve/<int:pk>/", views.ReserveDetailAPIView.as_view()),

    path("api/reserve/delete/<int:form_pk>/<int:reserve_pk>/", views.ReserveDelete.as_view()),

    path("upload/", views.ImageView.as_view(), name='file-upload'),

    path('', include(router.urls))
]

