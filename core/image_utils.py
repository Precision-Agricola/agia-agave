"""Image processing utilities."""
from PIL import Image
from numpy import array
from sympy import factorint



class ImageUtils:
    """Image processing utilities."""

    def read_images_from_path(path:list) -> list:
        """Read images in gray scale from a list of paths."""
        images = []
        for image_path in path:
            image = Image.open(image_path)
            image_array = array(image)
            image_array[image_array<0] = 0
            images.append(image_array)
        return images
        
    def get_slice_by_matrix(image:array, matrix_size:tuple, slice_tuple:tuple) -> array:
        """Get a slice from a well defined matrix."""
        rows = matrix_size[0]
        cols = matrix_size[1]
        if slice_tuple[0]*slice_tuple[1] > rows*cols:
            raise ValueError("Slice number out of range")
        width = image.shape[0]
        height = image.shape[1]
        slice_width = width // cols
        slice_height = height // rows
        row = slice_tuple[0]
        col = slice_tuple[1]
        left = col * slice_width
        right = left + slice_width
        top = row * slice_height
        bottom = top + slice_height
        return image[left:right, top:bottom]

    def get_slices_params(image:array, slices_no:int, sample_index:int) -> array:
        """Segment the image according the factors fo the slices number."""
        if sample_index > slices_no:
            raise ValueError("Slice number out of range")
        factors = factorint(slices_no)
        factored = list(factors.items())
        if len(factored) == 1 and factored[0][1] == 2:
            rows = factored[0][0]
            cols = factored[0][0]
        else:
            rows = factored[0][0]**factored[0][1]
            cols = sum([factored[i][0]**factored[i][1] for i in range(1, len(factored))])
        element_row = sample_index // cols + 1
        element_col = sample_index % cols
        if image.shape[0] < image.shape[1]:
            return ((rows, cols), (element_row, element_col))
        return ((cols, rows), (element_row, element_col))