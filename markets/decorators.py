from redis import Redis
from django.conf import settings
from threading import Lock
from functools import wraps

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def on_exception_returns_response(response_class, name=None):
    """For API View`s methods. Defines response_class for response if some exceptions was raised.
    Also, prevents DDOS via frequently calls of failing methods"""
    def decorator(function):
        qln = function.__qualname__

        @wraps(function)
        def proxy(*args, **kwargs):
            fail_flag = f'{qln}:{name}:{kwargs[name]}:failed' if name is not None and name in kwargs else None
            try:
                if fail_flag is not None and redis.exists(fail_flag):
                    raise ValueError(f'Processing failed: {name}={kwargs[name]}')
                return function(*args, **kwargs)
            except Exception as e:
                if fail_flag is not None:
                    redis.set(name=fail_flag, value=1, ex=settings.FAIL_EXPIRE_SECONDS)
                response = response_class()
                response.content = str(e)
                return response

        proxy.__doc__ = qln
        return proxy
    return decorator


def on_exception_returns(result):
    def decorator(function):
        qln = function.__qualname__

        @wraps(function)
        def proxy(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception:
                return result

        proxy.__doc__ = qln
        return proxy
    return decorator


def globally_lonely_action(return_if_busy=None):
    """Creates system-wide "lonely" action like long-time database operation, etc."""
    def decorator(function):
        qln = function.__qualname__
        gla_lock = Lock()
        gla_name = f'GLA:{qln}:launched'

        def launched():
            with gla_lock:
                return redis.exists(gla_name)

        @wraps(function)
        def proxy(*args, **kwargs):
            with gla_lock:
                if not redis.set(name=gla_name, value=1, ex=1800, nx=True):
                    return return_if_busy
            try:
                return function(*args, **kwargs)
            finally:
                with gla_lock:
                    redis.delete(gla_name)

        proxy.__doc__ = qln
        proxy.launched = launched
        return proxy
    return decorator

