import datetime

import pytest
from asyncron import Schedule, to_seconds, to_timedelta, to_datetime

def test_assignment():

    with pytest.raises(TypeError) as err:
        sch = Schedule().days("10")
        print(sch._days)
    assert "days must be integer" in str(err.value)

    with pytest.raises(ValueError) as err:
        sch = Schedule().days(-1)
    assert "days can not be negative"

    sch = Schedule().days(10).hours(10).minutes(10).seconds(10)
    assert sch._days == 10
    assert sch._hours == 10
    assert sch._minutes == 10
    assert sch._seconds == 10


def test_schedule_conversions():

    sch = Schedule().minutes(1).seconds(10)
    assert to_seconds(sch) == 70

    assert to_timedelta(sch) == datetime.timedelta(seconds=70)

    now = datetime.datetime.now()
    assert to_datetime(now=now, sch=sch).second == now.second + 10
    assert to_datetime(now=now, sch=sch).minute == now.minute + 1

