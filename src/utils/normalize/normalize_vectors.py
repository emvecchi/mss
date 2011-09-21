
'''
This program is to combine the features of serveral types
It works by concatenate line by line of each features file
Note: feature file contains numbers of words per line that are described in the following format
word [space] freq1 freq2 freq3 ... 

@usage:
Parameter list is described as following:
    @param1: (N) number of files to normalize
    @param2, 3, ... (N+1) : files
    @param (N+2): output

@author: elia bruni (2011)
'''

import sys
from numpy import *
from numpy.linalg import norm

if __name__ == "__main__":
    N = eval(sys.argv[1])
    # open each file, create and normalize the vectors
    for i in range(2, N+2):
        print i
        F = open(sys.argv[i], 'r')
	d = 0
	matrix = {}
	idx = 0
        for line in F:
	    if (d == 0):
	        d = line.count(' ')
	    v = zeros(d, float32)	
            line = line.strip()
	    sep = line.find(' ', 0)
	    word = line[0:sep]
            v = array(line.split()[1:], dtype=float32)
	    matrix[word] = v/norm(v)
	F.close()
            
	# write the output
        outfile = sys.argv[i] + '-norm.txt'
	FO = open(outfile, "w")
	
	for word in matrix:
	    FO.write(word + ' ')
	    for feat in matrix[word]:
		FO.write(str(feat) + ' ')
	    FO.write('\n')
	FO.close()	




