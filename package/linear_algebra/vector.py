from __future__ import annotations
import math
import typing
from .point import Point
from .system import System


# TODO: Use DI here to create a singleton system object
class Vector(Point):

    def __init__(self, coordinates: typing.List[float]):
        Point.__init__(self, coordinates)
        self.type = 'Vector'

    def __eq__(self, v):
        self.coordinates == v.coordinates

    def __add__(self, other: Vector) -> Vector:
        self.__check_vector_dimension(other)

        new_coordinates = [x + y for x, y in zip(self.coordinates, other.coordinates)]

        return Vector(new_coordinates)

    def __sub__(self, other: Vector) -> Vector:
        self.__check_vector_dimension(other)

        new_coordinates = [x - y for x, y in zip(self.coordinates, other.coordinates)]

        return Vector(new_coordinates)

    def __truediv__(self, div: float):
        new_coordinates = [ coord / div for coord in self.coordinates]
        return Vector(new_coordinates)

    def __mul__(self, other: float) -> Vector:
        self.__check_number(other)

        new_coordinates = [other * coord for coord in self.coordinates]

        return Vector(new_coordinates)

    def magnitude(self) -> float:
        powed = [pow(coord, 2) for coord in self.coordinates]

        result = math.sqrt(sum(powed))
        return result

    def normalize(self) -> Vector:
        magnitude = self.magnitude()

        return self.__mul__(1 / magnitude)

    @staticmethod
    def dot_between(v1: Vector, v2: Vector) -> float:
        v1.__check_vector_dimension(v2)
        return sum([x * y for x, y in zip(v1.coordinates, v2.coordinates)])

    def dot_with(self, v: Vector) -> float:
        return Vector.dot_between(self, v)

    @staticmethod
    def angle_between(v1: Vector, v2: Vector, degree: bool = False) -> float:
        v1.__check_vector_dimension(v2)
        magnitude_product = v1.magnitude() * v2.magnitude()

        # when the angle is zero, magnitude product might be a little smaller
        # because of precision of floats
        dot = v1.dot_with(v2)
        if (dot - 1e-7) < magnitude_product < (dot + 1e-7): magnitude_product = dot

        for_acos = dot / magnitude_product
        for_acos = -1 if (for_acos - 1e-7) < -1 else for_acos
        for_acos = 1 if (for_acos + 1e-7) > 1 else for_acos

        result = math.acos(for_acos)
        # Or: acos of the dot product of both normalized vectors
        if degree: result = math.degrees(result)
        return result

    def angle_to(self, v: Vector, degree: bool = False) -> float:
        return Vector.angle_between(self, v, degree)

    def is_orthogonal_to(self, other: Vector, tolerance: float = 1e-10) -> bool:
        self.__check_vector_dimension(other)
        return self.dot_with(other) < tolerance

    @staticmethod
    def are_parallel(v1: Vector, v2: Vector) -> bool:
        v1.__check_vector_dimension(v2)
        return (v1.is_zero()
                or v2.is_zero()
                or Vector.angle_between(v1, v2) == 0
                or Vector.angle_between(v1, v2) == math.pi)

    def is_zero(self, tolerance: float = 1e-10) -> bool:
        return self.magnitude() < tolerance

    @staticmethod
    def project(v1: Vector, v2: Vector) -> Vector:
        v1.__check_vector_dimension(v2)
        return v2.normalize().__mul__(v1.dot_with(v2.normalize()))

    def project_onto(self, v: Vector) -> Vector:
        return Vector.project(self, v)

    @staticmethod
    def component(v1: Vector, v2: Vector) -> Vector:
        v1.__check_vector_dimension(v2)
        projected = v1.project_onto(v2)
        return v1.__sub__(projected)

    def component_to(self, v: Vector) -> Vector:
        return Vector.component(self, v)

    # [x, y, z]
    @staticmethod
    def cross_between(v1: Vector, v2: Vector) -> Vector:
        Vector.__is_three_dimensional_vector(v1)
        Vector.__is_three_dimensional_vector(v2)

        x1, y1, z1 = v1.coordinates
        x2, y2, z2 = v2.coordinates

        cross_x = y1 * z2 - y2 * z1
        cross_y = -1 * (x1 * z2 - x2 * z1)
        cross_z = x1 * y2 - x2 * y1

        return Vector([cross_x, cross_y, cross_z])

    def cross_with(self, v: Vector) -> Vector:
        return Vector.cross_between(self, v)

    def area_parallelogram_with(self, v: Vector) -> float:
        self.__check_vector_dimension(v)
        return self.cross_with(v).magnitude()

    def area_triangle_with(self, v: Vector) -> float:
        self.__check_vector_dimension(v)
        return self.area_parallelogram_with(v) / 2

    @staticmethod
    def from_magnitude_angle(magnitude: float, angle: float) -> Vector:
        y = math.sin(math.radians(angle)) * magnitude
        x = math.cos(math.radians(angle)) * magnitude

        return Vector([x, y])

    def __check_vector_dimension(self, v: Vector) -> None:
        if not self.dimension == v.dimension: raise ValueError

    @staticmethod
    def __check_three_dimensional_vector(v: Vector) -> None:
        if not Vector.__is_three_dimensional_vector(v): raise ValueError

    @staticmethod
    def __is_three_dimensional_vector(v: Vector) -> bool:
        if not isinstance(v, Vector): raise TypeError
        return (len(v.coordinates) == 3)



