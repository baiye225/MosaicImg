MosaicImg
==

This project introduces a kind of mosaic image generator by combining a lot of images into a designated picture. In the target picture, each pixel point can be matched with closest image from images pool.

run command below:

		python3 main.py

## Resize images pool

All images from images pool need to be resize into a reasonable shape (eg: 100*100) for the next step.

## Labelize each image

Build a kind of image matching method: calculate most commom RGB color as the label of each image
    
## Genarate mosaic image

Pick up a designated picture, match each pixel of the picture with images pool by choose "closest image" (the shortest euclidean distance), and resize the final picture to save as ".jpg" file.
  
## Result
![image](https://github.com/baiye225/MosaicImg/blob/master/results_images/TestImage_Before.jpg)
![image](https://github.com/baiye225/MosaicImg/blob/master/results_images/TestImage_After.jpg)

## Troubleshooting
+ This method of labelizing each image is not the the best way, it need to be optimized;
+ Finding the closest image to match each pixel point of the designated piture need calculate eclidean distance pixel point by pixel point, time complexity is too high.
+ If the target image is too big to generate matrix by using numpy.zeros(), it need to be splitted into serveral parts reasonably.

Original method was refered for this project with authorization

ID: York1996

https://me.csdn.net/york1996

https://blog.csdn.net/york1996/article/details/84489051
