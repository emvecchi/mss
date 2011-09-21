
'''
This program is to normalize the feature vectors of the given matrices.
Note: feature file contains numbers of words per line that are described in the following format
word [space] freq1 freq2 freq3 ... 

@usage:
Parameter list is described as following:
    @param1: (N) number of files to normalize
    @param2, 3, ... (N+1) : files

@author: elia bruni (2011)
'''

import sys
from numpy import *
from numpy.linalg import norm

if __name__ == "__main__":
    N = eval(sys.argv[1])
    #  normalize the vectors for each file
    for i in range(2, N+2):
        FI = open(sys.argv[i], 'r')
	outfile = sys.argv[i] + '-norm.txt'
	FO = open(outfile, "w")
        for line in F:
            line = line.strip()
	    sep = line.find(' ', 0)
	    word = line[0:sep]
	    FO.write(word + ' ')
            for feat in array(line.split()[1:], dtype=float32):
	        FO.write(str(feat) + ' ')
	    FO.write('\n')
	FI.close()
        FO.close()
            
