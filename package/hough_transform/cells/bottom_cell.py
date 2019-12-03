from package.hough_transform.cells.edge_cell import EdgeCell
from .position import Position


class BottomCell(EdgeCell):
    position = Position.BOTTOM

    @property
    def children(self):
        yield BottomCell(self)
