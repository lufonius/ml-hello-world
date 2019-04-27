from __future__ import annotations
from decimal import Decimal, getcontext
from .vector import Vector
from .point import Point
from enum import Enum

getcontext().prec = 30


class IntersectionType(Enum):
    INTERSECT = 'Intersect'
    SAME = 'Same line'
    PARALLEL = 'Parallel'


class IntersectionResult:

    def __init__(self, result: Point, type: IntersectionType):
        self.result = result
        self.type = type

    def __str__(self):
        return 'Type: {0} Intersection point: {1}'.format(self.type, self.result.__str__())

class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector: Vector = None, constant_term: float = None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = [0]*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = 0
        self.constant_term = float(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = [0]*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    def is_parallel_with(self, line: Line) -> bool:
        return Vector.are_parallel(self.normal_vector, line.normal_vector)

    def get_y(self, x) -> float:
        return (self.constant_term - self.normal_vector[0] * x) / self.normal_vector[1];

    def is_same_line(self, line: Line) -> bool:
        # we take vectors, as we need some vector calculation
        random_point_1 = Vector([6, self.get_y(6)])
        random_point_2 = Vector([9, line.get_y(9)])

        diff = random_point_1 - random_point_2

        # lets make some getters and setters for the components
        direction_vector = Vector([-self.normal_vector[1], self.normal_vector[0]])

        # if the diff and the direction vector are parallel (dot product is one)
        # -> true

        return Vector.are_parallel(diff, direction_vector)

    def get_intersection_with(self, line: Line) -> Point:
        return Line.get_intersection(self, line)

    @staticmethod
    def get_intersection(line1: Line, line2: Line) -> IntersectionResult:

        # we should return if it intersects, if it's parallel or if
        # they're even the same line
        if line1.is_same_line(line2):
            return IntersectionResult(None, IntersectionType.SAME)

        if line1.is_parallel_with(line2):
            return IntersectionResult(None, IntersectionType.PARALLEL)

        def x_y_dominator(a: float, b: float, c: float, d: float) -> float:
            return a * d - b * c

        def x_nominator(b: float, d: float, constant_term1: float, constant_term2: float) -> float:
            return d * constant_term1 - b * constant_term2

        def y_nominator(a: float, c: float, constant_term1: float, constant_term2: float) -> float:
            return (-c * constant_term1) + a * constant_term2

        a = line1.normal_vector[0]
        b = line1.normal_vector[1]
        c = line2.normal_vector[0]
        d = line2.normal_vector[1]
        constant_term1 = line1.constant_term
        constant_term2 = line2.constant_term

        x = x_nominator(b, d, constant_term1, constant_term2) / x_y_dominator(a, b, c, d)
        y = y_nominator(a, c, constant_term1, constant_term2) / x_y_dominator(a, b, c, d)

        return IntersectionResult(Point([x, y]), IntersectionType.INTERSECT)

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
