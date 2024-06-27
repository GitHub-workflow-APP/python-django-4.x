from django.apps import AppConfig


class SimpleXssConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simple_xss'
