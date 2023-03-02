from django.apps import AppConfig


class TypemonkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'typemonk'
    def ready(self):
        import typemonk.signals
