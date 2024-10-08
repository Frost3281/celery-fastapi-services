from celery import Celery

from .settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

VISIBILITY_TIMEOUT = 60 * 60 * 24
celery_app_instance = Celery(
    'celery-application',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)
celery_app_instance.conf.update(CELERY_TRACK_STARTED=True)
celery_app_instance.conf.broker_transport_options = {
    'visibility_timeout': VISIBILITY_TIMEOUT,
}
celery_app_instance.conf.result_backend_transport_options = {
    'visibility_timeout': VISIBILITY_TIMEOUT,
}
celery_app_instance.conf.visibility_timeout = VISIBILITY_TIMEOUT
celery_app_instance.conf.worker_deduplicate_successful_tasks = True
