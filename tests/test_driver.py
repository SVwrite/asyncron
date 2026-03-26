import pytest
from asyncron import AsynCron

def test_singleton():
    cron1 = AsynCron()
    cron2 = AsynCron()
    id1 = id(cron1.event_loop)
    id2 = id(cron2.event_loop)
    print(id1, id2, id1 == id2)
    del cron1
    del cron2
    assert id1 == id2
    
    
