import logging
import functools


lg = logging.getLogger('starter_app')


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


def set_logger(lg, level):
    lg.setLevel(level)
    for hdr in lg.handlers:
        if hdr.level > level:
            hdr.setLevel(level)


def log_call(args=False, kwargs=False):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*_args, **_kwargs):
            argstr = ' '.join(filter(lambda x: x, [f'args={_args}' if args else '', f'kwargs={_kwargs}' if kwargs else '']))
            lg.info(f'call {func.__name__}({argstr})')
            return func(*_args, **_kwargs)
        return wrapper
    return deco
