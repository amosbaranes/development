from django.apps import AppConfig


class CorporatevaluationConfig(AppConfig):
    name = 'academycity.apps.corporatevaluation'

    def ready(self):
        from .updater_api import start
        start()
