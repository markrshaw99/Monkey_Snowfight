from django.apps import AppConfig


class AUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monkeyusers'
    
    def ready(self):
        import monkeyusers.signals
