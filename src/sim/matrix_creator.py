"""
This program is to create the vector space model matrix that is combined of both vision semantics and text semantics
@param 1 = l
@param 2 = alpha parameter to weight 2 vectors vision, text
@param 3 = number of blocks 4k to use to concat in text vector, for example: 8 --> 32k text features will be used
"""

import sys
import os
import numpy as np
from numpy import dot
from numpy.linalg import norm
from numpy.ctypeslib import _num_fromflags

"""
"""
DEBUG = 0

featureDic = {}
allfeat = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[], [], [], []]

wordlist = []

#reading the list of words then to generate the corresponding list of vector
def readwordlist(filename):
    Flist = open(filename, 'r')
    global wordlist
    for line in Flist:
        line.strip()
        line = line.replace('\n', '')
        wordlist.append(line)
    Flist.close()
    

#This function is to read the features of a word into some blocks of features
#Each block of feature contains features that have same value 
def readWord(word):
    global featureDic
    top = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
    vector = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    Wfile = open(os.path.join(textFeatDirectory, word), "r")
    for line in Wfile:
        feature, score = line.split()
        blocknum = featureDic[feature]
        top[blocknum][feature] = float(score)
    Wfile.close()
    
    #Vector found
    for i in range(0,len(allfeat)):
        for j in range(0, len(allfeat[i])):
            if allfeat[i][j] in top[i]:
                vector[i].append(top[i][allfeat[i][j]])
            else:
                vector[i].append(float(0))
    return vector

#This program is to read the list of features and their asscociate assigned block
def readFeatureList(featurelist):
    global featureDic
    global allfeat
    featureDic = {}
    Ffeat = open(featurelist, 'r')
    
    for line in Ffeat:
        feature, blocknum = line.split()
        featureDic[feature] = int(blocknum) -1 
        allfeat[int(blocknum)-1 ].append(feature)
    Ffeat.close()
    printvector(allfeat)

def tostr(value):
    if (value >0):
        return "%.10f" %value
    else:
        return "%.0f" %value
    
def printvector(v):
    print "number of block " + str(len(v))
    print "size: " + str(len(v[0])) + ":" + str(len(v[1])) + ":" + str(len(v[2])) + ":" +str(len(v[3])) + ":" + str(len(v[4]))   

# TODO:
# 0. Split the big function into subfunctions
# 1. Consider to insert a choice between output into file or db
def cossim(pairList, visualFeatsFile, outputFile, numDescrs):
    global wordlist
    wordsIdxs = []
    iter = 0
    notFound = 0
    
    imagesFeats = {}
    WFFile = open(visualFeatsFile, "r")
    WFLine = WFFile.readline()
    _count = 0
    while WFLine:
        values = WFLine.split()
        # TODO: this correction for mix, got to find a general way
        word = values.pop(0)
        if word in wordlist:
            _count+=1
            wordFeats = np.zeros((numDescrs), np.float32)
            featIdx = 0
            for feat in values:
                feat = float(feat)
                wordFeats[featIdx] = feat
                featIdx += 1
            imagesFeats[word] = wordFeats
        WFLine = WFFile.readline() 
        print _count
    print "The coverage of fulldata is " + str(float(_count) / len(wordlist))
    # Here i populate the list of all the words-feats files
    wordsFiles = os.listdir(textFeatDirectory)
    #Open the output file
    OFile = open(outputFile, 'w')
    _count = 0
    for word0 in wordlist:
        if not word0 in wordsFiles or not word0 in imagesFeats:
            continue
        _count +=1
        print _count
        vv0 = readWord(word0)
        v0 = []
        for i in range(0, len(vv0)):
            v0.append(np.array(vv0[i]))
        image_v0 =  imagesFeats[word0]
        if (norm(image_v0) !=0):
            image_v0 = image_v0/norm(image_v0)
        else:
            continue
        #for blocknum in range(0, len(v0)):
        #    if norm(v0[blocknum]) !=0:
        #        v0[blocknum] = v0[blocknum]/norm(v0[blocknum])

        #concatenation 
        #Concat image features and text features
                        
        #liner method with parameter alpha
        if (sys.argv[1] == "l"): 
            #Linear combination
            alpha = eval(sys.argv[2])
            text_v0 = v0[0]
            blocknum = eval(sys.argv[3]) #Number of 4k text blocks
            if blocknum > len(v0):
                print "Number of tested blocks is out of index"
                sys.exit()

            for bl in range(1,blocknum):
                text_v0 = np.concatenate((text_v0, v0[bl]))

            if (norm(text_v0) >0):
                text_v0 = text_v0/norm(text_v0)
                 
            concat0 = np.concatenate((alpha * text_v0, (1-alpha) * image_v0))
            #print norm(image_v0) * norm(image_v1)
            if (norm(concat0) >0):
                concat0 = concat0/norm(concat0)

            OFile.write(word0 + ' ')
            #print the combined model, comment next 2 lines if don't want to do so
            #for i in range(0, len(concat0)):
            #    OFile.write(tostr(concat0[i]) + ' ')
            
            #print the text model only, comment next 2 lines if don't want to do so
            #for i in range(0, len(text_v0)):
            #    OFile.write(tostr(text_v0[i]) + ' ')
            
            #print the vision model only, comment next 2 lines if don't want to do so
            for i in range(0, len(image_v0)):
                OFile.write(tostr(image_v0[i]) + ' ')

            OFile.write('\n')
    OFile.close()        
    
if __name__=="__main__":
    global textFeatDirectory
    print "Reading the feature list"
    readFeatureList("./featureValue_64k.txt")
    textFeatDirectory  = "./top_n/word_list_k64"
    readwordlist("./all-elements.txt")
    print "Total word to form vectors: "+ str(len(wordlist))
    global DEBUG
    if DEBUG == 1:
        v = readWord("zoo-n")
        x = []
        x.append(np.array(v[0]))
        x.append(np.array(v[1]))
        print type(x[1])
        printvector(v)
        sys.exit()
    _pairList = "./cleaned-wordsim-all.txt"
    _visualFeatFile = "./esp/new-esp-data/vision-matrix/vision-20k.txt"

    _outFile = "./matrix/vision-20k-only.txt"
    _numDescription = 20000
    cossim(_pairList, _visualFeatFile, _outFile, _numDescription)

    
