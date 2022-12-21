"""Utilities for raw image conversion and processing"""
import micasense.metadata as metadata
from micasense.utils import raw_image_to_radiance
from skimage import io
from numpy import var, abs, where, mean, argmax
from scipy import stats
import os 
from cv2 import normalize, threshold, findContours, approxPolyDP, boundingRect, contourArea
from cv2 import arcLength, NORM_MINMAX, RETR_TREE, CHAIN_APPROX_SIMPLE, CV_8U


class SensorUtils:
    """Class for handle sensor utils"""

    def __init__(self, set_path):
        self.set_path = set_path
        self.bands = ['red', 'green', 'blue', 'nir', 'red edge']
        self.meta = self.get_metadata(set_path)
        self.raw_images = []
        self.radiance_images = {
            'red': None,
            'green': None,
            'blue': None,
            'nir': None,
            'red edge': None
        }

    def process_sensor(self):
        self.read_raw_images()
        self.raw_images_to_radiance()
        return self

    def read_raw_images(self):
        """Read raw images from a set"""
        raw_images = []
        for image_path in self.set_path:
            raw_images.append(io.imread(image_path))
        self.raw_images = raw_images

    def get_metadata(self, set_path):
        """Get metadata for all images in a set"""
        metas = []
        if os.name == 'nt':
            exiftoolPath = os.environ.get('exiftoolpath')
        for image_path in set_path:
            meta = metadata.Metadata(image_path, exiftoolPath=exiftoolPath)
            metas.append(meta)
        metas.sort(key=lambda x: self.bands.index(x.get_item('XMP:BandName').lower()))
        return metas

    def raw_images_to_radiance(self):
        """Convert raw images to radiance"""
        radiance_images = []
        for meta in self.meta:
            band = meta.get_item('XMP:BandName').lower()
            band_index = self.bands.index(band)
            radiance_images.append(raw_image_to_radiance(meta, self.raw_images[band_index])[0])
            self.radiance_images.update({band: radiance_images[band_index]})

class PanelCalibration(SensorUtils):
    """Utils for panel calibration and image correction"""

    def __init__(self, panel_set_path):
        self.panel_set_path = panel_set_path
        self.bands =['red', 'green', 'blue', 'nir', 'red edge']
        self.metas = self.get_metadata(panel_set_path)
        self.panel_images = {
            'red': None,
            'green': None,
            'blue': None,
            'nir': None,
            'red edge': None
            }
        self.panel_calibration = { 
            "blue": 0.67, 
            "green": 0.69, 
            "red": 0.68, 
            "red edge": 0.67, 
            "nir": 0.61 
            }
        self.reflectance_factors = {
            'red': None,
            'green': None,
            'blue': None,
            'nir': None,
            'red edge': None
            }
        self.panel_regions = {
            'red': None,
            'green': None,
            'blue': None,
            'nir': None,
            'red edge': None
            }  

    def process_panel(self):
        self.read_panel_images()
        self.get_panel_regions()
        self.get_panel_reflectance_factors()
        return self
    
    def read_panel_images(self):
        """Read panel images from a set"""
        panel_images = []
        for image_path in self.panel_set_path:
            panel_images.append(io.imread(image_path))
        for meta in self.metas:
            band = meta.get_item('XMP:BandName').lower()
            band_index = self.bands.index(band)
            self.panel_images[band] = panel_images[band_index]
    
    def get_panel_regions(self):
        """Get panel regions for all images in a set"""
        for band, image in self.panel_images.items():
            x, y, w, h = self.get_panel_region(image)
            self.panel_regions[band] = image[y:y+h, x:x+w]
    
    def get_panel_region(self, panel_image):
        """Get panel region from an image"""
        image = normalize(panel_image, None, 0, 255, NORM_MINMAX, CV_8U)
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

    def get_panel_reflectance_factors(self):
        """Get panel reflectance factors for all images in a set"""
        for band, image in self.panel_regions.items():
            self.reflectance_factors[band] = self.get_panel_reflectance_factor(image, band)
    
    def get_panel_reflectance_factor(self, panel_region, band):
        """Get panel reflectance factor from an image"""
        return self.panel_calibration[band]/mean(panel_region)

    def correct_images(self, radiance_images, reflectances):
        """Transform raw images to reflectance images and correct lens distortion"""
        corrected_images = {
            'red': None,
            'green': None,
            'blue': None,
            'nir': None,
            'red edge': None
        }
        for band in reflectances.keys():
            corrected_images.update({band: radiance_images[band]*reflectances[band]})
        return corrected_images



