from __future__ import annotations
from .system import System
import numbers
import typing


class Point():
    def __init__(self, coordinates: typing.List[float], system: System = System()):
        self.round = 3
        self.system = system
        self.type = 'Point'
        try:
            if not coordinates:
                raise ValueError
            else:
                self.coordinates = tuple(coordinates)
                self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('wrong value')
        except TypeError:
            raise TypeError('coordinates is of wrong type')

    def __str__(self):
        return '{0} {1}'.format(self.type, [round(x, self.round) for x in self.coordinates])

    def __getitem__(self, arg):
        self.__check_number(arg)
        return self.coordinates[arg]

    @staticmethod
    def __check_number(value):
        if not Point.__is_number(value): raise TypeError

    @staticmethod
    def __is_number(value):
        return isinstance(value, numbers.Number)
