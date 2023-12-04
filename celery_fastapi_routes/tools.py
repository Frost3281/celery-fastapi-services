from datetime import datetime
from typing import Any, Callable, Union

from celery import Celery, states
from celery.result import AsyncResult
from celery.utils.saferepr import saferepr

from celery_fastapi_routes.models import CeleryTask

DictParams = dict[str, Union[str, datetime]]
CeleryTasksDictValue = list[dict[str, str]]
CeleryTasksDataResponse = dict[str, CeleryTasksDictValue]

TaskSelector = Callable[[CeleryTask], bool]


def kill_celery_tasks(
    celery_app: Celery,
    task_selector: TaskSelector = lambda celery_task: True,  # noqa: ARG005
) -> list[str]:
    """Убить Celery-таски."""
    killed_tasks = []
    for task in get_running_celery_tasks(celery_app, task_selector):
        celery_app.control.revoke(
            task.id, terminate=True, signal='SIGKILL',
        )
        killed_tasks.append(task.id)
    return killed_tasks


def get_running_celery_tasks(
    app: Celery, task_selector: TaskSelector = lambda celery_task: True,  # noqa: ARG005
) -> list[CeleryTask]:
    """Получаем данные по работающим таскам."""
    active_workers = app.control.inspect(timeout=5).active()
    return _celery_tasks_data_to_list(active_workers, task_selector)


def get_celery_task_result(task_id: str, app: Celery) -> dict[str, Any]:
    """Получаем статус выполнения и результаты celery-таска."""
    task_result = AsyncResult(id=task_id, app=app)
    return celery_result_to_dict(task_result)


def celery_result_to_dict(task_result: AsyncResult) -> dict[str, str]:
    """Трансформация AsyncResult в словарь."""
    response_data = {
        'task_id': task_result.task_id,
        'status': task_result.state,
        'result': task_result.result,
    }
    if task_result.state in states.EXCEPTION_STATES:
        response_data.update(
            {
                'result': saferepr(task_result.result),
                'exc': saferepr(task_result.result),
            },
        )
    return response_data


def flatten(main_list: list[list[Any]]) -> list[Any]:
    """Список списков в список."""
    return [any_item for sublist in main_list for any_item in sublist]


def _celery_tasks_data_to_list(
    celery_tasks: CeleryTasksDataResponse,
    task_selector: Callable[[CeleryTask], bool],
) -> list[CeleryTask]:
    """Трансформируем словарь от Celery о работающих воркерах в список CeleryTask."""
    tasks = flatten(list(celery_tasks.values()))
    return [CeleryTask(**task) for task in tasks if task_selector(CeleryTask(**task))]
