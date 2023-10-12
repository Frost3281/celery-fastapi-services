from fastapi import APIRouter
from fastapi.responses import UJSONResponse

from .app import celery_app_instance
from .models import CeleryTaskNoParams
from .tools import (
    get_celery_task_result,
    get_running_celery_tasks,
    kill_celery_tasks,
)

celery_router = APIRouter(
    prefix='/celery',
    tags=['Работа с тасками Celery'],
    default_response_class=UJSONResponse,
)


@celery_router.get('/tasks/get/all', response_model=list[CeleryTaskNoParams])
def get_running_tasks():
    """Получить все запущенные Celery-таски."""
    return get_running_celery_tasks(celery_app_instance)


@celery_router.get('tasks/get/{task_id}')
def get_task_state(task_id: str):
    """Статус таска."""
    return UJSONResponse(
        content={'message': get_celery_task_result(task_id, celery_app_instance)},
    )


@celery_router.post('tasks/kill/all')
def kill_all_tasks():
    """Убиваем все таски."""
    killed_tasks = kill_celery_tasks(celery_app=celery_app_instance)
    return UJSONResponse(
        content={'message': 'tasks were killed', 'task_ids': killed_tasks},
    )


@celery_router.post('tasks/kill/ids')
def kill_tasks_by_ids(task_ids: list[str]):
    """Убиваем таски по ID."""
    killed_tasks = kill_celery_tasks(
        celery_app=celery_app_instance,
        task_selector=lambda task: task.id in task_ids,
    )
    return UJSONResponse(
        content={'message': 'tasks were killed', 'task_ids': killed_tasks},
    )
