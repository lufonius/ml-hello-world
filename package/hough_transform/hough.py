import math
import numpy
from enum import Enum

class CoordinateSpace(Enum):
    IMAGE = 0,
    MATH = 1

class Hough:
    # condition for voting
    grayscale_bias = 100
    # the range for the angle axis. those are constants!
    angle_range = {"start": 0, "end": 360}

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
        p_axis_size = self.get_p_axis_size(image)
        angle_axis_size = self.get_angle_axis_size()

        # creates a new array with the same size as the image
        # angle becomes the x-value, p becomes the y value
        parameter_matrice_shape = (angle_axis_size, p_axis_size)
        parameter_matrice = numpy.zeros(parameter_matrice_shape)

        return parameter_matrice

    def transform(self, image):
        # we have to be careful with the axises. in an image,
        # the origin starts in the top left
        # but we want to have the origin on the bottom left
        # also, accessing values in an image happens like this
        # image[y, x], but we want to use image[x, y]
        # so we have to transform the image values into a different
        # x,y space
        image = self.transform_coordinate_space(image, CoordinateSpace.MATH)
        unique_grayscale_values_image = self.get_unique_grayscale_values_image(image)

        parameter_matrice = self.create_empty_parameter_matrice(image)

        p_axis_size = self.get_p_axis_size(image)

        image_height = self.get_image_height(image)
        image_width = self.get_image_width(image)

        # create a parameter matrice by the size of the coordinate matrice
        for (x, y) in numpy.ndindex(unique_grayscale_values_image.shape):
            # here we have to convert the points
            new_x = x - (image_width / 2)
            new_y = y - (image_height / 2)
            if (unique_grayscale_values_image[x, y] > self.grayscale_bias):
                for angle_step in self.get_angle_range_array():
                    # now we have the x,y values. if the grayscale is greater than the bias
                    # we pass the x, y and angle_step to the function
                    # we get the 'p-value', and vote => increasing the value by one
                    p = math.ceil(self.p_fn(angle_step, new_x, new_y))
                    parameter_matrice[angle_step, p] += 1

        return parameter_matrice

    def convert_to_grayscale_parameter_matrice(self, parameter_matrice):
        # now we got the matrice, and in each (x, y) or (p, angle) point, we have a certain
        # count for votings. we have to convert this to grayscale values from 0 to 255
        max_voting_value = numpy.amax(parameter_matrice)
        grayscale_parameter_matrice = numpy.zeros(parameter_matrice.shape)

        for (angle, p) in numpy.ndindex(grayscale_parameter_matrice.shape):
            voting_result = parameter_matrice[angle, p]
            grayscale_parameter_matrice[angle, p] = math.floor((voting_result/max_voting_value) * 255)

        return grayscale_parameter_matrice

    def to_rgb(self, grayscale_parameter_matrice):
        shape = grayscale_parameter_matrice.shape
        shape += (3,)
        rgb_parameter_matrice = numpy.zeros(shape)

        for (angle, p) in numpy.ndindex(grayscale_parameter_matrice.shape):
            rgb_parameter_matrice[angle, p, 0] = grayscale_parameter_matrice[angle, p]
            rgb_parameter_matrice[angle, p, 1] = grayscale_parameter_matrice[angle, p]
            rgb_parameter_matrice[angle, p, 2] = grayscale_parameter_matrice[angle, p]

        return rgb_parameter_matrice

    def get_unique_grayscale_values_image(self, image):
        # so we don't modify it via reference
        unique_grayscale_values_image = numpy.empty(image.shape[:2])

        # image is a 3d array. the innermost array holds rgb values. since they are all the same
        # (the image is black and white), we distinct them to have a 2d array
        for x, y in numpy.ndindex(unique_grayscale_values_image.shape[:2]):
            unique_grayscale_values_image[x, y] = numpy.unique(image[x, y])[0]

        return unique_grayscale_values_image

    def get_angle_range_array(self):
        return numpy.arange(self.angle_range['start'], self.angle_range['end'] + 1)

    def get_angle_axis_size(self):
        return self.get_angle_range_array().size

    def get_p_axis_size(self, image):
        # image diagonal is the p axis range

        empty_2d = numpy.empty(image.shape[:2])
        image_height = empty_2d[0, :].size
        image_width = empty_2d[:, 0].size

        return math.ceil(math.sqrt(image_height**2 + image_width**2))

    def get_image_height(self, image):
        return image.shape[1]

    def get_image_width(self, image):
        return image.shape[0]

    def to_image_space(self, space):
        new_space = numpy.copy(space)
        # make (x, y) as (y, x)
        new_space = numpy.swapaxes(new_space, 0, 1)
        # flip the values for the y axis
        new_space = numpy.flip(new_space, 0)
        return new_space

    def to_math_space(self, space):
        new_space = numpy.copy(space)
        # (y, x) becomes (x, y)
        new_space = numpy.swapaxes(new_space, 0, 1)
        # flip the values for the y axis
        new_space = numpy.flip(new_space, 1)
        return new_space

    def transform_coordinate_space(self, space, coordinate_space):
        switch = {
            CoordinateSpace.IMAGE: self.to_image_space,
            CoordinateSpace.MATH: self.to_math_space
        }

        return switch[coordinate_space](space)





