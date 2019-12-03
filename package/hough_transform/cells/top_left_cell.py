from .left_cell import LeftCell
from .edge_cell import EdgeCell
from .top_cell import TopCell
from .position import Position


class TopLeftCell(EdgeCell):
    position = Position.TOP_LEFT

    @property
    def children(self):
        yield TopCell(self)
        yield TopLeftCell(self)
        yield LeftCell(self)