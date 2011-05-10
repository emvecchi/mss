'''
This program is to compute the effectiveness of text models on semantics similarity measurement
Text features are split into pieces of ordered 4k-block-features
We compute the measurment by using the top 8k, 12k, 16k....64k features
Usage:
@param 1: l
@param 2: alpha (normally take 0.5) for combination of text and image vectors
@param 3: number of block 4k of text features, for example: param3 = 8 means we use 32K text feature to test
@param 4: visual features matrix

python this_file l alpha number_of_block visual_featurefile
where: k is number of 4k-blocks for testing

see the __main__ function to indicate the directory where the feature_list, visual_feature 
-----

'''
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
    
def printvector(v):
    print "number of block " + str(len(v))
    print "size: " + str(len(v[0])) + ":" + str(len(v[1])) + ":" + str(len(v[2])) + ":" +str(len(v[3])) + ":" + str(len(v[4]))   

# TODO:
# 0. Split the big function into subfunctions
# 1. Consider to insert a choice between output into file or db
def cossim(pairList, visualFeatsFile, outputFile):
    PLFile = open(pairList, "r")
    PLLine = PLFile.readline()
    pairsDic = {}
    words = []
    wordsIdxs = []
    iter = 0
    notFound = 0
    while PLLine:
        pair = PLLine.split()
        word0 = pair[0]
        word1 = pair[1]
        if not word0 in words:
            words.append(word0)
        if not word1 in words:    
            words.append(word1)

        if not pairsDic.has_key(word0):
            partners = []
            partners.append(word1)
            pairsDic[word0] = partners
        elif not word1 in pairsDic[word0]:
            pairsDic[word0].append(word1)
                
        PLLine = PLFile.readline()
    
    imagesFeats = {}
    WFFile = open(visualFeatsFile, "r")
    WFLine = WFFile.readline()
    while WFLine:
        values = WFLine.split()
        # TODO: this correction for mix, got to find a general way
        word = values.pop(0)
        numDescrs = len(values)
        if word in words:
            #print word
            wordFeats = np.zeros((numDescrs), np.float64)
            featIdx = 0
            for feat in values:
                feat = float(feat)
                wordFeats[featIdx] = feat
                featIdx += 1
            imagesFeats[word] = wordFeats
        WFLine = WFFile.readline()    
    
    # Here i populate the list of all the words-feats files
    wordsFiles = os.listdir(textFeatDirectory)
    #Open the output file
    OFile = open(outputFile, 'w')
    for word0 in pairsDic:
        if not word0 in wordsFiles or not word0 in imagesFeats:
            continue
        vv0 = readWord(word0)
        v0 = []
        for i in range(0, len(vv0)):
            v0.append(np.array(vv0[i]))
        image_v0 =  imagesFeats[word0]
        if (norm(image_v0) !=0):
            image_v0 = image_v0/norm(image_v0)
        else:
            continue

        #If need to weight the text,  using this 
        #for blocknum in range(0, len(v0)):
        #    if norm(v0[blocknum]) !=0:
        #        v0[blocknum] = v0[blocknum]/norm(v0[blocknum])

        for word1 in pairsDic[word0]:
            if not word1 in wordsFiles or not word1 in imagesFeats:
                continue
            vv1 = readWord(word1)
            v1 = []
            for i in range(0, len(vv1)):
                v1.append(np.array(vv1[i]))
            image_v1 =  imagesFeats[word1]
            if (norm(image_v1) !=0):
                image_v1 = image_v1/norm(image_v1)
            else:
                continue
            #If need to weight the text, using this
            #for blocknum in range(0, len(v0)):
            #    if norm(v1[blocknum]) >0:
            #        v1[blocknum] = v1[blocknum]/norm(v1[blocknum])

            #concatenation 
            #Concat image features and text features
                        
            #liner method with parameter alpha
            pairCosine = 0

                        
            if (sys.argv[1] == "l"): 
                #Linear combination
                #Alpha is not important here because we dont concat text with vision
                alpha = eval(sys.argv[2])
                text_v0 = v0[0]
                text_v1 = v1[0]
                blocknum = eval(sys.argv[3]) #Number of 4k text blocks
                if blocknum > len(v0):
                    print "Number of tested blocks is out of index"
                    sys.exit()

                for bl in range(1,blocknum):
                    text_v0 = np.concatenate((text_v0, v0[bl]))
                    text_v1 = np.concatenate((text_v1, v1[bl]))

                if (norm(text_v0) >0):
                    text_v0 = text_v0/norm(text_v0)
                if (norm(text_v1) >0):
                    text_v1 = text_v1/norm(text_v1)
                
                 
                concat0 = np.concatenate((alpha * text_v0, (1-alpha) * image_v0))
                concat1 = np.concatenate((alpha * text_v1, (1-alpha) * image_v1))
                #print norm(image_v0) * norm(image_v1)
                if (norm(concat0) >0):
                    concat0 = concat0/norm(concat0)
                if (norm(concat1) >0):
                    concat1 = concat1/norm(concat1)

                pairCosine = float(dot(concat0,concat1))

                #pairCosine = float(dot(text_v0,text_v1))
                OFile.write(word0 + ' ' + word1 + ' ' + str(pairCosine))
                OFile.write('\n')
    OFile.close()        
    
if __name__=="__main__":
    global textFeatDirectory
    print "Reading the feature list"
    readFeatureList("./featureValue_64k.txt")
    textFeatDirectory  = "./top_n/word_list_k64"

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

    _visualFile = sys.argv[4]
    _visualFeatFile = "./esp/new-esp-data/vision-matrix/" + _visualFile

    _outFile = "./WS.vision.only." + sys.argv[3] + "." + _visualFile
    
    cossim(_pairList, _visualFeatFile, _outFile)

    
