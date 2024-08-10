from functools import wraps
from django.core.cache import cache
import logging


lg = logging.getLogger('app.cache')


def cached_func(key, timeout):
    """
    make a cached function by key
    """
    def deco(func):
        def get_key(*args, **kwargs):
            if callable(key):
                return key(*args, **kwargs)
            return key

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = get_key(*args, **kwargs)
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                lg.info(f'get cache {cache_key}')
                return cached_result
            result = func(*args, **kwargs)
            lg.info(f'set cache {cache_key} for {timeout}')
            cache.set(cache_key, result, timeout)
            return result

        wrapper.__cache_key__ = get_key
        return wrapper
    return deco


def clear_func_cache(func, *args, **kwargs):
    cache_key = func.__cache_key__(*args, **kwargs)
    lg.info(f'delete cache: {cache_key}')
    cache.delete(cache_key)
