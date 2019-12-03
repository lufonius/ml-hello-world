from package.hough_transform.cells.right_cell import RightCell
from .edge_cell import EdgeCell
from .bottom_cell import BottomCell
from .position import Position


class BottomRightCell(EdgeCell):
    position = Position.BOTTOM_RIGHT

    @property
    def children(self):
        yield RightCell(self)
        yield BottomRightCell(self)
        yield BottomCell(self)
