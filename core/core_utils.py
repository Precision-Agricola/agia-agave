"""Core Module Utilities for image processing and other functions."""

from PIL import Image, ImageOps
from pathlib import Path
from sympy import factorint

class CoreUtils:
	"""Core Module Utilities for image processing and other functions.
		Attributes:
		images_set: A list of images to be processed.
		images_set_processed: A list of processed images.
		images_sampled: Just a section for every image in the set.
		raw_images_path: The path to the raw images.
		rgb_image: A image for visualization.
	"""

	def __init__(self):
		self.images_set = []
		self.images_sampled = []
		self.images_set_processed = []
		self.raw_images_path = ""
		self.rgb_image = None

	def load_images_from_integer_names(self, path:str, format:str = '.png') -> list(Image):
		"""Load images from a path with integer names. The images must contain a set of five images
  		numerated from 1-5. Format supported: .png, .tif
		Args:
			path: The path to the images.
		Returns:
			A list of images.
		"""
		data_dir = Path(path)
		images_files = list(data_dir.glob("*" + format))
		images = []
		if not images_files:
			raise ValueError("Invalid path or images format, images format must include a dot")
		if len(images_files) != 5:
			raise ValueError("Missing files in folder, images set must contain five files")
		for file in images_files:
			image = Image.open(file)
			gray_image = ImageOps.grayscale(image)
			images.append(gray_image)
		return images

	def build_rgb_image(images:list(Image)) -> Image:
		"""Build an RGB image from a list of images.
		Args:
			images: A list of images.
		Returns:
			A RGB image.
		"""
		if len(images)<3:
			raise ValueError("Not sufficient channels in the set of images")
		for image in images:
			channels = image.size[2]
		if channels != 1:
			raise IndexError("Each image in set must be formatted in grayscale")
		return Image.merge("RGB", (images[0], images[1], images[2]))

	def get_segment_by_position(image:Image, size: tuple, slice_no:int) -> Image:
		"""Get a sample of the image corresponding to n file and m column."""
		rows = size[0]
		cols = size[1]
		if slice_no > rows*cols:
			raise ValueError("Slice number out of range")
		width = image.size[0]
		height = image.size[1]
		slice_width = width // cols
		slice_height = height // rows
		row = slice_no // cols
		col = slice_no % cols
		left = col * slice_width
		right = left + slice_width
		top = row * slice_height
		bottom = top + slice_height
		return image.crop((left, top, right, bottom))

	def get_segment_by_index(image:Image, sample_no:int, samples:int) -> Image:
		"""Get a sample of the image given the sample number and the total number of samples."""
		if sample_no > samples:
			raise ValueError("Sample number out of range")
		factors = factorint(samples)
		factored = list(factors.items())
		if len(factored) == 1 and factored[0][1] == 2:
			rows = factored[0][0]
			cols = factored[0][0]
		else:
			rows = factored[0][0]**factored[0][1]
			cols = sum([factored[i][0]**factored[i][1] for i in range(1, len(factors))])
		element_row = sample_no // rows 
		element_col = sample_no // cols + sample_no % cols - element_row
		width, height = Image.size[0], Image.size[1]
		pixels_per_row = width // rows
		pixels_per_col = height // cols
		left = element_col * pixels_per_row
		right = left + pixels_per_row
		top = element_row * pixels_per_col
		bottom = top + pixels_per_col
		return image.crop((left, top, right, bottom))

		