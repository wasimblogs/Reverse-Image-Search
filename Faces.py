import cv2
import numpy as np
import glob
import os
import pickle
import feature

# MAJAKO
def writeEC(path):
    """Writes image - histogram-------Takes path as input"""
    edge = open('G:\ImageS\Edge.csv','w')
    color = open('G:\ImageS\Color.csv','w')
    folder = glob.glob(path+'\*.*')
    col = []
    freq = []
    count = 0
    total = len(folder)
    for files in folder:
        print count, ' / ', total,'\t',files
        count = count +1
        image = cv2.imread(files)
        histC = feature.pyrHist(image)
        histE = feature.pyrEdge(image)
        freq.append((files, histE))
        col.append((files, histC))
        pickle.dump(freq, edge)
        pickle.dump(col, color)
        col.pop()
        freq.pop()
    edge.close()
    color.close()


# TAKES PATH AS INPUT
def writeFaceEC(path):
    """Writes image - histogram-------Takes path as input"""
    edge = open('G:\ImageS\FaceEdge.csv','w')
    color = open('G:\ImageS\FaceColor.csv','w')
    folder = glob.glob(path+'\*.*')
    col = []
    freq = []
    count = 0
    total = len(folder)
    for files in folder:
        print count, ' / ', total,'\t',files
        count = count +1
        image = cv2.imread(files,0)
        histC = feature.histF(image)
        histE = feature.pyrEdgeF(image)
        freq.append((files, histE))
        col.append((files, histC))
        pickle.dump(freq, edge)
        pickle.dump(col, color)
        col.pop()
        freq.pop()
    edge.close()
    color.close()


#PURE SEARCH BY COLOR - NO LOCALIZATION
def writeCC(path):
    """Writes image - histogram-------Takes path as input"""
    color = open('G:\ImageS\CC.csv','w')
    folder = glob.glob(path+'\*.*')
    col = []
    count = 0
    for files in folder:
        print count, ' / ', len(folder), '\t',files
        count = count + 1
        image = cv2.imread(files)
        histC = feature.histCC(image)
        col.append((files, histC))
        pickle.dump(col, color)
        col.pop()
    color.close()


def findFace(image):
    """Takes grey image as input and returns face rectangles"""
    face_cascade = cv2.CascadeClassifier('G:/ImageS/XML/haarcascade_frontalface_alt.xml')
    # shuttle_cascade = cv2.CascadeClassifier('G:/ImageS/haarcascade_profileface.xml')
    # shuttle_cascade = cv2.CascadeClassifier('G:/ImageS/haarcascade_upperbody.xml')
    rects = face_cascade.detectMultiScale(image, 1.3, 5)
    return rects


# TEMPLATE MATCHING ---ISN"T RELIABLE
def matchFace(image, template):
    """image is the template which is searched on template"""
    w, h = template.shape
    res = cv2.matchTemplate(image,template,cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0]+w, top_left[1]+h)
    cv2.rectangle(image,top_left,bottom_right,255,2)
    cv2.imshow('Found Face',image)

    cv2.waitKey(-1)
    cv2.destroyAllWindows()


# GENERATE FACE
def genFace(path):
    """Generates faces with proper names for grouping similar images according to faces"""
    folder = glob.glob(path+'/*.jpg')
    print "Number of elements :\t",folder.__len__()
    count = 0
    # i = len(folder)
    i = 0
    for name in folder:
        # print i,'\t/  ',len(folder),'\t',files
        i = i +1
        image = cv2.imread(name, 0)
        rects = findFace(image)
        nameCount = 0
        for x,y,h,w in rects:
            nn = name.split("\\")[1]
            fname = "G:/Images/Face/"+nn+"," + str(nameCount)+".jpg"
            print fname
            f = image[y:y+h, x:x+w]
            f = cv2.equalizeHist(f)
            cv2.imwrite(fname, f)
            count = count + 1
            nameCount = nameCount +1

# GROUP SIMILAR FACES
def groupFace(path):
    """Uses color and frequency information to group similar images"""
    folder = glob.glob("D:/Images/Face/*.*")
    faceFile = open('D:\ImageS\Faces.csv','w')

    for i in folder:
        name, ext =  i.split(",")
        # print name, '\t', ext
        list = search.searchFace(i)

        group = []
        group.append(name)
        for j in list:
            n, e = j.split(",")
            if n != name:
                group.append(n)
                # print name,'\t\t',n
        if len(group) >1:
            pickle.dump(group, faceFile)
        else:
            # group.append("None")
            pickle.dump(group, faceFile)
        print group
    faceFile.close()


# IMAGE - SIMILAR FACE CONTAINGING IMAGE
# IMAGE ONLY IF NO FACE MATCH
def writeFaceGroups(path):
    """Images - 0/1 0 for lack of face and 1 for presence of face"""
    folder = glob.glob(path+'/*.*')
    groups = open('D:\ImageS/faces.csv','r')
    final = open('D:\ImageS\FinalFace.csv','w')
    list = []
    while 1:
        try:
            l = pickle.load(groups)
            list.append(l)
            # print l
        except:
            print "END OF FILE REACHED"
            break

    count = 0
    for i in xrange(0, len((list))):
        search = True
        l = list[i]
        # print "\n\nFROM LIST : \t", l
        while search:
            print count, "/", len(folder)
            file = folder[count]
            # print "IMAGE : ",file
            # print l,'\n\n'

            lf = l[0].split("\\")[1]
            ff = file.split("\\")[1]

            if lf == ff:
                # print "\n\nYEYYYY...MATCH FOUND"

                temp = []
                for k in l:
                    kf = k.split("\\")[1]
                    name = path + '/' + kf
                    temp.append(name)
                pickle.dump(temp, final)
                search = False

            else:
                pickle.dump(file,final)
                # print "WRITTEN : \t", file

            count = count + 1

    final.close()
    groups.close()


def check():
    # all = open('G:\ImageS/finalface.csv','r')
    all = open('G:\ImageS/black.csv','r')

    while 1:
        try:
            list = pickle.load(all)
            print list

        except:
            print "END OF FILE REACHED"
            break


# path = "D:/Images/feature"

path = "G:/Images/Feature"
# writeEC(path)

# print "GENERATING FACES . . ."
# genFace(path)
#
# print "GROUPING FACES . . ."
# groupFace("")

# print "MAKING THE FILE .. . "
# writeFaceGroups(path)

# print "CHECKING IT ALL . . ."
# check()

# writeEC(path)
# path = "G:/Images/Face"
# writeFaceEC(path)

# writeCC("G:/Images/Feature/")