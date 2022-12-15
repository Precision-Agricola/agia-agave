"""Utilities for raw image conversion and processing"""
import micasense.metadata as metadata
import os 
if os.name == 'nt':
	exiftoolPath = os.environ.get('exiftoolpath')

class SensorUtils:
	"""Class for holding"""

	def __init__(self, set_path):
		self.set_path = set_path
		self.meta = []

	def __call__(self):
		self.get_metadata()

	def get_metadata(self):
		"""Get metadata for all images in a set"""
		for image_path in self.set_path:
			meta = metadata.Metadata(image_path, exiftoolPath=exiftoolPath)
			self.meta.append(meta)
