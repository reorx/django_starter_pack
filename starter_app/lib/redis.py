
from django_redis import get_redis_connection
from redis import StrictRedis


# pass decode_responses=True to automatically decode bytes to str, so that .get() returns str not bytes
# redis = StrictRedis.from_url(REDIS_URL, decode_responses=True)

# although we can use the above code, but it's better to use django_redis to get the connection to avoid potential problems,
# just remember to .decode() bytes to str when needed
redis: StrictRedis = get_redis_connection('default')


class RedisStateBase:
    db: StrictRedis
    prefix: str
    key: str
    key_arg: str
    ex: int = None

    def __init__(self, key_arg):
        self.key = f'{self.prefix}{key_arg}'
        self.key_arg = key_arg

    def get(self):
        v = self.db.get(self.key)
        return v.decode() if v else None

    def set(self, value, ex=None):
        if ex is None:
            ex = self.ex
        self.db.set(self.key, value, ex=ex)

    def delete(self):
        self.db.delete(self.key)

    def publish(self, value):
        self.db.publish(self.key, value)
