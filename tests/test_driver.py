import pytest
from asyncron import AsynCron
import asyncio

def test_singleton():
    cron1 = AsynCron()
    cron2 = AsynCron()
    id1 = id(cron1.event_loop)
    id2 = id(cron2.event_loop)
    print(id1, id2, id1 == id2)
    del cron1
    del cron2
    assert id1 == id2
    
    
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



    # async def _run(c):
    #     await c

    # asyncio.run(_run(coro1))
    # asyncio.run(_run(coro2))
