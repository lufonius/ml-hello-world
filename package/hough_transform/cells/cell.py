from __future__ import annotations


class Cell:
    angle = 0
    p = 0

    def __init__(self, parent: Cell = None):
        self._angle_step = 1
        self._parent = parent
        self.votes = 0

    def __hash__(self):
        return hash((self.angle, self.p))

    def __eq__(self, other: Cell):
        return hash(self) == hash(other)

    def vote(self):
        self.votes += 1

    @property
    def level(self):
        if self._parent is None:
            return 1
        return self._parent.level + 1

    @property
    def children(self):
        return []

    def get_surrounding_cells(self, level: int, p_axis_size: int):
        map = {}
        for cell in self.__get_surrounding_cells(level, p_axis_size):
            map[hash(cell)] = cell

        # del map[hash(self)]
        return map

    def __get_surrounding_cells(self, level: int, p_axis_size: int):
        if self.level <= level:
            for child in self.children:
                child.__get_surrounding_cells(level, p_axis_size)
                if not child.angle > 360 \
                        or not child.p > p_axis_size \
                        or not child.angle <= 0 \
                        or not child.p <= 0:
                    yield child