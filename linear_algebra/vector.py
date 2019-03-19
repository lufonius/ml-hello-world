import numbers
import math

class Vector(object):
    def __init__(self, coordinates, ):
        self.round = 3
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
    
    @staticmethod
    def cross_between(v1, v2):
        pass

    def cross_to(self, v):
        self.__check_vector(v)
        return Vector.cross_between(self, v)

    def __check_vector(self, v):
        if not Vector.__isVector(v): raise TypeError
        if not self.dimension == v.dimension: raise ValueError

    @staticmethod
    def __check_number(value):
        if not Vector.__isNumber(value): raise TypeError

    @staticmethod
    def __isNumber(value):
        return isinstance(value, numbers.Number)

    @staticmethod
    def __isVector(v):
        return isinstance(v, Vector)



