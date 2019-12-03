from __future__ import annotations
from .system import System
import numbers
import typing


class Point():
    def __init__(self, coordinates: typing.List[float]):
        self.round = 3
        self.type = 'Point'
        self.coordinates = list(coordinates)
        self.dimension = len(coordinates)

    def __str__(self):
        return '{0} {1}'.format(self.type, [round(x, self.round) for x in self.coordinates])

    def __getitem__(self, arg):
        self.__check_number(arg)
        return self.coordinates[arg]

    def __setitem__(self, key, value):
        self.coordinates[key] = value

    def __hash__(self):
        return hash(self.coordinates)

    def shift(self, x: int, y: int):
        return Point([self.coordinates[0] + x, self.coordinates[1] + y])

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]


    @staticmethod
    def __check_number(value):
        if not Point.__is_number(value): raise TypeError

    @staticmethod
    def __is_number(value):
        return isinstance(value, numbers.Number)
