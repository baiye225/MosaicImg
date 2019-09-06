#coding=utf-8

import os
import cv2

# Initialize load path and save path
img_folder_path = "./download"
save_path = "./mosaic_img_pool"

# list all files' name
files = os.listdir(img_folder_path)

# process all files and save
n = 1
N = len(files)

for file in files:
	# display process
	print('Processing (%d/%d) image' %(n, N))

	# current image directory
	img_path = img_folder_path + '/' + file

	# read img and re-size it
	img = cv2.imread(img_path)
	img = cv2.resize(img,(100,100))

	# save re-sized img
	saved_file_name = str(n) + '.jpg'
	cv2.imwrite(save_path + '/' + saved_file_name, img)

	n += 1