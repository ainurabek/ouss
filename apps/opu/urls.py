from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from apps.opu.objects import urls as objects_urls
from apps.opu.circuits import urls as circuits_urls
from apps.opu.customer import urls as customer_urls
from apps.opu.management import urls as management_urls
from apps.opu.form51 import urls as form51_urls
from apps.opu.forma51_v2 import urls as forma51_v2_urls



app_name = 'opu'

router = routers.DefaultRouter()






urlpatterns = [

    path('objects/', include(objects_urls, namespace='objects')),
    path('circuits/', include(circuits_urls, namespace='circuits')),
    path('customer/', include(customer_urls, namespace='customer')),
    path('form51/', include(form51_urls, namespace='form51')),
    path('management/', include(management_urls, namespace='management_url')),
    path('form51-v2/', include(forma51_v2_urls, namespace='forma51_v2')),


    path('', include(router.urls)),

]