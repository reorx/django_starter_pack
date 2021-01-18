import logging
import functools


class PrefixLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, prefix):
        super().__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return f'[{self.prefix}] {msg}', kwargs


def func_name_logger(parent_logger):

    def real_decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['logger'] = PrefixLoggerAdapter(parent_logger, func.__name__)

            return func(*args, **kwargs)

        return wrapper

    return real_decorator
