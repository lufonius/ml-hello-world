import cv2 as cv
import numpy as np

class CropLayer(object):
    def __init__(self, params, blobs):
        self.xstart = 0
        self.xend = 0
        self.ystart = 0
        self.yend = 0

    # Our layer receives two inputs. We need to crop the first input blob
    # to match a shape of the second one (keeping batch size and number of channels)
    def getMemoryShapes(self, inputs):
        inputShape, targetShape = inputs[0], inputs[1]
        batchSize, numChannels = inputShape[0], inputShape[1]
        height, width = targetShape[2], targetShape[3]

        self.ystart = (inputShape[2] - targetShape[2]) // 2
        self.xstart = (inputShape[3] - targetShape[3]) // 2
        self.yend = self.ystart + height
        self.xend = self.xstart + width

        return [[batchSize, numChannels, height, width]]

    def forward(self, inputs):
        return [inputs[0][:,:,self.ystart:self.yend,self.xstart:self.xend]]


class EdgeDetector:

    def __init__(
            self,
            width = 500,
            height = 500,
            prototxt = "deploy.prototxt",
            caffemodel = "hed_pretrained_bsds.caffemodel"
    ):
        self.prototxt = prototxt
        self.caffemodel = caffemodel
        self.height = height
        self.width = width
        self.net = cv.dnn.readNet(self.prototxt, self.caffemodel)
        cv.dnn_registerLayer('Crop', CropLayer)

    def detect_edges(self, filepath):
        inp = self.prepare_blob(filepath)
        self.net.setInput(inp)
        out = self.net.forward()
        out = out[0, 0]
        # out = cv.resize(out, (cap.shape[1], cap.shape[0]))
        out = 255 * out
        out = out.astype(np.uint8)

        return out

    def prepare_blob(self, filepath):
        cap = cv.imread(filepath)
        return cv.dnn.blobFromImage(cap, scalefactor=1.0, size=(self.width, self.height),
                                   mean=(104.00698793, 116.66876762, 122.67891434),
                                   swapRB=False, crop=False)