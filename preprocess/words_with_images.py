import glob, os, shutil, uuid, sys


def filter_dataset(dataset_path):
    '''
    Dataset_path must contain one folder called 'original_data', with two subfolders 'images' and 'labels'.
    Images are in '.jpg' format, labels in '.jpg.desc' format (maybe labels' format has to be changed).
    '''
    

    preprocessed_path = os.path.join(dataset_path, 'preprocessed')
    os.mkdir(preprocessed_path)
    os.mkdir(os.path.join(preprocessed_path, 'labels'))
    os.mkdir(os.path.join(preprocessed_path, 'images'))
    num_files = len([f for f in os.listdir(os.path.join(dataset_path, 'original_data/labels'))])

    # create a unique name for each label/image
    print num_files
    UUIDS = []
    for ii in range(0, num_files):
        UUIDS.append(uuid.uuid1())
    UUIDS.sort()
    count = 0
    words_with_images = {}

    for file_path in glob.glob(os.path.join(dataset_path, 'original_data/labels/*.desc')):
	file = open(file_path, "r")
	for token in file:
	    #print token
	    # check if the label contains at least one word of words_list
	    #if token in list:
		
	    file_name = os.path.basename(file_path)
           
            image_name = file_name[:-5] #esp
            image_path = os.path.join(dataset_path, 'original_data/images/', image_name)
            label = str(UUIDS[count]) #esp
            image = str(UUIDS[count]) + '.jpg'
	    shutil.copy(str(file_path), os.path.join(preprocessed_path,'labels', uuid_label))
            shutil.copy(str(image_path), os.path.join(preprocessed_path,'images', uuid_image))
	    count += 1
	    break
        file.close()


if __name__ =="__main__":
    dataset_path = sys.argv[1]
    filter_dataset(dataset_path)   
        
        
 
