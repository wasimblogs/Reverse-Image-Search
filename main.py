import numpy as np
import cv2
import feature
import os
import Faces

import search

def parseQuery(query):

    # print query
    query = str(query)
    path = "G:/Images/Query/"

    if query.__contains__(" "):
        image, cat = query.split(" ")[0], query.split(" ")[1]
        cat.lower()
        print image
    else:
        image = query
        cat = "color"

    name = path + image + '.jpg'

    image = cv2.imread(name)
    cv2.imshow("QUERY IMAGE", image)
    cv2.waitKey(1)
    cv2.moveWindow("QUERY IMAGE", 1400/2, 10)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = Faces.findFace(gray)

    res = []
    if rects != ():
        print "We have a face ! "
        for (x,y,w,h) in rects:
            face = gray[y:y+h, x:x+h]
            search.searchFace3(face, image)

    elif cat == "tshirt" or cat == "t-shirt" or cat == "number":
        # print "Search by edge"
        res = search.searchE(name)

    elif cat == "image" or cat == "" or cat == "color":
        # print "Search by Color"
        res = search.searchC(name)

    elif cat == "quote" or cat == "shape" or cat == "sketch":
        print "Search by edge"
        res = search.searchEC(name, 0.9)

    else:
        res = search.searchC(name)

    if len(res) > 1:
        search.disp(res)

while 1:
    query = raw_input("Search Image :\t")
    parseQuery(query)
