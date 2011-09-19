"""
This program is specifically designed for MirFlickr extraction
THe program is to construct visual features from VLFEAT output SIFT
It uses temple file to store information to avoid overloading memory

Usage:
@param1: image feature director
@param2: word_feature target file
@param3: directory of unique labels
@param4: size (number of elemements) of the dictionary storing word - features

Giang Binh Tran (14 Jun 2011)

"""

#To compute the topic modelling of imange labels 
#Note that the before that we have images represented as "bag of visual" words

import glob, math, os, re, sys  
import numpy as np
import gc
from scipy import io

label_files = ''
num_descrs = -1
labels_dir = ''
words_in_dic = 0
MEMORY_LIMIT = 0
words_features_target_file = ''
DEBUG = False

#Initialization
def to_str(value):
    if (value >0):
        return "%.10f" %value
    else:
        return "%.0f" %value

#Store dictionary of words' features to temple file in the target dictionary 
def store_to_file(words_features):
    #open the current temple file and write to new file, then rename the file
    global words_features_target_file
    TMP_OUT = open ( words_features_target_file + '_wftmpout.txt','w')
    mark = {}
    if os.path.exists(words_features_target_file + '_wftmpin.txt'):
        TMP_IN = open (words_features_target_file+ '_wftmpin.txt','r')
        update_line = ''
        for line in TMP_IN:
            line = line.strip()
            values = line.split()
            word = values.pop(0)
            mark[word] = True
            update_line = '' 
            if words_features.has_key(word):
                if (len(values) != len(words_features[word])):
                    print str(len(values)) + " " + str(len(words_features[word]))
                    print word
                    exit()
                update_line = word + ' '
                for i in range(0,len(words_features[word])):
                    update_line += str(words_features[word][i] + float(values[i])) + ' '
                
                TMP_OUT.write(update_line + '\n')
            else:
                TMP_OUT.write(line + '\n')
        TMP_IN.close()
        os.remove(words_features_target_file + '_wftmpin.txt')
    
    for word in words_features.keys():
        if not mark.has_key(word):
            update_line = word + ' '
            for i in range(0, len(words_features[word])):
                update_line += str(words_features[word][i]) + ' '
            TMP_OUT.write(update_line + '\n')
    TMP_OUT.close()
    
    #Delete the old temple file and rename the new temple file to wftmpin.txt
    os.rename(words_features_target_file + '_wftmpout.txt', words_features_target_file + '_wftmpin.txt')
    


def get_label_info(index):
    global labels_dir
    file_name = os.path.join(labels_dir, label_files[index])
    tmp = []
    F = open (file_name, 'r')
    for token in F:
        token = token.replace('\r', '')
        token = token.replace('\n', '')
        token = token.strip()
        if len(token) >0:
            tmp.append(token)
    F.close()
    return tmp

#Read the image feature given its key
def get_image_features( filename):
    matfile = io.matlab.loadmat(filename)
    k = matfile.keys()
    key = ""
    for i in k:
        if len(i) >19:
            key = i
    return matfile.get(key)

def get_words_features(images_features_path, words_features_target_file):
    global num_descrs
    global MEMORY_LIMIT
    IMAGE_LIMIT = 500000

    file_map =  {}
    file_list = []
    dir_list = []
    #extracting filename from visual feature directory
    for dname in os.listdir(images_features_path):
        if (dname.find('.') <0):
            try:
                dir_list.append(eval(dname.strip()))
            except:
                continue
    dir_list.sort()

    for dd in dir_list:
        dname = str(dd)
        if len(dname)>0:
            dr = os.path.join(images_features_path, dname)
            current_list = []
            tmp = []

            for fname in os.listdir(dr):
                if (str.endswith(fname, '.mat')):
                    key, ext = fname.split('.')
                    if (len(key) >= 20):
                        fpath = os.path.join(dr, fname)
                        current_list.append(fpath)
                if (fname.find('rest') >=0):
                    drest = os.path.join(dr, fname)
                    #tmp = []
                    for nextfile in os.listdir(drest):
                        if (str.endswith(nextfile, '.mat')):
                            k, e = nextfile.split('.')
                            if len(k) >=20:
                                npath = os.path.join(drest, nextfile)
                                tmp.append(npath)
                    tmp.sort()
                    
            current_list.sort()
            if len(tmp) >0:
                current_list += tmp

            file_list += current_list

    print "Finish reading file list....."
    iter = 0
    print str(len(file_list)) + " filepaths indexed!"
    words_features = {}

    if num_descrs == -1:
        images_features =  get_image_features(file_list[0])
        num_descrs = len(images_features[0])
        images_block_size = len(images_features)


    totFeats = np.zeros((num_descrs), np.float32)
    print "Reading the information of images .....\n"
    count_null_image = 0
    _count_images = 0
    for filename in file_list:
        if _count_images > IMAGE_LIMIT:
            break
        print "reading file name : " + filename
        images_features =  get_image_features(filename)
        image_idx = 0
        image_idx_mult = iter*images_block_size
        for i in range(len(images_features)):
            _count_images +=1
            if _count_images >IMAGE_LIMIT:
                break
            image_idx = i + image_idx_mult
            image_row = get_label_info(image_idx); #
            
            for word in image_row:
                if (len(word.split())>1):
                    print "Exists a tag having 2 tokens!!!! - " + word
                    #exit()
                    #word = word.replace(' ','')
                if not words_features.has_key(word) and not math.isnan(images_features[i][0]):
                    words_features[word] = images_features[i]
                    totFeats = np.add(totFeats, images_features[i])
                elif not words_features.has_key(word) and math.isnan(images_features[i][0]):
                    count_null_image +=1 
                elif not math.isnan(images_features[i][0]):
                    words_features[word] = np.add(words_features[word], images_features[i])
                    totFeats = np.add(totFeats, images_features[i])
        #endfor
        """
        If the dictionary consume a lot of RAM, we store it to the file
        Then restore the original state
        """
        if len(words_features) >= MEMORY_LIMIT:
            store_to_file(words_features)
            words_features.clear()
            gc.collect()
        
        iter +=1
    #endfor

    #Now print the rest of dictionary words_features to the file
    store_to_file(words_features)
    words_features.clear()
    gc.collect()

        
    
    print "Finished reading images infor. - there's total " + str(count_null_image) + " images having NULL feature"

    N = np.sum(totFeats)

    print "Constructing words (image labels) BOW visual features.....\n"
    RAW_WF = open (words_features_target_file + '_wftmpin.txt','r')
    OFILE = open(words_features_target_file, 'w')

    progress_count = 0
    
    for line in RAW_WF:
        values = line.split()
        word = values.pop(0)
        update_line = word + ' '
        if len(values) != num_descrs:
            print "DEBUG MODE: different number of features in the raw file"
            continue

        raw_word_features = np.zeros((num_descrs), np.float32)
        for i in range(0, num_descrs):
            raw_word_features[i] = float(values[i])

        progress_count +=1
        if (DEBUG == True) and (progress_count % 500 == 0):
            print "DEBUG MODE: " + str(progress_count) + " words indexed...."

        wordOcc = sum(raw_word_features) 
        colIdx = 0
        for word_feature in raw_word_features:
            if wordOcc != 0 and word_feature != 0.0 and totFeats[colIdx] != 0.0:
                totFeat = float(word_feature * N) / float(totFeats[colIdx] * wordOcc)
                lmi_score = float(word_feature) * float(math.log(totFeat))
                if lmi_score < 0:
                    lmi_score = 0.0
            else:
                lmi_score = 0.0
            
            colIdx +=1
            update_line += str(lmi_score) + ' '

        OFILE.write(update_line + '\n')
    
    OFILE.close()
    RAW_WF.close()
    os.remove(words_features_target_file + '_wftmpin.txt')

def read_label_file(labels_dir):
    temp = []
    for fname in os.listdir(labels_dir):
        if (len(fname) > 20):
            temp.append(fname)
    temp.sort()
    return temp

if __name__ == "__main__":
    global labels_dir
    global MEMORY_LIMIT
    global DEBUG
    global images_features_path
    global words_features_target_file
    global label_files

    gc.enable()
    DEBUG = True
    images_features_path = sys.argv[1]
    words_features_target_file = sys.argv[2]
    labels_dir = sys.argv[3]
    MEMORY_LIMIT = int(sys.argv[4])

    label_files = read_label_file(labels_dir)
    print "Number of label files is " + str(len(label_files));
    get_words_features(images_features_path, words_features_target_file)

