import os
from dotenv import load_dotenv
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Create Celery beat schedule:
celery_get_manifest_schedule = {
    'schedule-name': {
        'task': 'app.getManifest.periodic_run_get_manifest',
        'schedule': timedelta(seconds=300),
    },
}


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "you-will-never-guess")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['petitpatrice@gmail.com']
    POSTS_PER_PAGE = 3
    LANGUAGES = ['en', 'fr']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or \
        'http://localhost:9200'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
