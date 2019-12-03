from .edge_cell import EdgeCell
from .position import Position


class TopCell(EdgeCell):
    position = Position.TOP

    @property
    def children(self):
        yield TopCell(self)
