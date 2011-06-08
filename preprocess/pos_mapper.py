import glob, os, sys

pos_dic = {}
pos_freq = {}


def read_pos_list(pos_list):
    global pos_dic
    global pos_freq
    pos_file = open(pos_list, "r")
    for line in pos_file:
        tokens = line.split()
	pos_dic[tokens[0]] = tokens[1] + '-' +tokens[2].lower()
	pos_freq[tokens[0]] = tokens[3]

def map_pos(pos_list, dataset_path):
    global pos_dic
    global pos_freq
    pos_file = open(pos_list, "r")
    read_pos_list(pos_list)
    os.mkdir(os.path.join(dataset_path, 'pos_tagged'))
    for file_path in glob.glob(os.path.join(dataset_path, 'label/*.txt')):
	Ifile = open(file_path, "r")
	file_name = os.path.basename(file_path)
	Ofile = open(os.path.join(dataset_path, 'pos_tagged', file_name), "w")
	for line in Ifile:
	    tokens = line.split()
	    for token in tokens:
		if pos_freq[token] > 100:
		    Ofile.write(pos_dic[token])
		    Ofile.write('\n')
	Ifile.close()
	Ofile.close()
	
		    
if __name__=='__main__':
    _pos_list = sys.argv[1]
    _dataset_path=sys.argv[2]

    map_pos(_pos_list, _dataset_path)
		
