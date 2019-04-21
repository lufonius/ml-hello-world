import math
import numpy
from package.utils.coordinate_space import CoordinateSpace
from package.utils.coordinate_space_converter import CoordinateSpaceConverter
from package.utils.memoize import Memoize

class Hough:
    # condition for voting
    grayscale_bias = 100
    # the range for the angle axis. those are constants!
    angle_range = {"start": 0, "end": 360, "step": 3}

    # setting as methods, inside the function call doesn't make sense
    # since the memoized params are always empty
    @Memoize  # omg i love python!
    def _cos_angle(self, angle):
        return math.cos(math.radians(angle))

    @Memoize
    def _sin_angle(self, angle):
        return math.sin(math.radians(angle))

    # later on, when we provide this as a service, we could
    # keep some results (till 300x300 image) in the memory
    # to make it faster
    # but memoizing cos and sin is good for now
    # p = x * cos(angle) + y * sin(angle) => see hesse normal form
    def p_fn(self, angle, x, y):
        result = x * self._cos_angle(angle) + y * self._sin_angle(angle)
        return result

    def create_empty_parameter_matrice(self, image):
        p_axis_size = self._get_p_axis_size(image)
        angle_axis_size = self._get_angle_axis_size()

        # creates a new array with the same size as the image
        # angle becomes the x-value, p becomes the y value
        parameter_matrice_shape = (angle_axis_size, p_axis_size)
        parameter_matrice = numpy.zeros(parameter_matrice_shape)

        return parameter_matrice

    def transform(self, image):
        # we have to be careful with the axises. in an image,
        # the origin starts in the top left
        # but we want to have the origin on the bottom left.
        # also, accessing values in an image happens like this
        # image[y, x], but we want to use image[x, y]
        # so we have to transform the image values into a different
        # x,y space
        image = CoordinateSpaceConverter.transform(image, CoordinateSpace.MATH)

        parameter_matrice = self.create_empty_parameter_matrice(image)

        p_axis_size = self._get_p_axis_size(image)
        image_height = self._get_image_height(image)
        image_width = self._get_image_width(image)

        angle_range_array = self._get_angle_range_array()
        angle_range_array_index = range(angle_range_array.shape[0])
        image_index = numpy.ndindex(image.shape[:2])

        # create a parameter matrice by the size of the coordinate matrice
        for (x, y) in image_index:
            # here we have to convert the points
            new_x = x - (image_width / 2)
            new_y = y - (image_height / 2)
            grayscale = image[x, y] if image.shape.count() < 3 else image[x, y][0]
            if (grayscale > self.grayscale_bias):
                for angle_index in angle_range_array_index:
                    # now we have a x,y point and have to calculate each
                    # each value for each angle step
                    p = math.ceil((p_axis_size / 2 - 1) + self.p_fn(angle_range_array[angle_index], new_x, new_y))
                    # there's another solution
                    # p = p_axis_size + self.p_fn(...)
                    # p >>= 1
                    # but idk what its about
                    # we plot them into the parameter matrice
                    parameter_matrice[angle_index, p] += 1

        return self._convert_to_grayscale_parameter_matrice(parameter_matrice)

    def _convert_to_grayscale_parameter_matrice(self, parameter_matrice):
        # now we got the matrice, and in each (angle, p) point, we have a certain
        # count for votings. we have to convert this to grayscale values from 0 to 255
        max_voting_value = numpy.amax(parameter_matrice)

        def convert(voting_result):
            return math.floor((voting_result / max_voting_value) * 255)

        fn = numpy.vectorize(convert)

        return fn(parameter_matrice).astype(numpy.uint8)

    def _get_angle_range_array(self):
        return numpy.arange(
            self.angle_range['start'],
            self.angle_range['end'],
            self.angle_range["step"]
        )

    def _get_angle_axis_size(self):
        return self._get_angle_range_array().size

    def _get_p_axis_size(self, image):
        # image diagonal is the p axis range
        return math.ceil(math.sqrt(image.shape[0]**2 + image.shape[1]**2))

    def _get_image_height(self, image):
        return image.shape[1]

    def _get_image_width(self, image):
        return image.shape[0]







