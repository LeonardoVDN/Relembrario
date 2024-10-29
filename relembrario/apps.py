# relembrario/apps.py
from django.apps import AppConfig

class RelembrarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relembrario'

    def ready(self):
        import relembrario.signals  # Assegure-se de que esta linha está presente
