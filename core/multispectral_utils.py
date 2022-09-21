"""Multi-Spectral utilities."""
import cv2

class MultiSpectralUtils():
	"""Multi-Spectral methods and utilities for Micasense RedEdge Sensor."""

	def __init__(self, image):
		"""Initialize multi-spectral utilities."""
		self.red = image[:,:,0]
		self.green = image[:,:,1]
		self.blue = image[:,:,2]
		self.red_edge = image[:,:,3]
		self.nir = image[:,:,4]
		self.height, self.width = self.red.shape[:2]

	def validate_image(self, image):
		"""Validate image."""
		if image.shape != (self.height, self.width, 5):
			raise ValueError('Image must be a 5-channel image.')
	
	"""Image Registration using Enhanced Correlation Coefficient (ECC) Maximization"""
	def image_register(self, image):
		"""Register image."""
		pass

	def get_ndvi(self):
		"""Get NDVI index."""
		return (self.nir - self.red) / (self.nir + self.red)
	
	def get_ndre(self):
		"""Get NDRE index."""
		return (self.nir - self.red_edge) / (self.nir + self.red_edge)
	
	def get_clorosol(self):
		"""Get chlorosol index."""
		return (self.nir - self.blue) / (self.nir + self.blue)

	def get_cloroplast(self):
		"""Get chloroplast index."""
		return (self.nir - self.green) / (self.nir + self.green)

	def get_clorophyll(self):
		"""Get chlorophyll index."""
		return (self.nir - self.red_edge) / (self.nir + self.red_edge)