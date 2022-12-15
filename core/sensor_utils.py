"""Utilities for raw image conversion and processing"""
import micasense.metadata as metadata
from micasense.utils import raw_image_to_radiance
from skimage import io
import os 


class SensorUtils:
	"""Class for handle sensor utils"""

	def __init__(self, set_path):
		self.set_path = set_path
		self.meta = []
		self.raw_images = []
		self.bands =['red', 'green', 'blue', 'nir', 'red edge']
		self.radiance_images = []

	def process_sensor(self):
		self.get_metadata()
		self.read_raw_images()
		self.raw_images_to_radiance()
		return self

	def read_raw_images(self):
		"""Read raw images from a set"""
		raw_images = []
		for image_path in self.set_path:
			raw_images.append(io.imread(image_path))
		self.raw_images = raw_images

	def get_metadata(self):
		"""Get metadata for all images in a set"""
		metas = []
		if os.name == 'nt':
			exiftoolPath = os.environ.get('exiftoolpath')
		for image_path in self.set_path:
			meta = metadata.Metadata(image_path, exiftoolPath=exiftoolPath)
			metas.append(meta)
		metas.sort(key=lambda x: self.bands.index(x.get_item('XMP:BandName').lower()))
		self.meta = metas

	def raw_images_to_radiance(self):
		"""Convert raw images to radiance"""
		radiance_images = []
		for meta in self.meta:
			band = meta.get_item('XMP:BandName').lower()
			band_index = self.bands.index(band)
			radiance_images.append(raw_image_to_radiance(meta, self.raw_images[band_index])[0])
		self.radiance_images = radiance_images
