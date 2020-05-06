from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls import include
from apps.accounts import urls as accounts_urls
from apps.dispatching import urls as dispatching_urls
from apps.opu import urls as opu_urls

router = DefaultRouter()



app_name = 'apps'


urlpatterns = [
    path('accounts/', include(accounts_urls, namespace='accounts')),
    path('dispatching/', include(dispatching_urls, namespace='dispatching')),
    path('opu/', include(opu_urls, namespace='opu')),
    path('', include(router.urls)),

]
