from .edge_cell import EdgeCell
from .position import Position


class LeftCell(EdgeCell):
    position = Position.LEFT

    @property
    def children(self):
        yield LeftCell(self)
