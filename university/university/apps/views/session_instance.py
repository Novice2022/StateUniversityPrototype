from django.contrib.sessions.backends.db import SessionStore


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if not (cls in cls._instances):
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    

class Session(metaclass=MetaSingleton):
    def __init__(self):
        self.__session = SessionStore()

    @property
    def session(self) -> SessionStore:
        return self.__session
