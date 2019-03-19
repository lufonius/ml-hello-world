import numbers
import math
from linear_algebra.system import System


# TODO: Use DI here to create a singleton system object
class Vector(object):

    def __init__(self, coordinates, system = System()):
        self.round = 3
        self.system = system
        try:
            if not coordinates:
                raise ValueError
            else:
                self.coordinates = tuple(coordinates)
                self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('wrong value')
        except TypeError:
            raise TypeError('coordinates is of wrong type')

    def __str__(self):
        return 'Vector {}'.format([round(x, self.round) for x in self.coordinates])

    def __getitem__(self, arg):
        self.__check_number(arg)
        return self.coordinates[arg]

    def __eq__(self, v):
        self.coordinates == v.coordinates

    def __add__(self, other):
        self.__check_vector(other)

        new_coordinates = [x + y for x, y in zip(self.coordinates, other.coordinates)]

        return Vector(new_coordinates)

    def __sub__(self, other):
        self.__check_vector(other)

        new_coordinates = [x - y for x, y in zip(self.coordinates, other.coordinates)]

        return Vector(new_coordinates)

    def __mul__(self, other):
        self.__check_number(other)

        new_coordinates = [other * coord for coord in self.coordinates]

        return Vector(new_coordinates)

    def magnitude(self):
        powed = [pow(coord, 2) for coord in self.coordinates]

        result = math.sqrt(sum(powed))
        return result

    def normalize(self):
        magnitude = self.magnitude()

        return self.__mul__(1 / magnitude)

    @staticmethod
    def dot_between(v1, v2):
        v1.__check_vector(v2)
        return sum([x * y for x, y in zip(v1.coordinates, v2.coordinates)])

    def dot_with(self, v):
        return Vector.dot_between(self, v)

    @staticmethod
    def angle_between(v1, v2, degree = False):
        v1.__check_vector(v2)
        magnitude_product = v1.magnitude() * v2.magnitude()

        result = math.acos(v1.dot_with(v2) / magnitude_product)
        # Or: acos of the dot product of both normalized vectors
        if degree: result = math.degrees(result)
        return result

    def angle_to(self, v, degree = False):
        return Vector.angle_between(self, v, degree)

    def is_orthogonal_to(self, other, tolerance = 1e-10):
        self.__check_vector(other)
        return self.dot_with(other) < tolerance

    @staticmethod
    def are_parallel(v1, v2):
        v1.__check_vector(v2)
        return (v1.is_zero()
                or v2.is_zero()
                or Vector.angle_between(v1, v2) == 0
                or Vector.angle_between(v1, v2) == math.pi)

    def is_zero(self, tolerance = 1e-10):
        return self.magnitude() < tolerance

    @staticmethod
    def project(v1, v2):
        v1.__check_vector(v2)
        return v2.normalize().__mul__(v1.dot_with(v2.normalize()))

    def project_onto(self, v):
        return Vector.project(self, v)

    @staticmethod
    def component(v1, v2):
        v1.__check_vector(v2)
        projected = v1.project_onto(v2)
        return v1.__sub__(projected)

    def component_to(self, v):
        return Vector.component(self, v)

    # [x, y, z]
    @staticmethod
    def cross_between(v1, v2):
        Vector.__is_three_dimensional_vector(v1)
        Vector.__is_three_dimensional_vector(v2)

        x1, y1, z1 = v1.coordinates
        x2, y2, z2 = v2.coordinates

        cross_x = y1 * z2 - y2 * z1
        cross_y = -1 * (x1 * z2 - x2 * z1)
        cross_z = x1 * y2 - x2 * y1

        return Vector([cross_x, cross_y, cross_z])

    def cross_with(self, v):
        return Vector.cross_between(self, v)

    def area_parallelogram_with(self, v):
        self.__check_vector(v)
        return self.cross_with(v).magnitude()

    def area_triangle_with(self, v):
        self.__check_vector(v)
        return self.area_parallelogram_with(v) / 2

    def __check_vector(self, v):
        if not Vector.__is_vector(v): raise TypeError
        if not self.dimension == v.dimension: raise ValueError

    @staticmethod
    def __check_three_dimensional_vector(v):
        if not Vector.__is_three_dimensional_vector(v): ValueError


    @staticmethod
    def __check_number(value):
        if not Vector.__is_number(value): raise TypeError

    @staticmethod
    def __is_number(value):
        return isinstance(value, numbers.Number)

    @staticmethod
    def __is_vector(v):
        return isinstance(v, Vector)

    @staticmethod
    def __is_three_dimensional_vector(v):
        if not isinstance(v, Vector): raise TypeError
        return (len(v.coordinates) == 3)



