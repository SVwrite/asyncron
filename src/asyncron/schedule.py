import datetime
from typing import Callable
import functools

class Schedule:

    def __init__(self):
        self._days: int = 0
        self._hours: int = 0
        self._minutes: int = 0
        self._seconds: int = 0

    @staticmethod
    def _validate(fn: Callable):
        @functools.wraps(fn)
        def wrap(obj, value: int):
            if not isinstance(value, int):
                raise TypeError(f"{fn.__name__} must be integer")
            if value < 0:
                raise ValueError(f"{fn.__name__} can not be negative")
            return fn(obj, value)
        return wrap

    @staticmethod
    def _assign(fn: Callable):
        @functools.wraps(fn)
        def wrap(obj, value: int):
            attr = f"_{fn.__name__}"
            setattr(obj, attr, value)
            return obj
        return wrap

    @_validate
    @_assign
    def days(self, days: int):
        pass

    @_validate
    @_assign
    def hours(self, hours: int):
        pass

    @_validate
    @_assign
    def minutes(self, minutes: int):
        pass

    @_validate
    @_assign
    def seconds(self, seconds: int):
        pass


def to_seconds(sch: Schedule) -> int:
    return sch._days * 24*3600 + sch._hours * 3600 + sch._minutes * 60  + sch._seconds

def to_timedelta(sch: Schedule) -> datetime.timedelta:
    return datetime.timedelta(seconds=to_seconds(sch))

def to_datetime(sch: Schedule, now: datetime.datetime = None) -> datetime.datetime:
    if now is None:
        now = datetime.datetime.now(tz=datetime.UTC)
    return now + to_timedelta(sch)
