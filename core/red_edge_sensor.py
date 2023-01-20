"""RedEdge Sensor Utils"""

# pylint: disable=E0401, E0411
from micasense.metadata import Metadata
from glob import glob
from micasense.utils import raw_image_to_radiance, correct_lens_distortion
from skimage import io, exposure
from numpy import var, eye, float32, argmin
from cv2 import normalize, threshold, findContours, boundingRect, contourArea
from cv2 import NORM_MINMAX, RETR_TREE, CHAIN_APPROX_SIMPLE, CV_8U, MOTION_AFFINE
from cv2 import findTransformECC, warpAffine, TERM_CRITERIA_EPS, TERM_CRITERIA_COUNT, INTER_LINEAR
from cv2 import WARP_INVERSE_MAP
import os

class Sensor:
    """ Micasense RedEdge Sensor Class"""
    def __init__(self, set_path):
        self.set_path = set_path
        self.bands = []
        self.images_path = {}
        self.meta = self.get_metadata(set_path)
        self.raw_images = self.read_raw_images()
        self.radiance_images = self.raw_images_to_radiance()

    def get_metadata(self, set_path):
        """Get metadata for all images in a set"""
        if isinstance(set_path, str):
            set_path = glob(os.path.join(set_path, '*.tif'))
        metas = {}
        if os.name == 'nt':
            exiftool_path = os.environ.get('exiftoolpath')
        else:
            exiftool_path = None
        for image_path in set_path:
            meta = Metadata(image_path, exiftoolPath=exiftool_path)
            band = meta.get_item('XMP:BandName').lower()
            metas.update({band: meta})
            self.bands.append(band)
            self.images_path.update({band: image_path})
        return metas

    def read_raw_images(self):
        """Read raw images from a set"""
        raw_images = {}
        for band in self.bands:
            raw_images.update({band: io.imread(self.images_path[band])})
        return raw_images

    def raw_images_to_radiance(self):
        """Convert raw images to radiance"""
        radiance_images = {}
        for band in self.bands:
            radiance_images.update({
                band: raw_image_to_radiance(
                        self.meta[band], self.raw_images[band])[0]})
        return radiance_images

class Panel(Sensor):
    """ Micasense RedEdge Panel Class (inherits from Sensor)"""
    def __init__(self, set_path):
        super().__init__(set_path)
        self.panel_values = self.get_panel_values()
        self.panel_regions = self.get_panel_regions()
        self.reflectance_factor = self.get_reflectance_factor()

    def get_panel_values(self):
        """Get panel values from metadata"""
        return {
            "blue": 0.67,
            "green": 0.69,
            "red": 0.68,
            "red edge": 0.67,
            "nir": 0.61
        }

    def get_panel_regions(self):
        """Get panel regions from metadata"""
        panel_regions = {}
        for band in self.bands:
            row, column, width, height = self.get_panel_region(self.radiance_images[band])
            image_region =  self.radiance_images[band][row:row+height, column:column+width]
            panel_regions.update({band: image_region})
        return panel_regions

    def get_panel_region(self, radiance_image):
        """Get panel region from radiance image"""
        image = normalize(radiance_image, None, 0, 255, NORM_MINMAX, CV_8U)
        _, thresh = threshold(image, 127, 255, 0)
        contours, _ = findContours(thresh, RETR_TREE, CHAIN_APPROX_SIMPLE)
        variances = []
        bounding_boxes = []
        for cnt in contours:
            box = boundingRect(cnt)
            area = contourArea(cnt)
            if area > 0.002 * image.shape[0] * image.shape[1]:
                height, width = box[3], box[2]
                left, top = box[0], box[1]
                variances.append(var(image[top:top+height, left:left+width]))
                bounding_boxes.append(box)
        panel_region = bounding_boxes[argmin(variances)]
        return panel_region

    def get_reflectance_factor(self):
        """Get reflectance factor from panel values"""
        reflectance_factor = {}
        for band in self.bands:
            factor = self.panel_values[band] / self.panel_regions[band].mean()
            reflectance_factor.update({band: factor})
        return reflectance_factor

class ImageProcessor():
    """ Micasense RedEdge Image Processor Class"""

    def __init__(self, sensor: Sensor, panel: Panel):
        sensor = self.register_images(sensor)
        self.reflectance_images = self.get_reflectance_images(sensor, panel)
        self.corrected_images = self.correct_lens(sensor)
        self.adjusted_images = self.adjust_images()

    def register_images(self, sensor: Sensor):
        """Register images"""
        raw_images = sensor.raw_images
        reg_images = sensor.raw_images
        aligned_images = {}
        normalized_images = {}
        warp_mode = MOTION_AFFINE
        warp_matrix = eye(2, 3, dtype=float32)
        number_of_iterations = 500
        termination_eps = .00005
        criteria = (TERM_CRITERIA_EPS | TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)
        for band in sensor.bands:
            normalized_images.update(
                {band: normalize(
                    raw_images[band], None, 0, 255, NORM_MINMAX, CV_8U)})
        reference_band = 'red edge'
        reference_image = normalized_images[reference_band]
        for band in sensor.bands:
            _, warp_matrix = findTransformECC(
                reference_image,
                normalized_images[band],
                warp_matrix, warp_mode,
                criteria
                )
            aligned_image = warpAffine(
                reg_images[band],
                warp_matrix,(
                    raw_images[band].shape[1],
                    raw_images[band].shape[0]),
                    flags=WARP_INVERSE_MAP + INTER_LINEAR
                    )
            aligned_images.update({band: aligned_image})
        sensor.radiance_images = aligned_images
        return sensor

    def get_reflectance_images(self, sensor: Sensor, panel: Panel):
        """Get reflectance images from sensor and panel"""
        reflectance_images = {}
        for band in sensor.bands:
            image = sensor.radiance_images[band] * panel.reflectance_factor[band]
            reflectance_images.update({band: image})
        return reflectance_images

    def correct_lens(self, sensor: Sensor):
        """Correct lens distortion from sensor and panel"""
        corrected_images = {}
        for band in sensor.bands:
            image = correct_lens_distortion(sensor.meta[band], self.reflectance_images[band])
            corrected_images.update({band: image})
        return corrected_images

    def adjust_images(self):
        """Adjust images"""
        images = {}
        for band in self.corrected_images.keys():
            image = normalize(self.corrected_images[band], None, 0, 255, NORM_MINMAX, CV_8U)
            image = exposure.adjust_gamma(image, 0.85)
            images.update({band: image})
        return images
