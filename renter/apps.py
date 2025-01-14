from django.apps import AppConfig


class RenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'renter'

    def ready(self):
        super().ready()
        import renter.signals

