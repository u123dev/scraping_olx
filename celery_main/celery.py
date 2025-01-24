from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

celery_app = Celery("tasks", broker="redis://redis:6379", backend="redis://redis:6379")

# Route 'scraping' and 'web_server' tasks to queues
celery_app.conf.task_routes = {
    "olx.tasks.*": {"queue": "scraping_queue"},
    "olx.dump.*": {"queue": "dumping_queue"},
}

# Define Queues
celery_app.conf.task_queues = {
    "scraping_queue": {"binding_key": "scraping_queue"},
    "dumping_queue": {"binding_key": "dumping_queue"},
}

celery_app.conf.update(
    timezone="Europe/Kiev",
    beat_max_loop_interval=691200,  # default 8 days in seconds
    broker_connection_retry_on_startup=True
)


celery_app.conf.beat_schedule = {
    "scraping": {
        "task": "olx.tasks.start_scraping",
        "schedule": timedelta(seconds=60),
    },
    "dumping": {
        "task": "olx.dump.dump_start",
        "schedule": crontab(hour=00, minute=28),  #
    },
}


# register tasks
celery_app.autodiscover_tasks()
