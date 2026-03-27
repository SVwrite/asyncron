"""
The obejctive of this package is to make a pacakge that allows users to convert non-async functions to run as coroutines 
1. Generate a new event loop if there isn't any 
2. Wrap a function in a wrappper to make it a coroutine 
3. Run a cron job in the event loop inturrupting the sleep to make sure that job runs at time. 
4. Adjustment for the time lost in execution and sleep 
"""
from threading import Thread
from typing import Callable, Coroutine, Awaitable, Tuple, Union, Any
import asyncio
from asyncio import coroutines, BaseEventLoop, AbstractEventLoop
import inspect
import threading
import time
import threading
import sys


class AsynCron:

    _event_loop: asyncio.AbstractEventLoop = None
    _thread: threading.Thread = None
    
    def __init__(self):
        try:
            if self._event_loop is not None and hasattr(self._event_loop, "is_running"):
                if self._event_loop.is_running():
                    return
        except RuntimeError:
            pass
        self._event_loop, self._thread = _get_event_loop()
    
    @property
    def event_loop(self):
        return self._event_loop
    
    @property
    def thread(self):
        return self._thread
    

    def __del__(self):
        if self._event_loop is not None:
            if self._event_loop.is_running():
                if self._thread is None:
                    self._event_loop.stop()
                else:
                    self._event_loop.call_soon_threadsafe(self._event_loop.stop)

        if self._thread is not None:
            self._thread.join()
    
    @staticmethod
    def _wrap(c: Callable):
        async def a(*args, **kwargs):
            return c(*args, **kwargs)
        a.__name__ = c.__name__
        return a
    
    @staticmethod
    def make_async(c : Union[Callable]) -> Callable:
        if isinstance(c, Callable):
            if inspect.iscoroutinefunction(c):
                return c            
            return  AsynCron._wrap(c)
        raise TypeError("Expecting Callable objects!")

    def _run(self, c: Coroutine) -> Any:
        if self._thread is not None and self._thread.is_alive() is False:
            self._event_loop, self._thread = _get_event_loop()
            return self._run(c)

        fut = asyncio.Future()
        async def _exec():
            res = await c
            fut.set_result(res)
        asyncio.run_coroutine_threadsafe(_exec(), self._event_loop)
        while not fut.done():
            pass
        return fut.result()
            

    def run(self, c: Union[Callable, Awaitable], *args, **kwargs) -> Any:
        if inspect.isawaitable(c):
            return self._run(c)
        if inspect.iscoroutinefunction(c):
            return self._run(c(*args, **kwargs))
        raise TypeError("Expecting coroutine function or coroutine!")

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, tb):
        pass

LOOP: asyncio.AbstractEventLoop = None
THREAD: threading.Thread = None
def _get_event_loop() -> tuple[AbstractEventLoop, Thread]:
    global LOOP, THREAD
    loop = LOOP
    new_thread = THREAD

    _thread_good = lambda : THREAD is not None and THREAD.is_alive()
    _loop_good = lambda : loop is not None and loop.is_running()

    if _thread_good() and _loop_good():
        return loop, new_thread
    
    if _thread_good():
        # Wait for thread to stop 
        THREAD.join(timeout=1)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
        loop = asyncio.new_event_loop()
        def love(lp):
            try:
                lp.run_forever()
            finally:
                lp.run_until_complete(loop.shutdown_asyncgens())
                lp.close()

        new_thread = threading.Thread(target=love, args=(loop,))
        new_thread.start()
        while not loop.is_running():
            time.sleep(0.2)
    LOOP = loop 
    THREAD = new_thread
    return loop, new_thread


if __name__ == "__main__":
    pass