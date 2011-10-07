import glob, os, sys


"""
Given a list <word lemma pos freq>, this code assign the most frequent 
pos-tag in the given list to each word of each label in the dataset directory
    
    Usage:
    @param1: pos list
    @param2: dataset directory
"""

pos_dic      = {}
pos_freq     = {}
colors       = ['black','blue','brown','grey','green','orange','pink','purple','red','white','yellow']
color_counts = {}

def read_pos_list(pos_list):
    global pos_dic
    global pos_freq
    pos_file = open(pos_list, "r")
    for line in pos_file:
	tokens              = line.split()
	pos_dic[tokens[0]]  = tokens[1] + '-' + tokens[2].lower()
	pos_freq[tokens[0]] = tokens[3]
    pos_file.close()


def map_pos(pos_list, in_file_path, ou_file_path):
    global pos_dic
    global pos_freq
    global color_counts
    pos_file = open(pos_list, 'r')
    read_pos_list(pos_list)
    in_file = open(in_file_path, 'r')
    ou_file = open(ou_file_path, 'w')
    for line in in_file:
    	line = line.split(' ')
        tag   = line[0]
	image = line[1]
	check_color(tag)
	if tag in pos_freq and pos_freq[tag] > 100:
	    pos_tag = pos_dic[tag]
	    check   = pos_tag.lower()
	    if check[:-2] == 'gray':
	        check = 'grey-j'
	    if check[:-2] in colors:
	        #check_color(check[:-2])
	        pos_tag = check[:-2] + '-j'
	    ou_file.write(pos_tag + ' ' + image + '\n')
    in_file.close()
    ou_file.close()
    for color in color_counts:
        print color + ' ' + str(color_counts[color])


def check_color(tag):
    global color_counts
    global colors
    ctag = tag
    if ctag in colors:
        if ctag in color_counts:
	    count = color_counts[ctag]
	    count += 1
	    color_counts[ctag] = count
	else:
	    count = 1
	    color_counts[ctag] = count
			
if __name__=='__main__':
    _pos_list     = sys.argv[1]
    _in_file_path = sys.argv[2]
    _ou_file_path = sys.argv[3]

    map_pos(_pos_list, _in_file_path, _ou_file_path)
