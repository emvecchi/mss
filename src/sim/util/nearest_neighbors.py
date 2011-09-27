import sys, fileinput
from numpy.linalg import norm
from numpy import *
from operator import itemgetter
from heapq import nlargest

bless_words = []
bless_types = []
features = {}
cosine_pairs = {}

words = {}

def read_bless_pairs(pairs_list):
    global bless_pairs 
    pairs_file = open(pairs_list, 'r')
  
    last_word = '' 
    for line in pairs_file:
       	line = line.split()
        word = line[0]
        if word == last_word:
            adj_list = words[word]
            adj_list[line[3]] = line[2]
            bless_types.append(line[3])
	    words[word] = adj_list
	else:
	    adj_list = {}
	    adj_list[line[3]] = line[2]
	    bless_types.append(line[3])
	    words[word] = adj_list
            last_word = word

    pairs_file.close()

def read_feature_list(feature_list):
    global cosine_pairs
    global bless_words
    global cosine_types
    global features
    global words
    feature_file = open(feature_list, 'r')
    
    for line in feature_file:
        line = line.split()
	word = line[0]
	if word in words or word in bless_types:
    	    features[word] = array(line[1:], dtype=float32)  	
    
    feature_file.close()

def compute_cosines():
    global words
    global cosine_pairs
    for word in features:
        if word in words:
            for relata in words[word]:
		if word in cosine_pairs.keys() and relata in features:
		    word_cosines = cosine_pairs[word]
		    word_cosines[relata] = dot(features[word], features[relata]) / (norm(features[word]) * norm(features[relata]))
		    cosine_pairs[word] = word_cosines
		elif relata in features:
		    word_cosines = {}
		    word_cosines[relata] = dot(features[word], features[relata]) / (norm(features[word]) * norm(features[relata]))
	 	    cosine_pairs[word] = word_cosines

def get_top(N, output_file):
    global bless_words
    global cosine_pairs
    OFILE = open(output_file, 'w')
    for word in cosine_pairs:
	word_cosines = cosine_pairs[word]
	sorted_list = sorted(word_cosines, key=word_cosines.__getitem__, reverse=True)
	#topn = nlargest(N, word_cosines.iteritems(), itemgetter(1))
	for relata in sorted_list:
	    OFILE.write(word + ' ' + words[word][relata] + ' ' + relata + '\n')
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

