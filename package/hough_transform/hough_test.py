import unittest
from package.hough_transform.cells.cell import Cell
from .hough import Hough

class HoughTest(unittest.TestCase):
    hough = Hough()

    def setUp(self):
        self.hough = Hough()

    def test_to_lines(self):
        maximas = {}

        maxima = Cell()
        maxima.p = -92.0
        maxima.angle = 0.0

        maximas[hash(maxima)] = maxima

        lines = self.hough.to_lines(maximas)
        assert lines[0].normal_vector[0] == -92
        assert lines[0].constant_term == 8464




