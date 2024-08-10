import functools
import logging
import time


lg = logging.getLogger('app')
sql_lg = logging.getLogger('app.sql')

lg.info('app logger 已创建')


def set_logger(lg, level):
    lg.setLevel(level)
    for hdr in lg.handlers:
        if hdr.level > level:
            hdr.setLevel(level)


LOG_FORMAT = '%(name)s\t%(levelname)s\t%(asctime)s\t[%(funcName)s] %(message)s'


def configure_logger(lg, level, extra_handler=None, log_format=None, propagate=False):
    if not log_format:
        log_format = LOG_FORMAT
    lg.setLevel(level)

    # stream handler
    hdr = logging.StreamHandler()
    hdr.setFormatter(logging.Formatter(log_format, '%Y-%m-%dT%H:%M:%S'))
    lg.addHandler(hdr)
    lg.propagate = propagate

    if extra_handler:
        lg.addHandler(extra_handler)


def log_call(logger=None, show_args=False, show_kwargs=False):
    if logger is None:
        logger = lg
    def deco(func):
        @functools.wraps(func)
        def wrapper(*_args, **_kwargs):
            argstr = ' '.join(filter(lambda x: x, [f'args={_args}' if show_args else '', f'kwargs={_kwargs}' if show_kwargs else '']))
            t0 = time.time()
            r = func(*_args, **_kwargs)
            logger.info(f'call {func.__name__}({argstr}), took {int(1000 * (time.time() - t0))}ms')
            return r
        return wrapper
    return deco


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
