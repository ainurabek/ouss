from django.apps import AppConfig


class ObjectsConfig(AppConfig):
    name = 'apps.opu.objects'

    def ready(self):
        import apps.opu.objects.signals
