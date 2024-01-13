from django.apps import AppConfig


class MensfashionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mensfashion'


    def ready(self):
        print("Ready method of YourAppConfig is called.")
