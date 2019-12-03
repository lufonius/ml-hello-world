import numpy
from package.linear_algebra.line_copy import *
from package.hough_transform.cells.root_cell import RootCell
from package.drawing.image import Image

# the accumulator is an object holding the values for the hough transform
# it uses a tree data structure in combination with the composite pattern, so it's
# easier to get neighbour values until a certain level around it.
# since the whole range checking is done in the tree data structure, we don't hav to care
# about it here
class Accumulator:
    def __init__(self, image: Image, angle_step=1):
        self.accumulator = {}
        self.angle_step = angle_step
        self.image = image
        self.biggest_vote = 0

        self.p_axis_size = self._get_p_axis_size(image)
        self.angle_axis_size = self.angles().size

    def angles(self):
        return numpy.arange(
            0,
            360,
            self.angle_step
        )

    def _get_p_axis_size(self, image):
        # image diagonal is the p axis range
        return math.ceil(math.sqrt((image.width/2)**2 + (image.height/2)**2))

    def __getitem__(self, keys):
        angle, p = self.get_angle_p(keys)

        position_hash = hash((angle, p))

        return self.accumulator[position_hash]

    def vote(self, angle, p):
        # angle, p = self.get_angle_p([angle, p])

        position_hash = hash((angle, p))

        if not position_hash in self.accumulator:
            root_cell = RootCell()
            root_cell._angle_step = self.angle_step
            root_cell.angle = angle
            root_cell.p = p
            self.accumulator[position_hash] = root_cell

        self.accumulator[position_hash].vote()
        votes = self.accumulator[position_hash].votes

        if (votes > self.biggest_vote):
            self.biggest_vote = votes

    def votes_median(self):
        cells_arr = numpy.array([cell.votes for cell in self.accumulator.values()])
        unique_sorted_arr = numpy.sort(numpy.unique(cells_arr))
        middle_index = int(len(unique_sorted_arr) / 2)
        median = unique_sorted_arr[middle_index]
        return median

    def get_angle_p(self, keys):
        if len(keys) != 2:
            raise Exception('you must access the accumulator with the x and y values')
        angle, p = keys[0], keys[1]

        if angle > 360:
            raise Exception('you provided an angle bigger than 360')

        if p > self.p_axis_size:
            raise Exception('you provided a p-index bigger than possible')

        return angle, p

    # TODO: still needed?
    def to_image(self) -> numpy.ndarray:
        angles = self.angles()
        image = numpy.zeros((self.p_axis_size, angles.size))
        for p in range(0, self.p_axis_size - 1):
            for angle in angles:
                position_hash = hash((angle, p))
                votes = self.accumulator[position_hash].votes
                votes_as_grayscale = votes * 255 / self.biggest_vote
                image[p, angle] = votes_as_grayscale

        return image


