def on_exception_returns(response_class):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                response = response_class()
                response.content = str(e)
                return response
        return wrapper
    return decorator