import numpy
from .coordinate_space import CoordinateSpace

# TODO: Check if there's a library for this
class CoordinateSpaceConverter:

    @staticmethod
    def _to_image_space(space):
        new_space = numpy.copy(space)
        # make (x, y) as (y, x)
        new_space = numpy.swapaxes(new_space, 0, 1)
        # flip the values for the y axis
        new_space = numpy.flip(new_space, 0)
        return new_space

    @staticmethod
    def _to_math_space(space):
        new_space = numpy.copy(space)
        # (y, x) becomes (x, y)
        new_space = numpy.swapaxes(new_space, 0, 1)
        # flip the values for the y axis
        new_space = numpy.flip(new_space, 1)
        return new_space

    @staticmethod
    def transform(space, coordinate_space):
        switch = {
            CoordinateSpace.IMAGE: CoordinateSpaceConverter._to_image_space,
            CoordinateSpace.MATH: CoordinateSpaceConverter._to_math_space
        }

        return switch[coordinate_space](space)
