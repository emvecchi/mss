import sys, glob, os

"""
This program create a csv file where each row contains an image and one of its associated tag
<"image_path, tag">

Usage:
@param1: dataset directory
@param2: url base where images and labels have to be located
@param3: output directory

"""

def write_csv(dataset_path, url_path, out_path):
    info = {}   
    for file_path in glob.glob(os.path.join(dataset_path, 'labels/*')):
	file       = open(file_path, "r")
	file_name  = os.path.basename(file_path)
	image_name = file_name[:-4] + ".jpg"
	print file_name
	print image_name
	print 'xxxxxx'
	if image_name in info:
	    label = info[image_name]
	else:
	    label = []
	for token in file:
	    label.append(token)
	info[image_name] = label
    data = []
    for image in info:
	for tag in info[image]:
	    image_file_name = url_path + 'images/' + image
	    data.append((str(image_file_name), str(tag)))
    csv_file = open(out_path, 'w')
    csv_file.write("Image,Tag" + '\n')
    for pair in data:
	csv_file.write(pair[0] + ',' + pair[1] + '\n')
    csv_file.close()

if __name__ =="__main__":
    _dataset_path = sys.argv[1]
    _url_path     = sys.argv[2]
    _out_path     = sys.argv[3] 
	    
    write_csv(_dataset_path, _url_path, _out_path)	
