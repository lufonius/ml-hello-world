import cv2 as cv
from package.hough_transform.hough import Hough
from package.edge_detection.edge import EdgeDetector
from package.linear_algebra.line_copy import Line
from package.hough_transform.cells.cell import Cell
from package.linear_algebra.vector import Vector
import numpy

## Create a display window
kWinName = 'Holistically-Nested_Edge_Detection'
cv.namedWindow(kWinName, cv.WINDOW_AUTOSIZE)

filepath = "receipt3.jpg"
original = cv.imread(filepath)

height, width = original.shape[:2]
new_width = 200
new_height = int(height / (width / new_width))

original = cv.resize(original, (new_width, new_height))

edge_detector = EdgeDetector(
    new_width,
    new_height,
    "package/edge_detection/deploy.prototxt",
    "package/edge_detection/hed_pretrained_bsds.caffemodel"
)
out = edge_detector.detect_edges(filepath)

hough = Hough()
accumulator = hough.transform(out, 2)
# accumulator_image = accumulator.to_image()
maximas = hough.get_local_maximas(accumulator)
'''
maximas = {}
maxima = Cell()
maxima.p = -12.0
maxima.angle = 358.0

maximas[hash(maxima)] = maxima'''

lines = hough.to_lines(maximas)
'''lines = [
    Line(Vector([31.98, 1.16]), 1024),
    Line(Vector([-3.24, 92.94]), 8649),
    Line(Vector([-25, 0.01]), 625),
    Line(Vector([-6, -85.8]), 7396)
]'''
original_with_lines = hough.draw_onto_image(lines, original)
quadrilaterals = hough.get_quadrilaterals(original, lines)
quadrilateral = hough.most_likely_quadrilateral(out, quadrilaterals)
hough.draw_quadrilaterals(original, [quadrilateral])

cv.imshow(kWinName, original)
cv.waitKey()
