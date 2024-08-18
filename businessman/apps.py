from django.apps import AppConfig


class BusinessmanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'businessman'

    def ready(self):
        import businessman.signals
