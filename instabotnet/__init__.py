from .bot import Bot
from .execute import execute
import asyncio
import atexit
import concurrent.futures.thread




async def async_execute(script, variables={}, Executor=concurrent.futures.ThreadPoolExecutor(max_workers=5)):
    loop = asyncio.get_event_loop()
    atexit.unregister(concurrent.futures.thread._python_exit)
    # Executor.shutdown = lambda wait: None
    return await loop.run_in_executor(Executor, lambda: execute(script, variables))


