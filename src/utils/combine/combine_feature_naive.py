'''
This program is to combine the features of serveral types
It works by concatenate line by line of each features file
Note: feature file contains numbers of words per line that are described in the following format
word [space] freq1 freq2 freq3 ... 

NOTICE: they have the same number of lines in the same order
@usage:
Parameter list is described as following:
    @param 1, 2 input files
    @param 3: output

@author: giang binh giang (2011)
'''
import sys
if __name__ == "__main__":
    #open the first file and create the hash map
    sizefeat = 0
    F1 = open (sys.argv[1], 'r')
    F2 = open (sys.argv[2], 'r')
    FO = open (sys.argv[3], 'w')

    hash = {}
    for line in F1:
        line = line.strip()
        sep = line.find(' ', 0)
        word = line[0:sep]
        
        line2 = F2.readline()
        line2 = line2.strip()
        sep2 = line2.find(' ',0)
        feat2 = line2[sep2:]
        word2 = line2[0:sep2]

        if word != word2:
            print "different lines in 2 files"
            exit()
        FO.write(line + feat2 + '\n')

    F1.close()
    F2.close()
    #combine with next files
    #write the output
    FO.close()

