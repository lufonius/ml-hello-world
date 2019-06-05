from .top_cell import TopCell
from .edge_cell import EdgeCell
from .cell import Cell
from .right_cell import RightCell
from .position import Position


class TopRightCell(EdgeCell):
    position = Position.TOP_RIGHT

    def __init__(self, parent: Cell):
        super().__init__(parent)

    def grow_leafes(self):
        self.children = [
            TopCell(self),
            TopRightCell(self),
            RightCell(self)
        ]