"""Class to process the images in multi-spectral mode (five channels)."""
from core.core_utils import CoreUtils


class MultiSpectralTreatment(CoreUtils):
	"""Image Treatments Class for image processing and other functions.
		Attributes:
		image_path: The path to the image.
		images_set_processed: A list of processed images.
		images_sampled: Just a section for every image in the set.
		raw_images_path: The path to the raw images.
		rgb_image: A image for visualization.
	"""

	def __init__(self, raw_images_path: str):
		super().__init__(raw_images_path)
		self.raw_images_path = raw_images_path
		self.images_set = []
		self.images_sampled = []
		self.images_set_processed = []
		self.rgb_image = None
		self.image_treated = None

	def __call__(self):
		"""Run the image treatments."""
		self.load_images()
		self.normalize_images()
		self.pre_process_images()
		self.segment_images()
		self.enhance_images()
		self.run_treatments()
		self.get_image_results()
		return self

	def load_images(self):
		"""Load images from a path with integer names. The images must contain a set of five images
		  numerated from 1-5. Format supported: .png, .tif
		Args:
			path: The path to the images.
		Returns:
			A list of images.
		"""
		self.images_set = self.load_images_from_integer_names()