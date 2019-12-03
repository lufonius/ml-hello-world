import unittest
from .origin_transform_strategies import math_to_image, image_to_math
from package.linear_algebra.point import Point

class OriginTransformStrategiesTest(unittest.TestCase):


    def test_math_to_image(self):
        image_point = Point([0, 80])
        math_point = image_to_math(p=image_point, width=200, height=300)
        assert math_point.x == -100
        assert math_point.y == 70

        image_point = Point([110, 170])
        math_point = image_to_math(p=image_point, width=200, height=300)
        assert math_point.x == 10
        assert math_point.y == -20

    def test_image_to_math(self):
        math_point = Point([10, -20])
        image_point = math_to_image(p=math_point, width=200, height=300)
        assert image_point.x == 110
        assert image_point.y == 170

        math_point = Point([-100, 70])
        image_point = math_to_image(p=math_point, width=200, height=300)
        assert image_point.x == 0
        assert image_point.y == 80




