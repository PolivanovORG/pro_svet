from django.apps import AppConfig


class ProSvetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pro_svet'

    def ready(self):
        import pro_svet.signals