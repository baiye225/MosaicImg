#coding=utf8

'''
Process Displacement
It is used to monitor procedure's proccess
to display for users.
'''
class Display(object):
	# Start
	def Start(self):
		self.LargeTitle('Start to generate mosaic image', 4)

	# PreProcess images (resize and label)
	def PreProcess(self, n, N):
		print('PreProcessing (%d/%d) Image...' %(n, N))
		return

	# Render images begin
	def ProcessBegin(self):
		self.LargeTitle('Rendering Mosaic Image', 2)
		return

	# Render images
	def Process(self, n, N):
		print('Processing (%d/%d) Image...' %(n, N))
		return

	# Post processing
	def PostProcess(self):
		print('Post processing...')

	# Finish
	def End(self):
		self.LargeTitle('Complete!!!', 4)
		return

	# Add a frame of displacement
	def LargeTitle(self, TitleWords, Height):
		Width = len(TitleWords)
		for i in range(Height):
			print('-' * Width)
		print(TitleWords)
		for i in range(Height):
			print('-' * Width)
		return