import math
import numpy
import cv2 as cv
import typing
from sklearn.cluster import DBSCAN
from package.utils.coordinate_space import CoordinateSpace
from package.utils.coordinate_space_converter import CoordinateSpaceConverter
from package.utils.memoize import Memoize
from package.linear_algebra.line import Line
from package.linear_algebra.vector import Vector

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
            grayscale = image[x, y] if len(image.shape) < 3 else image[x, y][0]
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
                    # BIG NOTE: If you're going to calculate with the angle, you have to multiply the index
                    # times the step
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

    def get_local_maximas(self, grayscale_parameter_matrice):
        clusters = DBSCAN(0.5).fit(grayscale_parameter_matrice)
        maximas = numpy.empty((0, 2))
        for (x, y) in numpy.ndindex(grayscale_parameter_matrice.shape[:2]):
            if grayscale_parameter_matrice[x, y] > 100:
                maximas = numpy.append(maximas, numpy.array([[x, y]]), axis=0)

        return maximas.astype(numpy.uint8)

    # TODO: improve to always get maximas ... now only values greater than
    # 255 are being recognised
    def mark_maximas(self, grayscale_parameter_matrice, maximas):
        rgb_parameter_matrice = cv.cvtColor(grayscale_parameter_matrice, cv.COLOR_GRAY2BGR)
        for i in numpy.ndindex(maximas.shape[:1]):
            rgb_parameter_matrice[maximas[i[0], 0], maximas[i[0], 1]] = [125, 0, 190]

        return rgb_parameter_matrice

    # TODO: move this into another class ... it's just from hesse normal form to the other one
    def to_lines(self, maximas) -> numpy.ndarray:
        lines = numpy.empty((0, ))
        for (i) in numpy.ndindex(maximas.shape[:1]):
            p = maximas[i[0], 1] # magnitude of the vector
            angle = maximas[i[0], 0] * self.angle_range["step"] # direction
            normal_vector = Vector.from_magnitude_angle(p, angle)
            x_intercept = p / math.cos(math.radians(angle))
            # now we can calculate the constant term k
            # since Ax + By = k
            # A = normal_vector[0]
            # x = x_intercept
            # y = 0
            # so Ax = k
            constant_term = normal_vector[0] * x_intercept
            line = Line(normal_vector, constant_term)
            lines = numpy.append(lines, numpy.array([line]), axis = 0)

        return lines

    # TODO: move to another class
    def draw_onto_image(self, lines: numpy.ndarray, image: numpy.ndarray) -> numpy.ndarray:
        image_math_space = CoordinateSpaceConverter.transform(image, CoordinateSpace.MATH)
        image_width = image_math_space.shape[0]
        image_height = image_math_space.shape[1]

        for (i) in numpy.ndindex(lines.shape[:1]):
            for x in range(0, image_width -1, 1):
                new_x = math.floor(x - (image_width / 2))
                new_y = math.floor(lines[i[0]].get_y(new_x))

                if -image_height < new_y < image_height:
                    image_math_space[new_x, new_y] = [120, 0, 190]

        return CoordinateSpaceConverter.transform(image_math_space, CoordinateSpace.IMAGE)


