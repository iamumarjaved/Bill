import os

from celery import Celery
from django.conf import settings
import sys

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app', broker=os.environ.get("CELERY_BROKER", "redis://redis:6379/0"), backend=os.environ.get("CELERY_BROKER", "redis://redis:6379/0"))
app.conf.broker_connection_retry_on_startup = True
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-task-every-5-minutes': {
        'task': 'core.tasks.download_file_FTP',  # Replace with the actual path to your task function
        'schedule': 7200.0,  # Run the task every 2hr (7200 seconds)
    },
}

# if 'runserver' in sys.argv:
#     # Discard pending tasks during hot reload
#     app.control.purge()