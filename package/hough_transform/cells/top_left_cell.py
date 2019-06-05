from .left_cell import LeftCell
from .edge_cell import EdgeCell
from .cell import Cell
from .top_cell import TopCell
from .position import Position


class TopLeftCell(EdgeCell):
    position = Position.TOP_LEFT

    def __init__(self, parent: Cell):
        super().__init__(parent)

    def grow_leafes(self):
        self.children = [
            TopCell(self),
            TopLeftCell(self),
            LeftCell(self)
        ]