from datetime import datetime
from typing import Any, Union

import pytz
from pydantic import BaseModel, field_validator

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

    @field_validator('time_start', mode='before')
    @classmethod
    def convert_float_time_to_dt(cls, time: Union[float, datetime]) -> datetime:
        """Конвертируем timestamp в datetime."""
        if isinstance(time, float):
            return datetime.fromtimestamp(time, tz=pytz.timezone('Europe/Moscow'))
        return time


class CeleryTask(CeleryTaskNoParams):
    """Данные о таске Celery."""

    args: Union[list[dict[str, ArgsValue]], Any, None] = None
    kwargs: Union[dict[str, Any], Any, None] = None
