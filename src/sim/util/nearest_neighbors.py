'''
This program is to compute the top-n nearest neighbors from bless list of word-relation.
Semantic similarity is measured with cosine similalrity.
Usage:

@param 1: N of top-n nearest neighbors to extract
@param 2: bless list in format <concept class relation relatum>
@param 3: features matrix
@param 4: ouput file

-----
'''

import sys, fileinput
from numpy.linalg import norm
from numpy import *
from operator import itemgetter
from heapq import nlargest

bless_words = []
bless_types = {}
features = {}
cosine_pairs = {}



def read_bless_pairs(pairs_list):
    global bless_pairs 
    pairs_file = open(pairs_list, 'r')
   
    for line in pairs_file:
       	pair = line.split()
	if pair[0] not in bless_words:
	    bless_words.append(pair[0])
	bless_types[pair[3]] = pair[2]

    pairs_file.close()

def read_feature_list(feature_list):
    global cosine_pairs
    global bless_words
    global cosine_types
    global features
    feature_file = open(feature_list, 'r')
    
    for line in feature_file:
        line = line.split()
	word = line[0]
	if word in bless_words or word in bless_types.keys():
    	    features[word] = array(line[1:], dtype=float32)  	
    
    feature_file.close()

def compute_cosines():
    for word in features:
        if word in bless_words:
            for relatum in bless_types.keys:
		if word in cosine_pairs.keys() and word != relatum and relatum in features:
		    word_cosines = cosine_pairs[word]
		    word_cosines[relatum] = dot(features[word], features[relatum]) / (norm(features[word]) * norm(features[relatum]))
		    cosine_pairs[word] = word_cosines
		elif word != relatum and relatum in features:
		    word_cosines = {}
	 	    word_cosines[relatum] = dot(features[word], features[relatum]) / (norm(features[word]) * norm(features[relatum]))
		    cosine_pairs[word] = word_cosines

def get_top(N, output_file):
    global bless_words
    global cosine_pairs
    OFILE = open(output_file, 'w')
    for word in cosine_pairs:
	if word in bless_words:
	    word_cosines = cosine_pairs[word]
	    sorted(word_cosines, key=word_cosines.__getitem__, reverse=True)
	    topn = nlargest(N, word_cosines.iteritems(), itemgetter(1))
	    for relatum in topn:
	        OFILE.write(word + ' ' + bless_types[relatum[0]] + ' ' + relatum[0] + ': ' + str(relatum[1]) + '\n')
	OFILE.write('\n')
    OFILE.close()		
			
	    
def get_nearest_neighbors(N, pairs_list, feature_list, output_file):
    read_bless_pairs(pairs_list)
    read_feature_list(feature_list)
    compute_cosines()
    get_top(N, output_file)    



if __name__=="__main__":
    _pairs_list = sys.argv[1]
    _feature_list = sys.argv[2]
    _N = eval(sys.argv[3])
    _output_file = sys.argv[4]

    get_nearest_neighbors(5, _pairs_list, _feature_list, _output_file)

