from .edge_cell import EdgeCell
from .position import Position


class RightCell(EdgeCell):
    position = Position.RIGHT

    @property
    def children(self):
        yield RightCell(self)
