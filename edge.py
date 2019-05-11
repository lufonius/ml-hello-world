import cv2 as cv
import numpy

from package.hough_transform.hough import Hough
from package.edge_detection.edge import EdgeDetector
from package.utils.coordinate_space_converter import CoordinateSpaceConverter
from package.utils.coordinate_space import CoordinateSpace

## Create a display window
kWinName = 'Holistically-Nested_Edge_Detection'
cv.namedWindow(kWinName, cv.WINDOW_AUTOSIZE)

filepath = "recipe.jpg"

edge_detector = EdgeDetector(
    200,
    200,
    "package/edge_detection/deploy.prototxt",
    "package/edge_detection/hed_pretrained_bsds.caffemodel"
)
out = edge_detector.detect_edges(filepath)

hough = Hough()

transformed = hough.transform(out)
maximas = hough.get_local_maximas(transformed)
transformed = hough.mark_maximas(transformed, maximas)
transformed = CoordinateSpaceConverter.transform(transformed, CoordinateSpace.IMAGE)
transformed = cv.resize(transformed, (transformed.shape[0] * 4, transformed.shape[1] * 4))
# transformed = numpy.swapaxes(transformed, 0, 1)
lines = hough.to_lines(maximas)

original = cv.imread(filepath)
original = cv.resize(original, (edge_detector.width, edge_detector.height))
test = numpy.zeros((200, 200, 3))
original_with_lines = hough.draw_onto_image(lines, original)

cv.imshow(kWinName, transformed)
cv.waitKey()