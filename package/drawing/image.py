from __future__ import annotations
import numpy
import typing
import cv2 as cv
from package.linear_algebra.section import Section
from package.linear_algebra.point import Point
from package.utils.origin_transform_strategies import math_to_image, image_to_math
from package.linear_algebra.line_copy import Line
import math


class Image():
    __image = None
    __height = None
    __width = None

    def __init__(self, image: numpy.ndarray):
        self.image = image

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    @property
    def image(self) -> numpy.ndarray:
        return self.__image

    @image.setter
    def image(self, value: numpy.ndarray) -> None:
        self.__height = value.shape[0]
        self.__width = value.shape[1]
        self.__image = value

    def set_pixel(self, p: Point, color: typing.List[int]):
        new_point = math_to_image(p, self.width, self.height)
        self.image[new_point[1], new_point[0]] = color

    def get_pixel(self, p: Point) -> typing.List[int]:
        new_point = math_to_image(p, self.width, self.height)
        return self.image[new_point[1], new_point[0]]

    def pixels(self):
        for (y, x) in numpy.ndindex(self.image.shape[:2]):
            math_pixel = image_to_math(Point([x, y]), self.width, self.height)
            yield (Point([x, y]), math_pixel)

    def image_pixels(self):
        width = self.image.shape[1] - 1
        height = self.image.shape[0] - 1
        return [Point([x, y]) for (y, x) in numpy.ndindex((height, width))]

    def section_points(self, section: Section):
        start = list(x for x in section.start.coordinates)
        end = list(x for x in section.end.coordinates)
        start_x = start[0] if start[0] < end[0] else end[0]
        end_x = end[0] if start[0] < end[0] else start[0]
        if start[0] == end[0]:
            return

        slope = math.fabs(section.get_y(1) - section.get_y(2))
        step = 1 / slope if slope > 1 else 1

        range_arr = numpy.arange(start_x, end_x, step)
        for x1 in range_arr:
            y1 = section.get_y(x1)
            if y1 is not None:
                y1 = int(math.floor(y1))
                p = Point([int(math.floor(x1)), y1])
                yield p

    # lets do this another time, above implementation is enough for now
    def floating_bresenham(self, section: Section):
        slope = math.fabs(section.slope)
        step = 1 / slope if slope > 1 else 1

        y_increment = step
        if section.slope < 0:
            y_increment = y_increment * -1

        error = slope - step
        y = section.start[1]
        x_range = numpy.arange(section.start[0], section.end[0], step)

        # we have to make sure that we always increment y by one!
        for x in x_range:
            if error >= 0:
                y += y_increment
                error -= slope

            error += slope

            x_as_int = math.floor(x)
            y_as_int = math.floor(y)
            coordinates = [x_as_int, y_as_int]
            math_point = Point(coordinates)
            yield math_point
            # yield math_to_image(math_point, width=self.width, height=self.height)

    # TODO: refactor
    def draw_line(self, line: Line):
        is_zero_normal_vector = False
        v = line.normal_vector
        if (0 - 1e-7) < v[0] < (0 + 1e-7): is_zero_normal_vector = True
        if (0 - 1e-7) < v[1] < (0 + 1e-7): is_zero_normal_vector = True

        if not is_zero_normal_vector:
            zero_as_math = image_to_math(Point([0, 0]), self.width, self.height)[0]
            width_as_math = image_to_math(Point([self.width, self.width]), self.width, self.width)[0]

            first_point_math = Point([zero_as_math, int(line.get_y(zero_as_math))])
            last_point_math = Point([width_as_math, int(line.get_y(width_as_math))])

            first_point = math_to_image(first_point_math, self.width, self.height)
            last_point = math_to_image(last_point_math, self.width, self.height)

            image_dimension = (0, 0, self.width, self.height)
            clipped_line = cv.clipLine(
                image_dimension,
                (int(first_point[0]), int(first_point[1])),
                (int(last_point[0]), int(last_point[1]))
            )
            if clipped_line[0]:
                cv.line(self.image, clipped_line[1], clipped_line[2], (120, 0, 190))


