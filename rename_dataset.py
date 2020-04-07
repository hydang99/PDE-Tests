from __future__ import absolute_import
from __future__ import print_function
import os,errno 
import os.path as osp 
import numpy as np 
import glob
import shutil
import errno

def copy_img(src, dest, dest_label):
    
    if not osp.exists(src):
        raise ValueError('--The Source Folder {} you inputted does not exist. Not my faultttttt!!!--'.format(src))
    if not osp.exists(dest):
        os.makedirs(dest)
    if not osp.exists(dest_label):
        os.makedirs(dest_label)
    i = 0   
    file_types = (src +"*[!_mask].jpg", src +"*[!_mask].png")
    #file_types = (src + "*[!_mask]")
    for files in file_types:
        if (files == file_types[0]):
            only_file = glob.glob(files)
            for index, filename in enumerate(only_file):
                list = filename.split(".jpg")
                mask_path_jpg = list[0] + "_mask.png"
                mask = glob.glob(mask_path_jpg)
                if(mask != None):
                    for index_mask, filename_mask in enumerate(mask):
                        dest_name = dest +"{}.jpg".format(str(i).zfill(4))
                        shutil.copyfile(filename,dest_name)
                        dest_name_mask = dest_label +"{}_mask.jpg".format(str(i).zfill(4))
                        shutil.copyfile(filename_mask,dest_name_mask)
                        i+=1
                else:
                    continue     
