import cv2 as cv
import numpy

from package.hough_transform.hough import Hough
from package.edge_detection.edge import EdgeDetector
from package.utils.coordinate_space_converter import CoordinateSpaceConverter
from package.utils.coordinate_space import CoordinateSpace

## Create a display window
kWinName = 'Holistically-Nested_Edge_Detection'
cv.namedWindow(kWinName, cv.WINDOW_AUTOSIZE)

filepath = "outside.jpg"

edge_detector = EdgeDetector(
    200,
    200,
    "package/edge_detection/deploy.prototxt",
    "package/edge_detection/hed_pretrained_bsds.caffemodel"
)
out = edge_detector.detect_edges(filepath)

hough = Hough()

transformed = hough.transform(out)
transformed = CoordinateSpaceConverter.transform(transformed, CoordinateSpace.IMAGE)

# con=np.concatenate((frame,out),axis=1)
cv.imshow(kWinName, transformed)
cv.waitKey()