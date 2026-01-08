from prometheus_fastapi_instrumentator import Instrumentator


class Debugger(object):

    def __init__(self):
        self.__instrumentator: Instrumentator | None = None

    def init_app(self, app: object) -> None:
        self.__instrumentator = Instrumentator().instrument(app).expose(app)

    @property
    def instrumentator(self) -> Instrumentator:
        if not self.__instrumentator:
            raise ValueError("Debugger not initialized")
        return self.__instrumentator


debugger = Debugger()
