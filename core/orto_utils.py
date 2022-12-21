"""Module to create ortomosaic utilities"""
from numpy import array
from skimage import io

class OrtomosaicUtils:
    """Class to handle ortomosaic utilities"""

    def __init__(self, image:array, mosaic_size:tuple, save_path:str):
        self.image = image
        self.width = image.shape[0]
        self.height = image.shape[1]
        self.mosaic_size = mosaic_size
        self.columns = mosaic_size[0]
        self.rows = mosaic_size[1]
        self.save_path = save_path

    def get_segment(self, column:int, row:int):
        """Get the segment of the image"""
        if column >= self.columns or row >= self.rows:
            raise ValueError("Column or row out of range")
        x_1, x_2, y_1, y_2 = self.get_limits(column, row)
        return self.image[x_1:x_2, y_1:y_2]

    def build_mosaic(self):
        """Build the mosaic"""
        if self.height < self.width:
            self.columns, self.rows = self.rows, self.columns
        for row in range(self.rows):
            for column in range(self.columns):
                self.save_segment(column, row)

    def save_segment(self, column:int, row:int):
        """Save the segment of the image"""
        x_1, x_2, y_1, y_2 = self.get_limits(column, row)
        segment = self.image[x_1:x_2, y_1:y_2]
        segment_path = self.save_path + f"segment_{column}_{row}.png"
        io.imsave(segment_path, segment)
        return segment_path

    def get_limits(self, column:int, row:int):
        """Get the limits of the image to be cropped"""
        x_1 = int(self.width / self.columns * column)
        x_2 = int(self.width / self.columns * (column + 1))
        y_1 = int(self.height / self.rows * row)
        y_2 = int(self.height / self.rows * (row + 1))
        return x_1, x_2, y_1, y_2
