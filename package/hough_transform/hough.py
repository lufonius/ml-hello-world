import math
import numpy
import cv2 as cv
import typing
from package.utils.coordinate_space import CoordinateSpace
from package.utils.coordinate_space_converter import CoordinateSpaceConverter
from package.utils.memoize import Memoize
from package.linear_algebra.line_copy import Line
from package.linear_algebra.vector import Vector
from package.hough_transform.cells.root_cell import RootCell

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
        image_height = image.shape[1]
        image_width = image.shape[0]

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
                    p = math.floor(self.p_fn(angle_range_array[angle_index], new_x, new_y))
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
        return math.ceil(math.sqrt((image.shape[0]/2)**2 + (image.shape[1]/2)**2))

    def get_local_maximas(self, grayscale_parameter_matrice: numpy.ndarray):
        grayscale_parameter_matrice_pad = numpy.pad(grayscale_parameter_matrice, 1, mode='constant', constant_values=0)
        flat_matrice = grayscale_parameter_matrice.flatten()
        unique_matrice = numpy.sort(numpy.unique(flat_matrice))
        middle_index = int(unique_matrice.shape[0] / 2)
        median = unique_matrice[middle_index]
        shape = grayscale_parameter_matrice_pad.shape[:2]
        acc = {}
        local_maximas = {}
        for (x, y) in numpy.ndindex(shape):
            if(x < 1 or y < 1 or x > shape[0] -2 or y > shape[1] - 2):
                continue
            value = grayscale_parameter_matrice_pad[x, y]
            cell = RootCell(x, y)
            is_local_maxima = True
            if value != 255:
                # we add all of the neighbours around the cells to the cells
                neighbours = grayscale_parameter_matrice_pad[x - 1:x + 2, y - 1:y + 2]
                for (x1, y1) in numpy.ndindex(neighbours.shape):
                    if x1 == 1 and y1 == 1:
                        continue
                    actual_x = x + x1 - 1
                    actual_y = y + y1 - 1
                    neighbour_value = grayscale_parameter_matrice_pad[actual_x, actual_y]
                    if neighbour_value > value or value < median:
                        is_local_maxima = False
                        break

            acc[hash(cell)] = value

            if is_local_maxima:
                cell.value = value # we need the value for sorting
                local_maximas[hash(cell)] = cell

        # maybe we can solve this more elegant with a better data structure?
        copy_local_maximas = list(local_maximas.copy().values())
        # this line is important, it makes the maximas much more accurate
        copy_local_maximas.sort(key=lambda cell: cell.value, reverse=True)

        # what this basically does is to look around 10 cells and check if
        # in this range is any local maxima
        # if so, we remove it
        # we could also increase the level until the local median
        # is smaller than the median
        # or just consider the variation in other ways
        for maxima in copy_local_maximas:
            if hash(maxima) in local_maximas:
                level = 10
                surrounding_cells = []
                # TODO: implement boundary check to make this more efficient
                maxima.get_cells_till_level(level, surrounding_cells)

                keep_going = False
                for cell in surrounding_cells:
                    if hash(cell) in local_maximas:
                        del local_maximas[hash(cell)]
                        # keep_going = True

        return numpy.array([[maxima.x, maxima.y] for maxima in local_maximas.values()])

    # TODO: improve to always get maximas ... now only values greater than
    # 255 are being recognised
    def mark_maximas(self, grayscale_parameter_matrice, maximas):
        rgb_parameter_matrice = cv.cvtColor(grayscale_parameter_matrice, cv.COLOR_GRAY2BGR)
        for i in numpy.ndindex(maximas.shape[:1]):
            rgb_parameter_matrice[maximas[i[0], 0] - 1, maximas[i[0], 1] - 1] = [125, 0, 190]

        return rgb_parameter_matrice

    # TODO: move this into another class ... it's just from hesse normal form to the vector form
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
    def draw_onto_image(self, lines: numpy.ndarray, image: numpy.ndarray):
        width = image.shape[0] - 1
        height = image.shape[1] - 1
        for (i) in numpy.ndindex(lines.shape[:1]):
            line = lines[i[0]]
            line.constant_term += (width / 2) * line.normal_vector[0]
            first_point = (0, int(line.get_y(0)))
            last_point = (width, int(line.get_y(width)))
            if int(line.normal_vector[1]) == 0:
                continue
                #first_point = (int(line.normal_vector[0]), 0)
                #last_point = (int(line.normal_vector[0]), height)
            clipped_line = cv.clipLine((0, 0, image.shape[0], image.shape[1]), first_point, last_point)
            if clipped_line[0]:
                cv.line(image, clipped_line[1], clipped_line[2], (120, 0, 190))

        return image



