import numbers
import math

class Vector(object):
    def __init__(self, coordinates):
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
        return 'Vector {}'.format(self.coordinates)

    def __eq__(self, v):
        self.coordinates == v.coordinates

    def __add__(self, other):
        self.__check_vector(other)

        new_coordinates = [round(x + y, self.round) for x, y in zip(self.coordinates, other.coordinates)]

        return Vector(new_coordinates)

    def __sub__(self, other):
        self.__check_vector(other)

        new_coordinates = [round(x - y, self.round) for x, y in zip(self.coordinates, other.coordinates)]

        return Vector(new_coordinates)

    def __mul__(self, other):
        self.__check_number(other)

        new_coordinates = [round(other * coord, self.round) for coord in self.coordinates]

        return Vector(new_coordinates)

    def magnitude(self):
        powed = [pow(coord, 2) for coord in self.coordinates]

        result = math.sqrt(sum(powed))
        return round(result, self.round)

    def unit(self):
        magnitude = self.magnitude()

        return self.__mul__(1 / magnitude)

    def dot(self, other):
        self.__check_vector(other)
        return round(sum([x * y for x, y in zip(self.coordinates, other.coordinates)]), self.round)

    def angle(self, other, degree = False):
        self.__check_vector(other)
        magnitude_product = self.magnitude() * other.magnitude()

        result = math.acos(self.dot(other) / magnitude_product)
        # Or: acos of the dot product of both normalized vectors
        if degree: result = math.degrees(result)
        return round(result, self.round)

    def __check_vector(self, value):
        if not self.__isVector(value): raise TypeError
        if not self.dimension == value.dimension: raise ValueError

    def __check_number(self, value):
        if not self.__isNumber(value): raise TypeError

    def __isNumber(self, value):
        return isinstance(value, numbers.Number)

    def __isVector(self, value):
        return isinstance(value, Vector)

