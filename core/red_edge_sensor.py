"""RedEdge Sensor Utils"""
from micasense.metadata import Metadata
from micasense.utils import raw_image_to_radiance, correct_lens_distortion
from skimage import io, exposure
from numpy import where, var, eye, float32, dstack
from scipy import stats
from cv2 import normalize, threshold, findContours, approxPolyDP, boundingRect, contourArea, GaussianBlur
from cv2 import arcLength, NORM_MINMAX, RETR_TREE, CHAIN_APPROX_SIMPLE, CV_8U, MOTION_AFFINE
from cv2 import findTransformECC, warpAffine, TERM_CRITERIA_EPS, TERM_CRITERIA_COUNT, INTER_LINEAR
from cv2 import WARP_INVERSE_MAP
import os

class Sensor:
    def __init__(self, set_path):
        self.set_path = set_path
        self.bands = []
        self.images_path = {}
        self.meta = self.get_metadata(set_path)
        self.raw_images = self.read_raw_images()
        self.radiance_images = self.raw_images_to_radiance()

    def get_metadata(self, set_path):
        """Get metadata for all images in a set"""
        metas = {}
        if os.name == 'nt':
            exiftoolPath = os.environ.get('exiftoolpath')
        else:
            exiftoolPath = None
        for image_path in set_path:
            meta = Metadata(image_path, exiftoolPath=exiftoolPath)
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
            radiance_images.update({band: raw_image_to_radiance(self.meta[band], self.raw_images[band])[0]})
        return radiance_images

class Panel(Sensor):
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
        detections = []
        variances = []
        bounding_boxes = []
        for cnt in contours:
            approx = approxPolyDP(cnt, 0.01*arcLength(cnt, True), True)
            if len(approx) != 4:
                continue
            _, _, w, h = boundingRect(cnt)
            area = contourArea(cnt)
            area_thresh = 0.00025*image.shape[0]*image.shape[1]
            ratio = float(w)/h
            if 0.95 < ratio < 1.05 and area > area_thresh:
                detections.append(cnt)
                box = boundingRect(cnt)
                x, y, w, h = box
                variance = var(image[x:w + x, y:h + y])
                variances.append(variance)
                bounding_boxes.append(box)
        z_score = stats.zscore(variances)
        z_threshold =  1
        outliers = where(z_score > z_threshold)
        panel_region = bounding_boxes[outliers[0][0]]
        return panel_region

    def get_reflectance_factor(self):
        """Get reflectance factor from panel values"""
        reflectance_factor = {}
        for band in self.bands:
            factor = self.panel_values[band] / self.panel_regions[band].mean()
            reflectance_factor.update({band: factor})
        return reflectance_factor

class ImageProcessor():

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
        number_of_iterations = 1000
        termination_eps = 1e-10
        criteria = (TERM_CRITERIA_EPS | TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)
        for band in sensor.bands:
            normalized_images.update({band: normalize(raw_images[band], None, 0, 255, NORM_MINMAX, CV_8U)})
        reference_band = 'red edge'
        reference_image = normalized_images[reference_band]
        for band in sensor.bands:
            _, warp_matrix = findTransformECC(reference_image, normalized_images[band], warp_matrix, warp_mode, criteria)
            aligned_image = warpAffine(reg_images[band], warp_matrix, (raw_images[band].shape[1], raw_images[band].shape[0]), flags=WARP_INVERSE_MAP + INTER_LINEAR)
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