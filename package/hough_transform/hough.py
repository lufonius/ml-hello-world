import numpy
import cv2 as cv
import typing
from package.utils.memoize import Memoize
from package.linear_algebra.line_copy import *
from package.linear_algebra.vector import Vector
from package.linear_algebra.section import Section
import itertools
import random
from package.drawing.image import Image
from package.hough_transform.accumulator import Accumulator
from package.utils.origin_transform_strategies import image_to_math

class Hough:
    # condition for voting
    grayscale_bias = 75

    @Memoize  # omg i love python!
    def _cos_angle(self, angle):
        return math.cos(math.radians(angle))

    @Memoize
    def _sin_angle(self, angle):
        return math.sin(math.radians(angle))

    # later on, when we provide this as a service, we could
    # keep some results (till 300x300 image) in the memory
    # to make it faster
    # memoizing cos and sin is good for now
    # p = x * cos(angle) + y * sin(angle) => see hesse normal form
    def p_fn(self, angle, x, y):
        result = x * self._cos_angle(angle) + y * self._sin_angle(angle)
        return result

    def transform(self, image, precision=1):
        as_image = Image(image)
        accumulator = Accumulator(as_image, precision)
        pixels = as_image.image_pixels()
        angles = accumulator.angles()
        for image_point in pixels:
            # we're using the image directly, because accessing the numpy array directly is faster
            grayscale = image[image_point.y, image_point.x]
            if grayscale > self.grayscale_bias:
                as_math = image_to_math(image_point, as_image.width, as_image.height)
                for angle in angles:
                    p = math.floor(self.p_fn(angle, as_math.x, as_math.y))
                    accumulator.vote(angle, p)

        return accumulator

    def get_local_maximas(self, accumulator: Accumulator):
        median_votes = accumulator.votes_median()
        local_maximas = {}
        for cell in accumulator.accumulator.values():
            if cell.votes < median_votes:
                continue
            is_local_maxima = True
            # we add all of the neighbours around the cells to the cells
            neighbours = cell.get_surrounding_cells(1, accumulator.p_axis_size)
            for neighbour_cell in neighbours.values():
                # there might be the case that there were no votes on a cell, so that means
                # that the cell is not existent in the accumulator. we have to check
                # if the key exists, otherwise there will be a keyError
                neighbour_cell_hash = hash(neighbour_cell)
                if neighbour_cell_hash in accumulator.accumulator.keys():
                    if accumulator.accumulator[neighbour_cell_hash].votes > cell.votes:
                        is_local_maxima = False
                        break

            if is_local_maxima:
                local_maximas[hash(cell)] = cell

        # maybe we can solve this more elegant with a better data structure?
        copy_local_maximas = list(local_maximas.copy().values())

        # this line is important, it makes the maximas much more accurate
        copy_local_maximas.sort(key=lambda cell: cell.votes, reverse=True)

        # what this basically does is to look around 10 cells and check if
        # in this range is any local maxima
        # if so, we remove it
        # we could also increase the level until the local median
        # is smaller than the median
        # or just consider the variation in other ways
        for maxima in copy_local_maximas:
            if hash(maxima) in local_maximas:
                level = 10
                surrounding_cells = maxima.get_surrounding_cells(level, accumulator.p_axis_size)
                for neighbour_cell in surrounding_cells.values():
                    if hash(neighbour_cell) in local_maximas:
                        del local_maximas[hash(neighbour_cell)]

        return local_maximas

    # TODO: move this into another class ... it's just from hesse normal form to the vector form
    def to_lines(self, maximas) -> typing.List[Line]:
        lines = []
        for maxima in maximas.values():
            normal_vector = Vector.from_magnitude_angle(maxima.p, maxima.angle)
            y_intercept = maxima.p / math.cos(math.radians(maxima.angle))
            # now we can calculate the constant term k
            # since Ax + By = k
            # A = normal_vector[0]
            # x = x_intercept
            # y = 0
            # so Ax = k
            constant_term = normal_vector[0] * y_intercept
            line = Line(normal_vector, constant_term)
            lines.append(line)

        return lines

    def draw_onto_image(self, lines: typing.List[Line], image_arr: numpy.ndarray):
        image = Image(image_arr)

        for line in lines:
            image.draw_line(line)

        return image.image

    def get_quadrilaterals(self, image: numpy.array, lines: typing.List[Line]) -> typing.List:
        image_drawing = Image(image=image)
        tl = Point([-image.shape[1] / 2, image.shape[0] / 2])
        br = Point([image.shape[1] / 2, -image.shape[0] / 2])
        # lets review combinations in statistics
        # and also how to do this algorithm by hand
        line_combinations = itertools.combinations(lines, 4)

        quadrilaterals = []
        for combination in line_combinations:
            quadrilateral = []
            is_quadrilateral = True
            for line in combination:
                # we check each line against the other line
                # every line has to cross 2 other lines, otherwise it's not a quadrilateral
                intersections_for_line = []
                for other_line in combination:
                    intersection = line.get_intersection_in_area_with(other_line, tl, br)

                    if intersection is not None:
                        intersection_point = Point([intersection[0], intersection[1]])
                        # image_drawing.set_pixel(intersection_point, [120, 40, 230])
                        intersections_for_line.append(intersection_point)

                if len(intersections_for_line) != 2:
                    is_quadrilateral = False
                    break
                else:
                    quadrilateral.append(Section(intersections_for_line[0], intersections_for_line[1], line))

            if is_quadrilateral:
                quadrilaterals.append(quadrilateral)

        return quadrilaterals

    def most_likely_quadrilateral(self, edge_detected_image: numpy.ndarray, quadrilaterals: typing.List):
        nd_quadrilaterals = numpy.array(quadrilaterals)
        edge_detected_image_drawing = Image(image=edge_detected_image)
        biggest_quadrilateral = {
            "sum": 0,
            "quadrilateral": None,
            "points_n": 0
        }
        # each quadrilateral
        for i in numpy.ndindex(nd_quadrilaterals.shape[:1]):
            i = i[0]
            quadrilateral = nd_quadrilaterals[i]
            quadrilateral_sum = 0
            # quadrilateral_points_n = 0

            # each section
            for j in numpy.ndindex(quadrilateral.shape):
                j = j[0]
                section = quadrilateral[j]
                points_generator = edge_detected_image_drawing.section_points(section)

                # ech point of the section when it would have been drawn onto the image
                for section_point in points_generator:
                    value = edge_detected_image_drawing.get_pixel(section_point)
                    quadrilateral_sum += value

            if quadrilateral_sum > biggest_quadrilateral["sum"]:
                biggest_quadrilateral["sum"] = quadrilateral_sum
                biggest_quadrilateral["quadrilateral"] = quadrilateral

        return biggest_quadrilateral["quadrilateral"]

    def draw_quadrilaterals(self, image: numpy.ndarray, quadrilaterals: typing.List):
        for quadrilateral in quadrilaterals:
            nd_quadrilateral = numpy.array(quadrilateral)
            x_shift = int(image.shape[1] / 2)
            y_shift = int(image.shape[0] / 2)
            for x in numpy.ndindex(nd_quadrilateral.shape):
                x = x[0]
                start = list(int(x) for x in nd_quadrilateral[x].start.shift(x_shift, y_shift).coordinates)
                start[1] = image.shape[0] - start[1]
                end = list(int(x) for x in nd_quadrilateral[x].end.shift(x_shift, y_shift).coordinates)
                end[1] = image.shape[0] - end[1]
                r = random.randint(0, 254)
                g = random.randint(0, 254)
                b = random.randint(0, 254)
                cv.line(image, tuple(start), tuple(end), (120, 0, 230))




