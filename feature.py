import cv2
import numpy as np
import glob


# OPTIMAL 5-4-3
# FACE 1-5-5
# def localPyramidEdgeHist(image):
def pyrEdge(image):
    hist = []
    pyramidNumber = 5
    col = 4
    row = 3
    for k in xrange(0,pyramidNumber):
        histL = []
        query = cv2.Canny(image, 0, 00)
        histL.append(np.sum(query)/(query.size*255.0))
        r, c = image.shape[:2]
        width = c/col
        height = r/row
        startW = 0
        for i in xrange(0,col):
            correct = False
            startH = 0
            for j in xrange(0,row):
                roi = image[startH:startH+height, startW: startW+width]
                startH = startH + height
                edge_Content = np.sum(roi)/(roi.size*255.0)
                histL.append(edge_Content)
            startW = startW + width

            if roi.size == 0:
                correct = True
                break

        if correct:
            # print 'Corrected ',i,j
            histL = []
            for i in xrange(0,col*row):
                histL.append(0.001)
            # print 'Before Normalization\t',histL
            histL = np.ravel(histL)
            histL = cv2.normalize(histL)
            # print 'After normalization \t', histL

        histL = np.ravel(histL)
        histL = cv2.normalize(histL)
        hist.append(histL)
        image = cv2.pyrDown(image)

    hist = np.float32(hist)
    hist = np.ravel(hist)
    return hist

def pyrEdgeF(image):
    hist = []
    pyramidNumber = 1
    col = 8
    row = 8
    for k in xrange(0,pyramidNumber):
        histL = []
        query = cv2.Canny(image, 0, 00)
        histL.append(np.sum(query)/(query.size*255.0))
        r, c = image.shape[:2]
        width = c/col
        height = r/row
        startW = 0
        for i in xrange(0,col):
            correct = False
            startH = 0
            for j in xrange(0,row):
                roi = image[startH:startH+height, startW: startW+width]
                startH = startH + height
                edge_Content = np.sum(roi)/(roi.size*255.0)
                histL.append(edge_Content)
            startW = startW + width

            if roi.size == 0:
                correct = True
                break

        if correct:
            # print 'Corrected ',i,j
            histL = []
            for i in xrange(0,col*row):
                histL.append(0.001)
            # print 'Before Normalization\t',histL
            histL = np.ravel(histL)
            histL = cv2.normalize(histL)
            # print 'After normalization \t', histL

        histL = np.ravel(histL)
        histL = cv2.normalize(histL)
        hist.append(histL)
        image = cv2.pyrDown(image)

    hist = np.float32(hist)
    hist = np.ravel(hist)
    return hist


#OPTIMAL 5-3-2
# FACE 1-5-5
# LOCALISED COLOR HISTOGRAM
def calcHistogram(image):
    bins =10
    hist = []

    r, c = image.shape[:2]
    cols = 3
    rows = 2
    width = c/cols
    height = r/rows
    startW = 0
    for i in xrange(0,cols):
        startH = 0
        for j in xrange(0,rows):
            roi = image[startH:startH+height, startW: startW+width]
            startH = startH + height

            r = cv2.calcHist([roi], [0], None, [bins],[0,256])
            r =cv2.normalize(r)
            hist.append(r)
            g = cv2.calcHist([roi], [1], None, [bins],[0,256])
            g = cv2.normalize(g)
            hist.append(g)
            b = cv2.calcHist([roi], [2], None, [bins],[0,256])
            b = cv2.normalize(b)
            hist.append(b)

        startW = startW + width
    return np.ravel(hist)

def histF(image):
    bins =10
    hist = []

    r, c = image.shape[:2]
    cols = 8
    rows = 8
    width = c/cols
    height = r/rows
    startW = 0
    for i in xrange(0,cols):
        startH = 0
        for j in xrange(0,rows):
            roi = image[startH:startH+height, startW: startW+width]
            startH = startH + height

            r = cv2.calcHist([roi], [0], None, [bins],[0,256])
            r =cv2.normalize(r)
            hist.append(r)

        startW = startW + width
    return np.ravel(hist)


# PURE COLOR
def histCC(image):
    bins =10
    hist = []

    r, c = image.shape[:2]
    r = cv2.calcHist([image], [0], None, [bins],[0,256])
    r =cv2.normalize(r)
    hist.append(r)
    g = cv2.calcHist([image], [1], None, [bins],[0,256])
    g = cv2.normalize(g)
    hist.append(g)
    b = cv2.calcHist([image], [2], None, [bins],[0,256])
    b = cv2.normalize(b)
    hist.append(b)

    return np.ravel(hist)

def pyrHist(image):
    hist = []
    pyramidNumber = 5
    for k in xrange(0,pyramidNumber):
        histL = calcHistogram(image)
        hist.append(histL)
        image = cv2.pyrDown(image)

    hist = np.float32(hist)
    hist = np.ravel(hist)
    return hist
