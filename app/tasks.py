from flask import current_app
from . import celery


@celery.task()
def add_together(a, b):
    app = current_app._get_current_object()