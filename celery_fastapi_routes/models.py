from datetime import datetime
from typing import Any, Union

from pydantic import BaseModel, validator

UsualDict = dict[str, str]
ArgsValue = Union[UsualDict, str]


class CeleryTaskNoParams(BaseModel):
    """Данные о таске Celery."""

    name: str
    id: str
    type: str
    hostname: str
    time_start: datetime
    acknowledged: bool
    worker_pid: int

    @validator('time_start', pre=True)
    def convert_float_time_to_dt(
        cls, time: Union[float, datetime], values,  # noqa: ARG002, N805
    ) -> datetime:
        """Конвертируем timestamp в datetime."""
        return datetime.fromtimestamp(time) if isinstance(time, float) else time


class CeleryTask(CeleryTaskNoParams):
    """Данные о таске Celery."""

    args: list[dict[str, ArgsValue]]
    kwargs: dict[str, Any]
