import cv2 as cv
import numpy
import unittest
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
from cluster import Cluster
from package.linear_algebra.vector import Vector
from package.linear_algebra.line_copy import Line

from package.hough_transform.hough import Hough
from package.edge_detection.edge import EdgeDetector
from package.utils.coordinate_space_converter import CoordinateSpaceConverter
from package.utils.coordinate_space import CoordinateSpace

## Create a display window
kWinName = 'Holistically-Nested_Edge_Detection'
cv.namedWindow(kWinName, cv.WINDOW_AUTOSIZE)

filepath = "receipt3.jpg"
original = cv.imread(filepath)

height, width = original.shape[:2]
new_width = 300
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
transformed = hough.transform(out)
maximas = hough.get_local_maximas(transformed)
# transformed = hough.mark_maximas(transformed, maximas)
lines = hough.to_lines(maximas)
'''lines = [
    Line(Vector([31.98, 1.16]), 1024),
    Line(Vector([-3.24, 92.94]), 8649),
    Line(Vector([-25, 0.01]), 625),
    Line(Vector([-6, -85.8]), 7396)
]'''
#original_with_lines = hough.draw_onto_image(np.array(lines), original)
quadrilaterals = hough.get_quadrilaterals(original, lines)
quadrilateral = hough.most_likely_quadrilateral(out, quadrilaterals)
hough.draw_quadrilateral(original, quadrilateral)

cv.imshow(kWinName, original)
cv.waitKey()
