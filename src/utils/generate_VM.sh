#$ -wd /home/binhgiang.tran/
#$-l vf=8G
#$ -j y
#$ -S /bin/bash
#$ -m bea
#$ -M binhgiang.tran@unitn.it

echo "begin"
python2.6 LBOFF/LBOFF_no_swap.py /mnt/8tera/test-marco/image-and-text/elia/esp/dataset/esp_50k/ESP-ImageSet/vision/features/canny esp/old-esp-data/new-feat/canny.txt esp/old-esp-data/uuid_labels/ 15000

#python2.6 LBOFF_noDB_temple_file.py esp/new-esp-data/feature-100k/v1000_2000k_block1000 visualfeatures/matrix_k2000.txt esp/new-esp-data/labels/uuid_labels 15000
echo "done"
