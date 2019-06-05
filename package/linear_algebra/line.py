from .point import Point
from .vector import Vector
import typing

class Line:
    # Ax + By = k
    # where the normal vector is [A, B]
    # and the constant_term is k
    # [x, y] can be any direction vector
    def __init__(self, normal_vector: Vector, constant_term: float):
        self.__normal_vector = normal_vector
        self.__constant_term = constant_term
        self.__basepoints = [None, None]
        self.__direction_vector = None

        self.calculate_basepoints()
        self.calculate_direction_vector()


    @property
    def basepoints(self) -> typing.List[float]:
        return self.__basepoints

    # what happens when we extend this to higher dimensions?
    # most likely there are seldom any basepoints...
    def calculate_basepoints(self):
        test = 1
        # the basepoint is actually the x and y intercept
        # so when we insert a zero for the x value
        # we get By = k
        # the y-intercept is the following:
        # y = k / B
        # B cannot be 0
        # a zero as coefficient means the line is vertical or horizontal
        if self.__normal_vector[0] is not 0:
            self.__basepoints[1] = self.__constant_term / self.__normal_vector[0]
        else:
            self.__basepoints[1] = None

        if self.__normal_vector[1] is not 0:
            self.__basepoints[0] = self.__constant_term / self.__normal_vector[1]
        else:
            self.__basepoints[0] = None
        self.calculate_basepoints()
        self.calculate_direction_vector()

    def constant_term(self):
        self.calculate_basepoints()
        self.calculate_direction_vector()

    def normal_vector(self):
        pass

    def calculate_direction_vector(self):
        self.__direction_vector = Vector(self.basepoints)