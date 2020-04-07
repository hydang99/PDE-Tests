from __future__ import absolute_import
from __future__ import print_function
import glob 
import os.path as osp 
import os
import cv2
from PIL import Image
import glob

def convert_mask(dir_src,dir_dest):
    if not osp.exists(dir_src):
        raise KeyError("The directory doesn't exist, Just try again! LOL")
    if not osp.exists(dir_dest):
        os.mkdir(dir_dest)
    files = glob.glob(dir_src + "*.jpg")
    for index, filename in enumerate(files):
        img = cv2.imread(filename)
        if img is None:
            raise ValueError("Error Loading Image, Shouldn't be happened")
        rgb_channels = cv2.split(img)
        rows = img.shape[0]
        cols = img.shape[1]
        for i in range(0,rows):
            for j in range(0,cols):
                color = rgb_channels[0][i][j]
                if(color > 0):
                    rgb_channels[0][i][j] = 255
                    rgb_channels[1][i][j] = 255
                    rgb_channels[2][i][j] = 255
        image = cv2.merge((rgb_channels))
        k = osp.basename(filename)
        cv2.imwrite(dir_dest+osp.basename(filename),image)

'''def main():
    convert_mask("../datasets/labels_unconverted/","../datasets/labels_converted/")
if __name__ == "__main__":
    main()
'''
