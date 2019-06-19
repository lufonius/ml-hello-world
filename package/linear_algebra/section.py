from __future__ import annotations
from .line_copy import Line
from .vector import Vector
from .point import Point
from .utils import Utils
import typing

class Section(Line):
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
        self.start = start
        self.end = end


    # when the x or the y value are not within the section, then None is returned
    def get_y(self, x):
        if not Utils.within_range(self.start[0], self.end[0], x):
            return None

        shift = (x - self.x_shift) + (self.y_shift * self.normal_vector[1])
        nominator = (self.constant_term - self.normal_vector[0] * shift)
        dominator = self.normal_vector[1]

        y = nominator / dominator

        if not Utils.within_range(self.start[1], self.end[1], y):
            return None

        return y



