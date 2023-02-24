"""Train utility functions."""
from numpy import ndarray
from os.path import join, exists, dirname
from os import makedirs 
from skimage.measure import regionprops, label
from skimage import io
from glob import glob
from pandas import DataFrame
from deepforest.main import deepforest
from src.conf.config import DeepForestConfig
from wasabi import Printer
msg = Printer()


class TrainUtils:
    """Train Utilities for Deep Forest model."""

    def __init__(self, trainer:DeepForestConfig) -> None:
        """Initialize the class."""
        self.input = trainer.paths.input_image
        self.output = trainer.paths.mosaic_output
        self.image = io.imread(trainer.paths.input_image)
        self.labels = trainer.paths.labels
        self.trainer_config = trainer
        self.train_file = None
        self.model = None

    def create_train_mosaic(self, columns:int, rows:int) -> None:
        """Create a mosaic of images from the original one."""
        if exists(self.output):
            msg.info(f'Output folder already exists: {self.output}')
            return self
        makedirs(self.output)
        height = self.image.shape[0]//rows
        width = self.image.shape[1]//columns
        for row in range(rows):
            for column in range(columns):
                image_crop = self.image[row*height:(row+1)*height, column*width:(column+1)*width]
                io.imsave(join(self.output, f'crop_{row}_{column}.png'), image_crop)
        return self

    def create_train_csv(self, train_file_name:str = 'train.csv') -> None:
        """Create a csv file with the labels (labeled binary images)."""
        if exists(train_file_name):
            msg.info(f'Train file already exists: {self.train_file}')
            return self
        labeled_files = self.get_files(self.labels)
        train_image_files =  self.get_files(self.output)
        data_frame = self.build_dataframe()
        for file, reference in zip(labeled_files, train_image_files):
            data_frame = data_frame.append(self.get_data(file, reference), ignore_index=True)
        data_frame.to_csv(train_file_name, index=False)
        return self

    def train(self) -> None:
        """Train the deep forest model model."""
        model = self.init_model()
        model.create_trainer()
        model.use_release()
        return model

    def init_model(self) -> deepforest:
        """Initialize and configure the model."""
        model = deepforest()
        model = self.set_model(model)
        return model

    def set_model(self, model:deepforest) -> deepforest:
        """Config hyper-parameters."""
        model.config['workers'] = self.trainer_config.params.workers
        model.config['gpus'] = self.trainer_config.params.gpus
        model.config['score_thresh'] = self.trainer_config.params.score_thresh
        model.config['nms_thresh'] = self.trainer_config.params.nms_thresh
        model.config['lr'] = self.trainer_config.params.lr
        model.config['epochs'] = self.trainer_config.params.epochs
        model.config['train']['csv_file'] = self.trainer_config.paths.train_file_name
        model.config['train']['root_dir'] = dirname(self.trainer_config.paths.train_file_name)
        return model

    @staticmethod
    def get_files (path:str, ext:str = '.png') -> list:
        """ Return a list of the files in the path that match the given format. """
        return glob(join(path, f'*{ext}'))

    def get_data(self, file:str, reference:str) -> ndarray:
        """Get the data from the labeled images."""
        image = io.imread(file).astype('uint8')
        image = self.sharp_image(image)
        properties = self.get_properties(image)
        data_frame = self.build_dataframe()
        for prop in properties:
            ymin, xmin, ymax, xmax = prop.bbox
            data_frame = data_frame.append({
                'image_path': reference,
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
