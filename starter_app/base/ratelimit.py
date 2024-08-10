
from ..errors import OperationNotAllowed
from ..lib.redis import redis
from ..log import lg


lg = lg.getChild('ratelimit')


class RateLimiter:
    def __init__(self, topic: str, limit: int, in_seconds: int):
        self.topic = topic
        self.limit = limit
        self.in_seconds = in_seconds

    def _key(self, key):
        return f'ratelimit:{self.topic}:{key}'

    def get(self, key):
        v = redis.get(self._key(key))
        if v is not None:
            return int(v)
        return None

    def check(self, key, raise_exception=True):
        fullkey = self._key(key)
        _v = redis.get(fullkey)
        v = int(_v) if _v is not None else 0
        if v >= self.limit:
            lg.debug(f'{fullkey} exceeded: {v} >= {self.limit}')
            if raise_exception:
                raise OperationNotAllowed('超出频率限制')
            return False
        return True

    def incr(self, key):
        # use Pattern 2 in https://redis.io/commands/incr/
        fullkey = self._key(key)
        v = redis.incr(fullkey)
        if v == 1:
            redis.expire(fullkey, self.in_seconds)
        lg.debug(f'{fullkey} incr to {v}')

    # @contextmanager
    # def context(self):
    #     count = redis.get(self._key) or 0
    #     yield
