import cv2
import feature
import glob
import numpy as np
import pickle
import Faces

def disp(list):
    for (score,names) in list:
        image = cv2.imread(names)
        cv2.imshow("SEARCH RESULT", image)
        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()
            break


# Find closest matching face
# REQUIRES FACE as INPUT
def searchFace3(query, people):
    """REQUIRES FACE AS INPUT"""
    histQC = feature.histF(query)
    histQE = feature.pyrEdgeF(query)
    edgefile = open("G:\ImageS/faceEdge.csv", "r")
    colfile = open("G:\ImageS/faceColor.csv", "r")

    # SEARCH BY COLOR
    list = []
    count  = 0
    while 1:
        try:
            edgeF = pickle.load(edgefile)
            name1, e = edgeF[0][0], edgeF[0][1]

            colF = pickle.load(colfile)
            name2, c = colF[0][0], colF[0][1]

            scoreC = cv2.compareHist(histQC, c, cv2.cv.CV_COMP_CORREL)
            scoreE = cv2.compareHist(histQE, e, cv2.cv.CV_COMP_CORREL)

            score = scoreC + scoreE
            if score > 1:
                list.append((score,name1))

        except:
            print "END OF FILE REACHED"
            break

    list.sort()
    list.reverse()
    # return list
    print list

    # CONVERTING FACE LIST TO IMAGE LIST
    path = "G:/Images/Feature"
    temp = []
    for score, name in list:
        kf = name.split(",")[0].split("\\")[1]
        name = path + '/' + kf
        temp.append(name)

    histQC = feature.histF(people)
    histQE = feature.pyrEdgeF(people)
    rank = []
    for name in temp:
        res = cv2.imread(name)
        c = feature.histF(res)
        e = feature.pyrEdgeF(res)

        scoreC = cv2.compareHist(histQC, c, cv2.cv.CV_COMP_CORREL)
        scoreE = cv2.compareHist(histQE, e, cv2.cv.CV_COMP_CORREL)

        if scoreC > 0.042 and scoreE > 0.05:
            score = scoreE + scoreC
            # if score > 0.35:
            rank.append((score, name))

            if score < 1:
                print '\n\nC SCORE : ', scoreC
                print 'E SCORE : ', scoreE
                cv2.imshow("UNPRO", cv2.imread(name))
                cv2.moveWindow("UNPRO", 600,10)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    rank.sort()
    rank.reverse()

    for (score, name) in rank:
        cv2.imshow("RESULT\t"+str(score), cv2.imread(name))
        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()
            break
        cv2.destroyAllWindows()

# Find closest matching face
def searchFace(name):
    query = cv2.imread(name)

    histQC = feature.pyrHist(query)
    histQE = feature.pyrEdgeF(query)
    folder = glob.glob("D:/Images/Face/*.*")

    # SEARCH BY COLOR
    list1 = []
    count  = 0
    l = len(folder)
    for files in folder:
        # print 'Count \t', count,'  /  ',l,'\t',files
        image = cv2.imread(files)
        hist = feature.pyrHist(image)
        score = cv2.compareHist(histQC, hist, cv2.cv.CV_COMP_CORREL)
        list1.append((score,files))
        count = count + 1

    # SEARCH BY EDGE
    list2 = []
    count  = 0
    l = len(folder)
    for files in folder:
        # print 'Count \t', count,'  /  ',l,'\t',files
        image = cv2.imread(files)
        hist = feature.pyrEdge(image)
        score = cv2.compareHist(histQE, hist, cv2.cv.CV_COMP_CORREL)
        list2.append((score,files))
        count = count + 1

    list = []
    # OPTIMAL 0.8   85%
    # 0.5 80
    # 0.1 60
    weight = 0.8
    for i in xrange(0, len(list1)):
        # print list1[i][0],'\t', list2[i][0]
        t_score = (1-weight)*list1[i][0] + weight*list2[i][0]
        if t_score > 0.85:
            # list.append((t_score,list1[i][1]))
            list.append(list1[i][1])
        # print list1[i][1] ==  list2[i][1]
    list.sort()
    list.reverse()
    return list

# SEARCH EDGE AND COLOR
def searchEC(name, weight):
    query = cv2.imread(name)
    histQE = feature.pyrEdge(query)
    histQC = feature.pyrHist(query)
    folder = glob.glob("G:/Images/Feature/*.*")
    edge = open("G:\ImageS\edge.csv", "r")
    color = open("G:\ImageS\color.csv", "r")

    eRank = []
    Rank = []
    fileRead = 0

    weight = 0.6
    while 1:
        try:
            e = pickle.load(edge)
            name2, freq = e[0][0], e[0][1]
            l = pickle.load(color)
            name1, col = l[0][0], l[0][1]
            scoreE = cv2.compareHist(histQE, freq, cv2.cv.CV_COMP_CORREL)
            scoreC = cv2.compareHist(histQC, col, cv2.cv.CV_COMP_CORREL)
            score = (1-weight)*scoreC + weight*scoreE
            if score > 0.8:
                Rank.append((scoreE, name1))
            fileRead +=1
            # print 'FIle read', fileRead, '\t', name1
        except:
            break

    edge.close()
    color.close()

    Rank.sort()
    Rank.reverse()


    return Rank
    # for (score, name) in Rank:
    #     image = cv2.imread(name)
    #     nn = "SEARCH RESULTS   "+str(score)
    #     cv2.imshow("SEARCH RESULTS", image)
    #     k = cv2.waitKey(0)
    #     if k == 27:
    #         cv2.destroyAllWindows()
    #         break

# SEARCH LOCALISED COLOR
def searchC(name):

    query = cv2.imread(name)

    histQC = feature.pyrHist(query)
    folder = glob.glob("G:/Images/Feature/*.*")

    color = open("G:\ImageS\color.csv", "r")

    eRank = []
    Rank = []
    fileRead = 0
    # print pickle.load(color)

    while 1:
        try:
            c = pickle.load(color)
            name1, col = c[0][0], c[0][1]
            # print name1
            scoreC = cv2.compareHist(histQC, col, cv2.cv.CV_COMP_CORREL)
            if scoreC > 0.5:
                Rank.append((scoreC, name1))
            fileRead +=1
            # print 'FIle read', fileRead, '\t', name1
        except:
            # print "END OF FILE REACHED"
            break

    color.close()
    Rank.sort()
    Rank.reverse()

    return Rank

    # for (score, name) in Rank:
    #     image = cv2.imread(name)
    #     cv2.imshow("SEARCH RESULTS", image)
    #     k = cv2.waitKey(0)
    #     if k == 27:
    #         cv2.destroyAllWindows()
    #         break

# PURE COLOR SEARCH
def searchCC(name):

    query = cv2.imread(name)

    histQC = feature.pyrHist(query)
    folder = glob.glob("G:/Images/Feature/*.*")

    color = open("G:\ImageS\CC.csv", "r")

    eRank = []
    Rank = []
    fileRead = 0
    # print pickle.load(color)

    while 1:
        try:
            c = pickle.load(color)
            name1, col = c[0][0], c[0][1]
            # print name1
            scoreC = cv2.compareHist(histQC, col, cv2.cv.CV_COMP_CORREL)
            if scoreC > 0.8:
                Rank.append((scoreC, name1))
            fileRead +=1
        except:
            # print "END OF FILE REACHED"
            break

    color.close()
    Rank.sort()
    Rank.reverse()

    return Rank

def searchE(name):
    query = cv2.imread(name)
    histQE = feature.pyrEdge(query)
    folder = glob.glob("G:/Images/Feature/*.*")
    edge = open("G:\ImageS\edge.csv", "r")

    eRank = []
    Rank = []
    fileRead = 0

    weight = 0.6
    while 1:
        try:
            e = pickle.load(edge)
            name2, freq = e[0][0], e[0][1]
            scoreE = cv2.compareHist(histQE, freq, cv2.cv.CV_COMP_CORREL)
            if scoreE > 0.5:
                Rank.append((scoreE, name2))
            fileRead +=1
            # print 'FIle read', fileRead, '\t', name1
        except:
            # print "END OF FILE REACHED"
            break

    edge.close()

    Rank.sort()
    Rank.reverse()
    return Rank

    # for (score, name) in Rank:
    #     image = cv2.imread(name)
    #     nn = "SEARCH RESULTS   "+str(score)
    #     cv2.imshow("SEARCH RESULTS", image)
    #     k = cv2.waitKey(0)
    #     if k == 27:
    #         cv2.destroyAllWindows()
    #         break

def saveSearch(name):
    result = searchE(name)
    file = open("G:\ImageS/tshirt.csv", "w")
    for (score, name) in list :
        pickle.dump(name,file)
    file.close()

def writeColor(image):
    list = searchC(image)
    color = open("G:\ImageS/black.csv", "w")
    for (score, name) in list :
        pickle.dump(name,color)
    color.close()


image = "G:/IMages/Query/Black.jpg"
# writeColor(image)
# Repeat this thing for all the colors


