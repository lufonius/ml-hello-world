from .top_cell import TopCell
from .edge_cell import EdgeCell
from .right_cell import RightCell
from .position import Position


class TopRightCell(EdgeCell):
    position = Position.TOP_RIGHT

    @property
    def children(self):
        yield TopCell(self)
        yield TopRightCell(self)
        yield RightCell(self)
