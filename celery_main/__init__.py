from olx import tasks as scrapy_tasks
from olx import dump as dump_tasks

"""
Allow Celery to discover tasks
"""

__all__ = ["scrapy_tasks", "dump_tasks"]
