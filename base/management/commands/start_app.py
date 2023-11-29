# import os
# from django.core.management.base import BaseCommand
# from django.core.management import call_command
# from threading import Thread
# from datetime import datetime
# import time

# class Command(BaseCommand):
#     help = 'Starts the Gunicorn server and adds the django-crontab jobs'

#     def handle(self, *args, **kwargs):

#         # Add the django-crontab jobs
#         #call_command('crontab', 'add')
#         #call_command('crontab', 'show')
#         #call_command('update_free_credits')

#         # Start the Gunicorn server in a new thread
#         #Thread(target=os.system, args=('python manage.py runserver',)).start()
#         Thread(target=os.system, args=('gunicorn smartlearning.wsgi',)).start()
#         try:
#             while True:
#                 now = datetime.now()
#                 # If current hour is 0 (12:00 AM)
#                 if now.hour == 0:
#                     call_command('update_free_credits')
#                     time.sleep(3600)  # Sleep for an hour
#         except KeyboardInterrupt:
#             print("Stopping script...")

#         """while True:
#             call_command('update_free_credits')
#             time.sleep(120)"""


#Two Minutes update
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from threading import Thread
import time

class Command(BaseCommand):
    help = 'Starts the Gunicorn server and adds the django-crontab jobs'

    def handle(self, *args, **kwargs):

        # Add the django-crontab jobs
        #call_command('crontab', 'add')
        #call_command('crontab', 'show')
        #call_command('update_free_credits')

        # Start the Gunicorn server in a new thread
        #Thread(target=os.system, args=('python manage.py runserver',)).start()
        Thread(target=os.system, args=('gunicorn smartlearning.wsgi',)).start()
        while True:
            call_command('update_free_credits')
            time.sleep(120)


