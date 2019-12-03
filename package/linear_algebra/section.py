from __future__ import annotations
from .line_copy import Line
from .vector import Vector
from .point import Point
from .utils import Utils
import typing

class Section(Line):
    __start = None
    __end = None

    def __init__(
            self,
            start: Point,
            end: Point,
            line: Line
    ):
        super().__init__(
            line.normal_vector,
            line.constant_term,
            line.x_shift,
            line.y_shift
        )
        self.__start = start
        self.__end = end

    @property
    def start(self) -> Point:
        return self.__start

    @start.setter
    def start(self, value: Point) -> None:
        self.__start = value

    @property
    def end(self) -> Point:
        return self.__end

    @end.setter
    def end(self, value: Point) -> None:
        self.__end = value






