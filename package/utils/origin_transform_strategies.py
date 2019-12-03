from package.linear_algebra.point import Point
import math


def math_to_image(p: Point, width: int, height: int) -> Point:
    new_x = p[0] + (width / 2)
    new_y = (height / 2) - p[1]
    return Point([math.floor(new_x), math.floor(new_y)])


def image_to_math(p: Point, width: int, height: int) -> Point:
    new_x = p[0] - (width / 2)
    new_y = (height / 2) - p[1]
    return Point([new_x, new_y])
