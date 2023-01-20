"""Image processor module for E2E pipeline"""
from dataclasses import dataclass
from numpy import dstack
from core.red_edge_sensor import Panel, Sensor, ImageProcessor

@dataclass
class SensorSet:
    """Sensor set dataclass"""
    data_set: list[str]
    panel_set: list[str]

class E2EImageProcessor:
    """E2E image processor"""
    def __init__(self, sensor:SensorSet) -> None:
        self.data_set = sensor.data_set
        self.panel_set = sensor.panel_set
        self.image_processor = None
        self.rgb = None

    def __call__(self) -> None:
        """Run the image processor"""
        self.image_preprocessing()
        return self

    def image_preprocessing(self) -> None:
        """Image preprocessing"""
        panel = Panel(set_path=self.panel_set)
        sensor = Sensor(set_path=self.data_set)
        self.image_processor = ImageProcessor(panel=panel, sensor=sensor)
        self.rgb = self.get_rgb_image(self.image_processor)
        return self

    @staticmethod
    def get_rgb_image(images) -> None:
        """Get the RGB image"""
        rgb_set = dstack((
            images.adjusted_images['red'],
            images.adjusted_images['green'],
            images.adjusted_images['blue']))
        return rgb_set
