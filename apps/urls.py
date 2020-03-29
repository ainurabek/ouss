from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls import include
from apps.accounts import urls as accounts_urls
from apps.objects import urls as objects_urls
from apps.circuits import urls as circuits_urls
from apps.customer import urls as customer_urls
from apps.management import urls as management_urls
from apps.form51 import urls as form51_urls


router = DefaultRouter()



app_name = 'apps'


urlpatterns = [
    path('accounts/', include(accounts_urls, namespace='accounts')),
    path('objects/', include(objects_urls, namespace='objects')),
    path('circuits/', include(circuits_urls, namespace='circuits')),
    path('customer/', include(customer_urls, namespace='customer')),
    path('form51/', include(form51_urls, namespace='form51')),
    path('management/', include(management_urls, namespace='management_url')),
    path('', include(router.urls)),

]
