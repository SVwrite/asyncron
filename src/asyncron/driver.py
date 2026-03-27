"""
The obejctive of this package is to make a pacakge that allows users to convert non-async functions to run as coroutines 
1. Generate a new event loop if there isn't any 
2. Wrap a function in a wrappper to make it a coroutine 
3. Run a cron job in the event loop inturrupting the sleep to make sure that job runs at time. 
4. Adjustment for the time lost in execution and sleep 
"""
from typing import Callable, Coroutine, Awaitable, Tuple, Union
import asyncio
from asyncio import coroutines, BaseEventLoop
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
                    return self._event_loop
        except RuntimeError:
            pass
        self._event_loop, self._thread = _get_event_loop()
    
    @property
    def event_loop(self):
        return self._event_loop
    

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
    def make_async(c : Union[Callable, Awaitable]) -> Callable:
        if isinstance(c, Callable):
            if inspect.iscoroutinefunction(c):
                return c            
            return  AsynCron._wrap(c)
        
        raise TypeError("Expecting Callable objects!")


        



    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        pass



def close(loop: asyncio.AbstractEventLoop):
    loop.call_soon_threadsafe(loop.stop)


LOOP: asyncio.AbstractEventLoop = None
THREAD: threading.Thread = None
def _get_event_loop() -> Union[asyncio.AbstractEventLoop, threading.Thread]:
    global LOOP, THREAD
    loop = LOOP
    new_thread = THREAD

    _thread_good = lambda : THREAD is not None and THREAD.is_alive()
    _loop_good = lambda : loop is not None and loop.is_running()

    if _thread_good and _loop_good:
        return loop, new_thread
    
    if _thread_good:
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

def run_async(fn: Callable) -> Coroutine[None, None, None]:
    print(fn)
    # nue = fn()
    nue = None


    if inspect.iscoroutinefunction(fn):
        print("Function is a Coroutine function")
    if inspect.iscoroutine(fn):
        print("Function is a coroutine")
    if inspect.iscoroutine(nue):
        print("Nue is coroutine")
    if inspect.iscoroutinefunction(nue):
        print("Nue is not a coroutine function")

    if isinstance(fn, Callable):
        print("function is callable")
    if isinstance(fn, Awaitable):
        print("function is awaitable")
    
    if isinstance(fn, Coroutine):
        print("Function is a Coroutine")
    loop, thread = _get_event_loop()
    print(loop.is_running(), "Loop running")

    # task = asyncio.create_task(fn())
    task = loop.create_task(fn())
    time.sleep(2)

    
    close(loop)


    

    # print(loop)
    # nue.close()

async def some_function():
    print("I am running in an event loop")


if __name__ == "__main__":
    run_async(some_function)