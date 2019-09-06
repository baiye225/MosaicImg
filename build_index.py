#coding=utf-8
import cv2
import os
from collections import Counter

# Initialize images pool path
img_pool_path = "./mosaic_img_pool"

# List all fiels' name
files = os.listdir(img_pool_path)

# open text
f = open('ImgIndex.txt', 'w')

# process pixel of all files and write into text fiel
n = 1
N = len(files)

for file in files:
	# display process
	print('Collecting pixel of (%d/%d) image: %s' %(n, N, file))
	# current image directory
	img_path = img_pool_path + '/' + file

	# load image
	img = cv2.imread(img_path)

	# Initialize pixel pool of the current image
	pixel_pool = []

	# collect pixel
	for i in range(100):
		for j in range(100):
			b = img[i, j, 0]
			g = img[i, j, 1]
			r = img[i, j, 2]
			pixel_pool.append((b, g, r))

	# find most common color group
	most = Counter(pixel_pool).most_common(1)

	# summarize the current result
	file_sum = file \
			   + ':' \
			   + str(most[0][0]).replace("(", "")\
			   .replace(")","").replace(" ", "")\
			   + '\n'
    # write the summary
	f.write(file_sum)

	n += 1

f.close()


