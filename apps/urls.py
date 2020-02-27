from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls import include
from apps.accounts import urls as accounts_urls


router = DefaultRouter()



app_name = 'apps'


urlpatterns = [
    path('accounts/', include(accounts_urls, namespace='accounts')),
    path('', include(router.urls)),

]
