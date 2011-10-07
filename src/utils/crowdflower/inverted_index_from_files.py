import sys, os

color_counts = {}
colors       = ['black','blue','brown','grey','green','orange','pink','purple','red','white','yellow']
def read_csv(report_path, block_path, out_path):
    #debug
    tot_count   = 0
    print_count = 0

    index       = {}
    
    # 1st file
    report_file = open(report_path, 'r')
    first_line = True
    for line in report_file:
        if first_line:
	    first_line = False
	    continue
        line  = line.strip().split(',')
	image = line[8]
	image = image[+68:]
	tag   = line[9].rstrip()
	check_color(tag)
	tot_count += 1
        if tag in index:
	    list = index[tag]
	    list.append(image)
	    index[tag] = list
	else:
	    list = []
	    list.append(image)
	    index[tag] = list 
    report_file.close()

    # 2nd file
    block_file = open(block_path, 'r')
    first_line = True
    for line in block_file:
        if first_line:
	    first_line = False
	    continue
	line  = line.split(',')
	if line[0] != '\n':
	    image = line[0]
	    image = image[+68:]
	    tag   = line[1].rstrip()
	    check_color(tag)
	    tot_count += 1
            if tag in index:
	        list = index[tag]
                list.append(image)
                index[tag] = list
            else:
                list = []
                list.append(image)
                index[tag] = list
    block_file.close()	    
    out_file = open(out_path, 'w')
    for tag in index:
	for image in index[tag]:
            print_count += 1
	    out_file.write(tag + ' ' + image + '\n')
    out_file.close()

    print 'debug: tot_count = ' + str(tot_count) + ' print_count = ' + str(print_count)

    for color in color_counts:
        print color + ': ' + str(color_counts[color])
 
def check_color(tag):
    global color_counts
    global colors
    ctag = tag
    if ctag == 'gray':
	ctag = 'grey'
    if ctag in colors:
	if ctag in color_counts:
	    print ctag
	    count = color_counts[ctag]
	    count += 1
	    color_counts[ctag] = count
	else:
	    count = 1
	    color_counts[ctag] = count

if __name__ =="__main__":
    _report_path = sys.argv[1]
    _block_path  = sys.argv[2]
    _out_path    = sys.argv[3]	

    read_csv(_report_path, _block_path, _out_path)
