"""Train utility functions."""
from numpy import ndarray
from os.path import join, exists
from os import makedirs
from skimage.measure import regionprops, label
from skimage import io
from dataclasses import dataclass
from glob import glob
from pandas import DataFrame

@dataclass
class Paths:
    input_image: str
    output: str
    labels: str

@dataclass
class Trainer:
    paths: Paths

class TrainUtils:
    """Train Utilities for Deep Forest model."""

    def __init__(self, trainer:Trainer) -> None:
        """Initialize the class."""
        self.input = trainer.paths.input_image
        self.output = trainer.paths.output
        self.image = io.imread(self.input)
        self.labels = trainer.paths.labels

    def create_train_mosaic(self, columns:int, rows:int) -> None:
        """Create a mosaic of images from the original one."""
        if not exists(self.output):
            makedirs(self.output)
        height = self.image.shape[0]//rows
        width = self.image.shape[1]//columns
        for row in range(rows):
            for column in range(columns):
                image_crop = self.image[row*height:(row+1)*height, column*width:(column+1)*width]
                io.imsave(join(self.output, f'crop_{row}_{column}.png'), image_crop)
        return self

    def create_train_csv(self, ext:str = '.png') -> None:
        """Create a csv file with the labels (labeled binary images)."""
        image_files = glob(join(self.labels, f'*{ext}'))
        data_frame = self.build_dataframe()
        for file in image_files:
            data_frame = data_frame.append(self.get_data(file), ignore_index=True)
        data_frame.to_csv(join(self.labels, 'train.csv'), index=False)

    def get_data(self, file:str) -> ndarray:
        """Get the data from the labeled images."""
        image = io.imread(file).astype('uint8')
        image = self.sharp_image(image)
        properties = self.get_properties(image)
        data_frame = self.build_dataframe()
        for prop in properties:
            xmin, ymin, xmax, ymax = prop.bbox
            data_frame = data_frame.append({
                'image_path': file,
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax,
                'label': 'Tree'
            }, ignore_index=True)
        return data_frame

    @staticmethod
    def sharp_image(image:ndarray) -> ndarray:
        """Convert image borders to max value."""
        image[image > 0] = 255
        image[image == 0] = 0
        return image

    @staticmethod
    def get_properties(image:ndarray) -> ndarray:
        """Get the properties of the image."""
        return regionprops(label(image))

    @staticmethod
    def build_dataframe() -> DataFrame:
        """Build the dataframe."""
        columns = [
            'image_path',
            'xmin',
            'ymin',
            'xmax',
            'ymax',
            'label'
        ]
        return DataFrame(columns=columns)
