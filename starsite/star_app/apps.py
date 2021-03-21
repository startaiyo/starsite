from django.apps import AppConfig


class StarAppConfig(AppConfig):
    name = 'star_app'
    def ready(self):
        from . import scheduled
        scheduled.start()