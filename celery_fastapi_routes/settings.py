import os

REDIS_HOST = os.environ.get('REDIS_HOST') or 'redis'
REDIS_URL = f'redis://{REDIS_HOST}:6379'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or f'redis://{REDIS_HOST}:6379'
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or f'redis://{REDIS_HOST}:6379'
CELERY_ACCEPT_CONTENT = ('application/json',)
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
