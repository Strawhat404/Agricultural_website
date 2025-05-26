import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('agriconnect')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'update-weather-data': {
        'task': 'apps.weather.tasks.update_weather_data',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'update-weather-forecasts': {
        'task': 'apps.weather.tasks.update_weather_forecasts',
        'schedule': crontab(hour='*/3'),  # Every 3 hours
    },
    'check-weather-alerts': {
        'task': 'apps.weather.tasks.check_weather_alerts',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 