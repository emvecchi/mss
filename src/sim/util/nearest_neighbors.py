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
            for relata in features:
		if relata in bless_types.keys():
		    if word in cosine_pairs.keys() and word != relata:
			word_cosines = cosine_pairs[word]
		        word_cosines[relata] = dot(features[word], features[relata]) / (norm(features[word]) * norm(features[relata]))
			cosine_pairs[word] = word_cosines
		    else:
			word_cosines = {}
			word_cosines[relata] = dot(features[word], features[relata]) / (norm(features[word]) * norm(features[relata]))
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
	    for relata in topn:
	        OFILE.write(word + ' ' + bless_types[relata[0]] + ' ' + relata[0] + ': ' + str(relata[1]) + '\n')
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
    _output_file = sys.argv[3]

    get_nearest_neighbors(5, _pairs_list, _feature_list, _output_file)

