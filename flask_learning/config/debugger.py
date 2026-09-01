from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension


class Debugger:

    def __init__(self):
        self.__debugger = DebugToolbarExtension()

    def init_app(self, app: Flask):
        self.__debugger.init_app(app)


debugger = Debugger()
