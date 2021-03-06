from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls import include
from apps.accounts import urls as accounts_urls
from apps.dispatching import urls as dispatching_urls
from apps.opu import urls as opu_urls
from apps.analysis import urls as analysis_urls
from apps.secondary import urls as secondary_urls
from apps.logging import urls as logging_urls
from apps.views import MemoryInfoAPIView

router = DefaultRouter()


app_name = 'apps'


urlpatterns = [
    path('accounts/', include(accounts_urls, namespace='accounts')),
    path('dispatching/', include(dispatching_urls, namespace='dispatching')),
    path('opu/', include(opu_urls, namespace='opu')),
    path('analysis/', include(analysis_urls, namespace='analysis')),
    path('secondary/', include(secondary_urls, namespace='secondary')),
    path('logging/', include(logging_urls, namespace='logging')),
    path('memory-info/', MemoryInfoAPIView.as_view()),
    path('', include(router.urls)),

]
