from __future__ import annotations
from .cell import Cell
from .bottom_left_cell import BottomLeftCell
from .bottom_cell import BottomCell
from .bottom_right_cell import BottomRightCell
from .left_cell import LeftCell
from .top_left_cell import TopLeftCell
from .top_cell import TopCell
from .top_right_cell import TopRightCell
from .right_cell import RightCell


class RootCell(Cell):

    @property
    def children(self):
        yield TopLeftCell(self)
        yield TopCell(self)
        yield TopRightCell(self)
        yield RightCell(self)
        yield BottomRightCell(self)
        yield BottomCell(self)
        yield BottomLeftCell(self)
        yield LeftCell(self)
