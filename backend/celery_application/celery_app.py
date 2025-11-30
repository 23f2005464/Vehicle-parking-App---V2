from app import app_init
from celery_application.celery_factory import celery_init_app

flask_app = app_init()
celery_app = celery_init_app(flask_app)
import celery_application.celery_schedule