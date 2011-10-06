import glob, os, shutil, sys, random


def filter_dataset(dataset_path):
    '''
    Dataset_path must contain one folder called 'original_data', with two subfolders 'images' and 'labels'.
    Images are in '.jpg' format, labels in '.jpg.desc' format (maybe labels' format has to be changed).
    
    Usage:
    @param1: dataset directory
    '''
    preprocessed_path = os.path.join(dataset_path, 'preprocessed')
    os.mkdir(preprocessed_path)
    os.mkdir(os.path.join(preprocessed_path, 'labels'))
    os.mkdir(os.path.join(preprocessed_path, 'images'))
    words_with_images = {}
    for file_path in glob.glob(os.path.join(dataset_path, 'original-data/20k-labels/*.txt')):
        print file_path
	file          = open(file_path, "r")
	file_name     = os.path.basename(file_path)
        image_name    = 'im' + file_name[+4:-4] + '.jpg'
        image_path    = os.path.join(dataset_path, 'original-data/20k-images/', image_name)
        new_file_name = get_random_string(32);
        label         = new_file_name + '.txt'
        image         = new_file_name + '.jpg'
	shutil.copy(str(file_path), os.path.join(preprocessed_path,'labels', label))
        shutil.copy(str(image_path), os.path.join(preprocessed_path,'images', image))
        file.close()


def get_random_string(word_len):
    word = ''
    for i in range(word_len):
        word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return word


if __name__ =="__main__":
    dataset_path = sys.argv[1]
    filter_dataset(dataset_path)   
        
        
 
