import pytest
from asyncron import AsynCron
import asyncio
import time 

def test_singleton():
    cron1 = AsynCron()
    cron2 = AsynCron()
    id1 = id(cron1.event_loop)
    id2 = id(cron2.event_loop)
    print(id1, id2, id1 == id2)
    del cron1
    del cron2
    assert id1 == id2

def test_teardown():
    cron = AsynCron()
    thread = cron.thread
    loop = cron.event_loop
    assert thread.is_alive() is True 
    assert loop.is_running() is True
    del cron
    assert thread.is_alive() is False
    assert loop.is_running() is False
    assert loop.is_closed() is True

def test_new_thread():
    cron1 = AsynCron()
    assert cron1.thread is not None
    assert cron1.thread.is_alive()
    
def test_wrapper():
    async def main():
        def not_async(name: str):
            return f"Hello! {name}"

        cron = AsynCron()
        async1 = AsynCron.make_async(not_async)
        async2 = AsynCron.make_async(not_async)

        print(async1, async2)

        res1 = await async1("User")
        res2 = await async2(name="User")

        assert(res1 == "Hello! User")
        assert res1 == res2

        assert async1.__name__ == async2.__name__
        assert async1.__name__ == not_async.__name__

    asyncio.run(main())

@pytest.fixture
def new_asyncron():
    asyncron = AsynCron()
    yield asyncron
    del asyncron

def test_run(new_asyncron):
    def not_async():
        time.sleep(2)
        return "Success"

    # asyncron = AsynCron()
    asyncron = new_asyncron
    res = asyncron.run(asyncron.make_async(not_async))
    assert res == "Success"