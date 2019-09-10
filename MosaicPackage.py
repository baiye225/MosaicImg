#coding=utf8
import os
import time
import cv2
import numpy as np
from collections import Counter
from Display import Display

class Img(object):
	def __init__(self):
		self.ImgFolder     = 'download' 		 # original images folder
		self.ImgPoolFolder = 'mosaic_img_pool'   # processed images pool folder
		self.ResultsFolder = 'results_images'    # mosaic images folder
		self.ImgPoolSize   = (50, 50) 		     # resized shape
		self.ImgLabel	   = []
		self.Show  		   = Display()

	##########
	# Main API
	##########
	def main(self, TargetFile):
		# 1. Resize Images
		self.PreProcess()

		# 2. Mosaicing a Image
		self.GenMosaicImg(TargetFile)

		return

	# Pre process original images before rendering
	def PreProcess(self):
		self.Show.Start()
		time.sleep(1)
		
		# Locate the original images folder
		ImgFolderPath = os.path.join(os.getcwd(), self.ImgFolder)
		Files = os.listdir(ImgFolderPath)
		n = 1
		N = len(Files)

		# Start to process original images
		for FileName in Files:
			SavedFileName = str(n) + '.jpg'
			self.Show.PreProcess(n, N)
			self.ResizeAneSave(FileName, SavedFileName)
			self.Label(FileName, SavedFileName, Img)
			n += 1
		return

	# Resize the original images as desired shape
	def ResizeAneSave(self, FileName, SavedFileName):
		# Load the current image
		Img = self.LoadImg('ImgFolder', FileName)

		# Resize it
		Img = cv2.resize(Img, self.ImgPoolSize)

		# Save it as .jpg
		SavePath = os.path.join(os.getcwd(), self.ImgPoolFolder,\
								SavedFileName)
		cv2.imwrite(SavePath, Img)

		return

	# Find the most common RGB pixel and label it for the images
	def Label(self, FileName, SavedFileName, Img):
		# Load the current image
		#Img = self.LoadImg('ImgFolder', FileName)
		Img = self.LoadImg('ImgPoolFolder', SavedFileName)

		# Read geometrical parameters
		ImaShape = np.shape(Img)
		rows 	 = ImaShape[0]
		columns  = ImaShape[1]

		# Collect pixel of the current image
		PixelPool = []
		for i in range(rows):
			for j in range(columns):
				b = Img[i, j, 0]
				g = Img[i, j, 1]
				r = Img[i, j, 2]
				PixelPool.append((b, g, r))

		# Find most common color group and save it in the dict
		most = Counter(PixelPool).most_common(1)
		self.ImgLabel.append((SavedFileName, most[0][0]))

		return

	# Render the mosaic image
	def GenMosaicImg(self, TargetFile):
		self.Show.ProcessBegin()
		time.sleep(1)

		# Load the target image
		Img = self.LoadImg('CurrentFolder', TargetFile)

		# Read geometrical parameters
		ImaShape = np.shape(Img)
		rows 	 = ImaShape[0]
		columns  = ImaShape[1]

		# Initialize new img frame
		PICTURE = np.zeros((rows * self.ImgPoolSize[0],\
						    columns * self.ImgPoolSize[1], 3),\
						    dtype = np.uint8)

		# Start to rendering for each pixel point
		n = 1
		N = rows * columns

		for i in range(rows):
			for j in range(columns):
				self.Show.Process(n, N)

				# get RGB value of the current pixel
				B = Img[i, j, 0]
				G = Img[i, j, 1]
				R = Img[i, j, 2]
				ImgRGB   = [B, G, R]

				# Image matching
				FileName = self.PixelImgMatch(ImgRGB)

				# Load the matched image
				FillImg = self.LoadImg('ImgPoolFolder', FileName)

				# Image filling
				PICTURE[i*self.ImgPoolSize[0]:(i+1)*self.ImgPoolSize[0],\
				 		j*self.ImgPoolSize[1]:(j+1)*self.ImgPoolSize[1]]\
				 	    = FillImg
				n += 1


		# Post processing
		self.Show.PostProcess()
		Img = cv2.resize(Img,(rows * self.ImgPoolSize[0],\
						      columns * self.ImgPoolSize[1]))

		# Save Mosaic
		ResultPath = os.path.join(os.getcwd(), self.ResultsFolder,\
								  TargetFile)
		cv2.imwrite(ResultPath[0:-4] + '_Before.jpg', Img)
		cv2.imwrite(ResultPath[0:-4] + '_After.jpg', PICTURE)	
		self.Show.End()
		return

	# A method of finding the best image from Image pool 
	# to match the current pixel
	def PixelImgMatch(self, ImgRGB):
		CurrentDistance = float('inf')
		CurrentFileName = ''

		# shuffle Image Label to make variety
		np.random.shuffle(self.ImgLabel)

		# Find the shortest Euclidean distance
		for item in self.ImgLabel:
			FileName = item[0]
			PoolRGB  = item[1]
			Distance = self.ImgEuclideanDistance(ImgRGB, PoolRGB)

			# setup margin value is 100
			if Distance < 100:
				return FileName
			elif Distance < CurrentDistance:
				CurrentDistance = Distance
				CurrentFileName = FileName

		# if all distances are larger than 100, then use the minimum one
		return CurrentFileName

	# Caculate the  shotest euclidean distance
	def ImgEuclideanDistance(self, Img1, Img2):
		return np.sqrt(np.square(int(Img1[0]) - int(Img2[0]))\
				     + np.square(int(Img1[1]) - int(Img2[1]))\
					 + np.square(int(Img1[2]) - int(Img2[2])))

	# Load Img
	def LoadImg(self, request, FileName):
		# Initialize directory of the current image
		if request == 'ImgFolder':
			FilePath = os.path.join(os.getcwd(), self.ImgFolder,\
								    FileName)
		elif request == 'ImgPoolFolder':
			FilePath = os.path.join(os.getcwd(), self.ImgPoolFolder,\
								    FileName)
		elif request == 'CurrentFolder':
			FilePath = os.path.join(os.getcwd(), FileName)	

		Img = cv2.imread(FilePath)

		return Img