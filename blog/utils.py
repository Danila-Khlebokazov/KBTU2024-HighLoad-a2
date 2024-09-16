from django.core.cache import cache
from functools import wraps
from typing import Optional


def cache_decorator(cache_name: Optional[str] = None, timeout: int = 60):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            nonlocal cache_name
            if not cache_name:
                cache_name = f"{func.__module__}.{func.__name__}"

            print(cache_name)

            if (cached := cache.get(cache_name)) is not None:
                print(cached, "C")
                return cached

            result = func(*args, **kwargs)
            cache.set(cache_name, result, timeout)
            print(result)
            return result

        return inner

    return wrapper
