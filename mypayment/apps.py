from django.apps import AppConfig


class MypaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mypayment'

    def ready(self):
        import mypayment.signals
