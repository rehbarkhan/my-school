import os
from django.conf import settings
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# celery configuration
app.conf.broker_url = "redis://:coolpassword@127.0.0.1:6379/0"
app.conf.result_accept_content = ['json']
app.conf.task_compression = 'bzip2'
app.conf.task_serializer = 'json'
app.conf.result_extended = True
app.conf.result_backend ='django-db'

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')