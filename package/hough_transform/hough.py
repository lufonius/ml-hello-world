import math
import numpy
from package.utils.coordinate_space import CoordinateSpace
from package.utils.coordinate_space_converter import CoordinateSpaceConverter

class Hough:
    # condition for voting
    grayscale_bias = 100
    # the range for the angle axis. those are constants!
    angle_range = {"start": 0, "end": 360, "step": 3}

    cached_cos_angle = {}
    cached_sin_angle = {}
    # p = x * cos(angle) + y * sin(angle) => see normalization
    def p_fn(self, angle, x, y):
        cos_angle = 0
        # lets look up memoization in python
        if (angle in self.cached_cos_angle):
            cos_angle = self.cached_cos_angle[angle]
        else:
            cos_angle = math.cos(math.radians(angle))
            self.cached_cos_angle[angle] = cos_angle

        sin_angle = 0
        # lets look up memoization in python
        if (angle in self.cached_sin_angle):
            sin_angle = self.cached_sin_angle[angle]
        else:
            sin_angle = math.sin(math.radians(angle))
            self.cached_sin_angle[angle] = sin_angle

        result = x * cos_angle + y * sin_angle
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
            grayscale = image[x, y] if image.shape.__len__() < 3 else image[x, y][0]
            if (grayscale > self.grayscale_bias):
                for angle_index in angle_range_array_index:
                    # now we have a x,y point and have to calculate each
                    # each value for each angle step
                    p = p_axis_size + math.ceil(self.p_fn(angle_range_array[angle_index], new_x, new_y))
                    p >>= 1
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







