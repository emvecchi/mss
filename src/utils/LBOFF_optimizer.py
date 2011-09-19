#To compute the topic modelling of imange labels 
#Note that the before that we have images represented as "bag of visual" words
#The program is freesoftware and can be distributed under GNU license
#Authors: Elia Bruni (2011)
#Modified: Giang Tran Binh (2011)

import pycassa, os, glob, re, math
import numpy as np
from scipy import io
import sys


'''
imageFeatsPath: the folder where to find the computed image features
wordFeatsPath: the folder where to store the final word features
tmpDir: a folder where to put temporary files for the coputation
imageBlockSize: the number of images in each block of computed image features
numDescrs: the number of descriptors for each image
'''

#Read the image feature given its key
def readFeatures(key, filename):
    matfile = io.matlab.loadmat(filename)
    return matfile.get(key)

# TODO:
# 0. IMPORTANT!!!: GOT TO CHECK IF READLINE READS CORRECTLY FROM THE TMPFILE
# 1. Consider to save intermediate files at each iteration to understand how much numbers matter
# 2. Split in sub_functions?
def assignWordFeats(imagesFeatsPath, wordsFeatsPath, imageBlockSize, numDescrs, toZeros):
#def assignWordFeats(imagesFeatsPath, imageBlockSize, numDescrs):
    fileMap =  {}
    fileList = []
    for fname in os.listdir(imagesFeatsPath):
        if (str.endswith(fname, '.mat')):
            key, ext = fname.split('.')
            if (len(key)==20):
                fileList.append(key)
    print len(fileList)
    print "Finish reading file list"
    pool = pycassa.connect('Featurespace')
    CFImageInfos = pycassa.ColumnFamily(pool, 'imageInfos')
    cf_dicStrToIdx = pycassa.ColumnFamily(pool, 'dictionary_strToIdx')
    cf_dicIdxToStr = pycassa.ColumnFamily(pool, 'dictionary_idxToStr')
    
    iter = 0
    fileList.sort()
    wordsFeats = {}
    totFeats = np.zeros((numDescrs), np.float64)
    print "Reading the information of images .....\n"
    imageFeats = 0
    for key in fileList:
        filename = os.path.join(imagesFeatsPath, key + '.mat')
        print "reading file name : " + filename
        imagesFeats =  readFeatures(key, filename)
        imageIdx = 0
        print iter 
        if (iter >=10):
            exit()
        imageIdxMult = iter*imageBlockSize
        for i in range(len(imagesFeats)):
            imageIdx = i + imageIdxMult
            try:
                imageRow  = CFImageInfos.get(str(imageIdx)) #index of the tokens

                for wordIdx in imageRow:
                    #convert wordID to the real token
                    word = cf_dicIdxToStr.get(str(wordIdx))[str(0)]
                    word = word[0:-1]
                    word = word.replace('\n','')
                    print word
                    if not wordsFeats.has_key(word) and not math.isnan(imagesFeats[i][0]):
                        wordsFeats[word] = imagesFeats[i]
                    elif not wordsFeats.has_key(word) and math.isnan(imagesFeats[i][0]):
                        print 'here'
                        wordsFeats[word] = np.zeros((len(imagesFeats[i])), np.float64)
                    elif not math.isnan(imagesFeats[i][0]):
                        wordsFeats[word] = np.add(wordsFeats[word], imagesFeats[i])
                        #totFeats = np.add(totFeats, imagesFeats[i])        
                        #print imagesFeats[i]
                        totFeats = np.add(totFeats, imagesFeats[i])
                        #print 'totFeats[0] before:'
                        #print totFeats[0]
            except Exception, e:
                #print 'exception in CFImageInfos.get(str(imageIdx)): '
                #print ' imageIdx: '
                #print imageIdx
                x = 1

        iter += 1
        #del imagesFeats
    
    N = np.sum(totFeats)
    exit()
    # TODO: change the variable names to that pertaining the formula
    print "Constructing words (image labels) BOW visual features.....\n"
    newWordsFeats = {}
    pcount = 0
    for word in wordsFeats:
        #print 'totFeats[0]:'
        #print totFeats[0] 
        newWordsFeats[word] = np.zeros((numDescrs), np.float64)
        pcount +=1
        if pcount % 200 == 0:
            print pcount
        wordOcc = sum(wordsFeats[word]) 
        if wordOcc != 0:
            colIdx = 0
            for wordFeat in wordsFeats[word]:
                #print 'wordFeat:'
                #print wordFeat
                #print 'totFeats[colIdx]:'
                #print totFeats[colIdx]
                if wordFeat != 0.0 and totFeats[colIdx] != 0.0:
                    totFeat = float(wordFeat * N) / float(totFeats[colIdx] * wordOcc)
                    #print 'totFeat:'
                    #print totFeat
                    newWordFeat = float(wordFeat) * float(math.log(totFeat))
                    #print 'newWordFeat before:'
                    #print newWordFeat
                    if toZeros and newWordFeat < 0.0:
                        newWordsFeats[word][colIdx] = 0.0
                    else:
                        #print 'newWordFeat after:'
                        #print newWordFeat
                        newWordsFeats[word][colIdx] = newWordFeat
                    colIdx += 1
                else:
                    newWordsFeats[word][colIdx] = 0.0
                    colIdx += 1
        else:
            wordsFeats[word][:] = 0

    file = open(wordsFeatsPath, 'w')
    newWordsFeatsKeys = newWordsFeats.keys()
    newWordsFeatsKeys.sort()
    for word in newWordsFeatsKeys:
        file.write(str(word) + ' ')
        for wordFeat in newWordsFeats[word]:
            file.write(str(wordFeat) + ' ')
        file.write('\n')
    file.close()
    #return newWordsFeats        


if __name__ == "__main__":
    imagesFeatsPath = "/Volumes/Working/Works/Bolzano/Thesis/vision/experimental/IFFN_500_v1000"
    wordsFeatsPath = "/Volumes/Working/Works/Bolzano/Thesis/vision/WF/wordfeat_small/oldversion-test-lboff"
    imageBlockSize = 100
    numDescrs = 8000
    toZeros = True
    assignWordFeats(imagesFeatsPath, wordsFeatsPath, imageBlockSize, numDescrs, toZeros)

