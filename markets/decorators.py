from redis import Redis
from django.conf import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def on_exception_returns(response_class, name=None):
    def decorator(function):
        qln = function.__qualname__

        def proxy(*args, **kwargs):
            key = f'{qln}:{name}:{kwargs[name]}' if name is not None and name in kwargs else None
            try:
                if key is not None and redis.get(key):
                    raise ValueError(f'Не удалось обработать значение: {kwargs[name]}')
                return function(*args, **kwargs)
            except Exception as e:
                if key is not None:
                    redis.set(name=key, value=1, ex=settings.FAIL_EXPIRE_SECONDS)
                response = response_class()
                response.content = str(e)
                return response
        return proxy
    return decorator
