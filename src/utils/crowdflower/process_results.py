import sys, os, random, shutil


images = {}

thresh_1   = {}
thresh_051 = {}
thresh_033 = {}
thresh_0   = {}
sample_1 =   {}
sample_051 = {}
sample_033 = {}
sample_0   = {}

def read_report(report_path):
    global images
    report_file = open(report_path, 'r')
    for line in report_file:
    	line  = line.strip().split(',')
	if line[2] == 'true':
	    continue
	image = line[8]
	if image in images:
	    tags = images[image]
	else:
	    tags = {}
	tag     = line[9]
	confid  = line[6]
	choice  = line[5]
	if   choice == 'Yes':
	    tags[tag] = float(confid)	
	elif choice == 'No':
	    tags[tag] = 1 - float(confid)
	images[image] = tags

def make_samples():

    global thresh_1   
    global thresh_051 
    global thresh_033 
    global thresh_0   
    global sample_1 
    global sample_051 
    global sample_033 
    global sample_0   
    global images
    for image in images:
        for tag in images[image]:
	    confid = images[image][tag]
	    if confid == 1:
	        thresh_1[image]   = tag
	    elif confid >= 0.51 && confid < 1:
		thresh_051[image] = tag
      	    elif confid >= 0.33 && confid < 0.51:
		thresh_033[image] = tag
	    elif confid == 0:
		thresh_0[image]   = tag
    for i in range(30):
       tag = random.choice(thresh_1.keys())
       sample_1[tag]   = thresh_1[tag]
       tag = random.choice(thresh_051.keys())
       sample_051[tag] = thresh_051[tag]
       tag = random.choice(thresh_033.keys())
       sample_033[tag] = thresh_033[tag]
       tag = random.choice(thresh_0.keys())
       sample_0[tag]   = thresh_0[tag]

def write_to_files(images_path, output_path):
    
    os.mkdir(output_path + '/sample_1')
    os.mkdir(output_path + '/sample_1/images')
    os.mkdir(output_path + '/sample_1/tags')
    os.mkdir(output_path + '/sample_051-099')
    os.mkdir(output_path + '/sample_051-099/images')
    os.mkdir(output_path + '/sample_051-099/tags')
    os.mkdir(output_path + '/sample_033-050')
    os.mkdir(output_path + '/sample_033-050/images')
    os.mkdir(output_path + '/sample_033-050/tags')
    os.mkdir(output_path + '/sample_0')
    os.mkdir(output_path + '/sample_0/images')
    os.mkdir(output_path + '/sample_0/tags')

    for image in sample_1:
        image_name = os.path.basename(image)
	old_image_path = images_path + '/' + image_name
	new_image_path = output_path + '/sample_1/images/' + image_name
	new_tag_path   = output_path + '/sample_1/tags/' + image_name[:-4] + '.txt'
        shutil.copy(old_image_path, new_image_path)
	new_tag_file   = open(new_tag_path, 'w')
	new_tag_file.write(thresh_1[image])
        new_tag_file.close()
    for image in sample_051:
        image_name = os.path.basename(image)
	old_image_path = images_path + '/' + image_name
	new_image_path = output_path + '/sample_051-099/images/' + image_name
	new_tag_path   = output_path + '/sample_051-099/tags/' + image_name[:-4] + '.txt'
        shutil.copy(old_image_path, new_image_path)
	new_tag_file   = open(new_tag_path, 'w')
	new_tag_file.write(thresh_051[image])
        new_tag_file.close()
    for image in sample_033:
        image_name = os.path.basename(image)
	old_image_path = images_path + '/' + image_name
	new_image_path = output_path + '/sample_033-050/images/' + image_name
	new_tag_path   = output_path + '/sample_033-050/tags/' + image_name[:-4] + '.txt'
        shutil.copy(old_image_path, new_image_path)
	new_tag_file   = open(new_tag_path, 'w')
	new_tag_file.write(thresh_033[image])
        new_tag_file.close()
    for image in sample_0:
        image_name = os.path.basename(image)
	old_image_path = images_path + '/' + image_name
	new_image_path = output_path + '/sample_0/images/' + image_name
	new_tag_path   = output_path + '/sample_0/tags/' + image_name[:-4] + '.txt'
        shutil.copy(old_image_path, new_image_path)
	new_tag_file   = open(new_tag_path, 'w')
	new_tag_file.write(thresh_0[image])
        new_tag_file.close()


if __name__ =="__main__":
    _report_path = sys.argv[1]
    _images_path = sys.argv[2]
    _output_path = sys.argv[3]

    read_report(_report_path)
    make_samples()
    write_to_files(_images_path, _output_path)
