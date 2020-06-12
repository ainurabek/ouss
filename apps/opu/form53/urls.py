from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.form53 import views


app_name = 'form53'

router = routers.DefaultRouter()

urlpatterns = [
    ###HTML
    path("regions/", views.Region53ListView.as_view(), name="region53_list"),
    path("region/<slug:slug>/", views.FilterForm53View.as_view(), name="filter_form53"),
    path("", views.Form53ListView.as_view(), name="form53_list"),
    path("edit/<int:pk>/", views.Form53UpdateView.as_view(), name="form53_update"),
    path("create/<int:pk>/", views.Form53CreateView.as_view(), name="form53_create"),
    path("delete/<int:pk>/", views.form53_delete, name="form53_delete"),

    ###API
    path("<int:pk>/create/", views.Form53CreateViewAPI.as_view()),
    path("list/", views.Form53ListAPIView.as_view()),
    path("api/regions/", views.Region53ListAPIView.as_view()),
    path("<int:pk>/edit/", views.Form53UpdateAPIView.as_view()),
    path("<int:pk>/delete/", views.Form53DeleteAPIView.as_view()),

    path('', include(router.urls))
]

