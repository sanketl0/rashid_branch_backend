import tracemalloc
import functools
from django.conf import settings


def memory_profile(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if settings.DEBUG:
            tracemalloc.start()

        try:
            # Execute the original function
            result = func(*args, **kwargs)
            return result
        finally:
            if settings.DEBUG:
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                print(f"Current memory usage: {current / 10 ** 6} MB")
                print(f"Peak memory usage: {peak / 10 ** 6} MB")
    return wrapper