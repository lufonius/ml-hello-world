from __future__ import annotations
import typing


class Cell:
    value = None

    def __init__(self, x: int, y: int, parent: Cell = None):
        self._x = x
        self._y = y

        self._parent = parent

        # future implementation ... replace with array
        self.votes = 0

        self.children = []

    def __hash__(self):
        return hash((self._x, self._y))

    def __eq__(self, other: Cell):
        return hash(self) == hash(other)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def level(self):
        if self._parent is None:
            return 1
        return self._parent.level + 1

    def get_cells_till_level(self, level: int, cells: typing.List[Cell]):
        if self.level <= level:
            self.grow_leafes()
            for child in self.children:
                cells.append(child)
                child.get_cells_till_level(level, cells)

    def grow_leafes(self):
        pass


