from .cell import Cell
from .position import POSITION


class EdgeCell(Cell):
    position = None

    def __init__(self, parent: Cell):
        x = parent.x + POSITION[self.position][0]
        y = parent.y + POSITION[self.position][1]
        super().__init__(x, y, parent.value, parent)
