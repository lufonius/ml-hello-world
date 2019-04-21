import unittest
from .coordinate_space import CoordinateSpace
from .coordinate_space_converter import CoordinateSpaceConverter
import numpy

class TestCoordinateSpaceConverter(unittest.TestCase):

    def test_transform_coordinates_to_math(self):
        # an image full of zero rgb values
        # we set a point in an image and check if it's transformed
        # correctly
        image = numpy.zeros((300, 150, 3))
        image[40, 60, 0] = 1
        expected_x_index = 60
        expected_y_index = 259

        transformed_image = CoordinateSpaceConverter.transform(image, CoordinateSpace.MATH)

        self.assertEqual(1, transformed_image[expected_x_index, expected_y_index, 0])

    def test_transform_coordinates_to_image(self):
        # our coordinate system full of zeros
        # we set a value and look if it's mapped
        # to the right place inside
        # an images coordinate space
        space = numpy.zeros((150, 300, 3))
        space[60, 40, 0] = 1
        expected_x_index = 60
        expected_y_index = 259

        transformed_image = CoordinateSpaceConverter.transform(space, CoordinateSpace.IMAGE)

        self.assertEqual(1, transformed_image[expected_y_index, expected_x_index, 0])