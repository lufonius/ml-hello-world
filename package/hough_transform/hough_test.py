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
        expected_angle_size = 181
        image = numpy.ndarray((image_width, image_height))

        empty_parameter_matrice = self.hough.create_empty_parameter_matrice(image)

        zero_array = numpy.unique(empty_parameter_matrice)
        self.assertEqual(0, zero_array[0], "not zero - empty parameter space does not consist of only zeros")
        self.assertEqual(1, zero_array.size, "array size not equals one - empty parameter space does not consist of only zeros")

        actual_p_axis_size = empty_parameter_matrice[0, :].size
        actual_angle_axis_size = empty_parameter_matrice[:, 0].size
        self.assertEqual(expected_p_size, actual_p_axis_size, "p axis size is not created properly")
        self.assertEqual(expected_angle_size, actual_angle_axis_size, "angle axis size is not created properly")

    def test_unique_grayscale_values(self):
        expected = numpy.array([
                    [50, 101, 200, 7],
                    [60, 65, 240, 100]
                ])
        image = numpy.array([
                    [[50, 50, 50], [101, 101, 101], [200, 200, 200], [7, 7, 7]],
                    [[60, 60, 60], [65, 65, 65], [240, 240, 240], [100, 100, 100]]
                ])
        unique_grayscale_values_image = self.hough.get_unique_grayscale_values_image(image)
        numpy.testing.assert_array_equal(expected, unique_grayscale_values_image, "rgb values are not being converted to single grayscale values")

    def test_transform(self):
        image = numpy.array([
                    [[50, 50, 50], [101, 101, 101], [70, 70, 70], [7, 7, 7]],
                    [[60, 60, 60], [200, 200, 200], [90, 90, 90], [100, 100, 100]]
                ])
        transformed = self.hough.transform(image)

    def test_convert_to_grayscale_parameter_matrice(self):
        parameter_matrice = numpy.array([
            [1, 2, 1],
            [2, 1, 1]
        ])

        expected = numpy.array([
            [127, 255, 127],
            [255, 127, 127]
        ])
        actual = self.hough.convert_to_grayscale_parameter_matrice(parameter_matrice)
        numpy.testing.assert_array_equal(expected, actual, "parameter matrice wasn't converted to grayscale parameter matrice properly")

    def test_convert_to_rgb_parameter_matrice(self):
        parameter_matrice = numpy.array([
            [100, 50, 70],
            [20, 30, 40]
        ])

        expected = numpy.array([
            [[100, 100, 100], [50, 50, 50], [70, 70, 70]],
            [[20, 20, 20], [30, 30, 30], [40, 40, 40]]
        ])

        actual = self.hough.convert_to_rgb_parameter_matrice(parameter_matrice)
        numpy.testing.assert_array_equal(expected, actual)