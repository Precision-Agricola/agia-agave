"""Image processing utilities."""
import cv2
import numpy as np

class ImageUtils():
	"""Image processing utilities."""

	def __init__(self, image):
		"""Initialize image processing utilities."""
		self.image = image
		self.height, self.width = self.image.shape[:2]
		self.channels = self.image.shape[2] if len(self.image.shape) > 2 else 1

	def image_to_array(self, image):
		"""Convert image to numpy array."""
		return np.array(image)

	def	image_to_cv2(self, image):
		"""Convert image to cv2 image."""
		return cv2.imread(image)
	
	def image_to_gray(self):
		"""Convert image to grayscale."""
		return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
	
	def image_to_hsv(self):
		"""Convert image to hsv."""
		return cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
	
	def save_image(self, image, path):
		"""Save image."""
		cv2.imwrite(path, image)

	def image_2_PIL(self, image):
		"""Convert image to PIL image."""
		return Image.fromarray(image)	

	def split_image(self, image):
		"""Split image into channels."""
		return cv2.split(image)
	
	def merge_image(self, channels):
		"""Merge channels into image."""
		return cv2.merge(channels)
	
	def image_to_binary(self, image, threshold=128):
		"""Convert image to binary."""
		return cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]
	
	def image_resize(self, image, width, height):
		"""Resize image."""
		return cv2.resize(image, (width, height))
