import unittest
from package.hough_transform.cells.root_cell import RootCell


class TestRootCell(unittest.TestCase):

    def test_cell_level(self):
        cell2 = RootCell(7, 7, 0)
        cells = []
        cell2.get_cells_till_level(2, cells)
        test = 1