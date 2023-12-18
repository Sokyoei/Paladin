"""
Abstract 抽象
"""

from abc import ABC, abstractmethod


class AbstractAnimal(ABC):
    __isalive = True

    def __init__(self, name, age) -> None:
        super().__init__(ABC)
        self.name = name
        self.age = age

    @abstractmethod
    def eat(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def isalive(cls) -> bool:
        return cls.__isalive
