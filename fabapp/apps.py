from django.apps import AppConfig
from django.conf import settings


class FabappConfig(AppConfig):
    name = 'fabapp'

    def ready(self):
        from fabapp import jobs
        jobs.Ratingjob()
        #jobs.Resetjob()
        #jobs.DisableExijob()
