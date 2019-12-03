from .cell import Cell
from .position import get_position


class EdgeCell(Cell):

    @property
    def angle(self):
        return self._parent.angle + get_position(self._parent._angle_step)[self.position][0]

    @property
    def p(self):
        return self._parent.p + get_position(self._parent._angle_step)[self.position][1]

    @property
    def position(self):
        raise NotImplementedError('this is an abstract class. please use one of the implementations')

