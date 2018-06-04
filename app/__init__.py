import logging
import eventlet
import os
from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from celery import Celery
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
socketio = SocketIO()
eventlet.monkey_patch()
# # Set Redis connection:
# redis_url = urlparse.urlparse(Config.REDIS_URL)
# r = redis.StrictRedis(host=redis_url.hostname,
#                       port=redis_url.port, db=1, password=redis_url.password)

# # Test the Redis connection:
# try:
#     r.ping()
#     print("Redis is connected!")
# except redis.ConnectionError:
#     print("Redis connection error!")


def create_app(config_class=Config):
    logging.getLogger('elasticsearch').setLevel(logging.DEBUG)
    logging.getLogger('urllib3').setLevel(logging.DEBUG)
    tracer = logging.getLogger('elasticsearch.trace')
    tracer.setLevel(logging.DEBUG)
    tracer.addHandler(logging.FileHandler('indexer.log'))
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL']) \
        if app.config['ELASTICSEARCH_URL'] else None
    celery.conf.update(BROKER_URL=app.config['REDIS_URL'],
                       CELERY_RESULT_BACKEND=app.config['REDIS_URL'])

    from app.errors import bp as errors_bp  # noqa: F401
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp  # noqa: F401
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp  # noqa: F401
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp, api   # noqa: F401
    app.register_blueprint(api_bp)

    socketio.init_app(app, async_mode='eventlet',
                      message_queue=app.config['REDIS_URL'])

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config["MAIL_PASSWORD"]:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER', app.config['MAIL_PORT']]),
                fromaddr='no-reply@' + app.config["MAIL_SERVER"],
                toaddrs=app.config['ADMINS'], subject="My Blog failure",
                credentials=auth, secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/myblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s \
            [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('MyBlog startup')

    return app


@babel.localeselector
def get_locale():
    # return "fr"
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models  # noqa: F401
from app import websocket  # noqa: F401
