import unittest
from package.linear_algebra.point import Point
from package.linear_algebra.line_copy import Line
from package.linear_algebra.section import Section
from .image import Image
import numpy
import cv2 as cv

class ImageTest(unittest.TestCase):
    image_arr = None
    image = None
    expected_width = 300
    expected_height = 200

    def setUp(self):
        self.image_arr = numpy.zeros((self.expected_height, self.expected_width, 3))
        self.image = Image(self.image_arr)

    def test_height(self):
        assert self.image.height == self.expected_height

    def test_width(self):
        assert self.image.width == self.expected_width

    def test_set_image(self):
        self.image.image = numpy.zeros((400, 500))
        assert self.image.width == 500
        assert self.image.height == 400

    def test_set_pixel(self):
        math_point = Point([0, 0])
        self.image.set_pixel(p=math_point,color=[90, 90, 90])
        assert self.image.image[100, 150][0] == 90

    def test_get_pixel(self):
        math_point = Point([0, 0])
        self.image.image[100, 150] = [90, 90, 90]
        color = self.image.get_pixel(p=math_point)
        assert color[0] == 90

    def test_image_pixels(self):
        has_correct_x_iterations = False
        has_correct_y_iterations = False
        not_reaches_x_boundary = True
        not_reaches_y_boundary = True

        for p in self.image.image_pixels():
            if p.x == 250:
                has_correct_x_iterations = True
            if p.y == 112:
                has_correct_y_iterations = True
            if p.x == self.expected_width:
                not_reaches_x_boundary = False
            if p.y == self.expected_height:
                not_reaches_y_boundary = False

        assert has_correct_x_iterations
        assert has_correct_y_iterations
        assert not_reaches_x_boundary
        assert not_reaches_y_boundary

    def test_section_points(self):
        kWinName = 'Holistically-Nested_Edge_Detection'
        cv.namedWindow(kWinName, cv.WINDOW_AUTOSIZE)

        line = Line.from_slope_intercept(delta_y=40, delta_x=1, y_intercept=0)
        section = Section(Point([0, 0]), Point([10, 50]), line)

        for p in self.image.floating_bresenham(section):
            self.image.set_pixel(p, [0, 0, 255])

        cv.imshow(kWinName, self.image.image)
        cv.waitKey()
