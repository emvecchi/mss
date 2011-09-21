'''
This program is to combine the features of serveral types
It works by concatenate line by line of each features file
Note: feature file contains numbers of words per line that are described in the following format
word [space] freq1 freq2 freq3 ... 

@usage:
Parameter list is described as following:
    @param1: (N) number of files to combine
    @param2, 3, ... (N+1) : files
    @param (N+2): output

@author: giang binh giang (2011)
'''
import sys
if __name__ == "__main__":
    N = eval(sys.argv[1])
    #open the first file and create the hash map
    sizefeat = 0
    F1 = open (sys.argv[2], 'r')
    hash = {}
    for line in F1:
        line = line.strip()
        sep = line.find(' ', 0)
        word = line[0:sep]
        feat = line[sep:]
        hash[word] = feat
        if (sizefeat == 0):
            sizefeat = line.count(' ')

    F1.close()
    #combine with next files
    mark = {}
    for i in range(3,2 + N):
        F = open (sys.argv[i], 'r')
        old_sizefeat = sizefeat
        mark.clear()
        for line in F:
            line = line.strip()
            if sizefeat == old_sizefeat:
                sizefeat = sizefeat + line.count(' ')

            sep = line.find(' ', 0)
            word = line[0:sep]
            feat = line[sep:]
            if word in hash:
                hash[word] += feat
                mark[word] = True
            else:
                oldfeature = ''
                for j in range(0, old_sizefeat):
                    oldfeature += ' 0'
                hash[word] = oldfeature + feat
		mark[word] = True
        
        for wordleft in hash.keys():
            if not wordleft in mark:
                newfeature = ''
                for j in range(old_sizefeat, sizefeat):
                    newfeature += ' 0'
                hash[wordleft] += newfeature
        F.close()

    #write the output
    FO = open(sys.argv[N+2], 'w')

    for word in hash.keys():
        FO.write(word)
        FO.write(hash[word] + '\n')
    FO.close()

