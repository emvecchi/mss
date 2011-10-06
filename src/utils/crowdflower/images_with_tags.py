import sys, glob, os

"""
This program simply map the respective labels to the given mirflickr imagesc

Usage:
@param1: images directory
@param2: labels directory
@param3: output directory

"""

def map_tags_to_images(images_path, labels_path, out_path):
    
    for image_path in glob.glob(os.path.join(images_path)):
        image_name  = os.path.basename(image_path)
	label_name  = image_name[:-4] + ".txt"

        label_path  = labels_path + '/' + label_name
	shutil.copy(label_path), out_path, + '/' + label_name)


if __name__ =="__main__":
    _images_path = sys.argv[1]
    _labels_path = sys.argv[2]
    _out_path    = sys.argv[3]

    map_tags_to_images(_images_path, labels_path, _out_path)


