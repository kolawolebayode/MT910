from django.apps import AppConfig


class SwiftappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'swiftapp'


    #Apscheduler this runs the task
    def ready(self):
        from task import updater
        #updater.start()
 

