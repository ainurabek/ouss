from django.apps import AppConfig


class ObjectsConfig(AppConfig):
    name = 'apps.objects'

    def ready(self):
        import apps.objects.signals
