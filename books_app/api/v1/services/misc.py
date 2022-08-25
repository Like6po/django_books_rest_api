from api.v1.consts import StatusValues


def decorate_class_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            func = getattr(cls, attr)
            if callable(func):
                setattr(cls, attr, decorator(func))
        return cls

    return decorate


def pass_exception_http_500(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return {'detail': 'Ошибка на сервере',
                    'status': StatusValues.FAILED.value,
                    'status_code': 500}

    return wrapper
