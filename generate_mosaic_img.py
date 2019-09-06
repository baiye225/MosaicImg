#coding=utf-8

import cv2
import os
import cv2
import numpy as np 

# Initialize images pool path
img_pool_path = "./mosaic_img_pool"

# read index
f = open('ImgIndex.txt', 'r')
n = 1
dic = {}
array = []

for line in f.readlines():
	# split filename and RGB, and delete '\n'
	content = line.strip().split(':')

	# get fielname
	file = content[0]

	# get RGB data
	RGB = content[1].split(',')

	# process and add into dictionary
	b = int(RGB[0])
	g = int(RGB[1])
	r = int(RGB[2])
	dic[n] = file
	array.append([b, g, r])
	n += 1

matrix = np.array(array)
RGB_shape = np.shape(matrix)

#os._exit(0)

# load target image
target_img_folder  = './download/'
target_img_name  = 'images?q=tbn:ANd9GcQ6GKJsH5agHVDIk1PUDNzNpli_aartkPGoYh1jzxU5iHwTHl4ijw.jpg'
target_img       = cv2.imread(target_img_folder + target_img_name)

# read height and width
target_img_shape = np.shape(target_img)

rows    = target_img_shape[0]
columns = target_img_shape[1]

n = 1
N = rows * columns

# initialize new img frame
PICTURE = np.zeros((100 * rows, 100 * columns, 3), dtype = np.uint8)

print("Rending...")
# render picture
for i in range(rows):
	for j in range(columns):

		print("Processing (%d/%d) image..." %(n, N))
		# get RGB value of the current pixel
		b = target_img[i, j, 0]
		g = target_img[i, j, 1]
		r = target_img[i, j, 2]

		# Initialize matrix of the current piexl
		target_matrix = np.ones((RGB_shape[0], RGB_shape[1]))
		target_matrix[:,0] = b
		target_matrix[:,1] = g
		target_matrix[:,2] = r

		# find shotest euclidean distance
		distance_matrix = matrix - target_matrix
		distance_matrix = np.power(distance_matrix[:,0], 2) \
		+ np.power(distance_matrix[:,1], 2) \
		+ np.power(distance_matrix[:,2], 2)

		# load related image from image pool and put on the new picture
		img_index = np.argmin(distance_matrix)
		filepath = img_pool_path + '/' + dic[img_index]
		sub_img = cv2.imread(filepath)
		PICTURE[i*100:(i+1)*100, j*100:(j+1)*100] = sub_img

		n += 1

print("Post processing...")
PICTURE = cv2.resize(PICTURE,(rows,columns))

print("Saving Images...")
cv2.imwrite("./results_images/render_pic_before.jpg", target_img)
cv2.imwrite("./results_images/render_pic_after.jpg", PICTURE)

print("Done!!!")





