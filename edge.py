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

filepath = "receipt2.jpg"

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
#transformed = CoordinateSpaceConverter.transform(transformed, CoordinateSpace.IMAGE)
#transformed = cv.resize(transformed, (transformed.shape[0] * 4, transformed.shape[1] * 4))
#transformed = numpy.swapaxes(transformed, 0, 1)
#[[  1  34]
 #[  1 107]
 #[ 61  36]
 #[ 61 109]
 #[120  33]
 #[120 106]]
lines = hough.to_lines(maximas)
#lines = numpy.array([
#    Line(normal_vector=Vector([64.5, 1]), constant_term=2205.95)
#])
original = cv.imread(filepath)
original = cv.resize(original, (edge_detector.width, edge_detector.height))
# test = numpy.zeros((200, 200, 3))
original_with_lines = hough.draw_onto_image(lines, original)
'''
pff = Cluster.cluster(kp.astype(numpy.float), 2, 5, 1)

cols_count = range(0, kp.shape[1]-1)
rows = np.arange(2, 5, 1)

data = []
# get each column as x-value
for x in cols_count:
    scatter = go.Scatter(
        x = pff[:, x],
        y = rows,
        mode = 'markers',
        name = 'markers',
        connectgaps=False,
        marker=dict(
            size=10
        )
    )
    data.append(scatter)

layout = go.Layout(title="First Plot", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})
figure = go.Figure(data=data, layout=layout)
plotly.offline.plot(figure, filename='scatterfromhough.html')
'''
cv.imshow(kWinName, original_with_lines)
cv.waitKey()
