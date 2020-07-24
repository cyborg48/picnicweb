from django.apps import AppConfig


class MyPicnicsConfig(AppConfig):
    name = 'mypicnics'

    def ready(self):
        import mypicnics.signals