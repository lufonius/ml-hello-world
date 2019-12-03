from .bottom_cell import BottomCell
from .edge_cell import EdgeCell
from .left_cell import LeftCell
from .position import Position

class BottomLeftCell(EdgeCell):
    position = Position.BOTTOM_LEFT

    @property
    def children(self):
        yield LeftCell(self)
        yield BottomLeftCell(self)
        yield BottomCell(self)