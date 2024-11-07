from redis import Redis
from django.conf import settings
from threading import Lock

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


def globally_lonely_action(function):
    gla_lock = Lock()
    gla_name = f'GLA:{function.__qualname__}:launched'

    def launched():
        with gla_lock:
            return redis.exists(gla_name)

    def proxy(*args, **kwargs):
        with gla_lock:
            if redis.exists(gla_name):
                return None
            redis.set(name=gla_name, value=1, ex=1800)
        try:
            return function(*args, **kwargs)
        finally:
            with gla_lock:
                redis.delete(gla_name)

    proxy.launched = launched
    return proxy

