import unittest
import numpy
import math
from .hough import Hough

class HoughTest(unittest.TestCase):
    hough = Hough()

    def setUp(self):
        self.hough = Hough()

    def test_create_empty_parameter_matrice(self):
        image_width = 50
        image_height = 80
        expected_p_size = math.ceil(math.sqrt(image_height**2 + image_width**2))
        expected_angle_size = 360 / self.hough.angle_range["step"]
        image = numpy.ndarray((image_width, image_height))

        empty_parameter_matrice = self.hough.create_empty_parameter_matrice(image)

        zero_array = numpy.unique(empty_parameter_matrice)
        self.assertEqual(0, zero_array[0], "not zero - empty parameter space does not consist of only zeros")
        self.assertEqual(1, zero_array.size, "array size not equals one - empty parameter space does not consist of only zeros")

        actual_p_axis_size = empty_parameter_matrice[0, :].size
        actual_angle_axis_size = empty_parameter_matrice[:, 0].size
        self.assertEqual(expected_p_size, actual_p_axis_size, "p axis size is not created properly")
        self.assertEqual(expected_angle_size, actual_angle_axis_size, "angle axis size is not created properly")

    def test_convert_to_grayscale_parameter_matrice(self):
        parameter_matrice = numpy.array([
            [1, 2, 1],
            [2, 1, 1]
        ])

        expected = numpy.array([
            [127, 255, 127],
            [255, 127, 127]
        ])
        actual = self.hough._convert_to_grayscale_parameter_matrice(parameter_matrice)
        numpy.testing.assert_array_equal(expected, actual, "parameter matrice wasn't converted to grayscale parameter matrice properly")

